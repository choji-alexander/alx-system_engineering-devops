mport requests

def number_of_subscribers(subreddit):
    # Reddit API endpoint for subreddit information
    url = f'https://www.reddit.com/r/{subreddit}/about.json'
    
    # Set a custom User-Agent to avoid Too Many Requests errors
    headers = {'User-Agent': 'my_bot/0.1'}
    
    try:
        # Send GET request to the Reddit API
        response = requests.get(url, headers=headers, allow_redirects=False)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        # Parse the JSON response
        data = response.json()
        
        # Extract the number of subscribers from the response
        subscribers_count = data['data']['subscribers']
        
        return subscribers_count
    
    except requests.exceptions.HTTPError as errh:
        # Handle HTTP errors (4xx or 5xx)
        print(f"HTTP Error: {errh}")
        return 0
    
    except requests.exceptions.RequestException as err:
        # Handle other request exceptions
        print(f"Request Exception: {err}")
        return 0

# Example usage:
subreddit_name = 'python'
subscribers = number_of_subscribers(subreddit_name)

if subscribers != 0:
    print(f"The subreddit '{subreddit_name}' has {subscribers} subscribers.")
else:
    print(f"Invalid subreddit: '{subreddit_name}'.")

