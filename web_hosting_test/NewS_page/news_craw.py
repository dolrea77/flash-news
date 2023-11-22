from urllib.request import urlopen
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from .models import Crawring, Crawring_ct
import time
def iframe_src(detail_url):
    extracted_url = ''
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # headless 모드 활성화
    chrome_options.add_argument('--disable-gpu')  # GPU 가속 비활성화
    chrome_options.add_argument("--user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    # 웹페이지 열기
    driver.get(detail_url)
    # 명시적 대기: 최대 50초 동안 player_iframe 클래스가 있는 iframe을 찾을 때까지 기다림
    iframe_present = EC.presence_of_element_located((By.CLASS_NAME, 'player_iframe'))
    WebDriverWait(driver, 15).until(iframe_present)
    # iframe 찾기
    iframes = driver.find_elements(By.CLASS_NAME, 'player_iframe')
    # 첫 번째 iframe 선택
    if len(iframes) > 0:
        iframe = iframes[0]
        # iframe으로 전환
        driver.switch_to.frame(iframe)
        # 페이지 로드 완료를 기다리는 조건
        page_load_condition = EC.presence_of_element_located((By.XPATH, '//body'))
        # WebDriverWait를 사용하여 페이지 로드 완료를 기다리기
        WebDriverWait(driver, 30).until(page_load_condition)
        try:
            # Xpath를 사용하여 style 속성이 있는지 확인하는 조건
            iframe_image_condition = EC.presence_of_element_located((By.XPATH, '//div[@id="coverImage" and @style]'))
            # WebDriverWait를 사용하여 조건이 충족될 때까지 기다리기
            WebDriverWait(driver, 30).until(iframe_image_condition)
        except:
            return 'https://t1.daumcdn.net/cfile/tistory/124DC8434F6717EB0C'
        # iframe 내에서 HTML 가져오기
        iframe_html = driver.page_source
        # BeautifulSoup으로 HTML 파싱
        iframe_soup = BeautifulSoup(iframe_html, 'html.parser')
        # 원하는 div 태그 찾기
        div_tag = iframe_soup.find('div', {'id': 'coverImage'})
        # div 태그에서 정보 추출
        if div_tag:
            div_style = div_tag.get('style')
            match = re.search(r'url\("(.+)"\);', div_style)
            if match:
                extracted_url = match.group(1)
            else:
                print('URL을 찾을 수 없습니다.')
        else:
            print('Div 태그를 찾을 수 없습니다.')
    else:
        print('player_iframe 클래스를 가진 iframe을 찾을 수 없습니다.')
    # 웹드라이버 종료
    driver.quit()
    return extracted_url
def newscrawring():
    home_news = {'title': [], 'content': [], 'img': [], 'src': []}
    url = 'https://news.daum.net/'
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    news_list = soup.select('div.box_news_issue li')
    home = []
    for news in news_list:
        home.append(news.select_one('a').get('href', None))
    print('home: ',len(home))
    # 모델에서 가져온 값
    model_values = Crawring.objects.values_list('src', flat=True)
    # 리스트 a에서 모델에 있는 값을 제외
    home = [item for item in home if item not in model_values]
    if len(home) == 0:
        return print('pass')
    for url_de in home:
        page = urlopen(url_de)
        soup2 = BeautifulSoup(page, "lxml")
        # 기사 링크
        home_news['src'].append(url_de)
        # 제목 크롤링
        home_news['title'].append(soup2.select('div.head_view h3')[0].string)
        # # 본문 내용 크롤링
        # sep = soup2.div.article.section.find_all()
        # 기사 본문
        main_section = soup2.select('div.article_view>section')
        # main_section에 있는 div태크
        main_text_div = main_section[0].select('div')
        # main_section에 있는 p태크
        main_text_p = main_section[0].select('p')
        # text 내용 추출
        main_div = []
        for mtd in main_text_div:
            main_div.append(mtd.text)
        main_p = []
        for mtp in main_text_p:
            main_p.append(mtp.text)
        # 리스트 내에 여러 요소로 되어있는 내용을 한요소로 변경
        maind = ''.join(main_div)
        mainp = ''.join(main_p)
        # div와 p태그 내용 합치기
        main_text = maind + mainp
        # 이스케이프문자('\n'), 와 두번 띄어쓰기를 제거
        main_text = main_text.replace('\n', '').replace('  ', '')
        home_news['content'].append(main_text)
        # 만약 main_section에 iframe이 있을 때
        if main_section[0].find('figure'):
            home_news['img'].append(main_section[0].select_one('img').get("src", '#'))
        # 만약 main_section에 iframe이 있을 때
        elif main_section[0].select('iframe.player_iframe'):
            home_news['img'].append(iframe_src(url_de))
        # 이미지없고 영상도 없을 시 대체 이미지 넣는 곳
        else:
            home_news['img'].append('https://t1.daumcdn.net/cfile/tistory/124DC8434F6717EB0C')
    print('크롤링된 수: ', len(home_news['title']))
    return home_news
def category_crawring(category: str) -> dict:
    home_news = {'title': [], 'content': [], 'img': [], 'src': [], 'category': []}
    for page in range(1,3):
        url = f'https://news.daum.net/breakingnews/{category}?page={page}'
        page = urlopen(url)
        time.sleep(0.5)
        soup = BeautifulSoup(page, "lxml")
        news_list = soup.select('div.box_etc li')
        home = []
        for news in news_list:
            home.append(news.select_one('a').get('href', None))
        # 모델에서 가져온 값
        model_values = Crawring_ct.objects.filter(category=category).values_list('src_ct', flat=True)
        # 리스트 a에서 모델에 있는 값을 제외
        home = [item for item in home if item not in model_values]
        if len(home) == 0:
            return print('pass')
        for url_de in home:
            time.sleep(0.5)
            page = urlopen(url_de)
            soup2 = BeautifulSoup(page, "lxml")
            # 기사 링크
            home_news['src'].append(url_de)
            # 기사 카테고리
            home_news['category'].append(category)
            # 기사 제목
            home_news['title'].append(soup2.select_one('h3.tit_view').string)
            # 기사 본문
            main_section = soup2.select('div.article_view>section')
            # main_section에 있는 div태크
            main_text_div = main_section[0].select('div')
            # main_section에 있는 p태크
            main_text_p = main_section[0].select('p')
            # text 내용 추출
            main_div = []
            for mtd in main_text_div:
                main_div.append(mtd.text)
            main_p = []
            for mtp in main_text_p:
                main_p.append(mtp.text)
            # 리스트 내에 여러 요소로 되어있는 내용을 한요소로 변경
            maind = ''.join(main_div)
            mainp = ''.join(main_p)
            # div와 p태그 내용 합치기
            main_text = maind + mainp
            # 이스케이프문자('\n'), 와 두번 띄어쓰기를 제거
            main_text = main_text.replace('\n', '').replace('  ', '')
            home_news['content'].append(main_text)
            # 만약 main_section에 iframe이 있을 때
            if main_section[0].find('figure'):
                home_news['img'].append(main_section[0].select_one('img').get("src", '#'))
            # 만약 main_section에 iframe이 있을 때
            elif main_section[0].select('iframe.player_iframe'):
                home_news['img'].append(iframe_src(url_de))
            # 이미지없고 영상도 없을 시 대체 이미지 넣는 곳
            else:
                home_news['img'].append('https://t1.daumcdn.net/cfile/tistory/124DC8434F6717EB0C')
    print('크롤링된 수: ', len(home_news['title']))
    return home_news