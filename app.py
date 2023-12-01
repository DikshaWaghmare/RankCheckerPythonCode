# simpe code for finding ranking from query and url

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_google_ranking(query, website_url):
    try:
# Set up a headless Chrome browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        # Construct the Google search URL
        query = query.replace(' ', '+')
        google_url = f"https://www.google.com/search?q={query}"

        # Open Google search in the browser
        driver.get(google_url)

        # Find and interact with search results
        search_results = driver.find_elements(By.CLASS_NAME, 'tF2Cxc')

        for index, result in enumerate(search_results):
            # Skip "People also ask" results
            if "related-question" in result.get_attribute('class'):
                continue

            result_url = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if website_url in result_url:
                return index + 1  # Adding 1 to make it human-readable (1-based index)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    # finally:
    #     driver.quit()  # Make sure to quit the browser when done

    return None

# Example usage
query = "cricbuzz"
website_url = "https://www.cricbuzz.com/"
ranking = get_google_ranking(query, website_url)

if ranking:
    print(f"The website {website_url} is ranked #{ranking} on Google for the query '{query}'.")
else:
    print(f"The website {website_url} is not found in the search results for the query '{query}'.")















