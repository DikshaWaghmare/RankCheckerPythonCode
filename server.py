# collect updated rank after minutes in excel file even closing browser

import sys
import atexit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import openpyxl
import schedule
import time

logfile_path = 'logfile.txt'
excel_file_path = 'rankings.xlsx'

def log(message):
    with open('logfile.txt', 'a') as f:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_message = f"{timestamp} {message}\n"
        f.write(log_message)
        print(log_message, end='')

def get_google_rankings(queries, website_urls):
    log("Getting Google rankings...")
    rankings = []
    try:
        # Set up a headless Chrome browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        for query, website_url in zip(queries, website_urls):
            # Construct the Google search URL
            query = query.replace(' ', '+')
            google_url = f"https://www.google.com/search?q={query}"

            # Open Google search in the browser
            driver.get(google_url)

            # Find and interact with search results
            search_results = driver.find_elements(By.CLASS_NAME, 'tF2Cxc')
            found = False  # Flag to check if the URL is found in the search results

            for index, result in enumerate(search_results):
                # Skip "People also ask" results
                if "related-question" in result.get_attribute('class'):
                    continue

                result_url = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if website_url in result_url:
                    rankings.append({"url": website_url, "query": query, "rank": index + 1})
                    found = True
                    break  # No need to continue checking for this URL in subsequent results

            if not found:
                # If the URL is not found, add a default rank of None
                rankings.append({"url": website_url, "query": query, "rank": None})

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()  # Make sure to quit the browser when done

    return rankings

def save_to_excel(results, date):
    log(f"Saving results to Excel file for {date}...")
    # Create or load the Excel workbook
    try:
        workbook = openpyxl.load_workbook(excel_file_path)
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        workbook.active.title = "Rankings"
        workbook.active.append(["URL", "Query", "Rank", "Modified Time"])
    sheet = workbook.active
    # Add data to the Excel sheet
    for result in results:
        result["modified_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append([result["url"], result["query"], result["rank"], result["modified_time"]])
    # Save the workbook to a file
    workbook.save(excel_file_path)
    log(f"Results saved to {excel_file_path}")

def check_rankings_and_save():
    log("Checking rankings and saving...")
    queries = ["cricbuzz", "stackoverflow", "github"]
    website_urls = ["https://www.cricbuzz.com/", "https://stackoverflow.com/", "https://github.com/"]

    # Get rankings
    rankings = get_google_rankings(queries, website_urls)

    # Save results to Excel file with the current date
    today = datetime.now().strftime("%Y%m%d")
    save_to_excel(rankings, today)

# Schedule the check_rankings_and_save function to run every week
# schedule.every().day.at("00:00").do(check_rankings_and_save)

# Schedule the check_rankings_and_save function to run every 5 minutes
schedule.every(5).minutes.do(check_rankings_and_save)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)



















'''
for running this code continuously in background: 
1. Open Command Prompt.
2. Navigate to the directory where your script is located.
3. Run the following command:
    pythonw listofurls.py
'''