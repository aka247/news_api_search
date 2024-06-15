'''
News API:  https://newsapi.org/
Mittels News API wird eine umfassende Analyse von Nachrichtenartikeln
durchgeführt. Die verfügbaren unterschiedlichen Nachrichtenquellen werden mithilfe
unterschiedlicher Kriterien abgerufen (z.B. Stichwörter, Themen und Veröffentlichungsdatum).
Im folgenden Beispiel wird als Stichwort "Österreich" verwendet, eine detailierte Analyse soll erfolgen.
Infos: https://newsapi.org/docs/endpoints/everything
'''

#-------------------------------------
# see jupyter notebook abgabe data science with plots
#-------------------------------------

from datetime import datetime, date, timedelta
import requests
import pandas as pd
import newsapi
import os
from collections import Counter

# News infos API -------------------------------
# api key holen von https://newsapi.org
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api_key = os.environ.get('NEWS_API_KEY')

keyword = "Wien"
one_month = date.today() - timedelta(days=30)

# yesterday.strftime('%m%d%y')

# get articles from news API +++++++++++++++
def get_news():
    news_parameters = {
        "apiKey": news_api_key,
        "q": keyword,                               # Topic or keyword for search
        #"qInTitle": keyword,
        "language": "de",
        'pageSize': 10,                            # number of articles
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

    # convert to Pandas DataFrame
    allData_df = pd.DataFrame(data)
    # Extract relevant information
    news_df = allData_df[["title", "description", "publishedAt"]]

    return news_df

# count words longer than 5 letters and find the 10 most common words +++++++
def analyse_articles(news_df):
    long_words = []
    # get from each row of the dataframe the article text in column "description"
    for article in news_df['description']:
        if article is not None:
            # split the sentences in words
            article_split = article.split()
            # append words longer than 5 to list and remove punctuation
            #long_words = [word.strip('[]/.!,„“') for word in article_split if len(word) > 5]
            for word in article_split:
                clean_word = word.strip('[]/.!?,„“')
                if len(clean_word) > 5:
                    long_words.append(clean_word)
    word_counts = Counter(long_words)
    most_common_words = word_counts.most_common(10)
    return most_common_words


#****************************************************

news_df = get_news()
most_common_words = analyse_articles(news_df)
print(most_common_words)
print(most_common_words)