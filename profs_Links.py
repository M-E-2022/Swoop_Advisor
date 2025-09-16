from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time


# create webdriver object; Firefox
url = "https://www.ratemyprofessors.com/search/professors/4171?q=*&page={}"
options = webdriver.FirefoxOptions()
options.add_argument("detach")
driver = webdriver.Firefox(options = options)
driver.get(url) #send GET to page
time.sleep(5)



#hit load more button 
while True:
    try:
        prof_Links = set()
        # Find the "Load more" button by its Class name and click it
        load_more_button = driver.find_element(By.CLASS_NAME, "Buttons__Button-sc-19xdot-1")
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", load_more_button)
        time.sleep(5)
        load_more_button.click()
        time.sleep(5)
        #get html content after button is pressed    
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    # If no "Load More" button is found break out of the loop    
    except Exception as e:
        driver.quit()
        print("web driver stopped")
        break

    #get links
for cards in soup.find_all("a", class_="TeacherCard__StyledTeacherCard-syjs0d-0 eerjaA"):
    id_Num = cards.get('href')
    prof_Links.add("https://www.ratemyprofessors.com"+id_Num)
    
    

with open("uttyler_professor_links.csv", "w", newline="", encoding ="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # Write header row
    writer.writerow(["Profesor Links"])
    # Write all data rows
    for link in prof_Links:
        writer.writerow([link])
    print("Saved to CSV")