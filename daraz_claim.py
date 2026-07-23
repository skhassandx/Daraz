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
    print("🚀 Initializing Stealth Mobile Browser...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Linux aarch64",
        webgl_vendor="ARM",
        renderer="Mali-G78",
        fix_hairline=True,
    )
    driver.set_window_size(412, 915)
    return driver

def open_mission_list(driver):
    """Earn More বাটনে ক্লিক করে মিশন লিস্ট পপ-আপ ওপেন করার ফাংশন"""
    print("🔍 Attempting to open 'Earn More' mission list...")
    try:
        earn_more_btns = driver.find_elements(By.XPATH, "//*[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='earn more']")
        for btn in earn_more_btns:
            if btn.is_displayed():
                driver.execute_script("arguments[0].click();", btn)
                print("✅ Clicked 'Earn More' successfully!")
                time.sleep(3)
                return True
    except:
        pass
    print("⚠️ Could not open 'Earn More' list.")
    return False

def collect_rewards(driver):
    """মিশন লিস্ট ওপেন থাকা অবস্থায় Claim/Collect বাটন খোঁজা"""
    print("🎁 Scanning for 'Claim' or 'Collect' buttons in the list...")
    try:
        claim_btns = driver.find_elements(By.XPATH, "//*[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='claim' or translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='collect']")
        visible_claims = [b for b in claim_btns if b.is_displayed()]
        
        if visible_claims:
            for btn in visible_claims:
                driver.execute_script("arguments[0].click();", btn)
                print("✅ Jackpot! Successfully claimed points!")
                time.sleep(2)
        else:
            print("⏳ No claimable points ready yet.")
    except:
        pass

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
        time.sleep(8) 
        
        # প্রথমে জমে থাকা পয়েন্ট ক্লেইম করা (যদি থাকে)
        if open_mission_list(driver):
            collect_rewards(driver)
            # পপ-আপের বাইরে ক্লিক করে বা পেজ রিফ্রেশ করে লিস্ট বন্ধ করা
            driver.get(target_url)
            time.sleep(5)

        # Go বাটন খোঁজা
        if open_mission_list(driver):
            go_buttons = driver.find_elements(By.XPATH, "//*[text()='Go' or text()='Go!']")
            visible_go_btns = [b for b in go_buttons if b.is_displayed()]
            
            if len(visible_go_btns) > 0:
                print(f"🎯 Found {len(visible_go_btns)} visible missions.")
                max_missions = min(len(visible_go_btns), 4) # ৪টি মিশন করবে
                
                for i in range(max_missions):
                    print(f"\n▶️ Starting Mission {i+1}...")
                    try:
                        # প্রতিবার নতুন করে বাটন লিস্ট বের করতে হবে
                        btns = driver.find_elements(By.XPATH, "//*[text()='Go' or text()='Go!']")
                        v_btns = [b for b in btns if b.is_displayed()]
                        
                        if i < len(v_btns):
                            # Go তে ক্লিক করে মিশনে যাওয়া
                            driver.execute_script("arguments[0].click();", v_btns[i])
                            print("🚀 Navigated to mission page. Waiting for load...")
                            time.sleep(5) 
                            
                            # মিশনে গিয়ে যেকোনো স্টার্ট বাটন থাকলে ক্লিক করা
                            try:
                                start_btns = driver.find_elements(By.XPATH, "//*[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='start']")
                                for btn in start_btns:
                                    if btn.is_displayed():
                                        driver.execute_script("arguments[0].click();", btn)
                                        print("🎯 Clicked 'Start' timer button!")
                                        time.sleep(2)
                                        break
                            except:
                                pass
                            
                            # মিশনে ২৫ সেকেন্ড সময় কাটানো (সব ধরণের মিশনের জন্য যথেষ্ট)
                            print("⏳ Browsing mission page for 25 seconds...")
                            for _ in range(5):
                                driver.execute_script("window.scrollBy(0, 500);")
                                time.sleep(5)
                                
                            # ফলো বাটন থাকলে ক্লিক করা
                            try:
                                follow_btns = driver.find_elements(By.XPATH, "//*[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='follow' or text()='ফলো']")
                                for btn in follow_btns:
                                    if btn.is_displayed():
                                        driver.execute_script("arguments[0].click();", btn)
                                        print("🎯 Found and clicked 'Follow' button!")
                                        break
                            except:
                                pass
                                
                            # মিশন শেষ, মেইন পেজে ব্যাক করা
                            print("🔙 Returning to Main Coin Page...")
                            driver.get(target_url)
                            time.sleep(7) 
                            
                            # মেইন পেজে আসার পর আবার Earn More ওপেন করে পয়েন্ট নেওয়া
                            if open_mission_list(driver):
                                collect_rewards(driver)
                                
                    except Exception as ex:
                        print(f"⚠️ Could not complete mission {i+1}: {ex}")
            else:
                print("🤷 No visible 'Go' missions found right now.")
                
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
