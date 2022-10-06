# Import the required modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
options = Options() 
options.add_argument('--headless') 
options.add_argument('--disable-gpu') # Last I checked this was necessary. 
driver = webdriver.Chrome("C://Users//henri//Downloads//chromedriver_win32 (1)//chromedriver.exe", chrome_options=options)
driver = webdriver.Chrome("C://Users//henri//Downloads//chromedriver_win32 (1)//chromedriver.exe")