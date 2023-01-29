import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

from program_crud import create_program
from program_schema import ProgramBase
from database import yield_db



main = "https://www.k-startup.go.kr/web/module/bizpbanc-ongoing_bizpbanc-inquiry-ajax.do?page={0}"
detail = "https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do?schM=view&pbancSn={0}&page={1}&schStr=regist&pbancEndYn=N"

columns = ["title", "url", "category", "organization", "subject",
           "apply_period", "apply_method", "content", "inquiries", "age"]

storage = []
counter = 0

for page in range(1, 5):
    pages = requests.post(
        main.format(page)
    )
    bs_1 = BeautifulSoup(pages.text, 'html.parser')

    articles = bs_1.find_all(attrs={'class': 'notice'})

    for article in articles:
        title = article.select('.tit')[0].string

        link = re.findall(r'\d+', article.a['href'])

        for url in link:
            detail_page = requests.get(detail.format(url, page)).text
            bs_2 = BeautifulSoup(detail_page, 'html.parser')
            inner = bs_2.select(".content_wrap .content")[0]

            category = inner.select(".information_box-wrap .dot_list-wrap .dot_list .txt")[0].string.strip()
            age = inner.select(".information_box-wrap .dot_list-wrap .dot_list .txt")[1].string.strip()
            organization = inner.select(".information_box-wrap .dot_list-wrap .dot_list .txt")[2].string.strip()

            region = inner.select(".information_box-wrap .dot_list-wrap")[1].select(" .dot_list .txt")[0].string.strip()
            apply_period = inner.select(".information_box-wrap .dot_list-wrap")[1].select(" .dot_list .txt")[
                1].string.strip()

            subject = inner.select(".information_box-wrap .dot_list-wrap")[2].select(" .dot_list .txt")[
                0].string.strip()

            try:
                content = inner.select(".information_box-wrap .box .box_inner .txt")[0].string.strip()
            except AttributeError:
                clean = re.compile("<.*?>")
                content = str(inner.select(".information_box-wrap .box .box_inner .txt")[0])
                content = re.sub(clean, '', content)

            inquiries = inner.select(".information_list-wrap .information_list")[4].select(".tit")[0].string

            try:
                apply_method = inner.select(".information_list-wrap .information_list")[0].select(
                    ".dot_list-wrap .txt-button .btn_by-bl")[0].string
            except IndexError:
                apply_method = "N/A"

            storage.append(
                [title, detail.format(url, page), category, organization, subject, apply_period, apply_method, content, inquiries, age]
            )

            counter += 1
            print(counter)
            time.sleep(0.5)

result = pd.DataFrame(
    storage, columns=columns
)

#
# Login
#

token = requests.post(
    url="http://ec2-43-201-42-19.ap-northeast-2.compute.amazonaws.com:8080/vcac/login",
    data={
        'username': 'testvc',
        'password': 'aa'
    }
).content


for idx, sample in result.iterrows():
    print(str(idx), ProgramBase.parse_obj(sample).dict())
    requests.post("http://ec2-43-201-42-19.ap-northeast-2.compute.amazonaws.com:8080/program/",
                  json=ProgramBase.parse_obj(sample).dict(),
                  headers={'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dmMiLCJleHAiOjE2NzUwNDE1OTJ9.-u66482-DaAhW8f-mMX40S2oR9MklMnvMY3NUf0nCLM"}
                  )



