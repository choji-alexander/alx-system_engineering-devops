#!/usr/bin/python3
"""Function to count words in all hot posts of a given Reddit subreddit."""
import requests
from collections import Counter

def is_valid_keyword(word):
  """Checks if a word is a valid keyword for counting (avoids special characters)."""
  return word.isalnum() and len(word) > 1

def clean_word(word):
  """Cleans a word by converting it to lowercase and removing special characters."""
  return word.lower().strip("._!")

def parse_titles(subreddit, word_list, after=None, word_counts=None):
  """Recursively parses titles and updates word counts.

  Args:
      subreddit: The subreddit to query.
      word_list: The list of keywords to count.
      after: The 'after' parameter for pagination (optional).
      word_counts: A dictionary to store word counts (optional, used for recursion).

  Returns:
      A dictionary containing the final word counts or None if no posts match.
  """

  # Base case: No more posts to retrieve
  if not after:
    return word_counts

  # Base URL for hot posts
  url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"

  # Add 'after' parameter if provided
  if after:
    url += f"&after={after}"

  # Set a custom User-Agent header to avoid throttling
  headers = {"User-Agent": "MyCoolScript/0.0.1"}

  try:
    # Send GET request without following redirects
    response = requests.get(url, allow_redirects=False, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    # Parse JSON response
    data = response.json()

    # Check for valid subreddit data (presence of 'data' key)
    if not ('data' in data and data['data']):
      return None  # No data for subreddit

    # Extract after parameter for next iteration (if available)
    after = data['data'].get('after')

    # Initialize word counts if not provided
    if not word_counts:
      word_counts = Counter()

    # Parse titles and update word counts
    for post in data['data']['children']:
      title = post['data']['title'].lower()
      for word in word_list:
        clean_word_parts = clean_word(word).split()
        for part in clean_word_parts:
          if is_valid_keyword(part) and part in title:
            word_counts[part] += 1

    # Recursively call the function with the next page (if available)
    return parse_titles(subreddit, word_list, after, word_counts)

  except requests.exceptions.RequestException:
    return None  # Handle request errors

def count_words(subreddit, word_list):
  """Calls the recursive function and prints sorted word counts.

  Args:
      subreddit: The subreddit to query.
      word_list: The list of keywords to count.
  """

  # Clean and filter the word list
  cleaned_words = [clean_word(word) for word in word_list if is_valid_keyword(word)]

  # Start the recursive call
  word_counts = parse_titles(subreddit, cleaned_words)

  # Print results if word counts exist
  if word_counts:
    for word, count in sorted(word_counts.items(), reverse=True):
      print(f"{word}: {count}")
  else:
    print(None)

# Example usage (assuming 100-main.py exists in the same directory)
if __name__ == '__main__':
  import sys

  if len(sys.argv) < 3:
    print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
    print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
  else:
    count_words(sys.argv[1], [x for x in sys.argv[2].split()])

