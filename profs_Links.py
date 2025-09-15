#from the reviews get 
#course 
#quality
#difficulty 
#attendance
#textbook
#online class
#blob
#tags
#date

#once loaded it disapears on refresh
#profData drives then scrapes bc there is no refreshing, i need to drive and scrape at the same time; stateful web scraper 

#--PLAN--                   
#scan all current cards
#go into each and scrape - go into card load all html then parse 
#store last scraped prof name when run out of scanned cards to scrape 
#then hit load more button 
# once refreshed on a last scraped hit load more till find last scraped then load next cards keep moving last scraped pointer down
#stop when no load button AND last scraped is the last index of cards 


#the way im currently scraping is by loading all html and then parsing it- will prob need to do parsing periodicly  

#how do I store everything, cvs surely cant handle this much data (maybe it can), SQL how?
#figure out way to start on pointer of last scraped? -- leads to what is stored in cards array question 
#what does it store in cards; names? how to jump to a certain element in cards?
#how to tell which ones ive scraped already once I hit the load more button? -- use cards array and jump to last scraped then do last+1 index

'''
set last scraped index =-1 //int counter for index in cards
while true:
    scan all available cards 
    put in cards
    scrape all current cards in cards starting from pointer of last scraped + 1
        -click into current index card, load all html then scrape all
        load all data in SQLite
        upkeep last_scraped, ++
        if last scraped is last index in list:
            hit load more button until find last scraped and then hit load more button again to bring new cards
            update list 
            if else no button found:
                break while loop
''' 

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import re
import time


# create webdriver object; Firefox
url = "https://www.ratemyprofessors.com/search/professors/4171?q=*&page={}"
options = webdriver.FirefoxOptions()
options.add_argument("detach")
driver = webdriver.Firefox(options = options)
driver.get(url) #send GET to page
time.sleep(5)


#main loop
while True:
    try:
        

        #hit load more button 
        while True:
            try:
                # Find the "Load more" button by its Class name and click it
                load_more_button = driver.find_element(By.CLASS_NAME, "Buttons__Button-sc-19xdot-1")
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", load_more_button)
                time.sleep(5)
                load_more_button.click()
                time.sleep(5)
            except Exception as e:
                # If no "Load More" button is found break out of the loop
                print("No more elements to load. -- stops web driver")
                break

        #get html content        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        #get links
        for cards in soup.find_all("a", class_="TeacherCard__StyledTeacherCard-syjs0d-0 eerjaA"):
            print(cards.get('href'))


        
        













    #maybe load all profs then get links 
    #then soup .get all text once clicked into prof




            


    except Exception as e: 
        print("break driver loop")
        break



driver.quit()











# #get prof names then add to list
        # for card in cards:
        #     name_tag = card.find("div", class_="CardName__StyledCardName-sc-1gyrgim-0")
        #     name = name_tag.text.strip() if name_tag else "No Name"
        #     ProfsNames.append(name)
        #     Profs_links.append(card.get('href'))