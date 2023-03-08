from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set up the web driver
driver = webdriver.Chrome()

# Load the page
driver.get("https://www.myarkansaslottery.com/games/powerball/past-winners")

# Scroll to the bottom of the page
while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for the page to load new content
    time.sleep(2)

    # Check if we have reached the end of the page
    if driver.execute_script("return window.scrollY + window.innerHeight >= document.body.scrollHeight"):
        break

# Extract the content
content = driver.page_source

# Close the web driver
driver.quit()
