
import re
import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


headers_generator = Headers(os="win", browser="chrome")

url_base="https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

response = requests.get(url_base, headers = headers_generator.generate())

soup = BeautifulSoup(response.text,features='lxml')

pages = soup.find("div", class_="bloko-gap bloko-gap_top")
pages_max = int(pages.text.split("...")[1].split("дальше")[0])



#vakansy_list1=soup.find_all(class_="serp-item")
#vakansy_list=soup.find("main",class_="vacancy-serp-content")

#vakansys = vakansy_list.find_all('div',class_='vacancy-serp-item-body__main-info',limit=None)

vak_des = [["attrs={'data-qa': 'vacancy-description'}"],["div", 'class_= g-user-content', "attrs={'data-qa': 'vacancy-description'}"],
                   ["div", "class_= 'vacancy-section'"], ["div", "class_= 'bloko-columns-row'"],
                   ["div", "class_= 'vacancy-branded-user-content'"], ["div", "class_= 'vacancy-description'"],
                   ["div", "class_= 'vacancy-description-print'"]]

criteria_vakansy =r"([Dd][j][a][n][g][o])|([Ff][l][a][s][k])"

result_vakansy = []

for page in range(pages_max):
    url = url_base + '&page=' + str(page)
    response = requests.get(url, headers=headers_generator.generate())
    soup1 = BeautifulSoup(response.text, features='lxml')
    vakansy_start = soup1.find("main", class_="vacancy-serp-content")
    vakansys_list1 = vakansy_start.find_all('div', class_='vacancy-serp-item__layout', limit=None)

    for vakansy in vakansys_list1:
        vakansy_tag=vakansy.find('a',class_='serp-item__title')
        vakansy_salary = vakansy.find("span",attrs={'data-qa': 'vacancy-serp__vacancy-compensation'},class_ = 'bloko-header-section-2')
        vakansy_company = vakansy.find("a", attrs={'data-qa': 'vacancy-serp__vacancy-employer'},class_='bloko-link bloko-link_kind-tertiary')
        vakansy_city = vakansy.find("div", attrs={'data-qa': 'vacancy-serp__vacancy-address'},class_ = "bloko-text")
        vakansy_url = vakansy_tag["href"]
        vakansy_response = requests.get(vakansy_url, headers=headers_generator.generate())
        vakansy_soup = BeautifulSoup(vakansy_response.text, features='lxml')
        vakansy_description = vakansy_soup.find(attrs={'data-qa': 'vacancy-description'})
        vak_count = 0

        while vakansy_description == None and vak_count < len(vak_des):
            vakansy_description = vakansy_soup.find(vak_des[vak_count])
            vak_count=vak_count+1

        if vakansy_salary == None:
            vakansy_salary_text ='None'
        else:
            vakansy_salary_text = vakansy_salary.text

        if vakansy_company == None:
            vakansy_company_text ='None'
        else:
            vakansy_company_text = vakansy_company.text

        if vakansy_city == None:
            vakansy_city_text ='None'
        else:
            vakansy_city_text = vakansy_city.text


        if re.findall(criteria_vakansy,vakansy_description.text):

            print(re.findall(criteria_vakansy,vakansy_description.text))

            result_vakansy.append(
                {
                    'link': vakansy_url,
                    'company': vakansy_company_text,
                    'city': vakansy_city_text,
                    'salary': vakansy_salary_text,
                    #'description': vakansy_description.text,
                }
            )

with open("result.json", "w", encoding="utf-8") as file:
    json.dump(result_vakansy, file, ensure_ascii=False, indent=2)


print('eeer')