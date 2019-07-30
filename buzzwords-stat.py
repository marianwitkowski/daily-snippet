
# CAUTION!
# works with Python2.7

# pip install google-search
from googlesearch.googlesearch import GoogleSearch

import os, ssl

# http://blog.pengyifan.com/how-to-fix-python-ssl-certificate_verify_failed/
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

# something usefull module for drawing
import matplotlib.pyplot as plt

# module for creating word cloud data
# pip install wordcloud
from wordcloud import WordCloud

# Buzzwords list (each in new line)
KEYWORDS="""
Quantum Computing
Artificial Intelligence
IoT
Gamification
Technology Evangelist
Code Ninjas
Blockchain
Immersive Experience
Big Data
Robotic Process Automation
Mobile First
Industry 4.0
Chatbots
Machine Learning
Data Mining
Actionable Analytics
Net Neutrality
Augmented Reality
Virtual Reality
5G
Wearable
Cloud
Digital transformation
Agile
Industry leading
Customer journey
Microservice Architecture
Zettabyte Era
"""

items = KEYWORDS.split("\n")
result = {}
total = 0.0
google_search = GoogleSearch()

# don't execute too often - Google will detect unusual network activity and return HTTP Error 429
for item in items:
    phrase = item.strip()
    if len(phrase):
        response = google_search.search('"{}"'.format(phrase))
        found_search = int(response.total) / float(1E6)
        print("Result '{}' = {}".format(phrase, found_search))
        result[phrase] = found_search
        total += found_search

for key in result.keys(): result[key] /= float(total);

word_cloud = WordCloud(background_color="white",width=800,height=800,
               relative_scaling='auto', min_font_size=25,
               normalize_plurals=False).generate_from_frequencies(result)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(word_cloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()
plt.savefig('buzzwords.png')

print(result)
