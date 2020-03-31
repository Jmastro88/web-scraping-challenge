import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import re
import pandas as pd
import requests


def scrapeAll():
    # Inititiates webdriver that splinter controls
    browser = Browser('chrome', headless=False)
    title, para= mars_news(browser)

    # title1, photo1, title2, photo2, title3, photo3, title4, photo4=mars_hemis(browser)

    data={
        "featured_image": featured_image(browser),
        "mars_weather":mars_weather(browser),
        "mars_facts":mars_facts(browser),
        "mars_title": title,
        "mars_para": para,
        "hemispheres": mars_hemis(browser)
        # "hemi_title1": title1,
        # "hemi_photo1": photo1,
        # "hemie_title2": title2,
        # "hemi_photo2": photo2,
        # "hemi_title3": title3,
        # "hemi_photo3": photo3,
        # "hemi_title4": title4,
        # "hemi_photo4": photo4
        


    }
    browser.quit()
    return data

def featured_image(browser):
            # Image scape
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    base_url="https://www.jpl.nasa.gov"

    # Telling splinter to visit whatever URL is given
    browser.visit(url)

    # Selecting element on page
    browser.find_by_id("full_image").click()

    time.sleep(3)

    browser.links.find_by_partial_text("more info").click()

    # Grabs HTLM from selected page and converting to python readable text
    soup = bs(browser.html, 'html.parser')

    # Using beautiful soup to find an image tag with class 'main image'
    featured_image_url = base_url+soup.find("img", class_="main_image")["src"]

    return featured_image_url 

def mars_hemis(browser):
    url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(url)

    tags=browser.find_by_tag("h3")

    hemisphere_image_urls=[]


    for index_num in range(len(tags)):
        browser.find_by_tag("h3")[index_num].click()
        
        soup = bs(browser.html, 'html.parser')
        title= soup.find("h2", class_="title").text
    #     print(title)

        photo_link= soup.find("div", class_="downloads").find("a")["href"]
    #     print(photo_link)

        hemisphere_image_urls.append({
            "title": title,
            "photo": photo_link
        })
        
        browser.back()

        # title1= hemisphere_image_urls[0]["title"]
        # photo1= hemisphere_image_urls[0]["photo"]
        # title2 = hemisphere_image_urls[1]["title"] 
        # photo2 = hemisphere_image_urls[1]["photo"] 
        # title3 = hemisphere_image_urls[2]["title"] 
        # photo3 = hemisphere_image_urls[2]["photo"]
        # title4 = hemisphere_image_urls[3]["title"]
        # photo4 = hemisphere_image_urls[3]["photo"]


    return hemisphere_image_urls


def mars_weather(browser):
    url="https://twitter.com/marswxreport?lang=en"

    response = requests.get(url)
    weather_soup = bs(response.text, 'html.parser')

    tweets = weather_soup.find_all("p")
    for t in tweets:
        if 'InSight' in t.text:
            mars_weather = t.text
            break
    print(mars_weather)

    # browser.visit(url)
    # mars_weather="InSight sol 457 (2020-03-10) low -95.7ºC (-140.3ºF) high -9.1ºC (15.6ºF)\
    # winds from the SSE at 6.5 m/s (14.5 mph) gusting to 21.0 m/s (46.9 mph)\
    # pressure at 6.30 hPa"

    return mars_weather

def mars_facts(browser):
    url="https://space-facts.com/mars/"

    tables = pd.read_html(url)

    df = tables[0]
    df.columns = ['Statistic', 'Measurment']

    html_table = df.to_html(index=False)

    return html_table

def mars_news(browser):
    url="https://mars.nasa.gov/news"

    browser.visit(url)

    time.sleep(3)

    soup=bs(browser.html, 'html.parser')

    title=soup.find("li", class_="slide").find("div", class_="content_title").text
    
    para=soup.find("li", class_="slide").find("div", class_="article_teaser_body").text

    return title, para



