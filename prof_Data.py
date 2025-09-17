from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time

#read in prof links from csv file 
with open("uttyler_professor_links.csv") as f:
    prof_Links = f.read().splitlines()[1:]  # [1:] skips header row

# create webdriver object; Firefox
options = webdriver.FirefoxOptions()
options.add_argument("detach")
driver = webdriver.Firefox(options = options)

for link in prof_Links:
    driver.get(link) #send GET to page
    time.sleep(10)
    