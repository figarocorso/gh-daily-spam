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

# print("\n".join([f"{x.created_at} - {x.title}" for x in repo.get_pulls(state="closed", sort="created", direction="desc", base="staging").get_page(0)]))
class PullRequests:
    def __init__(self):
        self.prs = []
        self.repo = Github(config["github_token"]).get_repo(REPO)

    def retrieve_open_by_team(self):
        self.prs = [pr for pr in self.repo.get_pulls(state='open', sort='created', base='staging')
                    if True] #pr.user.login in config["team"] and not self.is_already_reviewed(pr)]

    def is_already_reviewed(self, pr):
        for review in reversed([review for review in pr.get_reviews()]):
            if review.user.login == ME:
                return review.state == APPROVED
        return False

    def add(self, pr):
        self.prs.append(pr)

    def print(self):
        if not self.prs:
            print("There are no PRs matching your filter")

        for index, pr in enumerate(self.prs):
            print(f"[{index + 1}] {pr.title} [{pr.user.login}]")

    def open(self, pr_number):
        webbrowser.open_new_tab(self.repo.get_pull(self.prs[pr_number -1].number).html_url)


def main():
    prs = PullRequests()
    while(True):
        os.system("clear")
        prs.retrieve_open_by_team()
        prs.print()
        pr_number = custom_input("\nPR number (0: exit | r: refresh) ")

        if not pr_number:
            pr_number = "1"

        if pr_number == "r":
            continue

        if pr_number == "0":
            exit()

        pr_number = int(pr_number)
        prs.open(pr_number)


def custom_input(message):
    try:
        return input(message)
    except KeyboardInterrupt:
        print("\nBye!\n")
        exit()


if __name__ == "__main__":
    main()
