from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://forms.gle/auE7evYtCqXTgq1k7")

name_field = driver.find_element_by_id("entry.//*[@id='mG61Hd']/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/inputYOUR_FIELD_ID")
name_field.send_keys("John Smith")

form = driver.find_element_by_tag_name("form")
form.submit()

driver.close()

