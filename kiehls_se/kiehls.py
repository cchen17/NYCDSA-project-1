from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import re


# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\the\chromedriver.exe')
driver = webdriver.Chrome(r'C:\nydsa bootcamp slides\web scrapting\Selenium\chromedriver.exe')
# Go to the page that we want to scrape
driver.get("https://www.kiehls.com/skincare/view-all-skincare/ultra-facial-cream/622.html?cgid=face-view-all&dwvar_622_size=1.7%20fl.%20oz.%20Jar")

# Click review button to go to the review section
#review_button = driver.find_element_by_xpath('//span[@class="padLeft6 cursorPointer"]')
#review_button.click()
csv_file = open('reviews.csv', 'w', encoding='utf-8')
writer = csv.writer(csv_file)
# Page index used to keep track of where we are.
index = 1

# We want to start the first two pages.
# If everything works, we will change it to while True
while True:
	try:
		time.sleep(1)
		print("Scraping Page number " + str(index))
		index = index + 1
		# Find all the reviews. The find_elements function will return a list of selenium select elements.
		# Check the documentation here: http://selenium-python.readthedocs.io/locating-elements.html

		wait_review=WebDriverWait(driver, 5)
		reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH,'//span[@itemprop="review"]')))

		print (len(reviews))
		print ("="*50)
		# Iterate through the list and find the details of each review.

		for review in reviews:
			# Initialize an empty dictionary for each review
			review_dict = {}
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use `element.get_attribute()`

			date_published = review.find_element_by_xpath('.//meta[@itemprop="datePublished"]').get_attribute('content')
			title = review.find_element_by_xpath('.//span[@itemprop="name"]').text
			rating = review.find_element_by_xpath('.//span[@class="BVRRNumber BVRRRatingNumber"]').get_attribute('innerHTML')
			#print(rating.get_attribute('innerHTML'))
			try:
				userlocation = review.find_element_by_xpath('.//span[@class="BVRRValue BVRRUserLocation"]').text
			except Exception as e:
				userlocation = None
			text =review.find_element_by_class_name('BVRRReviewText').text
			try:
				cons=review.find_element_by_xpath('.//span[@class="BVRRValue BVRRReviewConTags"]/span').get_attribute('innerHTML')
			except Exception as e:
				cons= None

			#print (cons)
			#print ('*'*50)

			review_dict['rating'] = rating
			review_dict['userlocation'] = userlocation
			review_dict['date_published']=date_published
			review_dict['title']=title
			review_dict['cons'] = cons
			review_dict['text']=text


			writer.writerow(review_dict.values())

		# Locate the next button element on the page and then call `button.click()` to click it.

		# next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,'.//a[text()="Next Page"]')))

		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		#time.sleep(1)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1000);")
		wait_button = WebDriverWait(driver, 3)
		next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,'.//a[text()="Next Page"]')))
		next_button.click()

		# ActionChains(driver).move_to_element(next_button_area).click(next_button).perform()

	except Exception as e:
		print("end",e)
		driver.close()
		csv_file.close()
		break


