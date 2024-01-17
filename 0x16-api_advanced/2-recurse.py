mport requests

def recurse(subreddit, hot_list=None, after=None):
    # Initialize the hot_list on the first call
    if hot_list is None:
        hot_list = []

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

        # Extract and append titles of the current page to the hot_list
        hot_list.extend([post['data']['title'] for post in data['data']['children']])

        # Recursively call the function with the 'after' parameter for the next page
        if data['data']['after']:
            recurse(subreddit, hot_list, after=data['data']['after'])
        else:
            return hot_list

    except requests.exceptions.HTTPError as errh:
        # Handle HTTP errors (4xx or 5xx)
        print(f"HTTP Error: {errh}")
        return None

    except requests.exceptions.RequestException as err:
        # Handle other request exceptions
        print(f"Request Exception: {err}")
        return None

# Example usage:
subreddit_name = 'python'
result = recurse(subreddit_name)

if result is not None:
    print(f"Titles of all hot articles in '{subreddit_name}':")
    for title in result:
        print(title)
else:
    print("Invalid subreddit or no results found.")

