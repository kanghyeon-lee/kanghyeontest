# saucedemo Playwright 자동화 연습 프로젝트

대상: https://www.saucedemo.com (pytest + pytest-playwright, sync API)

## 환경
- 가상환경: `.venv` (`source .venv/bin/activate`)
- 의존성: `pip install -r requirements.txt` 후 `playwright install chromium`
- 실행: `pytest` / 브라우저 보기: `pytest --headed --slowmo 500` / 리포트: `pytest --html=report.html`
- base URL은 `pytest.ini`에 설정되어 있으므로 `page.goto("/")`처럼 상대 경로를 사용한다.

## 구조 (POM)
- `pages/` — 페이지 객체. 화면당 클래스 하나, locator와 동작 메서드만 담는다.
- `tests/` — 테스트. 페이지 객체를 통해서만 화면을 조작하고, 테스트 안에 raw selector를 쓰지 않는다.
- `conftest.py` — 공용 fixture (페이지 객체 fixture, test id 속성 설정 등).

## 규칙
- `time.sleep()` / `page.wait_for_timeout()` 금지. Playwright의 auto-wait과 `expect()`를 사용한다.
- locator 우선순위: `get_by_role` · `get_by_test_id` → (불가할 때만) `get_by_label`/`get_by_text` → CSS/XPath는 최후 수단.
  - saucedemo는 `data-test` 속성을 쓰므로 conftest에서 `set_test_id_attribute("data-test")`로 설정해 두었다.
- 검증은 `playwright.sync_api.expect`를 사용한다.
- 테스트를 추가·수정하면 반드시 직접 실행해서 통과를 확인한 뒤 완료로 보고한다.
