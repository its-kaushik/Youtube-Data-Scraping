from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
import mysql.connector


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

service = Service("C:\Program Files (x86)\chromedriver.exe")
driver = webdriver.Chrome(service=service, chrome_options=chrome_options )

def gettingChannelLinks(searchText):
    url = "https://www.youtube.com/results?search_query="+searchText.replace(' ', '+')

    driver.get(url)

    searchResultChannels = driver.find_elements(by=By.XPATH, value='//*[@id="text"]/a')

    channelLinks = []

    for channelNameElement in searchResultChannels:
        channelLinks.append(channelNameElement.get_attribute('href'))

    channelLinks = list(set(channelLinks))

    for link in channelLinks:
        print(link)
    
    return channelLinks

keyword = input("Enter The Search Keyword")
channelLinks = gettingChannelLinks(keyword)

def visitingChannel(url):
    driver.get(url+'/about')
    time.sleep(3)

    channelName = driver.find_element(by=By.XPATH, value='//*[@id="text"]').text
    channelURL = url
    channelDescription = driver.find_element(by=By.XPATH, value='//*[@id="description-container"]').text

    channelEmail = re.findall('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', channelDescription)

    if(len(channelEmail)):
        channelEmail = channelEmail[0] 
    else:
        channelEmail = 'N/A'

    channelDetail = {
        'name': channelName, 
        'url': channelURL, 
        'description': channelDescription,
        'email': channelEmail
    }

    return channelDetail

data = []

for link in channelLinks:
    data.append(visitingChannel(link))

dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="admin@1234",
  database = "youtubescrapper"
)

cursorObject = dataBase.cursor()

for channel in data:
    sql = "INSERT INTO channelData (name, url, description, email)\
    VALUES (%s, %s, %s, %s)"
    val = (channel['name'], channel['url'], channel['description'], channel['email'])
    cursorObject.execute(sql, val)
    dataBase.commit()

dataBase.close()