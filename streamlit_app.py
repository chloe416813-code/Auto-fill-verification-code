import streamlit as st
import time
import io
from PIL import Image

# 嘗試載入關鍵套件
try:
    import ddddocr
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError as e:
    st.error(f"❌ 缺少必要套件或系統庫: {e}")
    st.info("💡 請確認專案中已有 requirements.txt 與 packages.txt")

# 初始化 OCR 引擎
@st.cache_resource
def load_ocr():
    return ddddocr.DdddOcr(show_ad=False)

def solve_captcha(driver, element_selector):
    """抓取驗證碼圖片並辨識"""
    try:
        # 找到驗證碼圖片元素
        captcha_img = driver.find_element(By.CSS_SELECTOR, element_selector)
        # 截取該元素的圖片內容
        img_bytes = captcha_img.screenshot_as_png
        
        ocr = load_ocr()
        result = ocr.classification(img_bytes)
        return result
    except Exception as e:
        return f"辨識失敗: {str(e)}"

def run_automation(target_url, img_selector, input_selector):
    """執行自動化流程"""
    # 針對手機背景運作的無頭模式設定
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 啟動瀏覽器
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        st.write(f"🌐 正在連線至: {target_url}...")
        driver.get(target_url)
        time.sleep(2)  # 等待頁面載入
        
        # 辨識驗證碼
        st.write("🔍 正在嘗試辨識驗證碼...")
        code = solve_captcha(driver, img_selector)
        st.success(f"✅ 辨識成功: {code}")
        
        # 自動填入 (範例)
        if code and "失敗" not in code:
            driver.find_element(By.CSS_SELECTOR, input_selector).send_keys(code)
            st.info("✏️ 已自動填入驗證碼框")
            
    except Exception as e:
        st.error(f"發生錯誤: {e}")
    finally:
        st.warning("⚠️ 腳本運行完畢，關閉模擬瀏覽器")
        driver.quit()

# --- Streamlit 介面 ---
st.title("🎫 售票自動驗證工具")

# 設定區 (可根據不同網站調整)
url = st.text_input("目標網站 URL", "https://範例網址.com")
img_css = st.text_input("驗證碼圖片 CSS Selector", "#captcha_image")
input_css = st.text_input("驗證碼輸入框 CSS Selector", "#captcha_code")

if st.button("開始監控與自動輸入"):
    run_automation(url, img_css, input_css)
