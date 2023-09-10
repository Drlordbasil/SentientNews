import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from datetime import datetime
import random


class Article:
    def __init__(self, title, author, publication_date, main_text, url=None, advertisement=None):
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.main_text = main_text
        self.url = url
        self.advertisement = advertisement
        self.categories = []
        self.sentiment = None


class NewsAggregator:
    def __init__(self):
        self.content_database = []

    def web_scraping(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.get_text()
            author = soup.find('meta', {'name': 'author'})['content']
            publication_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            main_text = soup.find('main').get_text()

            article = Article(title, author, publication_date, main_text, url)
            self.content_database.append(article)
        else:
            raise ValueError(f"Error accessing URL: {url}")

    def content_extraction(self):
        nlp = pipeline("article", framework="tf")
        for article in self.content_database:
            extracted_content = nlp(article.main_text)
            extracted_text = " ".join([sentence['text']
                                      for sentence in extracted_content])
            article.main_text = extracted_text

    def topic_extraction(self):
        nlp = pipeline("ner", framework="tf")
        for article in self.content_database:
            extracted_topics = nlp(article.main_text)
            categories = []
            for topic in extracted_topics:
                categories.append(topic['label'])
            article.categories = categories

    def sentiment_analysis(self):
        nlp = pipeline("sentiment-analysis", framework="tf")
        for article in self.content_database:
            result = nlp(article.main_text)
            article.sentiment = result[0]['label']

    def content_recommendations(self, user_reading_history):
        recommended_content = []
        for article in self.content_database:
            if article.sentiment == 'POSITIVE':
                recommended_content.append(article)
        random.shuffle(recommended_content)
        return recommended_content[:5]

    def social_media_integration(self):
        social_media_posts = []
        for article in self.content_database:
            post = f"New article: {article.title}\n\nRead more: {article.url}"
            social_media_posts.append(post)
        return social_media_posts

    def advertising_integration(self):
        advertising_placements = []
        for article in self.content_database:
            ad_placement = f"Advertisement: {article.title}\n\n{article.advertisement}"
            advertising_placements.append(ad_placement)
        return advertising_placements

    def dynamic_updates(self, rss_feeds):
        for feed_url in rss_feeds:
            response = requests.get(feed_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')
                for item in items:
                    title = item.title.get_text()
                    author = item.author.get_text()
                    publication_date = item.pubDate.get_text()
                    main_text = item.description.get_text()

                    article = Article(
                        title, author, publication_date, main_text)
                    self.content_database.append(article)
            else:
                raise ValueError(f"Error accessing RSS feed: {feed_url}")


class User:
    def __init__(self):
        self.reading_history = []

    def read_article(self, article):
        self.reading_history.append(article)


# Example usage
if __name__ == "__main__":
    aggregator = NewsAggregator()
    aggregator.web_scraping('https://example.com/article1')
    aggregator.web_scraping('https://example.com/article2')
    aggregator.web_scraping('https://example.com/article3')
    aggregator.content_extraction()
    aggregator.topic_extraction()
    aggregator.sentiment_analysis()

    user = User()
    recommended_articles = aggregator.content_recommendations(
        user.reading_history)
    social_media_posts = aggregator.social_media_integration()
    advertising_placements = aggregator.advertising_integration()

    aggregator.dynamic_updates(['https://example.com/rss_feed'])
