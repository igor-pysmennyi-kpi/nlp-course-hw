import json
from flair.models import SequenceTagger
from flair.data import Sentence


def load_file():
    with open('news.json', 'r') as f:
        data = json.load(f)
        return data
    
def parse_ner(text):
    # Load the pre-trained NER model
    tagger = SequenceTagger.load('dchaplinsky/flair-uk-ner')

    # Create a sentence object
    sentence = Sentence(text)

    # Run NER on the sentence
    tagger.predict(sentence)

    # Get the named entities from the sentence
    named_entities = sentence.get_spans('ner')

    # Extract the entity text and label
    entities = [(entity.text, entity.tag) for entity in named_entities]

    return entities


if __name__ == "__main__":
    data = load_file()
    for article in data:
        #first ner was not recognised without a dot at the beginning
        article['header_ner'] = parse_ner('.' + article['header'])
        article['text_ner'] = parse_ner('.' + article['text'])
    with open('news_ner.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=3)