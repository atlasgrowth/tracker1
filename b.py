import requests
import json
import time
from datetime import datetime

def scrape_and_simplify_reviews():
    # API endpoint and authentication
    api_url = "https://api.apify.com/v2/acts/compass~google-maps-reviews-scraper/run-sync-get-dataset-items"
    token = "apify_api_o7mYRW8cyWa4FtBMQFfhu8rBpfWqVb1AnFwN"

    # Fix and clean place IDs (they were concatenated in the input)
    raw_input = "ChIJJUc7qlIm1IcRx-cCCiI_yP0ChIJvyeTdRotvG8RkmIklJ97REQChIJ-whw30ec1ocRV6TF2A7qwmkChIJH1S2OdEr1IcRXxOY6as7lZgChIJT71U02aC1ocRebpED6PNcWEChIJs7AAYjsp1IcRd1qa1OgBeksChIJlfq9EDop1IcRyLTYZdiMl-kChIJ583lFvgr1IcR9RH9RZkUnxgChIJB-SmCwN91ocRDZkEqljH12cChIJNyZXsmBpW2YRLcv2JrAFnWUChIJjy8EKfM7X6cRjVVNorsmQT0ChIJEzJ4v1mA1ocRaY-rj8LgkBYChIJRYEyeFD-3CgRuU12zJNPrRYChIJFbjK3kEo1IcRtoCLhZFVyI4ChIJ8ygZxqaC1GURwDKLlfobyrMChIJC5JUq2hp1ocR8zmk7hNY6PoChIJgVQfYY9_1ocRLin9D9fv-nEChIJi4da6Vwp1IcR0bX5offer6gChIJ86k1UoPO1YcRfh3x4zkV1eoChIJNfLI22Ap1IcREiWBHhglr44ChIJv3qsZM8MO2gRMMNRgRfAvlsChIJg4gvel8-0YcRp-QbpDeFWWUChIJIawW7VXH1ocR1UrE4k0sKJIChIJPX-L90lBiogR3QgpY7cHZpoChIJYRUpb5Ko1YcRdMcRIX--CDsChIJq99fieBW0YcRMO9dP-NJRkAChIJ3z7lV_BW0YcRonmFlkE1SCIChIJh2MXfjaVZqwR8p8ljb7FEh4ChIJtwAIRs9Z1IcRXNsh3UrjUO8ChIJCTK1eVof1ocR4bXheNQUGlQChIJB-kFGerFNSsRyAHhrpnPYxwChIJ82Ep3z8nq6YRbhwClcPYwMAChIJXWV4VEXv0ocR_8n1NKHfJFUChIJv2MMMNlUzYcRMfKtJcqV2fIChIJ4fjTltLrM4YRCloQzpx1NDgChIJIxGltkcTZYkR1CN3FFW0MAoChIJoV1V4U-lyYcRywnjX7r2w5kChIJMzMR5v770ocRH73Tz3HiFYoChIJYdrmfl0aMoYR5DR1oqIRBGIChIJN5VGPlD_LYYR7Ou8OYLzgowChIJ1QAIfhIYMoYRs05ObsRz8a8ChIJnes2Ye5hMYYR3NO_7GDpDhcChIJ7YwD1rwSnYcRzLVIcA90rh8ChIJJR6S1DgDM4YRZUTM-gAm8EoChIJf896jKtxMoYR_f3QBtorbqAChIJt2CWiD6jLYYRMlcJZFlpdOoChIJjZ5EJsN7LYYR1TJFmYyXxLIChIJ97NraeNgM4YRMjcopSkIr4sChIJrehgvxROzYcR-YCz3kwduQM"

    # Split by "ChIJ" and filter out empty strings
    split_ids = ["ChIJ" + part for part in raw_input.split("ChIJ") if part]

    # Configure the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    all_results = []
    simplified_reviews = []
    batch_size = 3  # Processing in smaller batches to avoid timeouts

    print(f"Found {len(split_ids)} place IDs to process")

    # Process in batches
    for i in range(0, len(split_ids), batch_size):
        batch = split_ids[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1} with {len(batch)} place IDs")

        payload = {
            "placeIds": batch,
            "language": "en",
            "maxReviews": 40,  # Limiting to 40 reviews per place for efficiency
            "includeNonTextReviews": False
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()

            # Add results to our collection
            batch_results = response.json()
            all_results.extend(batch_results)

            print(f"Successfully scraped {len(batch_results)} reviews in this batch")

            # Immediately process this batch to simplified format
            for review in batch_results:
                # Format the date nicely
                try:
                    pub_date = datetime.fromisoformat(review.get('publishedAtDate', '').replace('Z', '+00:00'))
                    formatted_date = pub_date.strftime('%Y-%m-%d')
                except (ValueError, TypeError):
                    formatted_date = review.get('publishAt', 'Unknown date')

                business_name = review.get('title', 'Unknown Business')
                place_id = review.get('placeId', 'Unknown Place ID')

                simplified_review = {
                    "business_name": business_name,
                    "place_id": place_id,
                    "reviewer_name": review.get('name', 'Anonymous'),
                    "text": review.get('text', ''),
                    "date": formatted_date,
                    "stars": review.get('stars', 0)
                }
                simplified_reviews.append(simplified_review)

            # Add a short delay between batches to avoid rate limiting
            if i + batch_size < len(split_ids):
                print("Waiting 5 seconds before next batch...")
                time.sleep(5)

        except requests.exceptions.RequestException as e:
            print(f"Error processing batch: {e}")
            print(f"Continuing with next batch...")
            continue

    # Save both complete and simplified results
    with open('all_google_reviews_complete.json', 'w') as f:
        json.dump(all_results, f, indent=2)

    with open('all_google_reviews_simplified.json', 'w') as f:
        json.dump(simplified_reviews, f, indent=2)

    # Create an organized version by business
    reviews_by_business = {}
    for review in simplified_reviews:
        business_name = review['business_name']
        place_id = review['place_id']
        key = f"{business_name} ({place_id})"

        if key not in reviews_by_business:
            reviews_by_business[key] = []

        # Remove business info from individual reviews to avoid duplication
        review_copy = review.copy()
        del review_copy['business_name']
        del review_copy['place_id']
        reviews_by_business[key].append(review_copy)

    with open('reviews_by_business.json', 'w') as f:
        json.dump(reviews_by_business, f, indent=2)

    print(f"\nScraping and processing complete!")
    print(f"Total reviews collected: {len(all_results)}")
    print(f"Results saved to three files:")
    print(f"1. all_google_reviews_complete.json - Full data")
    print(f"2. all_google_reviews_simplified.json - Simplified format")
    print(f"3. reviews_by_business.json - Organized by business")

    # Show sample of results
    if simplified_reviews:
        print("\nSample of collected reviews:")
        for i, review in enumerate(simplified_reviews[:3]):
            print(f"\nReview {i+1}:")
            print(f"Business: {review['business_name']}")
            print(f"Name: {review['reviewer_name']}")
            print(f"Stars: {review['stars']}")
            print(f"Date: {review['date']}")
            text = review['text']
            print(f"Text: {text[:100]}..." if len(text) > 100 else f"Text: {text}")

    return simplified_reviews

if __name__ == "__main__":
    scrape_and_simplify_reviews()