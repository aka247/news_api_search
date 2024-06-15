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
import matplotlib.pyplot as plt
# regular expressions module
import re

pd.set_option('display.max_colwidth', None)

# News infos API -------------------------------
# api key holen von https://newsapi.org
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api_key = "c2228e0ce11543388acca5d1cbc9e5e5" #os.environ.get('NEWS_API_KEY')

keyword = "Wien"
one_month = date.today() - timedelta(days=30)

# yesterday.strftime('%m%d%y')

# function to get articles from news API
def get_news(keyword_, time_period, pageSize_, sortBy_):
    now = date.today().isoformat()
    pageSize = int(pageSize_+(pageSize_/2))  # retrieve more data due to possible duplicates
    news_parameters = {
        "apiKey": news_api_key,
        "q": keyword_,           # Topic or keyword for search
        # "qInTitle": keyword_,
        "language": "de",
        'pageSize': pageSize,  # number of articles
        'sortBy': sortBy_,
        'from': time_period,    # YYYY-MM-DD, start date
        'to': now,              # YYYY-MM-DD, end date
    }

    # API request
    response = requests.get(NEWS_ENDPOINT, params=news_parameters)

    # Check if the API request was successful
    if response.status_code == 200:
        print("API is accessible")
    else:
        print(f"API is not accessible, Status code: {response.status_code}, Response: {response.text}")

    # Parse the JSON response
    data = response.json()["articles"]

    # convert to Pandas DataFrame
    allData_df = pd.DataFrame(data)
    news_df = allData_df[["title", "description", "publishedAt"]]
    news_df = news_df.dropna(subset=['description'])          # remove incomplete datasets
    news_df = news_df.drop_duplicates()  # remove duplicates
    # Slice the DataFrame to include only the first `pageSize_` rows
    news_df = news_df.iloc[:pageSize_]
    pattern =  r'[^\w\s-]'  # matches any character that is not a letter, digit, underscore, or whitespace
    # Use regex substitution to remove special characters from the description column
    news_df["description"] = news_df["description"].apply(lambda x: re.sub(pattern, '', x))


    # Save DataFrame to csv, to check, if statistics are correct
    # now_f = f'{now.strftime("%m_%d_%Y_%H_%M_%S")}'
    # news_df.to_csv(f"file_{now_f}.csv", encoding='utf-8-sig', index=False)  # encoding="utf-8")
    # news_df["description"].to_csv(f"file_{now_f}.csv", encoding='utf-8-sig', index=False)  # encoding="utf-8")
    return news_df

# count words longer than 5 letters and find the 10 most common words +++++++
def analyse_articles(news_df):
    all_text = ""
    for description in news_df['description']:
        all_text += description + ' '

    words = all_text.split()
    filtered_words = [word for word in words if len(word) > 5]
    # get Statistics
    word_counts = Counter(filtered_words)
    most_common_words = word_counts.most_common(10)

    # just for evaluation
    news_df["description"].to_csv('description.csv', index=False, header=False)

    return most_common_words


# plot most common words in a bar chart
def plot_most_common_words(most_common_words, keyword_, time_period, pageSize_, sortBy_):
    # Extract categories and counts
    words = [word[0] for word in most_common_words]
    counts = [count[1] for count in most_common_words]

    plt.figure(figsize=(8, 5))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top 10 Most Common Words')

    expl = f'Keyword "{keyword_}", time period from {time_period} up to now, pagesize {pageSize_}, sort by {sortBy_}'
    #plt.figtext(expl, fontsize=10, y=0.95, ha='center')
    plt.figtext(0.5, -0.1, expl, wrap=True, horizontalalignment='center', fontsize=10)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # plt.figure(figsize=(7, 5))
    # #plt.rc('font', size=8)
    # plt.bar(words, counts, color="green")
    #
    # plt.xlabel("Words")
    # # Rotate x-axis labels
    # #plt.xticks(rotation=90)
    # plt.ylabel("Counts")
    # plt.show()


def visualize_news_articles(keyword_, days, pageSize_, sortBy_):
    # get news dataframe
    time_period = get_time_period(days)
    news_df = get_news(keyword_, time_period, pageSize_, sortBy_)
    #print(news_df)

    # calculate most common words
    most_common_words = analyse_articles(news_df)
    print(
        f'The most common words with keyword "{keyword_}" in a period from {time_period} up to now, with pagesize {pageSize_}, sort by {sortBy_} are:\n {most_common_words}')

    # plot statistics
    plot_most_common_words(most_common_words, keyword_, time_period, pageSize_, sortBy_)



def get_time_period(days):
    # subtract days from actual date, format the result
    return (date.today() - timedelta(days)).isoformat()



# #############################################################
# Visualize the word count of news articles with diffenent parameters
visualize_news_articles(keyword_="Österreich", days=5, pageSize_=10, sortBy_='publishedAt')

#visualize_news_articles(keyword_="Österreich", days=30, pageSize_=100. sortBy_="popularity"))