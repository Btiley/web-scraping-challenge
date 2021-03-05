from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome',**executable_path, headless=False)

    return browser

def scrape_all():
    final_dict = {}
    browser = init_browser()
    
    #Mars News
    url_n = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response_n = requests.get(url_n)
    soup_n = bs(response_n.text, 'html.parser')
    
    Latest_title = soup_n.find_all('div', class_ ='content_title')[0].text.strip()
    Latest_paragraph = soup_n.find_all('div', class_ = 'rollover_description_inner')[0].text.strip()

    #Mars Info
    table = pd.read_html('https://space-facts.com/mars/')
    info_table = table[0]
    info_table.columns = ['Description','Mars']
    info_table = info_table.set_index("Description")
    info_html = info_table.to_html(index=False)


    #JPL Image
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    index = 'index.html'
    browser.visit(url+index)
    
    
    # Parse HTML with Beautiful Soup
    html = browser.html
    image_soup = bs(html, 'html.parser')
    
    #Select main image
    header = image_soup.find('img',class_ = 'headerimage')
    #get image url
    f_img = header['src']
    featured_image_url = url + f_img
    

    #Hemispheres Images
    home_page = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'  
    site = 'https://astrogeology.usgs.gov'
    page = requests.get(home_page)

    soup = bs(page.text, 'html.parser')
    hemi_urls = []
    
    for item in soup.findAll('div', attrs = {'class':'item'}):
        hemi_dict = {}
    
        hemi_dict['title'] = str(item.find_all('div', attrs = {'class':'description'})[0].text)
    
        hemi_url = site + str(item.find_all('a', href = True)[0]['href'])
    
        hemi_page = requests.get(hemi_url)
    
        hemi_soup = bs(hemi_page.text, 'html.parser')
    
    for items in hemi_soup.findAll('div',attrs = {'class':'wide-image-wrapper'}):
        
        hemi_dict['img_url'] = str(items.ul.li.find_all('a', href = True)[0]['href'])
        
        hemi_urls.append(hemi_dict)
        
    

    final_dict = {"Latest_title": Latest_title,
        "Latest_paragraph": Latest_paragraph,
        "Mars_Info": info_html,  
        "Featured_image": featured_image_url,
        "Hemispheres_image": hemi_urls}
    browser.quit()
    return final_dict

