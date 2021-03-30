from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time


# def scrape_news():
#     # Define the path
#     executable_path = {'executable_path': ChromeDriverManager().install()}
#     browser = Browser('chrome', **executable_path, headless=False)
    
#     # Initiate the browser
#     url1 = 'https://redplanetscience.com/'
#     browser.visit(url1)

#     # Parse into Beautiful Soup object
#     news_html = browser.html
#     soup = BeautifulSoup(news_html, "html.parser")

#     # Iterate through all cards of the news in the bootstrap code
#     # Retrieve all elements that contain News Titles and Paragraph Text
#     articles = soup.find_all("div", class_ = "list_text")
   
#     # Iterate through each card and retrieve headline and paragraph
#     for article in articles:
       
#      # Use BeautifulSoup's find() method to navigate and retrieve attributes
#         news_title = article.find("div", class_ = "content_title").text
#         news_body = article.find("div", class_ = "article_teaser_body").text
    
#         print("------------------------------------------")
#         print(f"Headline:  {news_title}")
#         print(f"Content:  {news_body}")
   
#         # Dictionary to be inserted as a MongoDB document
#         post = {"Headline": news_title, 
#             "Content": news_body,
#            }
           
#         collection.insert_one(post)


#     # Quit the browser
#     browser.quit()

#     return collection

def scrape_feature():    
    # Define executable path and initialize the browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Initialize the browser
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

    # Parse into Beautiful Soup object
    image_html = browser.html
    soup = BeautifulSoup(image_html, "html.parser")

    # Find the image url
    image_path = soup.find("img", class_ = "headerimage")["src"]
    featured_img_url = "https://spaceimages-mars.com/"+image_path

    return featured_img_url

    browser.quit()


def scrape_facts():  
    # Scrape the table using pandas
    url3 = "https://galaxyfacts-mars.com/"
    
    tables = pd.read_html(url3) 

    # First Table 
    df1 = tables[0]
    # Drop the Earth column
    df1 = df1.drop([2], axis=1)
    # Rename headers
    df1 = df1.rename(columns = {0:'Fact', 1:'Data'})
    # Drop the first row
    df1[df1.Fact != "Mars - Earth Comparison"]

    # Second Table 
    df2 = tables[1]
    # Rename headers
    df2 = df2.rename(columns = {0:'Fact', 1:'Data'})
    facts_df = df1.append(df2, ignore_index=True, sort=False)

    return featured_facts_df

    browser.quit()

    
def scrape_hemi():  
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

    return hemisphere_image_urls


    # Close remote browser
    browser.quit()