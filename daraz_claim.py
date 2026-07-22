from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    print("🚀 Initializing Headless Mobile Browser...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    mobile_emulation = { "deviceName": "Nexus 5" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    return webdriver.Chrome(options=chrome_options)

def complete_mission(driver):
    print("⏳ Simulating human behavior (Scrolling)...")
    # আস্তে আস্তে নিচে স্ক্রল করা
    for _ in range(4):
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(2)
        
    # পেজে 'Follow' বাটন আছে কি না চেক করা এবং ক্লিক করা
    try:
        # கேস-ইনসেনসিটিভ ভাবে 'Follow' বাটন খোঁজার চেষ্টা
        follow_btn = driver.find_element(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'follow')]")
        driver.execute_script("arguments[0].click();", follow_btn)
        print("🎯 Found and clicked 'Follow' button!")
        time.sleep(2)
    except:
        pass # ফলো বাটন না থাকলে স্কিপ করবে
        
    # আবার আস্তে আস্তে উপরে ওঠা
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, -500);")
        time.sleep(2)
    print("✅ Mission browsing complete.")

def claim_daily_reward():
    driver = None
    try:
        # বর্তমান সময় দিয়ে স্ক্রিনশটের নাম তৈরি করা
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
        print("⏳ Waiting 7 seconds for page to load completely...")
        time.sleep(7) 
        
        # ডেইলি চেক-ইন করা
        print("🔍 Looking for 'Check-in' or 'Collect' button...")
        try:
            checkin_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Check-in') or contains(text(), 'Collect')]"))
            )
            driver.execute_script("arguments[0].click();", checkin_btn)
            print("✅ Clicked Daily Check-in button successfully!")
            time.sleep(4) 
        except Exception as e:
            print("⚠️ Check-in button not found. Maybe already claimed today?")

        # ডেইলি মিশন কমপ্লিট করা
        print("\n🔍 Looking for Daily Missions ('Go' buttons)...")
        try:
            go_buttons = driver.find_elements(By.XPATH, "//*[text()='Go' or text()='Go!']")
            
            if len(go_buttons) > 0:
                print(f"🎯 Found {len(go_buttons)} missions. Starting automation...")
                max_missions = min(len(go_buttons), 4) # একসাথে সর্বোচ্চ ৪টি মিশন করবে
                
                for i in range(max_missions):
                    print(f"\n▶️ Starting Mission {i+1}...")
                    try:
                        # প্রতিবার নতুন করে বাটন খুঁজতে হবে পেজ রিফ্রেশের কারণে
                        btns = driver.find_elements(By.XPATH, "//*[text()='Go' or text()='Go!']")
                        if i < len(btns):
                            driver.execute_script("arguments[0].click();", btns[i])
                            time.sleep(5) # নতুন পেজ লোড হওয়ার সময়
                            
                            # হিউম্যান সিমুলেশন (স্ক্রল ও ফলো) ফাংশন কল করা
                            complete_mission(driver)
                            
                            # মিশন শেষে আবার মূল কয়েন পেজে ফিরে আসা
                            driver.get(target_url)
                            time.sleep(6) 
                    except Exception as ex:
                        print(f"⚠️ Could not complete mission {i+1}: {ex}")
            else:
                print("🤷 No available 'Go' missions found right now.")
                
        except Exception as e:
            print("⚠️ Mission automation encountered an issue.")

        # কাজের শেষে ফাইনাল স্ক্রিনশট নেওয়া
        driver.save_screenshot(screenshot_name)
        print(f"\n📸 Saved final screenshot as '{screenshot_name}'.")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        if driver:
            driver.quit()
            print("🛑 Browser safely closed.")

if __name__ == "__main__":
    print("====================================")
    print("   Daraz Smart Automation Bot Started     ")
    print("====================================")
    claim_daily_reward()
