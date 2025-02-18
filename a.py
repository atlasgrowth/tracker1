
import json
import spacy
from collections import Counter, OrderedDict

def main():
    try:
        # Load the spaCy English model
        nlp = spacy.load("en_core_web_sm")
        
        # Get original place IDs order from raw input
        raw_input = "ChIJJUc7qlIm1IcRx-cCCiI_yP0ChIJvyeTdRotvG8RkmIklJ97REQChIJ-whw30ec1ocRV6TF2A7qwmkChIJH1S2OdEr1IcRXxOY6as7lZgChIJT71U02aC1ocRebpED6PNcWEChIJs7AAYjsp1IcRd1qa1OgBeksChIJlfq9EDop1IcRyLTYZdiMl-kChIJ583lFvgr1IcR9RH9RZkUnxgChIJB-SmCwN91ocRDZkEqljH12cChIJNyZXsmBpW2YRLcv2JrAFnWUChIJjy8EKfM7X6cRjVVNorsmQT0ChIJEzJ4v1mA1ocRaY-rj8LgkBYChIJRYEyeFD-3CgRuU12zJNPrRYChIJFbjK3kEo1IcRtoCLhZFVyI4ChIJ8ygZxqaC1GURwDKLlfobyrMChIJC5JUq2hp1ocR8zmk7hNY6PoChIJgVQfYY9_1ocRLin9D9fv-nEChIJi4da6Vwp1IcR0bX5offer6gChIJ86k1UoPO1YcRfh3x4zkV1eoChIJNfLI22Ap1IcREiWBHhglr44ChIJv3qsZM8MO2gRMMNRgRfAvlsChIJg4gvel8-0YcRp-QbpDeFWWUChIJIawW7VXH1ocR1UrE4k0sKJIChIJPX-L90lBiogR3QgpY7cHZpoChIJYRUpb5Ko1YcRdMcRIX--CDsChIJq99fieBW0YcRMO9dP-NJRkAChIJ3z7lV_BW0YcRonmFlkE1SCIChIJh2MXfjaVZqwR8p8ljb7FEh4ChIJtwAIRs9Z1IcRXNsh3UrjUO8ChIJCTK1eVof1ocR4bXheNQUGlQChIJB-kFGerFNSsRyAHhrpnPYxwChIJ82Ep3z8nq6YRbhwClcPYwMAChIJXWV4VEXv0ocR_8n1NKHfJFUChIJv2MMMNlUzYcRMfKtJcqV2fIChIJ4fjTltLrM4YRCloQzpx1NDgChIJIxGltkcTZYkR1CN3FFW0MAoChIJoV1V4U-lyYcRywnjX7r2w5kChIJMzMR5v770ocRH73Tz3HiFYoChIJYdrmfl0aMoYR5DR1oqIRBGIChIJN5VGPlD_LYYR7Ou8OYLzgowChIJ1QAIfhIYMoYRs05ObsRz8a8ChIJnes2Ye5hMYYR3NO_7GDpDhcChIJ7YwD1rwSnYcRzLVIcA90rh8ChIJJR6S1DgDM4YRZUTM-gAm8EoChIJf896jKtxMoYR_f3QBtorbqAChIJt2CWiD6jLYYRMlcJZFlpdOoChIJjZ5EJsN7LYYR1TJFmYyXxLIChIJ97NraeNgM4YRMjcopSkIr4sChIJrehgvxROzYcR-YCz3kwduQM"
        place_ids = ["ChIJ" + part for part in raw_input.split("ChIJ") if part]

        # Load reviews from the JSON file
        with open("reviews_by_business.json", "r", encoding="utf-8") as f:
            reviews_data = json.load(f)

        # Create ordered dictionary to store results in input order
        ordered_reviews = OrderedDict()
        
        # First populate with "None" for all place IDs
        for place_id in place_ids:
            ordered_reviews[place_id] = None
            
        # Then fill in actual reviews where they exist
        for business_key, reviews in reviews_data.items():
            place_id = business_key.split("(")[1].rstrip(")")  # Extract place ID from key
            if place_id in ordered_reviews:
                ordered_reviews[place_id] = reviews
            
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

        # Print results in order
        print("\nReviews by place ID in original input order:")
        for place_id, reviews in ordered_reviews.items():
            print(f"\nPlace ID: {place_id}")
            if reviews is None:
                print("None - No reviews found for this place ID")
            else:
                print(f"Found {len(reviews)} reviews:")
                for review in reviews[:3]:  # Show first 3 reviews as sample
                    print(f"- {review.get('reviewer_name', 'Anonymous')}: {review.get('stars', 0)} stars")

    except FileNotFoundError:
        print("Error: reviews_by_business.json file not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in reviews_by_business.json")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
