import streamlit as st
import time
from PIL import Image

# 嘗試匯入並解決 Python 3.13 的相容性錯誤
try:
    import ddddocr
except Exception as e:
    st.error("⚠️ ddddocr 匯入失敗。這通常是因為 Python 版本過新 (3.12+) 或缺少系統庫。")
    st.info("請檢查 Python 版本或確認 packages.txt 內容。")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    st.error("❌ 缺少 Selenium 或 WebDriver 套件。")

# 初始化 OCR 引擎
@st.cache_resource
def get_ocr():
    try:
        return ddddocr.DdddOcr(show_ad=False)
    except:
        return None

def run_automation(target_url, img_selector, input_selector):
    # 配置 Chrome 無頭模式 (重要：適合伺服器與手機背景執行)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # 啟動瀏覽器
    with st.spinner("正在啟動瀏覽器伺服器..."):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(target_url)
        st.write(f"🌐 已開啟頁面: {target_url}")
        time.sleep(3) # 等待頁面與驗證碼加載

        # 1. 抓取驗證碼圖片
        captcha_element = driver.find_element(By.CSS_SELECTOR, img_selector)
        img_bytes = captcha_element.screenshot_as_png
        
        # 顯示給使用者看
        st.image(img_bytes, caption="偵測到的驗證碼")

        # 2. 辨識驗證碼
        ocr = get_ocr()
        if ocr:
            res = ocr.classification(img_bytes)
            st.success(f"🔍 辨識結果: {res}")
            
            # 3. 自動填入
            driver.find_element(By.CSS_SELECTOR, input_selector).send_keys(res)
            st.info("✏️ 已將結果填入網頁輸入框")
        else:
            st.error("OCR 引擎初始化失敗。")

    except Exception as e:
        st.error(f"執行中出錯: {e}")
    finally:
        driver.quit()
        st.warning("🏁 任務結束，瀏覽器已關閉。")

# --- Streamlit 介面 ---
st.title("🎫 售票自動化驗證工具")

with st.expander("⚙️ 設定參數"):
    url = st.text_input("目標網站 URL", "https://example.com")
    img_css = st.text_input("驗證碼圖片 CSS Selector", "img.captcha")
    input_css = st.text_input("輸入框 CSS Selector", "input#verify_code")

if st.button("🚀 開始自動執行"):
    if url and img_css and input_css:
        run_automation(url, img_css, input_css)
    else:
        st.warning("請填寫完整的設定參數。")
