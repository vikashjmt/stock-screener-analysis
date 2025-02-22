import json

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
# from icecream import ic
from pathlib import Path
from shutil import move
from datetime import datetime

options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def download_screener(url):
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(6)
    driver.get(url)
    sleep(6)
    dom = driver.find_element(by=By.CSS_SELECTOR, value="a.btn-primary")
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
    data_dir = Path(__file__).parent
    config_file = f"{data_dir}/data_config.json"
    # Download screeners csvs
    screener_csvs = list()
    screener_output_file = f"{data_dir}/downloaded_csvs.json"
    # Get old downloaded csv data
    old_screener_data = dict()
    if Path(screener_output_file).exists():
        with open(screener_output_file) as fd:
            old_screener_data = json.load(fd)
    screener_downloaded = dict()
    data = get_data(config_file)
    # ic(data)
    for screener in data:
        screener_url = data[screener]['url']
        print(f'Downloading screener {data[screener]}')
        destination_folder = f"{data_dir}/{data[screener]['folder']}"
        Path(destination_folder).mkdir(parents=True,
                                       exist_ok=True)
        destination_file = (f"{destination_folder}/"
                            f"{datetime.today().strftime('%Y.%m.%d')}.csv")
        if not old_screener_data.get(destination_file):
            download_screener(screener_url)
            latest_file = get_latest_download()
            fetched_file = move(latest_file, destination_file)
        else:
            fetched_file = destination_file
        screener_csvs.append(fetched_file)
        screener_downloaded['csvs'] = screener_csvs

    # Add the downloaded files to the csv
    with open(screener_output_file, 'w') as fd:
        json.dump(screener_downloaded, fd)

    # Get Downloaded csv files
    print('Details of downloaded screenrs can be found '
          f'in {screener_output_file}')
