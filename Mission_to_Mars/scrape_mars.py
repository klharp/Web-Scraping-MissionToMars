from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import requests


def scrape_all():
    # Define the path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)



#### Current news: this will pass 2 variable strings ####

    # Initiate the browser
    url1 = 'https://redplanetscience.com/'
    browser.visit(url1)

    # Parse into Beautiful Soup object
    news_html = browser.html
    soup = BeautifulSoup(news_html, "html.parser")

    # Retrieve latest news elements
    articles = soup.find("div", class_ = "list_text")
   
    # Use BeautifulSoup's find() method to navigate and retrieve attributes
    news_title = articles.find("div", class_ = "content_title").text
    news_body = articles.find("div", class_ = "article_teaser_body").text



#### Image url: this will pass a string url ####

    # Initialize the browser
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

    # Parse into Beautiful Soup object
    image_html = browser.html
    soup = BeautifulSoup(image_html, "html.parser")

    # Find the image url
    image_path = soup.find("img", class_ = "headerimage")["src"]
    featured_img_url = "https://spaceimages-mars.com/"+image_path



#### Facts: this will pass html table ####

    # Scrape the table using pandas
    url3 = "https://galaxyfacts-mars.com/"
    
    tables = pd.read_html(url3)

    # First Table 
    df1 = tables[0]

    # Rename headers
    df1 = df1.rename(columns = {0:'Description', 1:'Mars', 2:'Earth'})

    # Drop the first row
    facts_df = df1[df1.Mars != "Mars"]

    # Reset index
    facts_df = facts_df.set_index(["Description"])

    # Rename headers
    df1 = df1.rename(columns = {0:'Description', 1:'Mars', 2:'Earth'})
    df1.head()

    # Parse to an html string
    fact_table = facts_df.to_html()



#### Hemispheres: This will pass a list of dictionaries ####
    
    # Initialize the browser
    url5 = "https://marshemispheres.com/"
    browser.visit(url5)

    # Parse into Beautiful Soup object
    hemi2_html = browser.html
    soup = BeautifulSoup(hemi2_html, "html.parser")

    # Retrieve all elements that contain image URLs (in an html table)
    links = soup.find_all("div", class_ = "description")

    # Create empty list for dictionaries
    hemisphere_image_urls = []

    # Iterate through the page
    for link in links:
    
        # Add delay (had to add this because I got put in timeout jail)
        time.sleep(5)
        
        # Use BeautifulSoup's find() to navigate and retrieve attributes
        img_title = link.find("h3").text
        img_link = link.find("a", class_ = "itemLink product-item")["href"]
    
        # Find the link with the full res image
        browser.visit(url5 + img_link)
    
        # HTML object
        link = browser.html
    
        # Parse HTML with BeautifulSoup
        linksoup = BeautifulSoup(link, "html.parser")
    
        # Full resolution image URL
        url = url5 + linksoup.find("img", class_ = "wide-image")["src"]
    
        # Append to list of dictionaries
        hemisphere_image_urls.append({"title":img_title, "img_url":url})

    #print(hemisphere_image_urls)


    # Store scraping functions in a dictionary
    mars_dict = {
        "id": 1,
        "news_title": news_title,
        "news_body": news_body,
        "featured_img_url": featured_img_url,
        "facts_table": fact_table,
        "hemispheres": hemisphere_image_urls
    }

    return mars_dict
    
if __name__== "__main__":
    print(scrape_all())

