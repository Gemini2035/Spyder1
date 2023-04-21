import requests
from bs4 import BeautifulSoup

# 设定目标网址以及页面后缀
url = 'https://news.uestc.edu.cn/?n=UestcNews.Front.CategoryV2.Page&CatId=50'
# 由于要爬取三页，而你校的翻页逻辑是在链接后加参数page=x，所以直接将前三页存入集合中
page_list = {'&page=1', '&page=2', '&page=3'}

# 获取网页信息
# 创建一个接受处理后数据的变量
news_info = []

# 这个for循环一次是代表爬取每一页的数据，比如第一次循环，page的值就是'&page=1'
for page in page_list:
    # (url + page)指的就是具体到每一页的链接，get就不对多说了，你懂的。.text就是get响应的文本内容(具体就是整个网页的html文本)
    response = requests.get(url + page).text
    # 用html文本内容创建 BeautifulSoup对象，使用lxml解析模式
    beatiful_soup_object = BeautifulSoup(response, 'lxml')
    # 该对象拥有一个findAll方法，即通过后面提供的参数返回符合参数要求的html内容。注意，返回形式是一个数组
    # 具体就是在该html文档中找到所有class属性为content-wrapper的div标签，并以数组形式返回
    content_wrappers = beatiful_soup_object.findAll(name='div', attrs={'class': 'content-wrapper'})
    # 想要的标题，时间，摘要属性都在这个名为content-wrapper的div中，下面使用for循环进行处理。变量content_wrappers本质上是一个数组，其中元素的类型都是BeautifulSoup类。
    # 具体就是每次循环的every_news的值都是BeautifulSoup类，可以使用其中的一切方法
    for every_news in content_wrappers:
        # 获取标题，BeautifulSoup类中有.find方法，类似于.findAll，不同的是，前者只会返回符合条件的第一个内容
        # get_text()同样也是BS类的方法，作用为返回指定标签中的文本内容
        # 后面的两个replace是python中字符串的方法，作用为将字符串的指定部分换成另一指定字符串
        # 具体来讲，就是将三个字符串中的所有换行符号和空格符号删去，简单理解就是格式化
        # 你校的title class中还有一层a标签，所以不能直接获取内容。解决办法先是.a获取到其中的a标签，再获取a标签中的文本内容
        title = every_news.find(name='div', attrs={'class': 'title'}).a.get_text().replace(' ', '').replace('\n', '')
        date = every_news.find(name='div', attrs={'class': 'date'}).get_text().replace(' ', '').replace('\n', '')
        content = every_news.find(name='div', attrs={'class': 'content'}).get_text().replace(' ', '').replace('\n', '')
        # 最后将结果加入到最开始创建的那个变量中
        news_info.append([title, date, content])
    
    # 此时news_info中的数据格式应该为[[新闻1标题, 新闻1发布时间, 新闻1摘要], [新闻2标题, 新闻2发布时间, 新闻2摘要]...]

# 将结果写入txt
# 使用with可以有效避免意外发生
with open(file=r'output.txt', mode='w') as file:
    # 这里的for循环是为了将每个新闻单独取出，处理后进行一行一行的文件写入
    # news_info[i]指向[新闻i标题, 新闻i发布时间, 新闻i摘要]，news_info[i][0]指向 新闻i标题， news_info[i][2、3]以此类推
    for i in range(len(news_info)):
        # 这里简单来说就是输出文本的格式化，你在txt文件中看到的格式就是在这里生成的，其中'\n'是换行符号，表示换行，+号在这里是字符串拼接
        text = '新闻' + str(i + 1) + ': \n' + '新闻标题: ' + news_info[i][0] + '\n' + '新闻发布时间: ' + news_info[i][1] + '\n' + '新闻摘要: \n' + news_info[i][2] + '\n\n'
        file.write(text)