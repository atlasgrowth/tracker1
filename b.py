import requests
import json
import time
from datetime import datetime

def scrape_all_reviews():
    # API endpoint and authentication
    api_url = "https://api.apify.com/v2/acts/compass~google-maps-reviews-scraper/run-sync-get-dataset-items"
    token = "apify_api_o7mYRW8cyWa4FtBMQFfhu8rBpfWqVb1AnFwN"

    # Load place IDs from file
    try:
        with open('place_ids.txt', 'r') as f:
            place_ids = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: place_ids.txt not found")
        return

    # Configure the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    all_results = []
    batch_size = 5  # Process in smaller batches

    print(f"Found {len(place_ids)} place IDs to process")

    # Process in batches
    for i in range(0, len(place_ids), batch_size):
        batch = place_ids[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1} with {len(batch)} place IDs")

        payload = {
            "placeIds": batch,
            "language": "en",
            "maxReviews": 20,
            "includeNonTextReviews": False
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            batch_results = response.json()
            all_results.extend(batch_results)

            print(f"Successfully scraped {len(batch_results)} reviews in this batch")

            if i + batch_size < len(place_ids):
                print("Waiting 5 seconds before next batch...")
                time.sleep(5)

        except requests.exceptions.RequestException as e:
            print(f"Error processing batch: {e}")
            continue

    # Save results
    if all_results:
        with open('all_google_reviews.json', 'w') as f:
            json.dump(all_results, f, indent=2)
        print("\nScraping complete!")
        print(f"Total reviews collected: {len(all_results)}")
        print("Results saved to all_google_reviews.json\n")

        # Show sample
        print("Sample of collected reviews:\n")
        if all_results:
            print("Review 1:")
            print(f"Place ID: {all_results[0].get('placeId', 'N/A')}")
            print(f"Rating: {all_results[0].get('stars', 'N/A')}\n")

if __name__ == "__main__":
    scrape_all_reviews()