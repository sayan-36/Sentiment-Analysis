import requests
from bs4 import BeautifulSoup
import pandas as pd
#from textblob import TextBlob


# Function to extract article text using BeautifulSoup
def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main content using the 'article' tag
    article_content = soup.find('article')

    # If 'article' tag is not found, try to find other common content tags
    if not article_content:
        article_content = soup.find(['div', 'section', 'main'])

    # If still not found, try to extract all text from the body
    if not article_content:
        article_content = soup.body

    # Extract text from paragraphs within the content
    paragraphs = article_content.find_all('p') if article_content else []
    article_text = " ".join([p.text for p in paragraphs])

    return article_text

# Read URLs from Input.xlsx
input_data = pd.read_excel('Input.xlsx')

# Iterate through each URL
for index, row in input_data.iterrows():
    url = row['URL']
    url_id = row['URL_ID']

    # Extract article text
    article_text = extract_article_text(url)

    # Save the extracted text to a file
    with open(f"{url_id}.txt", 'w', encoding='utf-8') as file:
        file.write(article_text)

    
    