import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
from itertools import repeat
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import re
import urllib.parse

urls = {
    '발라드': 'https://www.melon.com/chart/day/index.htm?classCd=GN0100',
    '댄스': 'https://www.melon.com/chart/day/index.htm?classCd=GN0200',
    '랩／힙합': 'https://www.melon.com/chart/day/index.htm?classCd=GN0300',
    'R&B／Soul': 'https://www.melon.com/chart/day/index.htm?classCd=GN0400',
    '인디음악': 'https://www.melon.com/chart/day/index.htm?classCd=GN0500',
    '록／메탈': 'https://www.melon.com/chart/day/index.htm?classCd=GN0600',
    '트로트': 'https://www.melon.com/chart/day/index.htm?classCd=GN0700',
    '포크／블루스': 'https://www.melon.com/chart/day/index.htm?classCd=GN0800'
}

driver = webdriver.Chrome(ChromeDriverManager().install())


def get_chart_data(url, genre):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    chart_data = []

    for tr in soup.select('#lst50, #lst100'):
        rank = tr.select_one('.rank').text.strip()
        artist = tr.select_one('.ellipsis.rank02 a').text.strip()
        title = tr.select_one('.ellipsis.rank01').text.strip()
        album = tr.select_one('.ellipsis.rank03').text.strip()
        album_img = tr.select_one('img[src*="/album/images/"]')
        album_img_temp = album_img['src']
        album_img_url = album_img_temp.replace('e/120/q', 'e/282/q')
        keyword = '{} {}'.format(artist, title)
        encoded_keyword = urllib.parse.quote(keyword)
        url2 = (
            f'https://www.youtube.com/results?search_query={encoded_keyword}')
        driver.get(url2)
        time.sleep(8)

        # 재생시간 확인용
        span_tag = driver.find_elements(
            By.CSS_SELECTOR, 'span#text.style-scope.ytd-thumbnail-overlay-time-status-renderer')

        # 재생시간 10분 넘으면 다음 영상으로 넘기기 위해 사용
        seq = 1
        if len(span_tag[0].get_attribute('innerText')) >= 5:
            for tag in span_tag:
                value = tag.get_attribute('innerText')
                # 10:00이 되면 길이가 5이므로 seq 1 증가시켜 다음 영상으로
                if (len(value) >= 5):
                    seq += 1
                else:
                    break

        page_source = driver.page_source
        pattern = re.compile(r'\/watch\?v=[-\w]+')  # 정규식 신기함
        links = pattern.findall(page_source)
        # watch 뒤에 오는 주소가 asd와 asd\qwe 이런 경우가 있는데 정규식을 사용하면 둘 다 asd만 걸러지기에
        # 중복 값이 생기므로 set()함수 사용
        links = list(set(links))
        # print(links)
        youtube_link = 'https://www.youtube.com' + links[seq]
        # print(youtube_link)
        chart_data.append([genre, rank, artist, title,
                           album, album_img_url, youtube_link])

    return chart_data


def save_csv(chart_data):
    with open('./team-1-project/data/popular_songs.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['장르', '순위', '아티스트', '곡명', '앨범', '앨범이미지', '유튜브링크'])
        writer.writerows(chart_data)


def main():
    chart_data_all = []
    for genre, url in urls.items():
        chart_data = get_chart_data(url, genre)
        chart_data_all += chart_data
    save_csv(chart_data_all)


if __name__ == '__main__':
    main()
