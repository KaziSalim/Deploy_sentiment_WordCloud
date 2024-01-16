from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
import os

app = Flask(__name__)

def get_reviews(url):
    reviews = []
    for page_number in range(1, 21):
        ip = []
        full_url = f"{url}&pageNumber={page_number}"
        response = requests.get(full_url)
        soup = bs(response.content, "html.parser")
        review_elements = soup.find_all("span", attrs={"class", "a-size-base review-text review-text-content"})
        for review in review_elements:
            ip.append(review.get_text())
        reviews += ip
    return reviews

def preprocess_reviews(reviews, stop_words_path):
    reviews_string = " ".join(reviews)
    reviews_string = re.sub("[^A-Za-z]+", " ", reviews_string).lower()

    with open(stop_words_path, "r") as sw:
        stop_words = sw.read().split("\n")
    stop_words.extend(["amazon", "echo", "time", "android", "phone", "device", "product", "day"])

    reviews_words = [w for w in reviews_string.split(" ") if w not in stop_words and len(w) > 1]
    return " ".join(reviews_words)

def generate_wordcloud(text, output_path, background_color='white'):
    if text:
        wordcloud = WordCloud(background_color=background_color, width=1800, height=1400).generate(text)
        wordcloud.to_file(output_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud_route():
    url = request.form['url']
    stop_words_path = "D:/Data Scientist/Unsupervised Learning/Text Mining & NLP/GitHub/SHAKAYA WORLD/stop.txt"
    pos_words_path = "D:/Data Scientist/Unsupervised Learning/Text Mining & NLP/GitHub/SHAKAYA WORLD/positive-words.txt"
    neg_words_path = "D:/Data Scientist/Unsupervised Learning/Text Mining & NLP/GitHub/SHAKAYA WORLD/negative-words.txt"


    reviews = get_reviews(url)
    preprocessed_reviews = preprocess_reviews(reviews, stop_words_path)

    print("Preprocessed Reviews:", preprocessed_reviews)  # Log preprocessed text

    generate_wordcloud(preprocessed_reviews, "static/wordcloud_ip.png", background_color='white')

    with open(pos_words_path, "r") as pos:
        pos_words = pos.read().split("\n")
    pos_in_pos = " ".join([w for w in preprocessed_reviews.split(" ") if w in pos_words])
    generate_wordcloud(pos_in_pos, "static/wordcloud_pos.png", background_color='white')

    with open(neg_words_path, "r") as neg:
        neg_words = neg.read().split("\n")
    neg_in_neg = " ".join([w for w in preprocessed_reviews.split(" ") if w in neg_words])
    generate_wordcloud(neg_in_neg, "static/wordcloud_neg.png", background_color='black')

    return render_template('index.html', wordcloud_generated=True)

if __name__ == '__main__':
    app.run(debug=True)
