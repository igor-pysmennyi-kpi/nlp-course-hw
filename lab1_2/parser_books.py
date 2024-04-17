import json
import pandas as pd
import logging

import spacy
from spacy_fastlang import LanguageDetector

nlp = spacy.load('uk_core_news_sm')
if 'language_detector' in nlp.pipe_names:
    nlp.remove_pipe('language_detector')

# Add the new language detector to the pipeline
language_detector = LanguageDetector()
nlp.add_pipe('language_detector')

view  = []
with open('data/books.jsonlines', 'r') as f:
    for line in f:
        data = json.loads(line)
        description_doc = nlp(data['description'])
        if not data['description'].strip() or sum(c.isalpha() for c in data['description']) < 3: 
            logging.debug(f"Skipping book {data['book_id']} because it has no description") 
            continue
        item = {}
        item['book_id'] = data['book_id']
        item['title'] = data['title']
        item['description'] = " ".join(token.text for token in description_doc if not token.is_punct and not token.is_stop and not token.is_space)
        item['language'] = description_doc._.language

        print(item)            
        view.append(item)

df = pd.DataFrame(view)
df.to_parquet('data/books.parquet', index=False)  