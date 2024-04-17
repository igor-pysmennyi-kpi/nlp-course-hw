import pandas as pd

# Read the Parquet file into a DataFrame
df_reviews = pd.read_parquet('data/reviews.parquet')
positive_reviews = df_reviews[df_reviews['is_positive'] == True].value_counts('book_id').sort_index(ascending=True)
max_reviews = positive_reviews.max()

df_books = pd.read_parquet('data/books.parquet')
df_books = df_books.merge(positive_reviews, on='book_id', how='left')
df_books = df_books.rename(columns={'count': 'positive_reviews_count'})
df_books = df_books.fillna({'positive_reviews_count': 0})
df_books['positive_reviews_score'] = df_books['positive_reviews_count'] / max_reviews

df_books.to_parquet('data/books_enriched.parquet', index=False)   
#todo implement wilson score
