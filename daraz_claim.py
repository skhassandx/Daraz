from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import datetime
import random

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
    
    # অ্যান্টি-বট বাইপাস
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

def collect_rewards(driver):
    """ক্লেম বা কালেক্ট বাটন খুঁজে ক্লিক করার স্মার্ট ফাংশন"""
    print("🎁 Scanning for 'Claim' or 'Collect' buttons...")
    try:
        # সব ধরণের ক্লেইম বাটন খোঁজার চেষ্টা
        claim_btns = driver.find_elements(By.XPATH, "//*[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='claim' or translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='collect']")
        visible_claims = [b for b in claim_btns if b.is_displayed()]
        
        if visible_claims:
            for btn in visible_claims:
                driver.execute_script("arguments[0].click();", btn)
                print("✅ Jackpot! Successfully claimed points!")
                time.sleep(2)
        else:
            print("⏳ No claimable points ready yet.")
    except Exception as e:
        pass

def handle_smart_mission(driver, mission_title):
    """মিশনের নাম পড়ে সিদ্ধান্ত নেওয়ার এআই লজিক"""
    print(f"🧠 AI analyzing mission: '{mission_title}'")
    
    # ১. প্রথমে স্টার্ট বাটন খোঁজা
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

    # ২. লজিক অনুযায়ী কাজ করা
    if "0/10" in mission_title or "explore to find" in mission_title.lower():
        print("🕵️‍♂️ Detected 10-Item Browse Mission. Clicking random items...")
        for i in range(11): # ১০-১১ বার স্ক্রল ও ক্লিক করবে
            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(2)
            # পেজে থাকা যেকোনো লিংকে ক্লিক করার চেষ্টা (খুব সাবধানে)
            try:
                links = driver.find_elements(By.TAG_NAME, "a")
                if links:
                    random_link = random.choice(links)
                    driver.execute_script("arguments[0].click();", random_link)
                    time.sleep(3)
                    driver.back() # ব্যাক করে আবার আগের পেজে আসবে
                    time.sleep(2)
            except:
                pass
            print(f"   -> Explored item {i+1}/10")
            
    elif "share" in mission_title.lower():
        print("📤 Detected Share Mission. Searching for share icon...")
        # শেয়ার বাটনে ক্লিক করার সিমুলেশন
        for _ in range(4):
            driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(3)
            
    elif "daraz land" in mission_title.lower() or "game" in mission_title.lower():
        print("🎮 Detected Game Mission. Waiting 20 seconds...")
        time.sleep(20) # গেম পেজে একটু বেশি সময় থাকতে হয়
        
    else:
        print("⏳ Standard Browse Mission. Scrolling for 15 seconds...")
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(3) 

    # ৩. ফলো বাটন থাকলে ক্লিক করা
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
        
    print("✅ Mission activity complete.")

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
        time.sleep(10) 
        
        # প্রথমে জমে থাকা পয়েন্ট ক্লেইম করা
        collect_rewards(driver)

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
                    time.sleep(4)
                    break
            
            # আবার ক্লেইম চেক
            collect_rewards(driver)

            # Go এবং Go! দুটিই খুঁজবে
            go_buttons = driver.find_elements(By.XPATH, "//*[text()='Go' or text()='Go!']")
            visible_go_btns = [b for b in go_buttons if b.is_displayed()]
            
            if len(visible_go_btns) > 0:
                print(f"🎯 Found {len(visible_go_btns)} visible missions.")
                max_missions = min(len(visible_go_btns), 5) # ৫টি মিশন করবে
                
                for i in range(max_missions):
                    print(f"\n▶️ Starting Mission {i+1}...")
                    try:
                        # মিশন লিস্ট পপ-আপ ওপেন করা
                        earn_more = driver.find_elements(By.XPATH, "//*[contains(text(), 'Earn More')]")
                        for btn in earn_more:
                            if btn.is_displayed():
                                driver.execute_script("arguments[0].click();", btn)
                                time.sleep(2)
                                break
                                
                        # প্রতিটি Go বাটনের আগের টেক্সট (মিশনের নাম) বের করা
                        mission_blocks = driver.find_elements(By.XPATH, "//div[.//div[text()='Go' or text()='Go!']]")
                        mission_title = "Unknown Mission"
                        if i < len(mission_blocks):
                            mission_title = mission_blocks[i].text.replace('\n', ' ')

                        btns = driver.find_elements(By.XPATH, "//*[text()='Go' or text()='Go!']")
                        v_btns = [b for b in btns if b.is_displayed()]
                        
                        if i < len(v_btns):
                            driver.execute_script("arguments[0].click();", v_btns[i])
                            time.sleep(6) 
                            
                            # স্মার্ট লজিক দিয়ে মিশন করা
                            handle_smart_mission(driver, mission_title)
                            
                            print("🔙 Returning to Main Coin Page...")
                            driver.get(target_url)
                            time.sleep(8) 
                            
                            # ফিরে আসার পর সাথে সাথেই পয়েন্ট ক্লেইম করা
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
