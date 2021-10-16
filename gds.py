from github import Github

import json
import os
import webbrowser


CONFIG_FILE = "config.json"
REPO = "draios/automation"
ME = "figarocorso"
APPROVED = "APPROVED"

config = {}
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)


def main():
    repo = Github(config["github_token"]).get_repo(REPO)
    while(True):
        os.system("clear")
        for pr in repo.get_pulls(state='open', sort='created', base='staging'):
            if pr.user.login in config["team"] and not is_already_reviewed(pr):
                print(f"[{pr.number}] {pr.title} [{pr.user.login}]")
        pr_number = int(input("\nPR number: "))
        webbrowser.open_new_tab(repo.get_pull(pr_number).html_url)


def is_already_reviewed(pr):
    for review in reversed([review for review in pr.get_reviews()]):
        if review.user.login == ME:
            return review.state == APPROVED
    return False


if __name__ == "__main__":
    main()
