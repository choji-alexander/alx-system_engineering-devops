mport requests

def top_ten(subreddit):
    # Reddit API endpoint for hot posts in a subreddit
    url = f'https://www.reddit.com/r/{subreddit}/hot.json?limit=10'
    
    # Set a custom User-Agent to avoid Too Many Requests errors
    headers = {'User-Agent': 'my_bot/0.1'}
    
    try:
        # Send GET request to the Reddit API
        response = requests.get(url, headers=headers, allow_redirects=False)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        # Parse the JSON response
        data = response.json()
        
        # Extract and print titles of the first 10 hot posts
        for post in data['data']['children']:
            print(post['data']['title'])
    
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
print(f"Top 10 hot posts in '{subreddit_name}':")
top_ten(subreddit_name)

