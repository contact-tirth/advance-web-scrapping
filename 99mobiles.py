from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
import time

# Setup Chrome driver path
s = Service("C:/Users/tirth/Desktop/chromedriver.exe")

# Setup browser options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")

# Create driver
driver = webdriver.Chrome(service=s, options=options)

# Bypass detection
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
    """
})

# Open the target site
driver.get('https://www.91mobiles.com/samsung-mobile-price-list-in-india')
wait = WebDriverWait(driver, 10)

# Click first checkbox //*[@id="pfcameraresolution6401500"]
# checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pfcameraresolution6401500"]')))
# checkbox.click()
# time.sleep(2)  # let filter apply
all_html = []
# Keep clicking Load More until it's gone
while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        all_html.append(driver.page_source)

        buttons = driver.find_elements(By.XPATH, '//*[@id="finder_pagination"]//span[contains(@onclick, "next")]')
        load_more = None
        for btn in buttons:
            if btn.is_displayed() and btn.is_enabled():
                load_more = btn
                break

        if load_more is None:
            print("No more 'Next' button found.")
            break


        # Try JS click to avoid interception
        driver.execute_script("arguments[0].click();", load_more)

        time.sleep(5)

    except Exception as e:
        print(f"Exception: {e}")
        break




# Save the full HTML after loading
# html1 = driver.page_source
with open('mobiles6.html', 'w', encoding='utf-8') as f:
    f.write('<html><head><title>Combined Products</title></head><body>\n')
    f.write('\n'.join(all_html))
    f.write('\n</body></html>')

print("Done. Saved full page to 'mobiles.html'")
input("Press Enter to close browser...")
driver.quit()
