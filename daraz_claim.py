from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import datetime

# ==========================================
# 🔑 আপনার দেওয়া কুকিগুলোর ভ্যালু
# ==========================================
DARAZ_COOKIES = [
    {
        'name': 'lzd_sid', 
        'value': '18eb03454e593be44c7de0a235e424e9',
        'domain': '.daraz.com.bd'
    },
    {
        'name': '_tb_token_', 
        'value': 'eb73e7eb31bee',
        'domain': '.daraz.com.bd'
    }
]
# ==========================================

def get_browser():
    print("🚀 Initializing Stealth Mobile Browser to bypass security...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # অ্যান্টি-বট বাইপাস করার স্পেশাল কমান্ড
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # ব্রাউজারকে একটি রিয়েল স্যামসাং (Samsung) মোবাইল হিসেবে সাজানো
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # Stealth Mode অ্যাপ্লাই করা (যাতে দারাজ বুঝতে না পারে এটি বট)
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Linux aarch64",
        webgl_vendor="ARM",
        renderer="Mali-G78",
        fix_hairline=True,
    )
    
    # মোবাইলের স্ক্রিন সাইজ সেট করা
    driver.set_window_size(412, 915)
    return driver

def collect_rewards(driver):
    print("🎁 Checking for any 'Claim' or 'Collect' buttons to grab points...")
    try:
        claim_btns = driver.find_elements(By.XPATH, "//*[text()='Claim' or text()='Collect' or text()='CLAIM' or text()='COLLECT']")
        visible_claims = [b for b in claim_btns if b.is_displayed()]
        for btn in visible_claims:
            driver.execute_script("arguments[0].click();", btn)
            print("✅ Successfully claimed points!")
            time.sleep(2)
    except:
        pass

def complete_mission(driver):
    print("⏳ Simulating human behavior on mission page...")
    try:
        start_btns = driver.find_elements(By.XPATH, "//*[text()='Start' or text()='START']")
        for btn in start_btns:
            if btn.is_displayed():
                driver.execute_script("arguments[0].click();", btn)
                print("🎯 Clicked 'Start' timer button!")
                time.sleep(2)
                break
    except:
        pass

    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(3) 
        
    try:
        follow_btns = driver.find_elements(By.XPATH, "//*[text()='Follow' or text()='FOLLOW' or text()='ফলো']")
        for btn in follow_btns:
            if btn.is_displayed():
                driver.execute_script("arguments[0].click();", btn)
                print("🎯 Found and clicked 'Follow' button!")
                time.sleep(2)
                break
    except:
        pass 
        
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, -500);")
        time.sleep(2)

def claim_daily_reward():
    driver = None
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"daraz_status_{timestamp}.png"
        driver = get_browser()
        
        print("🍪 Setting up Daraz cookies...")
        driver.get("https://www.daraz.com.bd")
        time.sleep(2)
        
        for cookie in DARAZ_COOKIES:
            driver.add_cookie(cookie)
            
        target_url = "https://pages.daraz.com.bd/wow/gcp/route/daraz/mm/upr/router?hybrid=1&data_prefetch=true&prefetch_replace=1&at_iframe=1&wh_pid=%2Flazada%2Fchannel%2Fbd%2Fe0d86ac70718d0b9%2F72nDH8pYpY&pha=true&lzd_navbar_hidden=true&wx_navbar_transparent=true&dsource=hp_icon&spm=a2a0e.tm80335411.icons.d1_Coins"
        
        print("🎯 Navigating to Coin Page...")
        driver.get(target_url)
        print("⏳ Waiting 10 seconds to mimic human loading...")
        time.sleep(10) 
        
        print("🔍 Checking for sticky 'Start' banner on main page...")
        try:
            main_start_btns = driver.find_elements(By.XPATH, "//*[text()='Start' or text()='START']")
            for btn in main_start_btns:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    print("✅ Clicked main page 'Start' banner! Waiting 12 seconds...")
                    time.sleep(12)
                    collect_rewards(driver)
                    break
        except:
            pass

        print("\n🔍 Looking for 'Check-in' button...")
        try:
            checkin_btn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Check-in')]"))
            )
            driver.execute_script("arguments[0].click();", checkin_btn)
            print("✅ Clicked Daily Check-in button successfully!")
            time.sleep(3) 
        except:
            print("⚠️ Check-in button not found. Moving to missions...")

        print("\n🔍 Opening Daily Missions list...")
        try:
            earn_more = driver.find_elements(By.XPATH, "//*[contains(text(), 'Earn More')]")
            for btn in earn_more:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    print("✅ Clicked 'Earn More' to open mission list.")
                    time.sleep(4)
                    break
            
            collect_rewards(driver)

            go_buttons = driver.find_elements(By.XPATH, "//*[text()='Go' or text()='Go!']")
            visible_go_btns = [b for b in go_buttons if b.is_displayed()]
            
            if len(visible_go_btns) > 0:
                print(f"🎯 Found {len(visible_go_btns)} visible missions.")
                max_missions = min(len(visible_go_btns), 4) 
                
                for i in range(max_missions):
                    print(f"\n▶️ Starting Mission {i+1}...")
                    try:
                        earn_more = driver.find_elements(By.XPATH, "//*[contains(text(), 'Earn More')]")
                        for btn in earn_more:
                            if btn.is_displayed():
                                driver.execute_script("arguments[0].click();", btn)
                                time.sleep(2)
                                break
                                
                        btns = driver.find_elements(By.XPATH, "//*[text()='Go' or text()='Go!']")
                        v_btns = [b for b in btns if b.is_displayed()]
                        
                        if i < len(v_btns):
                            driver.execute_script("arguments[0].click();", v_btns[i])
                            time.sleep(6) 
                            
                            complete_mission(driver)
                            
                            print("🔙 Returning to Main Coin Page...")
                            driver.get(target_url)
                            time.sleep(8) 
                            
                            earn_more = driver.find_elements(By.XPATH, "//*[contains(text(), 'Earn More')]")
                            for btn in earn_more:
                                if btn.is_displayed():
                                    driver.execute_script("arguments[0].click();", btn)
                                    time.sleep(3)
                                    break
                            
                            collect_rewards(driver)
                            
                    except Exception as ex:
                        print(f"⚠️ Could not complete mission {i+1}: {ex}")
            else:
                print("🤷 No visible 'Go' missions found right now.")
                
        except Exception as e:
            print("⚠️ Mission automation encountered an issue.")

        driver.save_screenshot(screenshot_name)
        print(f"\n📸 Saved final screenshot as '{screenshot_name}'.")
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
    finally:
        if driver:
            driver.quit()
            print("🛑 Browser safely closed.")

if __name__ == "__main__":
    claim_daily_reward()
