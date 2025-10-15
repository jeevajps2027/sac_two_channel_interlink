# mini_soft/utils.py
import threading
import time
import sys
from datetime import datetime, timezone
from django.db import connections

_HEALTH = {
    "ok": False,
    "status": "⏳ Not checked yet",
    "last_ok": None,
    "last_error": None,
    "last_checked": None,
}
_LOCK = threading.Lock()
_STOP = threading.Event()
_MONITOR_STARTED = False

def _ping_mssql():
    conn = connections['mssql']
    conn.close_if_unusable_or_obsolete()
    conn.ensure_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        cur.fetchone()

def check_mssql_once(timeout=5):
    res = {"ok": False, "status": "", "error": None}
    def target():
        try:
            _ping_mssql()
            res.update(ok=True, status="✅ MSSQL connection OK", error=None)
        except Exception as e:
            res.update(ok=False, status=f"❌ MSSQL connection FAILED: {e}", error=str(e))
    t = threading.Thread(target=target, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        res.update(ok=False, status="❌ MSSQL connection timeout", error="timeout")
    return res

def start_mssql_monitor(interval=5, timeout=2, print_changes=True):
    """Start MSSQL health monitor in a background thread (safe to call anytime)."""
    global _MONITOR_STARTED
    if _MONITOR_STARTED:
        return
    _MONITOR_STARTED = True

    def loop():
        while not _STOP.is_set():
            try:
                res = check_mssql_once(timeout=timeout)
                now = datetime.now(timezone.utc)
                with _LOCK:
                    _HEALTH.update({
                        "ok": res["ok"],
                        "status": res["status"],
                        "last_checked": now,
                        "last_ok": now if res["ok"] else _HEALTH["last_ok"],
                        "last_error": None if res["ok"] else res.get("error"),
                    })
                if print_changes:
                    print(f"[{now.strftime('%H:%M:%S')}] {res['status']}")
                    sys.stdout.flush()
            except Exception as e:
                print(f"[Monitor Error] {e}", flush=True)
            _STOP.wait(interval)

    threading.Thread(target=loop, daemon=True).start()

def stop_mssql_monitor():
    _STOP.set()

def get_mssql_status():
    with _LOCK:
        return dict(_HEALTH)


# ✅ Start monitor automatically
start_mssql_monitor(interval=1, timeout=1, print_changes=True)
