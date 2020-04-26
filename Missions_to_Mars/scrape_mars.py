#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

# Connect to the Chrome browser
def init_browser():
    executable_path = {"executable_path": "C:/Users/cindy/Downloads/chromedriver_win32/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
    
def scrape():
    browser = init_browser()

    # # NASA Mars News

    # In[8]:


    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())


   
    # find most recent news title from mars.nasa.gov

    news_title = soup.find_all('div', class_='content_title')[1].text
    print(news_title)


    # In[11]:


    # find the paragraph for the most recent news title from mars.nasa.gov

    news_p = soup.find('div', class_='article_teaser_body').text    
    print(news_p)


    # # JPL Mars Space Images - Featured Image

    # In[12]:


    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html

    # click the button to get to the page with the full image, wait 5 seconds for the page to load and click next button

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)

    browser.click_link_by_partial_text('more info')


    # In[14]:


    html = browser.html
    soup_jpl = BeautifulSoup(html, "html.parser")
    print(soup_jpl.prettify())


    # In[15]:


    featured_url_image1 = soup_jpl.find('figure', class_='lede')
    # print(featured_url_image1)


    # In[16]:


    featured_url_image2 = featured_url_image1.find('a')['href']

    featured_image_url = f'https://www.jpl.nasa.gov{featured_url_image2}'
    print(featured_image_url)


    # # Mars Weather twitter account

    # In[24]:


    #  Added in a sleep timer to allow all the data to load

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(10)

    html = browser.html
    soup_twitter = BeautifulSoup(html, "html.parser")
    print(soup_twitter.prettify())


   # re is Python 'regular expression' programming language embedded in Python to perform matching.
    import re
    pattern = re.compile(r'sol')

    mars_weather = soup_twitter.find('span', text=pattern).text
    print(mars_weather)


    # # Mars Facts

    # In[50]:


    # This will read HTML tables into a list of dataframe objects

    url = "https://space-facts.com/mars/"
    mars_list = pd.read_html(url)
    mars_list2 = mars_list[2]
    mars_list2


   
    # Rename the columns
    mars_list2.columns = ['Feature', 'Value']
    print(mars_list2)


   
    # put the data back into html format with html tags
    mars_list2 = mars_list2.set_index('Feature')
    mars_facts_html = mars_list2.to_html(classes='table table-bordered')
    mars_facts_html


    # # Mars Hemispheres

   
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(10)

    html = browser.html
    soup_hemi = BeautifulSoup(html, "html.parser")
    print(soup_hemi.prettify())


    
    hemi_list = soup_hemi.find('div', class_='collapsible results')
    print(hemi_list.prettify)

 


    hemi_list2 = hemi_list.find_all('div', class_='item')
    print(hemi_list2)
  


    # loop through the HTML to find the 4 hemispheres and the URL for the image.  Put into a dictionary.

    hemi_dict = []

    for x in hemi_list2:
        title = x.find("h3").text
        print (title)
        title = title.replace("Enhanced", "")
        link = x.find("a")["href"]
        img_link = "https://astrogeology.usgs.gov" + link
        print (img_link)
        browser.visit(img_link)
        time.sleep(5)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        image = soup.find('div', class_='downloads')
        image2 = image.find("a")["href"]
        hemi_dict.append({"title": title, "img url": image2})

    hemi_dict

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts_html,
        "hemisphere_image_urls": hemi_dict
    }

    browser.quit()
    return mars_data

if __name__ == '__main__':
    scrape()