#!/usr/bin/python3
"""Queries the Reddit API and
returns the number of subscribers
(not active users, total subscribers)
for a given subreddit.

If an invalid subreddit is given,
the function should return 0.
"""
import requests

def number_of_subscribers(subreddit):
  """Queries the Reddit API for the number of subscribers of a subreddit.

  Args:
      subreddit: The name of the subreddit to query.

  Returns:
      The number of subscribers for the subreddit, or 0 if the subreddit is invalid.
  """

  # Base URL for subreddit information
  url = f"https://www.reddit.com/r/{subreddit}/about.json?limit=0"

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
      return data['data']['subscribers']
    else:
      return 0

  except requests.exceptions.RequestException:
    # Handle any request errors (e.g., network issues)
    return 0

# Example usage (assuming 0-main.py exists in the same directory)
if __name__ == "__main__":
  import sys

  if len(sys.argv) < 2:
    print("Please pass an argument for the subreddit to search.")
  else:
    subreddit = sys.argv[1]
    subscribers = number_of_subscribers(subreddit)
    print(f"{subreddit}: {subscribers}")
