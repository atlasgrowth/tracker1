import json
import spacy
from collections import Counter

def main():
    # Load the spaCy English model.
    nlp = spacy.load("en_core_web_sm")

    # Load reviews from your JSON file (assumed to be "reviews.json")
    with open("reviews_by_business.json", "r", encoding="utf-8") as f:
        reviews = json.load(f)

    name_counter = Counter()

    # Process each review's text.
    for review in reviews:
        text = review.get("text")
        if text:
            doc = nlp(text)
            # For each named entity recognized as a person...
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    # Clean up the text and update our counter.
                    name = ent.text.strip()
                    # Optional: skip names that are too short or have nonalphabetic characters.
                    if len(name) > 1 and name.replace("'", "").isalpha():
                        name_counter[name] += 1

    # Print out names sorted by frequency.
    print("Guessed owner names from review texts:")
    for name, count in name_counter.most_common():
        print(f"{name}: {count} occurrences")

if __name__ == '__main__':
    main()
