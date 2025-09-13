pyinstaller --onefile --noconsole --name Youtube you.py

🔹 경우 1: 브레이브 창 2개 (같은 프로필)

기본적으로 하나의 Brave 실행 프로세스만 뜨고, 창은 여러 개가 떠 있습니다.

이때는 --remote-debugging-port=9222 로 실행하면, 모든 창+탭이 같은 디버깅 포트에서 관리됩니다.

browser.list_tab() 하면 전체 창의 탭이 한 배열로 들어오기 때문에, 1번 탭·2번 탭 기준이 열린 모든 창을 합친 순서가 됩니다.
→ 창을 2개 띄웠을 때, 어느 창의 1번 탭을 제어할지는 구분이 안 돼요.

🔹 경우 2: 브레이브 프로필 2개

예: 일반 프로필 / 게스트 프로필, 또는 --user-data-dir 옵션으로 새 프로필 지정.

이 경우 브레이브를 별도 프로세스로 실행할 수 있습니다.

각각 다른 --remote-debugging-port 를 열어야 합니다:

brave.exe --remote-debugging-port=9222 --user-data-dir="C:\BraveProfile1"
brave.exe --remote-debugging-port=9333 --user-data-dir="C:\BraveProfile2"


그러면 포트별로 완전히 분리된 디버깅 서버가 뜹니다:

첫 번째 프로필: http://127.0.0.1:9222/json

두 번째 프로필: http://127.0.0.1:9333/json

Python 코드에서 DEBUG_URL 을 바꿔주면 됩니다:

DEBUG_URL = "http://127.0.0.1:9222"  # 첫 번째 브레이브
# or
DEBUG_URL = "http://127.0.0.1:9333"  # 두 번째 브레이브

🔹 정리

창만 여러 개 띄운 경우 → list_tab() 배열 안에 다 같이 들어와서 탭 번호가 섞임. “창1의 1번 탭” 이런 구분은 불가.

프로필(프로세스)을 나눈 경우 → 디버깅 포트 번호로 확실히 분리 가능. 원하는 브레이브만 제어할 수 있음.

👉 질문 주신 게 창 2개 상황인지, 아니면 프로필 2개로 완전히 나누려는 상황인지 알려주시면, 그에 맞게 탭 번호 정렬이나 코드 분기 예시까지 드릴 수 있어요.
