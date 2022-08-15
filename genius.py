import requests
from bs4 import BeautifulSoup
import nltk
import config

nltk.download('punkt')

def determineLabel(name, artist, classifier):
    total_words = []
    
    # Search For Song In Genius
    search_term = artist + name
    URL = f"http://api.genius.com/search?q={search_term}&access_token={config.GENIUS_ACCESS_TOKEN}"
    req = requests.get(URL)

    # Get Song's Lyrics From Genius
    response = req.json()['response']
    url = response['hits'][0]['result']['url']
    page = requests.get(url)

    # Use BeautifulSoup To Extract Lyrics
    soup = BeautifulSoup(page.content, 'html.parser')
    lyrics = soup.find_all('div', class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")

    # Clean And Process Song Lyrics For Testing
    for section in lyrics:
        for lyric in section:
            lyric = lyric.text
            if (']' not in lyric) and (len(lyric) != 0): # checking for [verse 1]:marco or empty lines
                lyric = nltk.word_tokenize(lyric)
                total_words.append(lyric)
    total_words_cpy = [token for tokens in total_words for token in tokens]
    label = classifier.classify(dict([token, True] for token in total_words_cpy))
    return label