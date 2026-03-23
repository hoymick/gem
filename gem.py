from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def collect_gems_fully_automated():
    # Setup Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # Headless mode configuration
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print("\n" + "="*60)
        print("🤖 FULLY AUTOMATED GEM COLLECTOR - HEADLESS MODE")
        print("="*60)
        print("👻 Running in headless mode (invisible browser)")
        
        # Step 1: Open the site
        print("\n📱 Opening Prize Protocol...")
        driver.get("https://prizeprotocol.com/")
        time.sleep(3)
        
        # Step 2: Click Login button (top right corner)
        print("🔐 Clicking login button in top right corner...")
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/login']"))
        )
        login_button.click()
        print("✅ Clicked login button")
        time.sleep(2)
        
        # Step 3: Enter email
        print("📧 Entering email...")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_input.send_keys("midejnr9@gmail.com")
        print("✅ Email entered")
        time.sleep(1)
        
        # Step 4: Enter password
        print("🔑 Entering password...")
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_input.send_keys("aaaaaaaa")
        print("✅ Password entered")
        time.sleep(1)
        
        # Step 5: Click the correct login submit button
        print("✅ Clicking login submit button...")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
        )
        submit_button.click()
        print("✅ Login submitted")
        
        # Wait for login to complete
        print("⏳ Waiting for login to complete (5 seconds)...")
        time.sleep(5)
        
        # Step 6: Click Mine button
        print("⛏️ Looking for Mine button...")
        try:
            mine_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Mine')]"))
            )
            mine_button.click()
            print("✅ Clicked Mine button")
        except Exception as e:
            print(f"⚠️ Could not find Mine button by text: {e}")
            
            try:
                mine_img = driver.find_element(By.CSS_SELECTOR, "img[alt='Mine']")
                clickable = mine_img.find_element(By.XPATH, "./ancestor::div[contains(@class, 'relative')]")
                clickable.click()
                print("✅ Clicked Mine button via image")
            except Exception as e2:
                print(f"⚠️ Could not find Mine button by image: {e2}")
                elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Mine')]")
                for elem in elements:
                    if elem.is_displayed() and elem.is_enabled():
                        elem.click()
                        print("✅ Clicked Mine button via text search")
                        break
        
        time.sleep(3)
        
        print("\n" + "="*60)
        print("💎 STARTING GEM COLLECTION - HEADLESS MODE")
        print("="*60)
        print("🎮 Script is running in the background")
        print("🔄 Will reload page if no gem detected within 12 seconds")
        print("📊 Status updates will appear here")
        print("🖱️ Press Ctrl+C to stop\n")
        
        total_clicks = 0
        start_time = time.time()
        last_print_time = time.time()
        last_gem_time = time.time()
        reload_count = 0
        
        # Main gem clicking loop
        while True:
            current_time = time.time()
            
            # Check if no gem has been clicked for 12 seconds
            if current_time - last_gem_time > 12:
                print(f"\n⚠️ No gem detected for 12 seconds! Reloading page... (Reload #{reload_count + 1})")
                driver.refresh()
                time.sleep(3)
                reload_count += 1
                last_gem_time = current_time
                print("✅ Page reloaded, continuing to watch for gems...\n")
                continue
            
            # Look for and click the gem
            gem_clicked = driver.execute_script("""
                // Find all gem divs
                let divs = document.querySelectorAll('div.absolute.-inset-2.rounded-full');
                
                for (let div of divs) {
                    // Check for the gem glow effect
                    let boxShadow = window.getComputedStyle(div).boxShadow;
                    if (boxShadow && boxShadow.includes('rgba(255, 193, 7, 0.35)')) {
                        // Find clickable parent
                        let clickable = div;
                        while (clickable && !clickable.onclick && !clickable.getAttribute('onclick') && 
                               clickable.tagName !== 'BUTTON' && clickable.tagName !== 'A') {
                            clickable = clickable.parentElement;
                            if (!clickable || clickable.tagName === 'BODY') {
                                clickable = div;
                                break;
                            }
                        }
                        
                        // Click it
                        clickable.click();
                        return true;
                    }
                }
                return false;
            """)
            
            if gem_clicked:
                total_clicks += 1
                last_gem_time = current_time
                
                # Print status every 5 seconds
                if current_time - last_print_time >= 5:
                    elapsed = current_time - start_time
                    rate = total_clicks / elapsed if elapsed > 0 else 0
                    print(f"🖱️ Clicks: {total_clicks:6d} | Rate: {rate:.1f}/sec | 💎 ACTIVE | Reloads: {reload_count}")
                    last_print_time = current_time
                
                # Small visual feedback
                if total_clicks % 100 == 0:
                    print(f"   🎉 Milestone: {total_clicks} clicks! Still running strong...")
            
            # Small delay to prevent CPU overload
            time.sleep(random.uniform(0.001, 0.005))
            
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("⏹️ STOPPING AUTO-CLICKER")
        elapsed = time.time() - start_time if 'start_time' in locals() else 0
        print(f"📊 Total clicks: {total_clicks}")
        print(f"🔄 Total reloads: {reload_count}")
        print(f"⏱️ Time: {elapsed:.1f} seconds")
        if elapsed > 0:
            print(f"⚡ Average rate: {total_clicks/elapsed:.2f} clicks/sec")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n🔒 Closing browser...")
        driver.quit()

if __name__ == "__main__":
    collect_gems_fully_automated()