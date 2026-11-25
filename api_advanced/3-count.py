#!/usr/bin/python3
"""
This recursively counts given keywords in the titles
of all hot posts of a subreddit using the Reddit API.
"""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Print a sorted count of the keywords found in hot post titles."""
    if counts is None:
        counts = {}
        for word in word_list:
            counts[word.lower()] = 0

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alu-api-advanced/1.0"}
    params = {"limit": 100, "after": after}

    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json().get("data", {})
    posts = data.get("children", [])

    for post in posts:
        title = post.get("data", {}).get("title", "")
        for title_word in title.lower().split():
            if title_word in counts:
                counts[title_word] += 1

    next_page = data.get("after")
    if next_page is not None:
        count_words(subreddit, word_list, next_page, counts)
        return

    lower_words = [word.lower() for word in word_list]
    results = {}
    for word in counts:
        total = counts[word] * lower_words.count(word)
        if total > 0:
            results[word] = total

    sorted_results = sorted(results.items(), key=lambda x: (-x[1], x[0]))
    for word, total in sorted_results:
        print("{}: {}".format(word, total))
