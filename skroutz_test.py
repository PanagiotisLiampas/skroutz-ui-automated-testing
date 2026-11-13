from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.get("https://www.skroutz.gr")

wait = WebDriverWait(driver, 40)

# 1. Αναζήτηση
search_bar = wait.until(EC.presence_of_element_located((By.ID, "search-bar-input")))
search_bar.send_keys("κάρτα γραφικών")
search_bar.send_keys(Keys.RETURN)

# 2. Εισαγωγή Ελάχιστης Τιμής (Το σωστό ID είναι price_min)
min_price = wait.until(EC.presence_of_element_located((By.ID, "price_min")))
min_price.send_keys("200")

# 3. Εισαγωγή Μέγιστης Τιμής (Το σωστό ID είναι price_max)
max_price = driver.find_element(By.ID, "price_max")
max_price.send_keys("300")
max_price.send_keys(Keys.RETURN)

time.sleep(5)

print("\n Ξεκινάει η Εξαγωγή Τιμών και ο Έλεγχος")

# 4. Βρίσκουμε όλα τα στοιχεία που περιέχουν τις τιμές
price_elements = driver.find_elements(By.CSS_SELECTOR, "a.js-sku-link, .price")

prices_list = []
for element in price_elements:
    text = element.text
    if text and "€" in text:
        # Καθαρισμός κειμένου για μετατροπή σε αριθμό
        clean_text = text.replace("€", "").replace(".", "").replace(",", ".").strip()
        try:
            price_float = float(clean_text)
            prices_list.append(price_float)
        except ValueError:
            pass

print(f"Βρέθηκαν {len(prices_list)} τιμές προϊόντων στην πρώτη σελίδα.")

# 5. Το τελικό Test
test_passed = True
for price in prices_list:
    if not (200 <= price <= 300):
        print(f" Βρέθηκε λάθος τιμή! Η τιμή {price}€ είναι εκτός ορίων (200€-300€).")
        test_passed = False

if test_passed and len(prices_list) > 0:
    print("\n QA TEST PASSED: Όλες οι τιμές είναι σωστά φιλτραρισμένες μεταξύ 200€ και 300€!")
elif len(prices_list) == 0:
    print("\n QA TEST WARNING: Δεν βρέθηκαν τιμές.")
else:
    print("\n QA TEST FAILED: Το φίλτρο εμφάνισε αποτελέσματα εκτός ορίων.")

driver.quit()