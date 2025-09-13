# brave_yt_toggle_tab1.py
import time
import pychrome

DEBUG_URL = "http://127.0.0.1:9222"

def eval_js(tab, code):
    return tab.call_method("Runtime.evaluate", expression=code, returnByValue=True)

def toggle_first_tab():
    browser = pychrome.Browser(url=DEBUG_URL)
    tabs = browser.list_tab()

    if len(tabs) < 1:
        print("브레이브에 열린 탭이 없습니다.")
        return

    tab = tabs[0]
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
