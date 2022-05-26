#!/usr/bin/env python
# coding: utf-8

# In[353]:


# Import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


# In[354]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[355]:


url = 'https://redplanetscience.com/'
browser.visit(url)
# optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[356]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[357]:


# assign title and summary text to variables we'll reference later
slide_elem.find('div', class_='content_title')


# In[358]:


# use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[359]:


# use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[360]:


# visit URL
url = 'https://spaceimages-mars.com/'
browser.visit(url)


# In[361]:


# find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[362]:


html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[363]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[364]:


# use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[365]:


df = pd.read_html('https://galaxyfacts-mars.com/')[0]
df.columns = ['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[366]:


df.to_html()


# In[373]:


def hemisphere_images(browser):
    
    # store website URL in variable
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # tell the browser to visit the url
    browser.visit(url)

    # create the list that will hold the dictionaries
    hemisphere_image_urls = []

    # tell browser how to find the links to the pages w/ the images
    image_links = browser.find_by_tag('h3')

    # loop through the links
    for link in image_links:

        # create dictionaries to images and titles
        hemispheres = {}

        # click link but give website a chance to load
        time.sleep(1)

        link.click()

        # parse the html
        html = browser.html

        link_soup = soup(html, 'html.parser')

        try:
            downloads = link_soup.find('div', class_='downloads')
            hemi_images = downloads.find('a').get('href')

            title = link_soup.find('h2', class_='title').text

        except AttributeError:
            
            return None

        # add the images and titles to the dictionary
        hemispheres = {
            'image_url': hemi_images,
            'titl': title
        }

        hemisphere_image_urls.append(hemispheres)

        browser.back()

    return hemisphere_image_urls


# In[374]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_images(browser)


# In[375]:


# 5. Quit the browser
browser.quit()


# In[ ]:




