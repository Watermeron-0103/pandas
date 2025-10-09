from __future__ import annotations
from datetime import date, timedelta
import time
from pathlib import Path
from typing import Optional

from flask import Flask, render_template, request, send_from_directory, url_for, redirect, flash
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

# ================== 画面から渡されない固定値（必要があれば後でUI化） ==================
URL = "https://fftpim-s.fujifilm.co.jp/imart/samlsso/home"
TIMEOUT = 20
WINDOW_SIZE = "1400,1000"
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "downloads"        # サーバーが保存する実体の場所
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = "replace-me"  # flash() 用

# ------------------------ Flask ルーティング ------------------------

@app.get("/")
def index():
    # 既定値：きょうを終了、6日前を開始
    end = date.today()
    start = end - timedelta(days=6)
    return render_template(
        "index.html",
        default_start=start.isoformat(),   # "YYYY-MM-DD"
        default_end=end.isoformat(),
    )

@app.post("/run")
def run():
    # HTML5 date input は "YYYY-MM-DD"
    start_str = request.form.get("start") or ""
    end_str = request.form.get("end") or ""
    headless = request.form.get("headless") == "on"

    if not start_str or not end_str:
        flash("開始日と終了日を入力してください。")
        return redirect(url_for("index"))

    if start_str > end_str:
        flash("開始日は終了日以前にしてください。")
        return redirect(url_for("index"))

    # サイト側の書式 "YYYY/MM/DD" に変換
    START = start_str.replace("-", "/")
    END = end_str.replace("-", "/")

    try:
        output_name = f"imart_返品管理表_{start_str}_{end_str}.csv"
        csv_path = run_automation(START, END, output_name, headless=headless)
        flash("CSVの作成に成功しました。")
        # ダウンロードリンクへ
        return redirect(url_for("download_file", filename=csv_path.name))
    except Exception as e:
        flash(f"エラーが発生しました: {e!r}")
        return redirect(url_for("index"))

@app.get("/download/<path:filename>")
def download_file(filename):
    # downloads/ 配下のファイルを返す
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

# ------------------------ 自動化本体 ------------------------

def build_driver(*, headless: bool) -> webdriver.Chrome:
    """Chrome を希望のダウンロード先で起動。ヘッドレスもOK。"""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={WINDOW_SIZE}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")

    # ダウンロード先の固定
    prefs = {
        "download.default_directory": str(DOWNLOAD_DIR.resolve()),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True,
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)

    # ヘッドレス時はCDPで明示（環境によって必要）
    if headless:
        try:
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": str(DOWNLOAD_DIR.resolve())
            })
        except Exception:
            pass

    return driver


def go_to_parts_search_list(driver, wait):
    """ワークフロー → 不具合情報システム → 部品品記 → 部品品記検索一覧 へ移動"""
    driver.switch_to.default_content()
    ac = ActionChains(driver)

    wf = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//*[self::a or self::span][normalize-space(.)='ワークフロー']")))
    ac.move_to_element(wf).pause(0.25).perform()

    ng = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//*[self::a or self::span][normalize-space(.)='不具合情報システム']")))
    ac.move_to_element(ng).pause(0.25).perform()

    parts = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//*[self::a or self::span][normalize-space(.)='部品品記']")))
    ac.move_to_element(parts).pause(0.25).perform()

    target = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//*[self::a or self::span][normalize-space(.)='部品品記検索一覧']")))
    try:
        ac.move_to_element(target).pause(0.1).click().perform()
    except Exception:
        driver.execute_script("arguments[0].click();", target)

    time.sleep(0.3)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])


def switch_into_content_frame(driver, wait) -> bool:
    driver.switch_to.default_content()
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for f in frames:
        driver.switch_to.default_content()
        driver.switch_to.frame(f)
        try:
            wait.until(EC.presence_of_element_located((
                By.XPATH, "//*[contains(normalize-space(.),'起票日') or contains(normalize-space(.),'返品管理表')]"
            )))
            return True
        except TimeoutException:
            continue
    driver.switch_to.default_content()
    return False


def click_clear(wait):
    btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//input[@type='button' and @value='クリア'] | //button[normalize-space()='クリア']")))
    btn.click()


def select_doc_type(driver, wait, label="返品管理票", value="5"):
    """文書種別を '返品管理票' に確実に。UI表示/hidden双方を更新。"""
    container = wait.until(EC.presence_of_element_located((By.ID, "doc_type")))
    sel = container.find_element(By.NAME, "doc_type")                      # hidden <select>
    txt = container.find_element(By.CSS_SELECTOR, "input.imfr_select_text")# 表示用テキスト
    esc = driver.find_element(By.NAME, "escape_doc_type")                  # hidden <input>

    driver.execute_script(
        "arguments[0].value=arguments[1]; arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
        sel, value
    )
    driver.execute_script(
        "arguments[0].value=arguments[1];"
        "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
        "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
        txt, label
    )
    driver.execute_script("arguments[0].value=arguments[1];", esc, value)
    wait.until(lambda d: sel.get_attribute("value") == value)


def check_all_status(driver, wait):
    for v in ("2","6","7","8","9"):
        cb = wait.until(EC.presence_of_element_located((
            By.XPATH, f"//input[@type='checkbox' and @name='item_status' and @value='{v}']")))
        if not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)


def set_date_range(driver, wait, start_text: str, end_text: str):
    start_input = wait.until(EC.presence_of_element_located((By.ID, "apply_dt_from_display")))
    end_input = wait.until(EC.presence_of_element_located((By.ID, "apply_dt_to_display")))
    for el, value in ((start_input, start_text), (end_input, end_text)):
        driver.execute_script("arguments[0].value='';", el)
        driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
            "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
            el, value
        )
        time.sleep(0.05)


def click_search(wait):
    btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//input[@type='button' and @value='検索'] | //button[normalize-space()='検索']")))
    btn.click()


def click_csv(wait):
    btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//input[@type='button' and @value='CSV']"
                  " | //button[normalize-space()='CSV']"
                  " | //a[normalize-space()='CSV']")))
    try:
        btn.click()
    except Exception:
        wait._driver.execute_script("arguments[0].click();", btn)


def confirm_csv_ok(driver, wait):
    # 1) native alert
    try:
        driver.switch_to.alert.accept()
        return
    except Exception:
        pass

    # 2) jQuery UI / 独自ダイアログ
    wait.until(EC.visibility_of_any_elements_located(
        (By.CSS_SELECTOR, ".ui-widget-overlay, .imui-widget-overlay")
    ))
    ok_xpath = (
        "//div[contains(@class,'ui-dialog') and not(contains(@style,'display: none'))]"
        "//button[.//span[normalize-space()='OK'] or normalize-space()='OK']"
        " | //div[contains(@class,'ui-dialog') and not(contains(@style,'display: none'))]"
        "//a[contains(@class,'ui-button') and normalize-space()='OK']"
        " | //div[contains(@class,'imui-dialog') and contains(@style,'display')]"
        "//button[normalize-space()='OK']"
    )
    ok_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ok_xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ok_btn)
    driver.execute_script("arguments[0].click();", ok_btn)
    try:
        wait.until(EC.invisibility_of_element(ok_btn))
    except Exception:
        pass


def wait_for_download(dirpath: Path, *, expected_ext=".csv",
                      rename_to: Optional[str] = None, timeout: int = 90) -> Path:
    start = time.time()
    before = {p.name for p in dirpath.glob("*")}
    target: Optional[Path] = None

    while time.time() - start < timeout:
        now = list(dirpath.glob("*"))
        added = [p for p in now if p.name not in before]
        if added:
            for p in sorted(added, key=lambda x: x.stat().st_mtime, reverse=True):
                cr = Path(str(p) + ".crdownload")
                if cr.exists():
                    break
                if expected_ext is None or p.suffix.lower() == expected_ext:
                    target = p
                    break
        if target:
            break
        time.sleep(0.3)

    if target is None:
        raise TimeoutException("CSVのダウンロードが確認できませんでした")

    if rename_to:
        dest = target.with_name(rename_to)
        try:
            target.rename(dest)
            target = dest
        except Exception:
            pass
    return target


def run_automation(START: str, END: str, output_name: str, *, headless: bool) -> Path:
    """Selenium 一連の流れを実行して CSV のパスを返す。"""
    driver = build_driver(headless=headless)
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        driver.get(URL)
        go_to_parts_search_list(driver, wait)
        switch_into_content_frame(driver, wait)

        click_clear(wait)
        select_doc_type(driver, wait, label="返品管理票", value="5")
        check_all_status(driver, wait)
        set_date_range(driver, wait, START, END)
        click_search(wait)

        click_csv(wait)
        confirm_csv_ok(driver, wait)

        csv_path = wait_for_download(DOWNLOAD_DIR, expected_ext=".csv", rename_to=output_name)
        return csv_path
    finally:
        # 画面を残したいならここをコメントアウト
        driver.quit()


if __name__ == "__main__":
    # Flask dev server
    app.run(debug=True)
