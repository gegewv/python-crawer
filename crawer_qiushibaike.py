# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

def get_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    return r.text


def get_content(html, page):
    # 最终输出格式
    output = """第{}页 作者：{} 性别：{} 级别：{} 点赞：{} 评论：{}\n{}\n------------\n"""
    soup = BeautifulSoup(html, 'html.parser')
    content_left = soup.find(id='content-left')
    article_list = content_left.find_all('div', class_="article")

    for i in article_list:
        author = i.find('h2').string
        article_content = i.find('div', class_='content').find('span').get_text()
        stats = i.find('div', class_='stats')
        vote = stats.find('span', class_='stats-vote').find('i', class_='number').string
        comment = stats.find('span', class_='stats-comments').find('i', class_='number').string
        author_info = i.find('div', class_='articleGender')
        if author_info is not None:
            class_list = author_info['class']
            if "womenIcon" in class_list:
                gender = '女'
            elif "manIcon" in class_list:
                gender = '男'
            else:
                gender = ''
            level = author_info.string
        else:
            gender = ''
            level = ''
        save_txt(output.format(page, author, gender, level, vote, comment, article_content))


def save_txt(*args):
    for i in args:
        with open('qiushibaike.txt', 'a', encoding='utf-8') as f:
            f.write(i)


def main():
    url = 'https://qiushibaike.com/text/page/{}'
    page = get_page(url)
    # print(page)
    for i in range(1, page+1):
        html = get_html(url.format(i))
        get_content(html, i)


def get_page(url):
    
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('ul', class_='pagination').find_all('li')
    page = pagination[6].find('span').text
    return int(page)

if __name__ == '__main__':
    main()
