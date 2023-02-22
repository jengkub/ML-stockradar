from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
import pyautogui
import time
 


class autofill:
    def __init__(self):
        op = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=op)
        self.driver.get("https://accounts.google.com/v3/signin/identifier?dsh=S671932125%3A1673681827825897&continue=https%3A%2F%2Fdocs.google.com%2Fforms%2Fd%2Fe%2F1FAIpQLSeI8-SaZ-ZbgvWkM5GWLe3otPM4eQ41QOEQ7PGB77QTb6ESlw%2Fviewform&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AeAAQh7p9ky2oFedWZiH4cTpk31a6uHTQYs9SsOz-ldmhEpnvPa-jxID-0SmBY31LF6Wm0q1MSZcXg")
        

    def login(self):
        userinput = self.driver.find_element(By.XPATH, "//*[@id='identifierId']") 
        nextbutton = self.driver.find_element(By.XPATH, "//*[@id='identifierNext']/div/button")

        userinput.send_keys("กรอกอีเมล์")
        time.sleep(0.5)
        nextbutton.click()
        time.sleep(5)

        passwordinput = self.driver.find_element(By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input")
        nextbutton = self.driver.find_element(By.XPATH, "//*[@id='passwordNext']/div/button")

        passwordinput.send_keys("กรอกรหัสผ่าน")
        time.sleep(0.5)
        nextbutton.click()
        time.sleep(5)


    def fillpage1(self):
        #page 1
        radiobutton1 = self.driver.find_element(By.XPATH, "//*[@id='i8']")
        pagebutton = self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div")
        checkbox1 = self.driver.find_element(By.XPATH, "//*[@id='i22']")
        checkbox2 = self.driver.find_element(By.XPATH, "//*[@id='i25']")
        dropdown = self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div")
        textbox1 = self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input")

        radiobutton1.click()
        time.sleep(0.5)
        checkbox1.click()
        time.sleep(0.5)
        checkbox2.click()
        time.sleep(0.5)
        dropdown.click()
        time.sleep(0.5)
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        textbox1.send_keys("Hello World")
        time.sleep(0.5)
        pagebutton.click()
        time.sleep(5)

    def fillpage2(self):
        #page 2
        textbox2 = self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
        date = self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input")
        check = self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[4]/div/div/div[2]/div[1]/span/div/label[3]/div[2]/div/div")
        submitbutton = self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div[2]")

        textbox2.send_keys("2")
        time.sleep(0.5)
        date.click()
        time.sleep(0.5)
        pyautogui.press('left')
        time.sleep(0.5)
        pyautogui.press('left')
        time.sleep(0.5)
        date.send_keys("01")
        time.sleep(0.5)
        date.send_keys("11")
        time.sleep(0.5)
        date.send_keys("2023")
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        check.click()
        time.sleep(0.5)
        submitbutton.click()

    def close(self):
        self.driver.close()



form = autofill()
form.login()
form.fillpage1()
form.fillpage2()
form.close()