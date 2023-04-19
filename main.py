import requests
from bs4 import BeautifulSoup

# 设定目标网址以及页面后缀
url = 'https://news.uestc.edu.cn/?n=UestcNews.Front.CategoryV2.Page&CatId=50'
page_list = {'&page=1', '&page=2', '&page=3'}

# 获取网页信息
news_info = []

for page in page_list:
    response = requests.get(url + page).text
    target_info = [] # 接受目标信息
    beatiful_soup_object = BeautifulSoup(response, 'lxml')
    content_wrappers = beatiful_soup_object.findAll(name='div', attrs={'class': 'content-wrapper'})
    for every_news in content_wrappers:
        title = every_news.find(name='div', attrs={'class': 'title'}).a.get_text().replace(' ', '').replace('\n', '')
        date = every_news.find(name='div', attrs={'class': 'date'}).get_text().replace(' ', '').replace('\n', '')
        content = every_news.find(name='div', attrs={'class': 'content'}).get_text().replace(' ', '').replace('\n', '')
        news_info.append([title, date, content])

# 将结果写入txt
with open(file=r'output.txt', mode='w') as file:
    for i in range(len(news_info)):
        text = '新闻' + str(i + 1) + ': \n' + '新闻标题: ' + news_info[i][0] + '\n' + '新闻发布时间: ' + news_info[i][1] + '\n' + '新闻摘要: \n' + news_info[i][2] + '\n\n'
        file.write(text)