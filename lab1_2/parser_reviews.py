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
with open('data/reviews.jsonlines', 'r') as f:
    for line in f:
        data = json.loads(line)
        description_doc = nlp(data['review'])
        if not data['review'].strip() or sum(c.isalpha() for c in data['review']) < 3: 
            logging.debug(f"Skipping review {data['review']} because it has no content") 
            continue
        item = {}
        item['book_id'] = data['book_id']
        item['review_id'] = data['review_id']
        item['title'] = data['reviewTitle']
        item['is_positive'] = data.get('rating',0) > 3
        item['description'] = " ".join(token.text for token in description_doc if not token.is_punct and not token.is_stop and not token.is_space)
        item['language'] = description_doc._.language

        print(item)            
        view.append(item)

df = pd.DataFrame(view)
df.to_parquet('data/reviews.parquet', index=False)   
