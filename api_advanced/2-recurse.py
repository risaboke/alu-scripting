#!/usr/bin/python3
"""
This recursively gets the titles of all hot posts
of a subreddit using the Reddit API.
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Return a list of titles of all hot posts, or None if invalid."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alu-api-advanced/1.0"}
    params = {"limit": 100, "after": after}

    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    if response.status_code != 200:
        return None

    data = response.json().get("data", {})
    posts = data.get("children", [])

    # make a new list so the default list is not shared between calls
    new_list = hot_list + [post.get("data", {}).get("title")
                           for post in posts]

    next_page = data.get("after")
    if next_page is None:
        return new_list

    return recurse(subreddit, new_list, next_page)
