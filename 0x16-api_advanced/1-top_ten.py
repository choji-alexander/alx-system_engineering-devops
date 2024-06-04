#!/usr/bin/python3
"""Queries the Reddit API and
prints the titles of the first
10 hot posts listed for a given
subreddit.
"""
import requests

def top_ten(subreddit):
  """Prints the titles of the top 10 hot posts from a subreddit.

  Args:
      subreddit: The name of the subreddit to query.
  """

  # Base URL for hot posts
  url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

  # Set a custom User-Agent header to avoid throttling
  headers = {"User-Agent": "MyCoolScript/0.0.1"}

  try:
    # Send GET request without following redirects
    response = requests.get(url, allow_redirects=False, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    # Parse JSON response
    data = response.json()

    # Check for valid subreddit data (presence of 'data' key)
    if 'data' in data and data['data']:
      posts = data['data']['children']
      for post in posts:
        print(post['data']['title'])
    else:
      print(None)

  except requests.exceptions.RequestException:
    # Handle any request errors (e.g., network issues)
    print(None)

# Example usage (assuming 1-main.py exists in the same directory)
if __name__ == "__main__":
  import sys

  if len(sys.argv) < 2:
    print("Please pass an argument for the subreddit to search.")
  else:
    top_ten(sys.argv[1])
