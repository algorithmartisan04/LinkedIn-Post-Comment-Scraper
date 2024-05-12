import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

# Function to validate LinkedIn post URL
def validate_url(url):
    pattern = r'^https?://[\w\./]+\.linkedin\.com/(?:feed/update|posts)/[\w-]+$'
    return bool(re.match(pattern, url))

# Function to scrape comments from a LinkedIn post
def scrape_comments(url):
    # Initialize the web driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    # Wait for the page to load and scroll to the bottom to load all comments
    wait = WebDriverWait(driver, 10)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find all comment elements
    comment_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.comments-comments-list__comments-list')))

    comments = []
    for comment_element in comment_elements:
        name = comment_element.find_element_by_css_selector('span.comments-comment-renderer__name').text
        linkedin_url = comment_element.find_element_by_css_selector('a.app-aware-link').get_attribute('href')
        position = comment_element.find_element_by_css_selector('span.comments-comment-renderer__description').text
        comment_text = comment_element.find_element_by_css_selector('span.comments-comment-renderer__text').text

        comments.append({
            'name': name,
            'linkedin_url': linkedin_url,
            'position': position,
            'comment': comment_text
        })

    # Close the web driver
    driver.quit()

    return comments

def main():
    url = input("Enter the LinkedIn post URL: ")
    if validate_url(url):
        comments = scrape_comments(url)

        # Display the comments data
        for comment in comments:
            print(f"Name: {comment['name']}")
            print(f"LinkedIn URL: {comment['linkedin_url']}")
            print(f"Position: {comment['position']}")
            print(f"Comment: {comment['comment']}")
            print("-" * 50)

        # Save the comments data to a CSV file
        with open('comments.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'linkedin_url', 'position', 'comment']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for comment in comments:
                writer.writerow(comment)

        print(f"Comments data saved to 'comments.csv' file.")
    else:
        print("Invalid URL. Please enter a valid LinkedIn post URL.")

if __name__ == "__main__":
    main()