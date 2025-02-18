
import json
import spacy
from collections import Counter

def main():
    try:
        # Load the spaCy English model
        nlp = spacy.load("en_core_web_sm")
        
        # Load reviews from the JSON file
        with open("reviews_by_business.json", "r", encoding="utf-8") as f:
            reviews_data = json.load(f)
            
        name_counter = Counter()
        
        # Iterate through the business reviews
        for business_name, reviews in reviews_data.items():
            for review in reviews:
                text = review.get("text", "")
                if text:
                    doc = nlp(text)
                    for ent in doc.ents:
                        if ent.label_ == "PERSON":
                            name = ent.text.strip()
                            if len(name) > 1 and name.replace("'", "").isalpha():
                                name_counter[name] += 1

        # Print results
        print("\nGuessed owner names from review texts:")
        for name, count in name_counter.most_common():
            print(f"{name}: {count} occurrences")

    except FileNotFoundError:
        print("Error: reviews_by_business.json file not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in reviews_by_business.json")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
