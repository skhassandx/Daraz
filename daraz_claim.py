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

def collect_rewards(driver):
    """এই ফাংশনটির কাজ হলো পেজে থাকা যেকোনো Claim বা Collect বাটনে ক্লিক করে পয়েন্ট নেওয়া"""
    print("🎁 Checking for any 'Claim' or 'Collect' buttons to grab points...")
    try:
        claim_btns = driver.find_elements(By.XPATH, "//*[text()='Claim' or text()='Collect' or text()='CLAIM' or text()='COLLECT']")
        visible_claims = [b for b in claim_btns if b.is_displayed()]
        
        for btn in visible_claims:
            driver.execute_script("arguments[0].click();", btn)
            print("✅ Successfully claimed points for a completed mission!")
            time.sleep(2)
    except:
        pass

def complete_mission(driver):
    print("⏳ Simulating human behavior on mission page (Waiting 16+ seconds)...")
    
    # ১. পেজে কোনো 'Start' টাইমার বাটন থাকলে সেটিতে ক্লিক করা
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

    # ২. স্ক্রল করা এবং সময় কাটানো (অন্তত ১৬ সেকেন্ড)
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(3) # মোট ১৫ সেকেন্ড এখানে কাটবে
        
    # ৩. পেজে 'Follow' বাটন আছে কি না চেক করা
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
        
    # ৪. আবার আস্তে আস্তে উপরে ওঠা
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, -500);")
        time.sleep(2)
    print("✅ Mission browsing complete. Returning to collect points...")

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
        print("⏳ Waiting 7 seconds for page to load completely...")
        time.sleep(7) 
        
        # প্রথমে মেইন পেজে কোনো Start বাটন থাকলে ক্লিক করা
        print("🔍 Checking for sticky 'Start' banner on main page...")
        try:
            main_start_btns = driver.find_elements(By.XPATH, "//*[text()='Start' or text()='START']")
            for btn in main_start_btns:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    print("✅ Clicked main page 'Start' banner! Waiting 12 seconds...")
                    time.sleep(12)
                    # ব্যানার শেষ হওয়ার পর পয়েন্ট ক্লেইম করা
                    collect_rewards(driver)
                    break
        except:
            pass

        # ডেইলি চেক-ইন
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

        # ডেইলি মিশন কমপ্লিট করা
        print("\n🔍 Opening Daily Missions list...")
        try:
            # Earn More বাটনে ক্লিক করে মিশন পপ-আপ ওপেন করা
            earn_more = driver.find_elements(By.XPATH, "//*[contains(text(), 'Earn More')]")
            for btn in earn_more:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    print("✅ Clicked 'Earn More' to open mission list.")
                    time.sleep(3)
                    break
            
            # আগের করা কোনো মিশনের পয়েন্ট ঝুলে থাকলে সেটা আগে নিয়ে নেবে
            collect_rewards(driver)

            # পপ-আপের ভেতর দৃশ্যমান Go বাটন খোঁজা
            go_buttons = driver.find_elements(By.XPATH, "//*[text()='Go' or text()='Go!']")
            visible_go_btns = [b for b in go_buttons if b.is_displayed()]
            
            if len(visible_go_btns) > 0:
                print(f"🎯 Found {len(visible_go_btns)} visible missions.")
                max_missions = min(len(visible_go_btns), 4) # ৪টি মিশন করবে
                
                for i in range(max_missions):
                    print(f"\n▶️ Starting Mission {i+1}...")
                    try:
                        # পপ-আপ ওপেন আছে কি না নিশ্চিত করা
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
                            print("🚀 Navigated to mission page. Waiting for load...")
                            time.sleep(5) 
                            
                            complete_mission(driver)
                            
                            # মিশন শেষে আবার মূল কয়েন পেজে ফিরে আসা
                            print("🔙 Returning to Main Coin Page...")
                            driver.get(target_url)
                            time.sleep(7) 
                            
                            # Earn More বাটন আবার ওপেন করে পয়েন্ট ক্লেইম করা (সবচেয়ে গুরুত্বপূর্ণ অংশ)
                            earn_more = driver.find_elements(By.XPATH, "//*[contains(text(), 'Earn More')]")
                            for btn in earn_more:
                                if btn.is_displayed():
                                    driver.execute_script("arguments[0].click();", btn)
                                    time.sleep(3)
                                    break
                            
                            # এখানে সে নতুন তৈরি হওয়া 'Claim' বাটনটিতে ক্লিক করে পয়েন্ট নিয়ে নেবে
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
    print("====================================")
    print("   Daraz Smart Automation Bot v3    ")
    print("====================================")
    claim_daily_reward()
