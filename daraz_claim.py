from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

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
    
    # ব্রাউজারকে মোবাইল হিসেবে সাজানো
    mobile_emulation = { "deviceName": "Nexus 5" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    return webdriver.Chrome(options=chrome_options)

def claim_daily_reward():
    driver = None
    try:
        driver = get_browser()
        
        # ১. দারাজের ওয়েবসাইটে গিয়ে কুকি সেট করা
        print("🍪 Setting up Daraz cookies...")
        driver.get("https://www.daraz.com.bd")
        time.sleep(2)
        
        for cookie in DARAZ_COOKIES:
            driver.add_cookie(cookie)
            
        # ২. ডিরেক্ট কয়েন ক্লেইম লিংকে যাওয়া
        target_url = "https://pages.daraz.com.bd/wow/gcp/route/daraz/mm/upr/router?hybrid=1&data_prefetch=true&prefetch_replace=1&at_iframe=1&wh_pid=%2Flazada%2Fchannel%2Fbd%2Fe0d86ac70718d0b9%2F72nDH8pYpY&pha=true&lzd_navbar_hidden=true&wx_navbar_transparent=true&dsource=hp_icon&spm=a2a0e.tm80335411.icons.d1_Coins"
        
        print(f"🎯 Navigating to Coin Page...")
        driver.get(target_url)
        
        # পেজটি সম্পূর্ণ লোড হওয়ার জন্য একটু অপেক্ষা করা
        print("⏳ Waiting for page to load completely...")
        time.sleep(7) 
        
        # ৩. লগ চেক করার জন্য স্ক্রিনশট নেওয়া
        screenshot_name = "daraz_coin_page.png"
        driver.save_screenshot(screenshot_name)
        print(f"📸 Saved screenshot as '{screenshot_name}'. Please check your files.")
        
        print("✅ Navigation complete. Ready for next step.")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        if driver:
            driver.quit()
            print("🛑 Browser safely closed.")

if __name__ == "__main__":
    print("====================================")
    print("   Daraz Web Automation Started     ")
    print("====================================")
    claim_daily_reward()
