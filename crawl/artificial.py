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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import urllib.parse
import re
# 10대 남
woojin_artists = ["한로로", "김뜻돌", "박소은", "박소은", "박소은",
                  "모트", "모트", "쿠인",
                  "윤지영", "위수", "다섯", "수연이", "ADORA",
                  "신지훈", "신지훈", "이예린", "이고도",
                  "크르르", "clo", "clo", "n@di (나디)", "신인류", "이강승",
                  "onthedal", "김현창", "김현창", "민수", "민수", "백아", "dossi (도시)",
                  "Mingginyu (밍기뉴)", "찬주", "SURL (설)", "예빛", "나상현씨밴드",
                  "2단지", "안예은", "보배", "소낙별", "김마리"]

woojin_titles = ["비틀비틀 짝짜꿍", "삐뽀삐뽀", "말리부오렌지", "우리는 같은 음악을 듣고", "아무래도 난 더러운 사랑만 하나봐",
                 "논알콜", "대화", "진혼곡",
                 "토모토모", "교토", "점심시간", "love u too much !", "Trouble? TRAVEL!",
                 "시가 될 이야기", "별이 안은 바다", "love song", "Mouse",
                 "무슨 관계", "젊음", "적당히", "편지", "꽃말", "우리가 맞다는 대답을 할 거예요",
                 "Homework", "살아내기", "목마른 파랑", "민수는 혼란스럽다", "Perfect Time", "영화", "starstarstar",
                 "Meaningless", "춤", "Dry Flower", "신기루", "SITCOM",
                 "춘몽", "Proust (프루스트)", "에취! (AhChoo!)", "흑백나라의 엘리스", "나의 바다"]
# print('10대 남 :', len(woojin_artists), len(woojin_titles))
# 10대 녀
gpt10f_artists = ["방탄소년단", "STAYC", "Brave Girls", "aespa", "BLACKPINK", "NCT 127",
               "아이유", "OH MY GIRL", "ITZY", "TWICE", "방탄소년단", "BLACKPINK",
               "NCT DREAM", "IU", "SEVENTEEN", "TWICE", "MAMAMOO", "Red Velvet", "청하",
               "이하이", "ASTRO", "DAY6", "MAMAMOO", "ITZY", "TOMORROW X TOGETHER",
               "Red Velvet", "(여자)아이들", "AKMU",
               "전소미", "브레이브걸스", "로제", "Justin Bieber",
               "현아", "IZ*ONE", "방탄소년단", "아이유", "제니",
               "로제", "Etham", "태연"]

gpt10f_titles = ["Butter", "ASAP", "치맛바람", "Next Level", "How You Like That", "Sticker",
              "Celebrity", "Dolphin", "Mafia In The Morning", "Alcohol-Free", "Dynamite", "Lovesick Girls",
              "Hot Sauce", "Lilac", "Ready to love", "What is Love?", "HIP", "Psycho", "Bicycle",
              "Brave Enough", "ONE", "You were beautiful", "AYA", "달라달라", "0X1=LOVESONG (I Know I Love You) feat. Seori",
              "Queendom", "화", "어떻게 이별까지 사랑하겠어, 널 사랑하는 거지",
              "Dumb Dumb", "Rollin'", "On The Ground", "Peaches (feat. Daniel Caesar & Giveon)",
              "I'm Not Cool", "Panorama", "Permission to Dance", "Lilac", "SOLO",
              "Gone", "12:45 (Stripped)", "사계"]
# print('10대 녀 :', len(gpt_artists), len(gpt_titles))
# 20대 남
seunggyu_artists = ["Ed Sheeran", "Drake", "Post Malone", "The Weeknd", "Justin Bieber",
                    "Khalid", "Imagine Dragons", "Shawn Mendes",
                    "Bruno Mars", "Harry Styles", "The Chainsmokers ft. Halsey", "Charlie Puth", "Sam Smith",
                    "Wiz Khalifa ft. Charlie Puth", "Justin Timberlake", "Jason Derulo", "Maroon 5 ft. Cardi B",
                    "Camila Cabello ft. Young Thug", "Mark Ronson ft. Bruno Mars", "Lil Nas X ft. Billy Ray Cyrus",
                    "Coldplay x 방탄소년단", "Jawsh 685, Jason Derulo, BTS", "BLACKPINK", "ASH ISLAND", "전미도",
                    "로제", "BLACKPINK", "화사", "TWICE", "이무진",
                    "PURPLE KISS", "조정석", "전소미", "SG 워너비", "DK(디셈버)", "MC THE MAX", "프로미스나인", "브레이브걸스",
                    "TWICE", "태연"]

seunggyu_titles = ["Shape of You", "God's Plan", "Congratulations", "Blinding Lights", "Love Yourself",
                   "Young Dumb & Broke", "Believer", "There's Nothing Holdin' Me Back",
                   "That's What I Like", "Sign of the Times", "Closer", "Attention", "Stay With Me",
                   "See You Again", "Mirrors", "Want to Want Me", "Girls Like You",
                   "Havana", "Uptown Funk", "Old Town Road (Remix)",
                   "My Universe", "Savage Love (Laxed - Siren Beat)", "Kill This Love", "멜로디", "좋은 이별이 있을 리가 없잖아",
                   "On The Ground", "Lovesick Girls", "마리아", "The Feels", "신호등",
                   "Ponzona", "좋아좋아", "DUMB DUMB", "넌 좋은 사람", "심(心)", "어디에도", "Can't Hold Us", "We Ride",
                   "Alcohol-Free", "Weekend"]
# print('20대 남 :', len(seunggyu_artists), len(seunggyu_titles))
# 20대 녀
seulgi_artists = ["Adele", "Taylor Swift", "Billie Eilish", "Lady Gaga", "Beyoncé", "Ariana Grande",
                  "Rihanna", "Katy Perry", "Lorde", "Camila Cabello ft. Young Thug", "Demi Lovato",
                  "Dua Lipa", "Sia", "Selena Gomez", "Halsey", "Meghan Trainor",
                  "Cardi B", "Shakira ft. Rihanna", "Christina Aguilera", ",J-Lo ft. Ja Rule",
                  "KCM", "김민석", "MC THE MAX", "izi", "정동하", "이무진", "임영웅",
                  "주호", "마크툽(MAKTUB),구윤회", "에이치코드", "성시경", "KCM", "황인욱", "#안녕",
                  "에일리", "스탠딩에그", "윤하", "탑현", "송이한", "KCM",
                  "빅마마", "10cm", "정승환", "자우림", "멜로망스", "이승기", "KCM", "버즈", "조정석",
                  "마크툽(MAKTUB)", "김필", "폴킴", "소찬휘",
                  "야다", "닐로", "허각", "조유진,박기영", "정준일", "허각", "윤종신"]

seulgi_titles = ["Hello", "Shake It Off", "Bad Guy", "Bad Romance", "Crazy in Love", "7 Rings",
                 "Diamonds", "Roar", "Royals", "Havana", "Sorry Not Sorry",
                 "New Rules", "Cheap Thrills", "Lose You to Love Me", "Without Me", "All About That Bass",
                 "Bodak Yellow", "Can't Remember to Forget You", "Genie in a Bottle", "I'm Real (Remix)",
                 "천국의 계단", "취중고백", "어디에도", "응급실", "추억은 만남보다 이별에 남아", "신호등", "사랑은 늘 도망가",
                 "내가 아니라도", "Marry Me", "꿈속에 너 (Feat. 전상근)", "너의 모든 순간", "클래식", "포장마차", "너의번호를누르고",
                 "첫눈처럼 너에게 가겠다", "오래된노래", "사건의 지평선", "호랑수월가", "밝게 빛나는 별이 되어 비춰줄게", "태양의 눈물",
                 "체념", "스토커", "너였다면", "스물다섯,스물하나", "사랑인가봐", "삭제", "흑백사진", "가시", "아로하",
                 "찰나가 영원이 될 때", "다시 사랑한다면", "모든날, 모든순간", "Tears",
                 "이미슬픈사랑", "지나오다", "Hello", "나에게로의 초대", "안아줘", "나를 사랑했던 사람아", "좋니"]
# print('20대 녀 :', len(seulgi_artists), len(seulgi_titles))
# 30대 남
me30m_artists = ["미(MIIII)", "한희정", "HYNN", "Acoustic Collabo", "Acoustic Collabo", "Kassy", "윤미래",
              "김보경", "Big mama", "임재범", "박화요비", "박화요비", "박화요비", "ZIA", "ZIA", "Brown eyes",
              "browneyed SOUL", "나얼", "바닷길", "박혜경", "박화요비", "양파", "양파", "양파", "영준",
              "윤하", "윤하", "FREE STYLE", "BROWN EYED GIRLS", "가비엔제이", "가비엔제이", "가비엔제이",
              "에이치7", "혜령", "투샤이", "프리스타일", "러브홀릭", "러브홀릭", "에일리", "박혜경"]

me30m_titles = ["어디에 (Orchestra Ver.)", "잔혹한 여행", "시든 꽃에 물을 주듯", "설렘가득", "그대와 나, 설레임", "굿모닝 (Good Morning)", "검은 행복",
             "그댄가봐요", "연(捐)", "그대는 어디에", "어떤가요", "Lie", "그런 일은", "물론", "웃어줄래", "With Coffee",
             "LOVE BALLAD", "그대 떠난 뒤", "나만 부를 수 있는 노래", "빨간 운동화", "Promise", "령혼", "marry me", "L.O.V.E", "니 생각뿐 (feat. 개리)",
             "It's Beautiful", "My Song and...", "마음으로 하는 말 (Feat. Hanyi)", "Second", "Happiness", "Lie", "해바라기",
             "Love All", "바보", "Love Letter", "Y", "My Dear..", "다시 피운 꽃", "첫눈처럼 너에게 가겠다", "안녕"]
# print('30대 남 :', len(me_artists), len(me_titles))
# 30대 녀
choi_artists = ["Marshmello & Demi Lovato", "Whethan", "Alesso", "제이유나", "Loote", "Syn Cole",
                "Kygo", "비오", "BIG Naughty", "Florence + the Machine", "오마이걸", "Kygo & Oh Wonder", "Zedd & Jasmine Thompson", "치즈", "데이식스", "Jasmine Thompson & Zedd",
                "Zedd & Griff", "BIG Naughty", "Kygo & Oliver Nelson", "방탄소년단", "Cash Cash", "루시", "Sasha Sloan",
                "샵", "러브홀릭", "러브홀릭", "팀", "더 자두", "더 자두", "박혜경",
                "Emma Stone", "La La Land Cast", "에픽하이", "오반", "투모로우바이투게더",
                "릴러말즈", "언니네 이발관", "Kygo", "Kygo", "The Kid LAROi",
                "Anne-Marie", "Klingande", "Kris Kross", "박지윤", "브로콜리너마저", "시와",
                "델리스파이스", "국카스텐", "윤상", "장미여관"]

choi_titles = ["OK Not to Be", "Can't Hide (feat. Ashe)", "Sad Song (feat. TINI)", "Butterfly", "High Without Your Love (NAKID Remix)",
               "Sway (feat. Nevve)", "This Town (feat. Sasha Sloan)", "네가 없는 밤 (feat. ASH ISLAND)", "Vancouver", "You've Got the Love", "Nonstop", "How Would I Know",
               "Funny", "Madeleine Love", "Zombie", "Funny (Stripped)", "Inside Out", "Vancouver", "Riding Shotgun (feat. Bonnie McKee)", "Dynamite", "Love You Now (feat. Georgia Ku)", "개화", "Lie",
               "내 입술... 따뜻한 커피처럼", "Loveholic", "Want you hear", "사랑합니다", "대화가 필요해", "김밥", "내게 다시",
               "Someone In The Crowd", "Another Day Of Sun", "Fan", "어떻게 지내", "9와 4분의 3 승강장에서 너를 기다려",
               "불편해", "혼자 추는 춤", "Lose Somebody", "Beautiful", "STAY",
               "Ciao Adios", "Pumped Up", "Jump", "고백", "살얼음", "화양연화",
               "doxer", "LOST", "날 위로하려거든", "옥탑방"]
# print('30대 녀 :', len(choi_artists), len(choi_titles))

# 40대 남
me40m_artists = ["김현성", "정인호", "서문탁", "소냐", "h", "서문탁", "한희정", "간미연", "애즈원",
               "포지션", "최재훈", "양파", "BROWN EYED GIRLS", "JK 김동욱", "임현정",
               "얀", "J", "Big mama", "도원경", "Y2K", "Mariah Carey", "컬러핑크", "란", "페이지",
               "리즈", "유미", "유미", "이수영", "뱅크", "앤", "앤", "김형중",
               "이소은", "김동률", "애즈원", "정일영", "포지션", "야다",
               "이브", "izi", "서주경", "솔리드", "자자", "진주", "이지라이프"]

me40m_titles = ["행복", "해요", "사슬", "눈물이나", "잊었니", "웃어도 눈물이나", "내일", "하얀 겨울 (Duet. 노을 나성호)", "너만은 모르길",
              "마지막 약속", "비의 랩소디", "애송이의 사랑", "다가와서", "미련한 사랑", "사랑은 봄비처럼... 이별은 겨울비처럼",
              "심(心)", "어제처럼", "체념", "다시 사랑한다면", "헤어진 후에", "Angels Cry", "블루문", "어쩌다가", "이별이 오지 못하게",
              "그댄 행복에 살텐데", "별", "사랑은 언제나 목마르다", "라라라", "가질 수 없는 너", "혼자 하는 사랑", "아프고 아픈 이름", "그랬나봐",
              "키친", "욕심쟁이 (Feat. 이소은)", "원하고 원망하죠", "기도", "I Love You", "이미 슬픈 사랑",
              "너 그럴 때면", "응급실", "당돌한 여자", "천생연분", "버스 안에서", "난 괜찮아", "너 말고 니 언니"]
# print('40대 남 :', len(me2_artists), len(me2_titles))
# 40대 녀
seok_artists = ["영턱스클럽", "스페이스A", "스페이스A", "루머스", "인디고", "유피", "유피", "솔리드", "UN",
                "UN", "박혜경", "왁스", "페퍼톤스", "페퍼톤스", "10CM", "10CM", "BIG Naughty",
                "용준형", "새소년", "새소년", "새소년", "극동아시아타이거즈", "극동아시아타이거즈",
                "이소라", "이영지", "이영지", "자우림", "자우림", "자우림", "아이유",
                "방탄소년단", "태연", "볼빨간사춘기", "방탄소년단", "정은지", "황치열",
                "코나", "아이유", "성시경", "이무진"]

seok_titles = ["정", "섹시한 남자", "주홍글씨", "스톰", "여름아 부탁해", "뿌요뿌요", "바다", "천생연분", "선물",
               "선물", "고백", "화장을 고치고", "Thank You", "계절의 끝에서", "그라데이션", "봄이 좋냐??", "정이라고 하자",
               "소나기 (Feat. 10cm)", "긴 꿈", "난춘", "파도", "오늘은 비가 와도 좋을 것 같아", "별",
               "신청곡", "NOT SORRY", "낮 밤", "STAY WITH ME", "있지", "스물다섯, 스물하나", "Love poem",
               "Butterfly", "그대라는 시", "나만, 봄", "봄날", "너의 밤은 어때", "다시, 봄",
               "우리의 밤은 당신의 낮보다 아름답다", "밤편지", "다정하게, 안녕히", "신호등"]
# print('40대 녀 :', len(seok_artists), len(seok_titles))
# 50대 남
daesik_artists = ["김현식", "김완선", "이승철", "김민우", "조용필", 
                  "김건모", "김광석", "이적", "박완규", "김범수",
                  "이승환", "김현철", "김현철, 이소라", "김연우", "김광진", 
                  "유재하" "박상민", "박상민", "김종서", "김현식",
                  "신승훈", "김광석", "이승철", "김건모", "조관우", 
                  "임재범", "시나위", "시나위", "김민우", "유재하",
                  "유재하", "임영웅", "임영웅", "임영웅", "이은미", 
                  "산울림", "김건모", "윤도현", "신효범", "변진섭"]

daesik_titles = ["비처럼 음악처럼", "보낼 수 없는 사랑", "그런 사람 또 없습니다", "사랑일뿐야", "그대 발길 머무는 곳에",
                 "잘못된 만남", "서른 즈음에", "걱정말아요 그대", "하루애", "보고싶다",
                 "천일동안", "왜 그래", "그대안의 블루 (Duet With 이소라)", "여전히 아름다운지", "편지",
                 "그대 내 품에", "하나의 사랑", "눈물잔", "겨울비", "비처럼 음악처럼",
                 "미소 속에 비친 그대", "이등병의 편지", "희야", "핑계", "늪",
                 "비상", "크게 라디오를 켜고", "그대 앞에 난 촛불이여라", "친구에게", "사랑하기 때문에",
                 "가리워진 길", "사랑이 이런 건가요", "이제 나만 읻어요", "사랑은 늘 도망가", "애인 있어요",
                 "내 마음에 주단을 깔고", "잘못된 만남", "사랑했나봐", "난 널 사랑해", "그대 내게 다시"]

# 50대 녀
gpt50f_artists = ["소찬휘", "김연자", "김범룡", "임재현", "조용필", 
                "조정현", "이승환", "박정수", "신해철", "김광석",
                "신승훈", "김광석", "이문세", "김완선", "박정운", 
                "푸른하늘", "박상민", "신승훈", "김민종", "조용필",
                "전영록", "전영록", "오승근", "윤상", "이승철", 
                "박미경", "박미경", "박미경", "박상철", "이승철",
                "양수경", "양수경", "양수경", "송창식", "송창식", 
                "이승환", "이승환", "윤종신", "이소라", "이소라",
                "인순이", "인순이", "인순이", "조정현", "이은미"]

gpt50f_titles = ["현명한 선택", "나는 울었네", "사랑의 진실", "사랑에 연습이 있었다면", "청춘", 
               "그 아픔까지 사랑한거야", "너를 향한 마음", "그대 품에 잠들었으면", "슬픈 표정 하지 말아요", "먼지가 되어",
               "내일이 오면", "사랑했지만", "사랑은 늘 도망가", "삐에로는 우릴보고 웃지", "오늘 같은 밤이면", 
               "눈물나는 날에는", "해바라기", "미소속에 비친 그대", "착한 사랑", "이젠 그랬으면 좋겠네",
               "저녁놀", "사랑은 연필로 쓰세요", "내 나이가 어때서", "가려진 시간 사이로", "서쪽 하늘", 
               "이브의 경고", "기억속의 먼 그대에게", "이유같지 않은 이유", "무조건", "그런 사람 또 없습니다",
               "사랑은 창밖에 빗물 같아요", "이별의 끝은 어디인가요", "바라 볼 수 없는 그대", "우리는", "고래사냥", 
               "어떻게 사랑이 그래요", "천일동안", "좋니", "제발", "나를 사랑하지 않는 그대에게",
               "거위의 꿈", "밤이면 밤마다", "아버지", "그대에게 쓰는 편지", "애인있어요"]
# print('50대 여성 :', len(gpt2_artists), len(gpt2_titles))
      
      
      

 
# url = "https://vibe.naver.com/search?query="

# male10, female10, male20, female20, male30, female30, male40, female40, male50, female50 = [], [],[], [],[], [],[], [],[], []  

male_generation = {
    101 : zip(woojin_artists, woojin_titles),
    201 : zip(seunggyu_artists, seunggyu_titles),
    301 : zip(me30m_artists, me30m_titles),
    401 : zip(me40m_artists, me40m_titles),
    501 : zip(daesik_artists, daesik_titles)
}

female_generation = {
    102 : zip(gpt10f_artists, gpt10f_titles),
    202 : zip(seulgi_artists, seulgi_titles),
    302 : zip(choi_artists, choi_titles),
    402 : zip(seok_artists, seok_titles),
    502 : zip(gpt50f_artists, gpt50f_titles)

}

def gene_function(gene_dict):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    for gene, artsongs in gene_dict.items():
        chart_data = []
        for artist, title in artsongs:
            url = f'https://vibe.naver.com/search?query={artist} {title}'
            driver.get(url)
            time.sleep(1)
            
            # 팝업창 뜨면 끄기
            try:
                popup = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div.modal > div > div > a.btn_close')))
                popup.click()
            except:
                pass
        
            info = driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(3) > div > div > div > div.info_area > div.title > span.inner > a')
            info.click()
            time.sleep(1)
            
            # 텍스트가 '곡명\n비틀비틀 짝짜꿍' 이런식이어서 \n 이후의 텍스트만 가져오게함
            n = '\n'
            title_temp = driver.find_element(By.CSS_SELECTOR, '#content > div.summary_section > div > div.summary > div.text_area > h2 > span.title').text
            title = title_temp[title_temp.index(n)+len(n):]
            artist_temp = driver.find_element(By.CSS_SELECTOR, '#content > div.summary_section > div > div.summary > div.text_area > h2 > span.sub_title').text
            artist = artist_temp[artist_temp.index(n)+len(n):]
            album_name_temp = driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(4) > div > div.text_area > div > a').text
            album_name = album_name_temp[album_name_temp.index(n)+len(n):]
            album_img_temp = driver.find_element(By.CSS_SELECTOR, '#content > div.summary_section > div > div.summary_thumb > img').get_attribute('src')
            j = '.jpg'
            album_img = album_img_temp[:album_img_temp.index(j)+len(j)]
            
            keyword = '{} {}'.format(artist, title)
            encoded_keyword = urllib.parse.quote(keyword)
            url2 = (
                f'https://www.youtube.com/results?search_query={encoded_keyword}')
            driver.get(url2)
            time.sleep(1)
            page_source = driver.page_source
            pattern = re.compile(r'\/watch\?v=[-\w]+')  # 정규식 신기함
            links = pattern.findall(page_source)
            # watch 뒤에 오는 주소가 asd와 asd\qwe 이런 경우가 있는데 정규식을 사용하면 둘 다 asd만 걸러지기에
            # 중복 값이 생기므로 제거 필요
            # list(set())을 썼더니 자동으로 정렬이 되어 쓰지않고
            # 대신 데이터 프레임으로 변환 후 drop_duplicates().tolist() 사용
            df = pd.DataFrame(links, columns=['link'])
            links = df['link'].drop_duplicates().tolist()
            youtube_link = 'https://www.youtube.com' + links[0]
            
            # 심심해서 가사도 가져와봄
            try:
                lyrics = driver.find_element(By.CSS_SELECTOR, '#content > div.end_section.section_lyrics > div > p').text
            except:
                pass
            if (len(gene_dict) == 13):
                    gender = '남성'
            if (len(gene_dict) == 15):
                    gender = '여성'

                
            chart_data.append([gender, gene, artist, title, album_name, album_img, 
                    youtube_link, lyrics])
    return chart_data


def save_csv(chart_data):

    with open(f'./team-1-project/data/{gender}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['성별', '세대', '아티스트', '곡명', '앨범명', '앨범이미지', '유튜브링크'])
        writer.writerows(chart_data)

# def main():
#     chart_data_all = []
#     for genre, url in urls.items():
#         chart_data = get_chart_data(url, genre)
#         chart_data_all += chart_data
#     save_csv(chart_data_all)
#             with open('./team-1-project/data/popular_songs.csv', 'w', encoding='utf-8', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(['장르', '순위', '아티스트', '곡명', '앨범', '앨범이미지', '유튜브링크'])
#                 writer.writerows(chart_data)
            
print(gene_function(male_generation), gene_function(female_generation))



