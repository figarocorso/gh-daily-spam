#!/usr/bin/python

import argparse
import os
import sys
import webbrowser

from github import Github  # pip install PyGithub

REPOS = [
    "draios/frontend",
    "draios/backend",
    "draios/installer",
    "draios/automation",
    "draios/sds-frontend",
    "draios/secure-backend",
    "draios/template-renderer",
]


def get_github_token():
    github_token = os.environ.get("GITHUB_TOKEN", "")
    if not github_token:
        sys.exit("ERROR: You must set GITHUB_TOKEN env var")
    return github_token


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-bb", "--base_branch", required=True, help="Base branch for filtering")
    return parser.parse_args(sys.argv[1:])


if __name__ == "__main__":
    github_token = get_github_token()
    args = get_args()
    for repo in REPOS:
        repo = Github(github_token).get_repo(repo)
        for pr in repo.get_pulls(state='open', sort='created', base=args.base_branch):
            webbrowser.open_new_tab(pr.html_url)
