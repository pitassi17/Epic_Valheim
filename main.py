# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
import warnings
import os
import shutil

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

DOWNLOAD_PATH = "C:\\temporary\\"

def read_config():
    pass

def configure_options(chrome_options):
    # run in the background with no window
    #chrome_options.add_argument("--headless")

    # change download directory
    if not os.path.exists(DOWNLOAD_PATH):
       os.makedirs(DOWNLOAD_PATH)
    prefs = {"download.default_directory" : DOWNLOAD_PATH}
    chrome_options.add_experimental_option("prefs", prefs)

def nexus_login(driver):
    username = 'pitassi17@gmail.com'
    password = 'Jinglebells1221'
    url = 'https://users.nexusmods.com/'
    driver.get(url)
    driver.find_element(value='user_login').send_keys(username)
    driver.find_element(value='password').send_keys(password)
    driver.find_element_by_name('commit').click()

def get_zip_name(driver):
    filename_element = driver.find_element(By.XPATH, "//div[@class='container']//div[@class='page-layout']//div[@class='header']")
    return filename_element.get_attribute('innerHTML').strip().split('<')[0]

def nexus_manual_download(game, mod_id):
    chrome_options = Options()
    configure_options(chrome_options)

    driver = Chrome(chrome_options=chrome_options)

    url = "https://www.nexusmods.com/{game}/mods/{mod_id}?tab=files".format(game=game, mod_id=mod_id)
    driver.get(url)
    driver.find_element(By.ID, 'file-container-main-files').\
        find_element(By.XPATH, "//a[@class='btn inline-flex popup-btn-ajax']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='mfp-bg mfp-ready']").\
        find_element(By.XPATH, "//a[text()='Download']").click()
    download_url = driver.current_url

    driver.find_element(By.CLASS_NAME, "replaced-login-link").click()
    nexus_login(driver)

    driver.get(download_url)
    get_zip_name(driver)
    driver.find_element(value='slowDownloadButton').click()
    time.sleep(10)

    driver.quit()

def move_to_game(game):
    pass

def clean_up():
    try:
        shutil.rmtree(DOWNLOAD_PATH)
    except OSError as e:
        print("Error deleting folder: {path}".format(path=DOWNLOAD_PATH))

if __name__ == '__main__':

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    game = 'valheim'

    nexus_manual_download(game=game, mod_id='1401')

    clean_up()



