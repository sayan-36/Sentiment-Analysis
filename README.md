# Sentiment-Analysis

Approach

The solution involves sentiment analysis, web scraping articles from a list of URLs, and utilizing Python to compute various text-related features. The essential actions are listed below:

Web scraping: The articles' major material was extracted from the given URLs using the BeautifulSoup and requests libraries. The function extract_article_text searches the HTML structure for the relevant text.


Sentiment Analysis: To analyse sentiment, the TextBlob package was used. TextBlob was utilized to extract the polarity and subjectivity scores, while the positive and negative sentiment ratings were calculated using the calculate_positive_score and calculate_negative_score functions.
NLP-Related characteristics: To calculate additional characteristics including average word length, proportion of complicated words, Fog Index, average number of words per sentence, count of complex terms, word count, syllables per word, and average word length, the calculate_nlp_features function was developed. 

Output Handling: The final output was saved to an Excel file using the to_excel function, and the results were kept in a Pandas DataFrame.

How to Run the .py File to Generate Output

1.Install Dependencies:
pip install requests
pip install beautifulsoup4
pip install pandas
pip install textblob
pip install nltk
2.Load the input.xlsx file.
3.Run the Python script.
