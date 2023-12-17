"""
Webページから画像をスクレイピングするスクリプト。

このスクリプトは、指定されたWebページから画像をスクレイピングし、ローカルに保存します。
設定ファイル（config.json）からスクレイピングするURLとそのページごとの画像数を読み込み、
別のファイル（save_folder.txt）から画像を保存するディレクトリのパスを取得します。

スクレイピングはSeleniumとBeautifulSoupを使用して行われ、画像は指定されたフォルダに保存されます。
"""

# coding: utf-8

import time
import requests
import bs4
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def load_config(config_path):
    """
    設定ファイルからスクレイピングの設定を読み込む。
    Args:
    config_path (str): 設定ファイルのパス。
    Returns:
    dict: 設定情報が含まれた辞書。
    """
    with open(config_path, 'r') as file:
        return json.load(file)


def load_save_folder(path):
    """
    保存先フォルダのパスを読み込む。
    Args:
    path (str): 保存先フォルダのパスが記載されたファイルのパス。
    Returns:
    str: 保存先フォルダのパス。
    """
    with open(path, 'r') as file:
        return file.read().strip()


def go_to_next_page(driver):
    """
    次のページに遷移するための処理を行う。
    Args:
    driver (webdriver): WebDriverのインスタンス。
    """
    next_element = driver.find_element(
        "id", "next")  # 仮に次へのリンクがID 'next'の要素だと仮定
    next_element.click()
    time.sleep(1)  # ページ遷移のロード時間を待機
    return driver.current_url


def scrape_images(driver, url, count, save_folder, progress_file):
    """
    指定されたURLから画像をスクレイピングし、ローカルに保存する。
    各URLに対して、指定された回数だけページを遷移しながら画像を収集し、保存する。
    各ステップの進行状況を記録する。
    Args:
    driver (webdriver): WebDriverのインスタンス。
    url (str): スクレイピング対象のURL。
    count (int): スクレイピングするページ数。
    save_folder (str): 画像を保存するフォルダのパス。
    progress_file (str): 進行状況を保存するファイルのパス。
    """
    for num in range(count):
        time.sleep(1)
        driver.get(url)
        try:
            soup = bs4.BeautifulSoup(driver.page_source, features='lxml')
            images = [img.get("src") for img in soup.find_all(
                'img', id="img") if not img.get("src").endswith('.gif')]
            for target in images:
                re = requests.get(target)
                with open(f'{save_folder}{num}_{target.split("/")[-1]}', 'wb') as file:
                    file.write(re.content)

            url = go_to_next_page(driver)  # 次のページへの遷移

            # 進行状況を記録
            progress = {'url': url, 'count': num + 1}
            with open(progress_file, 'w') as file:
                json.dump(progress, file)
        except Exception as e:
            print(f"An error occurred: {e}")
            break


def setup_driver():
    """
    WebDriverのインスタンスを設定して返す。
    Returns:
    webdriver: WebDriverのインスタンス。
    """
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    return driver


def main():
    """
    メイン関数。設定を読み込み、画像のスクレイピングを行う。
    """
    config = load_config('config.json')
    save_folder = load_save_folder('save_folder.txt')
    progress_file = 'progress.json'
    driver = setup_driver()

    try:
        for url, count in config['pages'].items():
            scrape_images(driver, url, count, save_folder, progress_file)
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()
