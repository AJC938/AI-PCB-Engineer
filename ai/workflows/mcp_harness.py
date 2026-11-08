"""Reproducible MCP test harness for KiCAD-MCP-Server (JSON-RPC 2.0 over stdio).

Launches the server exactly as configured in the project's .mcp.json (same command, args
and env), optionally with per-process env overrides (e.g. KICAD_BACKEND=ipc), performs
initialize + tools/list, then executes a scripted sequence of tools/call requests and
records every raw response with wall-clock latency.

Usage:
  python -I mcp_harness.py --config .mcp.json --calls calls.json --out log.json
                           [--env KEY=VALUE ...] [--schemas tool1,tool2]

calls.json: list of steps. Each step is one of
  {"name": "<tool>", "arguments": {...}, "label": "T1", "timeout": 240}
  {"sleep": 2.0}
Machine paths in the output are NOT sanitized; sanitize before committing.
"""
import argparse
import json
import os
import subprocess
import sys
import threading
import time


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--calls")
    ap.add_argument("--out", required=True)
    ap.add_argument("--env", action="append", default=[])
    ap.add_argument("--schemas", default="", help="comma list of tool names whose input schemas to print")
    ap.add_argument("--server", default="kicad")
    a = ap.parse_args()

    srv = json.load(open(a.config, encoding="utf-8"))["mcpServers"][a.server]
    env = dict(os.environ)
    env.update(srv.get("env", {}))
    overrides = dict(kv.split("=", 1) for kv in a.env)
    env.update(overrides)
    steps = json.load(open(a.calls, encoding="utf-8")) if a.calls else []

    proc = subprocess.Popen([srv["command"], *srv["args"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, env=env, cwd=os.path.dirname(os.path.abspath(a.config)))
    stderr_lines, responses, pending = [], {}, {}
    threading.Thread(target=lambda: [stderr_lines.append(l.decode("utf-8", "replace").rstrip()) for l in proc.stderr],
                     daemon=True).start()

    def reader():
        for line in proc.stdout:
            try:
                msg = json.loads(line)
            except Exception:
                continue
            if "id" in msg and msg["id"] in pending:
                responses[msg["id"]] = msg
                pending[msg["id"]].set()

    threading.Thread(target=reader, daemon=True).start()
    nid = [0]

    def rpc(method, params=None, timeout=240):
        nid[0] += 1
        i = nid[0]
        ev = threading.Event()
        pending[i] = ev
        proc.stdin.write((json.dumps({"jsonrpc": "2.0", "id": i, "method": method, "params": params or {}}) + "\n").encode())
        proc.stdin.flush()
        t0 = time.perf_counter()
        ok = ev.wait(timeout)
        dt = round(time.perf_counter() - t0, 3)
        return (responses.get(i) if ok else {"error": f"TIMEOUT after {timeout}s"}), dt

    log = {"overrides": overrides, "started": time.strftime("%Y-%m-%dT%H:%M:%S")}
    r, dt = rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                               "clientInfo": {"name": "ai-pcb-harness", "version": "0.0.3"}})
    log["initialize"] = {"secs": dt, "serverInfo": (r.get("result") or {}).get("serverInfo")}
    proc.stdin.write((json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n").encode())
    proc.stdin.flush()
    r, dt = rpc("tools/list")
    tools = (r.get("result") or {}).get("tools", [])
    log["tool_count"] = len(tools)
    log["tools"] = [t["name"] for t in tools]
    for name in [n for n in a.schemas.split(",") if n]:
        t = next((t for t in tools if t["name"] == name), None)
        print(f"\n##### SCHEMA {name}:", json.dumps(t["inputSchema"], indent=1) if t else "NOT IN TOOL LIST")
        if t:
            print("##### DESC:", t.get("description", ""))

    log["steps"] = []
    for st in steps:
        if "sleep" in st:
            time.sleep(st["sleep"])
            continue
        r, dt = rpc("tools/call", {"name": st["name"], "arguments": st.get("arguments", {})}, st.get("timeout", 240))
        res = r.get("result") if isinstance(r, dict) else None
        text = " ".join(p.get("text", "") for p in (res or {}).get("content", []) if p.get("type") == "text")
        parsed = None
        try:
            parsed = json.loads(text)
        except Exception:
            pass
        entry = {"label": st.get("label", ""), "name": st["name"], "arguments": st.get("arguments", {}), "secs": dt,
                 "isError": (res or {}).get("isError"), "rpc_error": r.get("error") if isinstance(r, dict) else None,
                 "success": parsed.get("success") if isinstance(parsed, dict) else None,
                 "backend": parsed.get("_backend") if isinstance(parsed, dict) else None,
                 "text": text}
        log["steps"].append(entry)
        status = "ERR" if entry["isError"] or entry["rpc_error"] or entry["success"] is False else "ok "
        print(f"[{status}] {entry['label']:6} {st['name']:28} {dt:7.3f}s backend={entry['backend']}  {text[:260]!r}")

    log["alive_at_end"] = proc.poll() is None
    proc.stdin.close()
    try:
        proc.wait(15)
    except Exception:
        proc.kill()
    log["exit_code"] = proc.returncode
    log["stderr_tail"] = stderr_lines[-80:]
    json.dump(log, open(a.out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\ninit {log['initialize']['secs']}s, tools={log['tool_count']}, alive_at_end={log['alive_at_end']}, "
          f"exit={log['exit_code']} -> {a.out}")


if __name__ == "__main__":
    sys.exit(main())
