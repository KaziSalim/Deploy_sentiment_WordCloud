import requests
from bs4 import BeautifulSoup as bs
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Create empty list of reviews
SHAKAYA_reviews= []

for page_number in range(1,21):
    ip = []
    url = "https://www.amazon.in/SHAKYA-WORLD-Operated-Children-Toddlers/product-reviews/B09H4KZ4KW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"+ str(page_number)
    response = requests.get(url)
    soup = bs(response.content,"html.parser")
    reviews = soup.find_all("span", attrs = {"class","a-size-base review-text review-text-content"})
    for review in reviews:
        ip.append(review.get_text())
    
    SHAKAYA_reviews += ip    # a+=1 (a = a+1)
    
# Writing reviews in text file
with open("shakaya.text","w",encoding = 'utf8') as output:
    output.write(str(SHAKAYA_reviews))
    
import os
os.getcwd()   

# Joining all the reviews in single paragraph
ip_review_string = " ".join(SHAKAYA_reviews) 

import nltk

# removing unwanted symbols incase they exists
ip_review_string = re.sub("[^A-Za-z" "]+", " ",ip_review_string).lower()

# words that are contained in the reviews
ip_review_word = ip_review_string.split(" ")

ip_review_word = ip_review_word[1:]

#TFIDF
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(use_idf = True, ngram_range = (1, 1))
X = vectorizer.fit_transform(ip_review_word)


with open("D:/Data Scientist/Text Mining & NLP/stop_+ve_-ve words/stop.txt", "r") as sw:
    stop_words = sw.read()
    
stop_words = stop_words.split("\n")

stop_words.extend(["Amazon", "echo", "time", "android", "phone", "device", "product", "day"])

ip_review_word = [w for w in ip_review_word if not w in stop_words]

# Joining all the reviews into single paragraph 
ip_rev_string = " ".join(ip_review_word)

# WordCloud can be performed on the string inputs.
# Corpus level word cloud

wordcloud_ip = WordCloud(background_color = 'White',
                      width = 1800,  height = 1400
                     ).generate(ip_rev_string)
plt.imshow(wordcloud_ip)

# Positive words 

# Choose the path for +ve words stored in system
with open("D:/Data Scientist/Text Mining & NLP/stop_+ve_-ve words/positive-words.txt", "r") as pos:
  poswords = pos.read().split("\n")

# Positive word cloud
# Choosing only words which are present in positive words
ip_pos_in_pos = " ".join ([w for w in ip_review_word if w in poswords])

wordcloud_pos_in_pos = WordCloud(
                      background_color = 'White',
                      width = 1800,
                      height = 1400
                     ).generate(ip_pos_in_pos)
plt.figure(2)
plt.imshow(wordcloud_pos_in_pos)

# Negative word cloud

# Choose path for -ve words stored in system
with open("D:/Data Scientist/Text Mining & NLP/stop_+ve_-ve words/negative-words.txt", "r") as neg:
  negwords = neg.read().split("\n")

# negative word cloud
# Choosing only words which are present in negwords
ip_neg_in_neg = " ".join ([w for w in ip_review_word if w in negwords])

wordcloud_neg_in_neg = WordCloud(
                      background_color = 'black',
                      width = 1800,
                      height = 1400
                     ).generate(ip_neg_in_neg)
plt.figure(3)
plt.imshow(wordcloud_neg_in_neg)












    
        
        