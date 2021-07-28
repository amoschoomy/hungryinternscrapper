from typing import List
from selenium.webdriver.chrome.webdriver import WebDriver,Options
from selenium.common.exceptions import NoSuchElementException
import re
import csv

class Candidate:
    def __init__(self,name:str="",gender:str="",age:int=999,address:str="",sector:str="",phone:str="0123456789",salary:str="") -> None:
        self.name=name
        self.sector=sector
        self.gender=gender
        self.address=address
        self.age=age
        self.salary=salary
        self.phone=phone

    def __str__(self) -> str:
        return self.name+"\n"+self.sector+"\n"+self.gender+"\n"+self.address+"\n"+str(self.age)+"\n"+self.phone+"\n"+self.salary

def hungry_intern_scrapper():

    pagenumber=1
    options_web = Options()
    options_web.add_argument("headless")
    driver=WebDriver("./chromedriver",options=options_web)
    xpath='//li[@class="jobsearch-column-12"]//h2[@class="jobsearch-pst-title"]//a'
    candidates_url=[]


    while True:
        url="https://hungryintern.com/candidate-listing/?ajax_filter=true&posted=all&candidate_page="+str(pagenumber)
        driver.get(url)
        candidate_list=driver.find_elements_by_xpath(xpath)
        if not candidate_list:
            driver.quit()
            break
        for c in candidate_list:
            candidates_url.append(c.get_attribute("href"))
        pagenumber+=1
    
    return candidates_url

def parse_candidate_data(candidates_url:List[str]):
    candidates=[]
    options_web = Options()
    options_web.add_argument("headless")
    driver=WebDriver("./chromedriver",options=options_web)
    name_xpath="/html/body/div[2]/div[4]/div/div/div/aside/div[1]/div/h2/a"
    sector_xpath="/html/body/div[2]/div[4]/div/div/div/aside/div[1]/div/p[2]"
    salary_xpath="/html/body/div[2]/div[4]/div/div/div/aside/div[1]/div/p[3]"
    age_xpath="/html/body/div[2]/div[4]/div/div/div/aside/div[1]/div/p[4]"
    gender_xpath="/html/body/div[2]/div[4]/div/div/div/div/div/div/div[2]/ul/li[4]/div/small"
    address_xpath="/html/body/div[2]/div[4]/div/div/div/aside/div[1]/div/span[1]"
    phone_xpath="/html/body/div[2]/div[4]/div/div/div/aside/div[1]/div/div/a"

    for link in candidates_url:
        driver.get(link)
        try:
            name=driver.find_element_by_xpath(name_xpath).text
        except(NoSuchElementException):
            name="N/A"

        try:
            sector=driver.find_element_by_xpath(sector_xpath).text
        except(NoSuchElementException):
            sector="N/A"

        try:
            salary=driver.find_element_by_xpath(salary_xpath).text
        except(NoSuchElementException):
            salary="N/A"

        try:
            
            age=int(parse_age((driver.find_element_by_xpath(age_xpath).text)))
        except(NoSuchElementException):
            age=999

        try:
            gender=driver.find_element_by_xpath(gender_xpath).text
        except(NoSuchElementException):
            gender="N/A"
        
        try:
            address=driver.find_element_by_xpath(address_xpath).text
        except (NoSuchElementException):
            address="N/A"
        
        try:
            phone_url=driver.find_element_by_xpath(phone_xpath).get_attribute("href")
            phone=parse_number(phone_url)
        except NoSuchElementException:
            phone="999999999"
        candidates.append(Candidate(name,gender,age,address,sector,phone,salary))
    return candidates


def parse_number(url:str)->str:
    number=re.findall("[0-9]+",url)
    if number and len(number[0])>7:
        return number[0]
    else:
        return "0123456789"

def parse_age(json:str)->str:
    number=re.findall("[0-9]+",json)
    if number:
        return number[0]
    else:
        return "999"

def write_to_csv(candidate_infos:List[Candidate]):
    with open('candidates.csv', 'w',) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name","Age","Gender","Address","Phone","Sector","Salary"])
        for candidate in candidate_infos:
            writer.writerow([candidate.name,candidate.age,candidate.gender,candidate.address,candidate.phone,candidate.sector,candidate.salary])

def main():
    candidates=hungry_intern_scrapper()
    candidates_list=parse_candidate_data(candidates)
    write_to_csv(candidates_list)

main()