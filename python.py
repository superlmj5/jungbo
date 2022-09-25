# 크롤링시 필요한 라이브러리 불러오기
import sys #시스템 
import subprocess #파이썬에서 새 프로세스 생성 -> 활용 모듈
import time #기다리기 모듈

#셀레니움 모듈 확인 및 불러오기
try:
    # 없는 모듈 import시 에러 발생
    from selenium import webdriver
    from selenium.webdriver.common.by import By
except:
    # pip 모듈 업그레이드
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip']) #서브 프로세스 명령 실행 후 리턴 값이 0(정상 종료)가 아닐 시 에러 발생 
    # 에러 발생한 모듈 설치
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'selenium']) #sys.executable 파이썬 실행 파일 경로 => 파이썬 실행 파일에 뒤에 있는 문구 실행
    # 다시 import
    from selenium import webdriver
    from selenium.webdriver.common.by import By

# 웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument('headless')
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome('Chrome_Driver\chromedriver.exe',options=options)
driver.implicitly_wait(3)

# 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
# 입력된 수를 1, 11, 21, 31 ...만들어 주는 함수
def makePgNum(num):
    if num == 1 or num == 0:
        return 1
    else:
        return 10 * num - 9

# 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)
def makeUrl(search, start_pg, end_pg):
    urls = []
    for i in range(start_pg, end_pg + 1):
        page = makePgNum(i)
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page)
        urls.append(url)
    # print("생성url: ", urls)
    return urls

################### 뉴스크롤링 시작 ###################

# 검색어 입력
search = input("검색할 키워드를 입력해주세요:")

# 검색 시작할 페이지 입력
page = int(input("\n크롤링할 시작 페이지를 입력해주세요. ex)1(숫자만입력):"))  # ex)1 =1페이지,2=2페이지...
print("\n크롤링할 시작 페이지: ", page, "페이지")
# 검색 종료할 페이지 입력
page2 = int(input("\n크롤링할 종료 페이지를 입력해주세요. ex)1(숫자만입력):"))  # ex)1 =1페이지,2=2페이지...
print("\n크롤링할 종료 페이지: ", page2, "페이지")

# naver url 생성
search_urls = makeUrl(search, page, page2)

#검색결과 없음 처리
driver.get(search_urls[0])

try:
    driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[2]/div[1]/p')
    no_result = True
except Exception as e:
    no_result = False

if no_result == True:
    exit()

# 뉴스 url 수집
news_urls = []
for i in search_urls:

    driver.get(i)

    news_elements = driver.find_elements(By.XPATH, '//div/div/div[1]/div[2]/a[2]')

    for j in news_elements:
        url = j.get_attribute("href")
        if url not in news_urls:
            news_urls.append(j.get_attribute("href"))
    
# print(news_urls)
# print(len(news_urls))

#파일 생성
try:
    with open("{0}.txt".format(search),'x', encoding="UTF-8") as file:
        print("{0}.txt 파일 생성됨".format(search))

        order = 1
        count = len(news_urls)

        file.write("키워드 : {0} \n".format(search))
        file.write("Url 개수 : {0} \n".format(count))
        for i in news_urls:
            order += 1
            line = str(order) +'. ' + i + '\n'
            file.write(line)
except Exception as e:
    print("중복되는 파일이 존재합니다. 파일을 제거하고 다시 해주세요.")
