'''
News API:  https://newsapi.org/
Mittels News API wird eine umfassende Analyse von Nachrichtenartikeln
durchgeführt. Die verfügbaren unterschiedlichen Nachrichtenquellen werden mithilfe
unterschiedlicher Kriterien abgerufen (z.B. Stichwörter, Themen und Veröffentlichungsdatum).
Im folgenden Beispiel wird als Stichwort "Österreich" verwendet, eine detailierte Analyse soll erfolgen.
Infos: https://newsapi.org/docs/endpoints/everything
'''

from datetime import datetime, date, timedelta
import requests
import pandas as pd
import newsapi
import os
import string
from collections import Counter

#from newsapi import NewsApiClient

# News infos API -------------------------------
# api key holen von https://newsapi.org
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api_key = os.environ.get('NEWS_API_KEY')

keyword = "Wien"
one_month = date.today() - timedelta(days=25)

# yesterday.strftime('%m%d%y')

def get_news():
    news_parameters = {
        "apiKey": news_api_key,
        "q": keyword,                               # Topic or keyword for search
        #"qInTitle": keyword,
        "language": "de",
        #"from": datetime.now(),
        'pageSize': 10,                             # number of articles
        'sortBy': 'publishedAt', #  popularity,     # Sortieren nach Veröffentlichungsdatum
        'from': one_month, #                        # YYYY-MM-DD,  # start date: yesterday
        'to':  datetime.now(), #    one_month,      # YYYY-MM-DD # end date
    }
    response = requests.get(NEWS_ENDPOINT, params= news_parameters)

    # Check if the API request was successful
    if response.status_code == 200:
        print("API is accessible")
    else:
        print("API is not accessible")

    # Parse the JSON response
    data = response.json()["articles"]

    # Extract relevant information from the response
    article_list = []
    # for all articles
    for article in data:
        # add extracted information for one article to a dictionary
        article_dict = {
            'author': article['author'],
            'title': article['title'],
            'description': article['description'],
            'publishedAt': article['publishedAt'],
        }
        # append dictionary of one article to a list of all articles
        article_list.append(article_dict)

    # Create a pandas DataFrame with the extracted information
    news_df = pd.DataFrame(article_list)
    return news_df


def analyse_articles(news_df):
    all_text = ""
    for article in news_df['articles']:
        description = article.get('description')
    if description is not None:
        all_text += description + ' '
    words = all_text.split()
    filtered_words = [word for word in words if len(word) > 5]
    word_counts = Counter(filtered_words)
    most_common_words = word_counts.most_common(10)
    print(most_common_words)



news_df = get_news()
analyse_articles(news_df)