import json

from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from icecream import ic
from pathlib import Path
from shutil import move
from datetime import datetime

def download_screener(url):
    driver = webdriver.Chrome()
    driver.implicitly_wait(6)
    driver.get(url)
    sleep(6)
    dom = driver.find_element(by=By.CSS_SELECTOR, value="a.btn-primary")
    ic(dom)
    sleep(6)
    dom.click()
    sleep(4)
    driver.quit()

def get_latest_download():
    download_folder = Path.home() / 'Downloads'
    # Get all csv files
    files = download_folder.glob('*csv')
    return max([file for file in files], 
               key=lambda item: item.stat().st_ctime)

def get_data(config_file):
    with open(config_file) as fd:
        data = json.load(fd)
    return data

if __name__ == "__main__":
    # Map screener url with screener type and its destination folder
    config_file = "data_config.json"
    data = get_data(config_file) 
    ic(data)
    # screener_url = "https://chartink.com/screener/high-volume-on-sma-20-crossover"
    for screener in data:
        # screener_url = "https://chartink.com/screener/stocks-trending-above-10-ema-for-a-month"
        # destination_folder = f"sample_screener_name/{datetime.today().strftime('%Y.%m.%d')}.csv"
        screener_url = data[screener]['url']
        destination_folder = data[screener]['folder']
        Path(destination_folder).mkdir(parents=True,
                                       exist_ok=True)
        destination_file = f"{destination_folder}/{datetime.today().strftime('%Y.%m.%d')}.csv"
        download_screener(screener_url)
        latest_file = get_latest_download()
        ic(latest_file)
        fetched_file = move(latest_file,destination_file)
        ic(fetched_file)
