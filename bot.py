from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import wget
import configparser
import urllib.request



class InstaBot:

  def __init__ (self, username, password):
    self.username = username
    self.password = password

    self.driver = webdriver.Edge('msedgedriver.exe')
    self.base_url = 'https://www.instagram.com'

    self.login()
    

  def login(self):
    self.driver.get('{}/accounts/login/'.format(self.base_url))

    username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username.clear()
    password.clear()

    username.send_keys(self.username)
    password.send_keys(self.password)

    logIn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    logIn.click()

    not_now = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))

    not_now.click()

    time.sleep(2)

  def directUser(self, user):
    self.driver.get('{}/{}/'.format(self.base_url, user))

  def infiniteScroll(self):

    self.last_height = self.driver.execute_script("return document.body.scrollHeight")

    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(5)

    self.new_height = self.driver.execute_script("return document.body.scrollHeight")

    if self.new_height == self.last_height:
      return True
    
    self.last_height = self.new_height
    return False


  def downloadContent(self, user):

    self.directUser(user)

    img_srcs = []
    finished = False
    while not finished:
      finished = self.infiniteScroll()

      img_srcs.extend([img.get_attribute('src') for img in self.driver.find_elements_by_class_name('FFVAD')])

    img_srcs = list(set(img_srcs))

    for idx, src in enumerate(img_srcs):
      self.downloadImage(src,idx,user)

  
  def downloadImage(self, src, image_filename, folder):

    folder_path = './{}'.format(folder)

    if not os.path.exists(folder_path):
      os.mkdir(folder_path)

    img_filename = 'image_{}.jpg'.format(image_filename)
    urllib.request.urlretrieve(src, '{}/{}'.format(folder, img_filename))

if __name__ == '__main__':

  config_path = 'config.ini'
  cparser = configparser.ConfigParser()
  cparser.read(config_path)

  username = cparser['IG_AUTH']['USERNAME']
  password = cparser['IG_AUTH']['PASSWORD']

  botIG = InstaBot(username, password)
  
  botIG.directUser('dlwlrma')
  botIG.downloadContent('dlwlrma')


