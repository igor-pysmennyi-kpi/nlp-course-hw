import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import spacy
import ast

BOOK_TO_RECOMMEND = 0

stopwords = []
with open('stopwords_ua_list.txt', 'r') as f:
    stopwords = ast.literal_eval(f.read())
nlp = spacy.load('uk_core_news_sm')


df_books = pd.read_parquet('data/books_enriched.parquet')
df_books = df_books.dropna(subset=['description'])
df_books = df_books[df_books['language'] == 'uk']

df_books.to_parquet('data/books_enriched_cleaned.parquet', index=False)   

print(df_books.shape)

def lemmatize_text(text):
    return ' '.join([token.lemma_ for token in nlp(text)])

vectorizer = TfidfVectorizer(tokenizer=lemmatize_text, stop_words=stopwords)

tfidf_matrix = vectorizer.fit_transform(df_books['description'])

from sklearn.metrics.pairwise import cosine_similarity

first_vector = tfidf_matrix[BOOK_TO_RECOMMEND]

cosine_similarities = cosine_similarity(first_vector, tfidf_matrix)
print(cosine_similarities)

normalized_scores = df_books['positive_reviews_score'] / df_books['positive_reviews_score'].max()
first_vector_similarities = cosine_similarities[0] *normalized_scores.values

most_similar_index = first_vector_similarities.argsort()[-4]
print(first_vector_similarities[most_similar_index])
print(df_books.iloc[most_similar_index])