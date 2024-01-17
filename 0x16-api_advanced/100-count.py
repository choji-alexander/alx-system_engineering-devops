mport requests
from collections import Counter

def count_words(subreddit, word_list, after=None, counts=None):
    # Initialize the counts and subreddit name on the first call
    if counts is None:
        counts = Counter()
        subreddit_name = subreddit.lower()

    # Reddit API endpoint for hot posts in a subreddit
    url = f'https://www.reddit.com/r/{subreddit}/hot.json?limit=100&after={after}' if after else f'https://www.reddit.com/r/{subreddit}/hot.json?limit=100'

    # Set a custom User-Agent to avoid Too Many Requests errors
    headers = {'User-Agent': 'my_bot/0.1'}

    try:
        # Send GET request to the Reddit API
        response = requests.get(url, headers=headers, allow_redirects=False)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Parse the JSON response
        data = response.json()

        # Extract and count keywords in the titles of the current page
        for post in data['data']['children']:
            title = post['data']['title'].lower()
            for word in word_list:
                if word.lower() in title:
                    counts[word.lower()] += 1

        # Recursively call the function with the 'after' parameter for the next page
        if data['data']['after']:
            count_words(subreddit, word_list, after=data['data']['after'], counts=counts)
        else:
            # Print the results in descending order by count and alphabetically by word
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")

    except requests.exceptions.HTTPError as errh:
        # Handle HTTP errors (4xx or 5xx)
        print(f"HTTP Error: {errh}")

    except requests.exceptions.RequestException as err:
        # Handle other request exceptions
        print(f"Request Exception: {err}")

# Example usage:
subreddit_name = 'python'
keywords = ['python', 'java', 'javascript']
count_words(subreddit_name, keywords)

