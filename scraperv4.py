import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from datetime import datetime

# Set up the web driver
driver = webdriver.Chrome()

# Load the page
driver.get("https://www.myarkansaslottery.com/games/powerball/past-winners")

# Scroll down on the webpage for a duration of 5 seconds
scroll_duration = 60 # in seconds
start_time = time.time()
while (time.time() - start_time) < scroll_duration:
    driver.execute_script("window.scrollBy(0, 4000);")
    time.sleep(2)

# Extract the content
content = driver.page_source

# Create a BeautifulSoup object
soup = BeautifulSoup(content, 'html.parser')

# Extract the dates, reformat them to mm/dd/yyyy format
dates_raw = [h2.text.replace('Powerball® Winners Data - ', '') for h2 in soup.find_all('h2') if 'Powerball® Winners Data -' in h2.text]
dates = [datetime.strptime(date, '%A %B %d, %Y').strftime('%m/%d/%Y') for date in dates_raw]

# Extract the winning numbers and special numbers
winners_numbers = [element.text for element in soup.find_all('div', {'class': 'draw-game__number'})]
special_numbers = [int(tag.text) for tag in soup.find_all('div', {'class': 'draw-game__number-special'})]

# Create a table and add the headers
table = PrettyTable()
table.field_names = ["Date", "Winning Numbers", "Special Number"]

# Add rows to the table
for i in range(len(dates)):
    table.add_row([dates[i], " ".join(winners_numbers[i*5:i*5+5]), special_numbers[i]])

# Print the table
print(table)

# Save the data to a CSV file
with open('../powerball_winners.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Date', 'Winning Numbers', 'Special Number']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(dates)):
        writer.writerow({'Date': dates[i], 'Winning Numbers': " ".join(winners_numbers[i*5:i*5+5]), 'Special Number': special_numbers[i]})
