from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import csv

# read in professor links (skip header)
with open("uttyler_professor_links.csv") as f:
    prof_links = f.read().splitlines()[1:]

# setup Firefox WebDriver
options = webdriver.FirefoxOptions()
options.add_argument("--detach")
driver = webdriver.Firefox(options=options)

# prepare CSV output
output_file = "uttyler_professor_reviews_rag.csv"
fields = [
    "professor_name",
    "department",
    "overall_score",
    "num_ratings",
    "feedback_take_again",
    "tags",
    "review_text",
    "source_link"
]

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)

    for link in prof_links:
        driver.get(link)
        time.sleep(5)

        # keep clicking "Load More" until none left
        while True:
            try:
                load_btn = driver.find_element(By.CLASS_NAME, "Buttons__Button-sc-19xdot-1")
                if not load_btn.is_displayed():
                    break
                driver.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                    load_btn
                )
                time.sleep(1)
                load_btn.click()
                print("Clicked Load More button...")
                time.sleep(3)
            except NoSuchElementException:
                print("No more load button found.")
                break
            except Exception as e:
                print(f"Error clicking Load More: {e}")
                break

        # parse HTML
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # extract metadata
        prof_name_soup = soup.find("div", class_="NameTitle__Name-dowf0z-0")
        prof_name = prof_name_soup.text.strip() if prof_name_soup else None

        prof_score_soup = soup.find("div", class_="RatingValue__Numerator-qw8sqy-2")
        prof_score = (prof_score_soup.text.strip() + "/5") if prof_score_soup else None

        prof_num_ratings_soup = soup.find("div", class_="RatingValue__NumRatings-qw8sqy-0")
        prof_num_ratings = prof_num_ratings_soup.text.strip() if prof_num_ratings_soup else None

        prof_dep_soup = soup.find("div", class_="NameTitle__Title-dowf0z-1")
        prof_dep = prof_dep_soup.text.strip() if prof_dep_soup else None

        prof_feedback_soup = soup.find("div", class_="TeacherFeedback__StyledTeacherFeedback-gzhlj7-0")
        prof_feedback = prof_feedback_soup.text.strip() if prof_feedback_soup else None

        prof_tags_soup = soup.find("div", class_="TeacherTags__TagsContainer-sc-16vmh1y-0")
        prof_tags = ", ".join([tag.text.strip() for tag in prof_tags_soup.find_all("span")]) if prof_tags_soup else None

        # extract each review
        prof_reviews_soup = soup.find_all("div", class_="Rating__RatingBody-sc-1rhvpxz-0")
        if not prof_reviews_soup:
            # still write one entry if no reviews (so metadata not lost)
            writer.writerow([prof_name, prof_dep, prof_score, prof_num_ratings, prof_feedback, prof_tags, None, link])
            print(f"{prof_name}: No reviews found.")
        else:
            for review_card in prof_reviews_soup:
                parts = list(review_card.stripped_strings)
                review_text = " | ".join(parts)
                writer.writerow([
                    prof_name,
                    prof_dep,
                    prof_score,
                    prof_num_ratings,
                    prof_feedback,
                    prof_tags,
                    review_text,
                    link
                ])

        print(f"Saved reviews for {prof_name or 'Unknown Professor'}")

driver.quit()
print(f"\nAll professor review data saved to: {output_file}")
