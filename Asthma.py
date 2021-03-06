# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import time
import csv

NAME = "氣喘疾病"
YEAR_LIST = [
    "94Q1", "94Q2", "94Q3", "94Q4", "95Q1", "95Q2", "95Q3", "95Q4", "96Q1", "96Q2", "96Q3", "96Q4", "97Q1", "97Q2", "97Q3", "97Q4", "98Q1", "98Q2", "98Q3", "98Q4", "99Q1", "99Q2", "99Q3", "99Q4", "100Q1","100Q2", "100Q3", "100Q4", "101Q1", "101Q2", "101Q3", "101Q4", "102Q1", "102Q2", "102Q3", "102Q4", "103Q1", "103Q2", "103Q3", "103Q4", "104Q1", "104Q2", "104Q3", "104Q4", "105Q1", "105Q2", "105Q3", "105Q4", "106Q1", "106Q2", "106Q3"
]

YEAR_DICT = {
    "94Q1": "94年第一季","94Q2": "94年第二季","94Q3": "94年第三季","94Q4": "94年第四季","95Q1": "95年第一季","95Q2": "95年第二季","95Q3":"95年第三季","95Q4": "95年第四季","96Q1": "96年第一季","96Q2": "96年第二季","96Q3": "96年第三季","96Q4": "96年第四季","97Q1": "97年第一季","97Q2": "97年第二季","97Q3": "97年第三季","97Q4": "97年第四季","98Q1": "98年第一季","98Q2": "98年第二季","98Q3": "98年第三季","98Q4": "98年第四季","99Q1": "99年第一季","99Q2": "99年第二季","99Q3": "99年第三季","99Q4": "99年第四季","100Q1": "100年第一季","100Q2": "100年第二季","100Q3": "100年第三季","100Q4": "100年第四季","101Q1": "101年第一季","101Q2": "101年第二季","101Q3": "101年第三季","101Q4": "101年第四季","102Q1": "102年第一季","102Q2": "102年第二季","102Q3": "102年第三季","102Q4": "102年第四季","103Q1": "103年第一季","103Q2": "103年第二季","103Q3": "103年第三季","103Q4": "103年第四季","104Q1": "104年第一季","104Q2": "104年第二季","104Q3": "104年第三季","104Q4": "104年第四季","105Q1": "105年第一季","105Q2": "105年第二季","105Q3": "105年第三季","105Q4": "105年第四季","106Q1": "106年第一季","106Q2": "106年第二季","106Q3": "106年第三季"
}

ASTHMA_OPTION = [
    "821", "822", "825", "1739", "1740"
]

ASTHMA_DICT = {
    "821": "氣喘病人參加「全民健康保險氣喘醫療給付改善方案」之比率",
    "822": "氣喘病人出院後14日以內因同一疾病再入院比率",
    "825": "氣喘病人使用短效乙型作用劑或類固醇藥物吸入劑藥物控制比率",
    "1739": "參加「全民健康保險氣喘醫療給付改善方案」之病人因氣喘發作而住院之比率",
    "1740": "參加「全民健康保險氣喘醫療給付改善方案」之病人因氣喘發作而至急診就醫之比率"
}

def dict2CSV(data, year, option):
    keys = data[0].keys()
    with open('{}/{}_{}.csv'.format(NAME, YEAR_DICT[year], ASTHMA_DICT[option]), 'w', encoding="utf8") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def checkExist(year, option):
    import os.path
    if not os.path.isdir(NAME):
        os.makedirs(NAME)
    if os.path.isfile("{}/{}_{}.csv".format(NAME, YEAR_DICT[year], ASTHMA_DICT[option])):
        return True
    return False

def getTableData(year, option):
    if checkExist(year, option):
        return

    DATA = []
    driver = webdriver.Firefox()
    try:
        driver.get("http://www1.nhi.gov.tw/mqinfo/SearchPro.aspx?Type=Asthma&List=4")

        driver.find_element_by_id("ContentPlaceHolder1_DropDA").click()
        driver.find_element_by_xpath("//option[@value='{}']".format(option)).click()
        time.sleep(2)
        driver.find_element_by_id("ContentPlaceHolder1_drop1").click()
        driver.find_element_by_xpath("//option[@value='{}']".format(year)).click()
        driver.find_element_by_id("ContentPlaceHolder1_RowBox").send_keys("000")
        driver.find_element_by_id("ContentPlaceHolder1_But_Query").click()
        time.sleep(60)

        table = driver.find_element_by_id("ContentPlaceHolder1_GV_List")
        first_line = True

        with tqdm(total=len(table.find_elements_by_tag_name("tr"))-1) as pbar:
            for row in table.find_elements_by_tag_name("tr"):
                if first_line:
                    first_line = False
                    continue
                column = row.find_elements_by_tag_name("td")
                info = {
                    "縣市別": column[1].text,
                    "醫事機構名稱": column[2].text,
                    "特約類別": column[3].text,
                    "分子": column[4].text,
                    "分母": column[5].text,
                    "院所指標值": column[6].text,
                    "所屬分區業務組指標值": column[7].text,
                    "全國指標值": column[8].text
                }
                DATA.append(info)
                pbar.update(1)
        dict2CSV(DATA, year, option)
    except Exception as e:
        print(e)
    driver.close()

for option in ASTHMA_OPTION:
    for year in YEAR_LIST:
        print("{} {}".format(YEAR_DICT[year], ASTHMA_DICT[option]))
        getTableData(year, option)
    
