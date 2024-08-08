from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
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
    time.sleep(60)  # Increased sleep time for QR code scanning

    # Click on the group by its title within the pane-side div
    group_title = "IT$olutionJobs8"
    group_selector = f'span[title="{group_title}"]'
    
    wait_for_element(group_selector)
    group_element = driver.find_element(By.CSS_SELECTOR, group_selector)
    driver.execute_script("arguments[0].scrollIntoView(true);", group_element)
    group_element.click()
    print("Clicked on the group")

    # Wait for the group chat to load
    time.sleep(10)

    # Click on the group info
    info_button = wait_for_element('div[class="x78zum5 x1cy8zhl xisnujt x1nxh6w3 xcgms0a x16cd2qt"]')
    info_button.click()
    print("Clicked on group info")

    # Wait for group info to load
    time.sleep(10)

    # Click on "view all" to show all members
    view_all_button = wait_for_element('div[class="x1iyjqo2 x1yc453h x1n68mz9"]')
    view_all_button.click()
    print("Clicked on 'view all' to show all members")

    # Wait for the members div to load
    time.sleep(10)

    # Scroll to load all contacts incrementally
    members_div_class = 'x1n2onr6 x1n2onr6 xyw6214 x78zum5 x1r8uery x1iyjqo2 xdt5ytf x6ikm8r x1odjw0f x1hc1fzr x1tkvqr7'
    members_div = driver.find_element(By.CSS_SELECTOR, f'div[class="{members_div_class}"]')
    
    numbers = []  # Initialize list to store contact numbers

    # Ensure the scrollable area is targeted
    driver.execute_script("arguments[0].scrollTop = 0;", members_div)  # Scroll to top
    
    while True:
        # Fetch and store contacts from the visible part of the members div
        new_members = driver.find_elements(By.CSS_SELECTOR, 'div._ak8l > div._ak8o > div._ak8q > div._aou8 > span._ao3e')
        for member in new_members:
            number = member.text
            if number not in numbers:  # Avoid duplicates
                numbers.append(number)
        
        # Scroll down a small amount
        driver.execute_script("arguments[0].scrollTop += 1600;", members_div)  # Scroll down by 300 pixels
        time.sleep(2)  # Adjust sleep time as needed

        # Check if we reached the end
        new_members = driver.find_elements(By.CSS_SELECTOR, 'div._ak8l > div._ak8o > div._ak8q > div._aou8 > span._ao3e')
        if not new_members:
            break

    # Print or process the numbers as needed
    for number in numbers:
        print(number)

    phone_numbers_with_plus = [number for number in numbers if number.startswith('+')]

    # Define the CSV file path
    csv_file_path = 'phone_numbers.csv'

    # Write the phone numbers to the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write a header (optional)
        writer.writerow(['PhoneNumber'])
        # Write each phone number as a new row
        for number in phone_numbers_with_plus:
            writer.writerow([number])

    print(f"Phone numbers exported to {csv_file_path}")


except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()