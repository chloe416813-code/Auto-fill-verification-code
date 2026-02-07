import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import ddddocr
import time

# 初始化 OCR
ocr = ddddocr.DdddOcr(show_ad=False)

def solve_captcha(driver, element_id):
    """
    driver: selenium 控制器
    element_id: 驗證碼圖片在網頁中的 ID 或 Selector
    """
    # 1. 找到驗證碼圖片元素並截圖
    captcha_img = driver.find_element(By.ID, element_id)
    img_bytes = captcha_img.screenshot_as_png
    
    # 2. 進行辨識
    result = ocr.classification(img_bytes)
    return result

def run_monitor():
    st.info("🚀 啟動背景監控流程...")
    
    # 設定 Chrome 為無頭模式 (伺服器運作，手機不卡頓)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    try:
        driver.get("https://example-ticket-site.com") # 替換為實際售票網址
        
        # 執行辨識邏輯
        # 假設驗證碼圖片 ID 是 'captcha_img'，輸入框 ID 是 'captcha_input'
        captcha_code = solve_captcha(driver, "captcha_img")
        st.write(f"🔍 辨識到驗證碼：{captcha_code}")
        
        # 自動填入
        driver.find_element(By.ID, "captcha_input").send_keys(captcha_code)
        
        # 點擊送出或繼續後續動作...
        # driver.find_element(By.ID, "submit_btn").click()
        
    except Exception as e:
        st.error(f"發生錯誤: {e}")
    finally:
        st.warning("監控任務結束")
        # driver.quit() # 測試時可先註解掉以檢查結果

# Streamlit 介面部分
if st.button("開始自動售票監控"):
    run_monitor()
