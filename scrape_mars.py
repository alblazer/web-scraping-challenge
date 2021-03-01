from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': "C:/Users/Rizky Gamal/.wdm/drivers/chromedriver/win32/88.0.4324.96/driver/chromedriver.exe"}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}

    # Checking out the nasa website
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    
    # I can't find them there's only soup
    soup = bs(html, 'html.parser')
    slide_element = soup.select_one("ul.item_list li.slide")
    slide_element.find("div", class_="content_title")
    
    # Scrape the latest News Title and Paragraph Text
    news_title = slide_element.find("div", class_="content_title").get_text()
    news_p = slide_element.find("div", class_="article_teaser_body").get_text()


    # Let's look at some pictures 
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html_image = browser.html
    # What do you mean there's only soup?
    soup = bs(html_image, 'html.parser')

    # Isolating the image url
    featured_image_url = soup.find_all('img')[2]["src"]

    # And now to check out some facts about Mars
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    html_image = browser.html
    
    # Reading the table with Pandas
    tables = pd.read_html(url)

    # Passing that table into a dataframe
    mars_facts_df = tables[2]
    mars_facts_df.columns = ["Description", "Value"]

    # Bringing it back to html
    mars_html = mars_facts_df.to_html()
    mars_html.replace('\n', '')

    # And now to check out the hemisepheres on Mars
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html_hemi = browser.html

    # It means there's only soup
    soup = bs(html_hemi, 'html.parser')

    hemisphere_image_urls = []
    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find element on each loop
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Get the hemisphere title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Find the images url
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Append objects to list
        hemisphere_image_urls.append(hemisphere)
        
        # Go back when looping
        browser.back()


    # Mars 
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict