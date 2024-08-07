from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Path to chromedriver executable
chrome_driver_path = r"C:\Users\mabdu\Downloads\Compressed\chromedriver-win64\chromedriver.exe"  # Update this path

# Check if the chromedriver file exists
if not os.path.isfile(chrome_driver_path):
    raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Set up the ChromeDriver service
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print(f"Failed to initialize WebDriver: {e}")
    exit(1)

def wait_for_element(selector, by=By.CSS_SELECTOR, timeout=30):
    """Wait for an element to be present and visible."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, selector))
    )

try:
    # Navigate to WhatsApp Web
    driver.get("https://web.whatsapp.com/")

    # Wait for user to scan QR code and log in
    print("Please scan the QR code to log in.")
    time.sleep(30)  # Increase if needed

    # Click on the group by its title within the pane-side div
    group_title = "IT$olutionJobs8"
    group_selector = f'span[title="{group_title}"]'
    
    wait_for_element(group_selector)
    group_element = driver.find_element(By.CSS_SELECTOR, group_selector)
    driver.execute_script("arguments[0].scrollIntoView(true);", group_element)
    group_element.click()
    print("Clicked on the group")

    # Wait for the group chat to load
    time.sleep(5)

    # Click on the group info
    info_button = wait_for_element('div[class="x78zum5 x1cy8zhl xisnujt x1nxh6w3 xcgms0a x16cd2qt"]')
    info_button.click()
    print("Clicked on group info")

    # Wait for group info to load
    time.sleep(5)

    # Click on "view all" to show all members
    view_all_button = wait_for_element('div[class="x1iyjqo2 x1yc453h x1n68mz9"]')
    view_all_button.click()
    print("Clicked on 'view all' to show all members") #we dont have to print this we need data from this div class( class="_ak8l")

    # Wait for the members div to load
    time.sleep(5)

    # Scroll to load all contacts
    contacts = []
    members_div_class = 'x1n2onr6 x1n2onr6 xyw6214 x78zum5 x1r8uery x1iyjqo2 xdt5ytf x6ikm8r x1odjw0f x1hc1fzr x1tkvqr7'
    members_div = driver.find_element(By.CSS_SELECTOR, f'div[class="{members_div_class}"]')
    
    last_height = driver.execute_script("return arguments[0].scrollHeight", members_div)
    while True:
        # Scroll down
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", members_div)
        time.sleep(3)  # Adjust sleep time if needed
        
        # Check new scroll height and compare with last height
        new_height = driver.execute_script("return arguments[0].scrollHeight", members_div)
        if new_height == last_height:
            break
        last_height = new_height
    
    print ("456",members_div.get_attribute('outerHTML'))
    #     # Collect all contacts
    #     contacts_elements = driver.find_elements(By.CSS_SELECTOR, 'span[class="_ao3e"]')
    #     for contact in contacts_elements:
    #         contact_text = contact.text.strip()
    #         if contact_text and contact_text not in contacts:
    #             contacts.append(contact_text)


    # # Print all collected contacts
    # for contact in contacts:
    #     print(contact)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()
