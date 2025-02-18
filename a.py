import json
import spacy
from collections import OrderedDict, Counter
import sys
import re

# A set of words we want to ignore from the PERSON candidates.
IGNORE_WORDS = {
    "Problem", "AR", "Highly", "Barkley", "Drainpro", "Superb", "Crew",
    "Call", "Likes", "Jack", "hammering", "Plumber", "The", "and", "of"
}

def load_reviews(filename):
    """Load reviews from the JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

def group_reviews_by_place(reviews):
    """
    Group reviews by place_id (or business_name if place_id is missing).
    Use an OrderedDict to preserve the order of first appearance.
    """
    groups = OrderedDict()
    for review in reviews:
        key = review.get("place_id") or review.get("business_name") or "unknown"
        if key not in groups:
            groups[key] = {
                "business_name": review.get("business_name", "unknown"),
                "reviews": []
            }
        groups[key]["reviews"].append(review)
    return groups

def clean_candidate(name):
    """
    Clean up candidate names by stripping extra punctuation and whitespace.
    Also remove if the name matches an ignore word (case-insensitive).
    """
    # Remove extra punctuation from the beginning or end.
    candidate = re.sub(r"^[^\w]+|[^\w]+$", "", name.strip())
    # If candidate (lowercase) is in the ignore list, return None.
    if candidate.lower() in {w.lower() for w in IGNORE_WORDS}:
        return None
    return candidate

def extract_person_names(text, nlp):
    """
    Process text using spaCy and return a list of cleaned PERSON entities.
    """
    doc = nlp(text)
    names = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            candidate = clean_candidate(ent.text)
            if candidate and len(candidate) > 1:
                names.append(candidate)
    return names

def guess_owner_for_group(reviews, nlp, min_frequency=2):
    """
    For a list of reviews (belonging to the same business),
    extract person names from non-empty review texts,
    count frequencies, and return the most common candidate if it appears
    at least min_frequency times. Otherwise, return "No owner found".
    """
    name_counter = Counter()
    for review in reviews:
        text = review.get("text")
        if text and text.strip():
            names = extract_person_names(text, nlp)
            name_counter.update(names)
    if name_counter:
        most_common, count = name_counter.most_common(1)[0]
        # Only return the candidate if it meets the frequency threshold.
        if count >= min_frequency:
            return most_common, dict(name_counter)
    return "No owner found", dict(name_counter)

def main():
    nlp = spacy.load("en_core_web_sm")
    filename = "enhanced_reviews.json"
    reviews = load_reviews(filename)

    groups = group_reviews_by_place(reviews)

    results = []
    for place_id, data in groups.items():
        business = data["business_name"]
        reviews_list = data["reviews"]
        guessed_name, counts = guess_owner_for_group(reviews_list, nlp, min_frequency=2)
        results.append({
            "place_id": place_id,
            "business_name": business,
            "guessed_owner": guessed_name,
            "name_counts": counts
        })

    # Print out the results in original order.
    print("Guessed owner names by place (in original order):")
    for res in results:
        print(f"Place ID: {res['place_id']}")
        print(f"  Business: {res['business_name']}")
        print(f"  Guessed Owner: {res['guessed_owner']}")
        print(f"  Candidate Counts: {res['name_counts']}")
        print("-" * 40)

    # Optionally, save the results to a JSON file for later comparison.
    with open("guessed_owners.json", "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, indent=2)

if __name__ == '__main__':
    main()
