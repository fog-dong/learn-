#源代码爬取的网页：https://news.house.qq.com/a/20170702/003985.htm
#encode = utf-8
import requests
import bs4
import re
import openpyxl

def open_url(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"}
    res = requests.get(url, headers = headers)

    return res

def find_data(res):
    data = []
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    content = soup.find(id = "Cnt-Main-Article-QQ")
    target = content.find_all("p", style = "TEXT-INDENT: 2em")
    target = iter(target)
    for each in target:
        if each.text.isnumeric():
            data.append([
                re.search(r'\[(.+)\]',next(target).text).group(1),
                re.search(r'\d.*', next(target).text).group(),
                re.search(r'\d.*', next(target).text).group(),
                re.search(r'\d.*', next(target).text).group()])
    return data

def to_excel(data):
    wb = openpyxl.Workbook()
    wb.guess_types  = True
    ws = wb.active
    ws.append(['城市', '平均房价', '平均工资', '放假工资比'])
    for each in data:
        ws.append(each)

    wb.save("2017全国城市房价工资排行榜.xlsx")

def main():
    url = "https://news.house.qq.com/a/20170702/003985.htm"
    res = open_url(url)
    data = find_data(res)
    to_excel(data)


if __name__ == "__main__":
    main()
