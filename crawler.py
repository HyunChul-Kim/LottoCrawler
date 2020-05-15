import requests
import re
from bs4 import BeautifulSoup
import json


def ordinal(n):
    if n == 1:
        return '1st'
    elif n == 2:
        return '2nd'
    elif n == 3:
        return '3rd'
    else:
        return str(n) + 'th'


def getWinningInfo(winning_round):
    return getWinningInfoWithRange(winning_round, winning_round+1)


def getWinningInfoWithRange(min_round, max_round):
    result = []
    for i in range(min_round, max_round):
        ## 번첨 번호, 등수별 당첨 금액 crawling
        win_result = {u'round': i}
        url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo=" + str(i)
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        win_nums = []
        for j in range(1, 7):
            selector = '#article > div:nth-of-type(2) > div > div.win_result > div > div.num.win > p > span:nth-of-type(' + str(
                j) + ')'
            win_nums.append(int(soup.select(selector)[0].text.strip()))

        win_result.update({u'win_result': {u'numbers': win_nums}})

        selector = '#article > div:nth-of-type(2) > div > div.win_result > div > div.num.bonus > p > span'
        bonus = int(soup.select(selector)[0].text.strip())

        win_result.update({u'win_result': {u'bonus': bonus}})

        win = {}
        for j in range(1, 6):
            selector = '#article > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                j) + ') > td:nth-of-type(2) > strong'
            total = int(re.sub(r",|원", "", soup.select(selector)[0].text.strip()))
            selector = '#article > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                j) + ') > td:nth-of-type(3)'
            num_of_win = int(re.sub(r",", "", soup.select(selector)[0].text.strip()))
            win.update({ordinal(j): {u'total_amount': total, u'number_of_winners': num_of_win}})

        win_result.update({u'win_result': {u'numbers': win_nums, u'bonus': bonus, u'win': win}})

        ## 당첨 판매점 crawling
        ## 262회차부터 판매점 조회 가능
        if i >= 262:
            store_url = "https://dhlottery.co.kr/store.do?method=topStore&pageGubun=L645&nowPage=1&rankNo=&gameNo=5133&drwNo=" + str(
                i) + "&schKey=all&schVal="
            store_html = requests.get(store_url).text
            store_soup = BeautifulSoup(store_html, 'html.parser')
            store = {}
            store_selector = "#article > div:nth-of-type(2) > div > div.group_content > table > tbody"

            ## 1등 당첨 판매점
            first_table = store_soup.select(store_selector)[0]
            first_store = []
            for tr in first_table.findAll('tr'):
                index = 0
                store_name = ""
                purchase_type = ""
                address = ""
                for td in tr.findChildren():
                    if index == 1:
                        store_name = td.text.strip()
                    elif index == 2:
                        purchase_type = td.text.strip()
                    elif index == 3:
                        address = td.text.strip()
                    index += 1
                store_info = {u'name': store_name, u'purchase_type': purchase_type, u'address': address}
                first_store.append(store_info)
            store.update({u'first_store': first_store})

            ## 2등 당첨 판매점
            second_store = []

            ## 2등 당첨 판매점 페이지
            page_selector = "#article > div:nth-of-type(2) > div > div.group_content > div.paginate_common"
            pages = store_soup.select(page_selector)[0]
            page_index = 1
            for page in pages.findAll('a'):
                page_url = "https://dhlottery.co.kr/store.do?method=topStore&pageGubun=L645&nowPage=" + str(
                    page_index) + "&rankNo=&gameNo=5133&drwNo=" + str(i) + "&schKey=all&schVal="
                page_html = requests.get(page_url).text
                page_soup = BeautifulSoup(page_html, 'html.parser')
                second_store_selector = "#article > div:nth-of-type(2) > div > div.group_content > table > tbody"
                second_store_table = page_soup.select(second_store_selector)[1]
                for tr in second_store_table.findAll('tr'):
                    index = 0
                    store_name = ""
                    address = ""
                    for td in tr.findChildren():
                        if index == 1:
                            store_name = td.text.strip()
                        elif index == 2:
                            address = td.text.strip()
                        index += 1
                    store_info = {u'name': store_name, u'address': address}
                    second_store.append(store_info)
                page_index += 1

            store.update({u'second_store': second_store})
            win_result.update({u'store_info': store})
        if max_round - min_round == 1:
            return win_result
        result.append(win_result)
    return result
