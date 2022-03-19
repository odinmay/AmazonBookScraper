from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from pprint import pprint

browser = webdriver.Firefox()


def read_url_file(path):
    with open(path, "r", encoding="utf-8") as file:
        urls = file.read().split(",")
        return urls


# Grab the url
def get_html(url=None):
    """
    This function will load selenium and grab data from the website and return it as a tuple

    :param url: A string of the url for the product you want to scrape, defaults to None
    :type url: str

    :rtype: tuple
    :return: Returns a tuple with the data in order (Title, Author, Publisher, ISBN, Price)
    """
    # Navigate to the url
    browser.get(url)

    # Wait 2 seconds
    browser.implicitly_wait(2)

    # Grab title element
    title = browser.find_element(by=By.CSS_SELECTOR, value="#productTitle")

    # Grab price element
    # If theres an error (Like a missing element)...
    # If so, the element may be under a different css selector, so we try the other selector within the except block
    try:
        price = browser.find_element(by=By.CSS_SELECTOR, value="#price")
    except:
        # Grab price element
        price = browser.find_element(by=By.CSS_SELECTOR, value=".a-text-price > span:nth-child(1)")

    try:
        # Grab author element
        author = browser.find_element(by=By.CSS_SELECTOR, value=".contributorNameID")
    except:
        author = browser.find_element(by=By.CSS_SELECTOR, value="span.author:nth-child(2) > a:nth-child(1)")

    # Grab publisher element
    publisher = browser.find_element(by=By.CSS_SELECTOR,
                                     value="ul.a-vertical:nth-child(1) > li:nth-child(1) > span:nth-child(1) > span:nth-child(2)")

    # Grab isbn element
    isbn = browser.find_element(by=By.CSS_SELECTOR,
                                value="ul.a-vertical:nth-child(1) > li:nth-child(4) > span:nth-child(1) > span:nth-child(2)")

    return title.text, author.text, publisher.text, isbn.text, price.text


def scrape_data(urls) -> list:
    book_list = []
    counter = 1
    total = len(urls)

    for url in urls:
        if len(url) < 10:
            print("Invalid url")
            continue

        data = get_html(url)

        book_list.append(data)
        print(f"{counter}/{total} complete")
        counter += 1

    return book_list
    # book_info = f"{data[0]} {data[1]} {data[2]} {data[3]} {data[4]}"


def write_csv(book_list):
    headers = ["Title", "Author", "Publisher", "ISBN", "Price"]

    with open("Books.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for row in book_list:
            writer.writerow(row)


if __name__ == "__main__":
    print("Reading url list")
    urls = read_url_file("book_list.txt")

    print("Scraping book data..")
    book_data = scrape_data(urls)
    print("Data Successfully Scraped")

    print("Writing to csv file")
    write_csv(book_data)

    print("Process complete!")
