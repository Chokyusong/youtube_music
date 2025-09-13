# brave_yt_toggle_tab1.py
import time
import pychrome
import sys,os
from datetime import datetime, timedelta

# ──[설정]────────────────────────────────────────────────────────
DEPLOY_DATE = datetime(2025, 9, 13)   # 배포일
VALID_DAYS  = 60                     # 사용 가능 기간 (일)
FORCE_EXPIRE = False                 # 테스트 강제 만료 스위치
# ────────────────────────────────────────────────────────────────

def _should_expire(now: datetime) -> bool:
    if FORCE_EXPIRE:
        return True
    if os.environ.get("TEST_EXPIRE", "").strip() == "1":
        return True
    if any(arg in ("--expire-now", "/expire-now") for arg in sys.argv[1:]):
        return True
    expire_date = DEPLOY_DATE + timedelta(days=VALID_DAYS)
    return now > expire_date

def _block_with_message(msg: str):
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk(); root.withdraw()
        messagebox.showerror("사용 기간 만료", msg)
    except Exception:
        print(msg)
    finally:
        sys.exit(1)

if _should_expire(datetime.now()):
    _block_with_message("⚠️ 사용 기간이 만료되었습니다.\n개발자에게 문의하세요.")

DEBUG_URL = "http://127.0.0.1:9222"

def eval_js(tab, code):
    return tab.call_method("Runtime.evaluate", expression=code, returnByValue=True)

def toggle_first_tab():
    browser = pychrome.Browser(url=DEBUG_URL)
    tabs = browser.list_tab()

    if len(tabs) < 1:
        print("브레이브에 열린 탭이 없습니다.")
        return

    tab = tabs[1]
    tab.start()

    # JS로 URL 확인
    r = eval_js(tab, "location.href")
    url = r.get("result", {}).get("value", "")
    print(f"1번 탭 URL: {url}")

    # 유튜브 영상 토글
    r = eval_js(tab, """
        (function(){
          var v=document.querySelector('video');
          if(!v) return 'no-video';
          if(v.paused){ v.play(); return 'played'; }
          v.pause(); return 'paused';
        })();
    """)
    print("result:", r.get("result", {}).get("value"))

    # ✅ tab.stop() 제거 → 불필요한 JSONDecodeError 방지
    print("브레이브 1번 탭 유튜브 토글 완료.")

if __name__ == "__main__":
    toggle_first_tab()
