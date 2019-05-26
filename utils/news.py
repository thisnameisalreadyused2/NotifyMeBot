import requests


def get_news_for_country(country_code):
    url = ('https://newsapi.org/v2/top-headlines?'
       f'country={country_code}&'
       'apiKey=a4e5ef0cf27d45ac8dfc2e6026f88fc5')
    r = requests.get(url).json()
    news = "*Popular news for today:*\n"
    if r['status'] != "ok":
        return

    for idx, article in enumerate(r['articles']):
        new = "{0}. [{1}]({2})\n".format(idx+1, article['title'], article['url'])
        news += new
        if idx > 4:
            return news

    return news
