import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tag import pos_tag

# Download NLTK resources 
nltk.download('punkt')
nltk.download('stopwords')

# Function to calculate positive score using TextBlob
def calculate_positive_score(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Function to calculate negative score using TextBlob
def calculate_negative_score(text):
    blob = TextBlob(text)
    return -blob.sentiment.polarity

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

# Function to calculate other NLP-related features
def calculate_nlp_features(text):
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    
    stop_words = set(stopwords.words("english"))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    word_lengths = [len(word) for word in filtered_words]

    # Check if word_lengths is not empty before calculating average
    avg_word_length = sum(word_lengths) / len(word_lengths) if len(word_lengths) > 0 else 0

    # Count the number of personal pronouns
    personal_pronouns = [word.lower() for word, tag in pos_tag(filtered_words) if tag == 'PRP']

    # Calculate AVG SENTENCE LENGTH
    avg_sentence_length = sum(len(sent.split()) for sent in sentences) / len(sentences) if len(sentences) > 0 else 0

    # Calculate PERCENTAGE OF COMPLEX WORDS
    complex_words = [word for word, tag in pos_tag(filtered_words) if tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']]
    percentage_complex_words = (len(complex_words) / len(filtered_words)) * 100 if len(filtered_words) > 0 else 0

    # Calculate FOG INDEX
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # Calculate AVG NUMBER OF WORDS PER SENTENCE
    avg_words_per_sentence = len(filtered_words) / len(sentences) if len(sentences) > 0 else 0

    # Calculate COMPLEX WORD COUNT
    complex_word_count = len(complex_words)

    # Calculate WORD COUNT
    word_count = len(filtered_words)

    # Calculate SYLLABLE PER WORD
    syllable_per_word = sum([sum(1 for c in word if c.lower() in 'aeiou') for word in filtered_words]) / len(filtered_words) if len(filtered_words) > 0 else 0

    return avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count, word_count, syllable_per_word, avg_word_length, personal_pronouns

# Read URLs from Input.xlsx
input_data = pd.read_excel('Input.xlsx')

# Create an empty DataFrame for output data
output_data = pd.DataFrame(columns=['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
                                    'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS',
                                    'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT',
                                    'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH',
                                    'ARTICLE_TEXT'])

# Iterate through each URL
for index, row in input_data.iterrows():
    url = row['URL']

    # Extract article text
    article_text = extract_article_text(url)

    # Perform text analysis
    blob = TextBlob(article_text)
    positive_score = blob.sentiment.polarity
    negative_score = -positive_score
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity

    # Calculate other NLP-related features
    avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count, word_count, syllable_per_word, avg_word_length, personal_pronouns = calculate_nlp_features(article_text)

    # Store results in the Output Data DataFrame
    output_data = output_data.append({'URL_ID': row['URL_ID'],
                                      'URL': url,
                                      'POSITIVE SCORE': positive_score,
                                      'NEGATIVE SCORE': negative_score,
                                      'POLARITY SCORE': polarity_score,
                                      'SUBJECTIVITY SCORE': subjectivity_score,
                                      'AVG SENTENCE LENGTH': avg_sentence_length,
                                      'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
                                      'FOG INDEX': fog_index,
                                      'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
                                      'COMPLEX WORD COUNT': complex_word_count,
                                      'WORD COUNT': word_count,
                                      'SYLLABLE PER WORD': syllable_per_word,
                                      'PERSONAL PRONOUNS': personal_pronouns,
                                      'AVG WORD LENGTH': avg_word_length,
                                      'ARTICLE_TEXT': article_text
                                      }, ignore_index=True)

# Save the output to a single Excel file
output_data.to_excel('SentimentAnalysisOutput.xlsx', index=False)
