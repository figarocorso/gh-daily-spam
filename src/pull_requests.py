from .config import Config

from github import Github

import webbrowser

REPO = "draios/automation"
ME = "figarocorso"
APPROVED = "APPROVED"


class PullRequests:
    def __init__(self):
        self.prs = []
        self.selected_number = None
        self.config = Config()
        self.repo = Github(self.config.github_token).get_repo(REPO)

    def retrieve_open_by_team(self):
        self.prs = [pr for pr in self.repo.get_pulls(state='open', sort='created', base='staging')
                    # if True]
                    if pr.user.login in self.config.team and not self.is_already_reviewed(pr)]

    def is_already_reviewed(self, pr):
        for review in reversed([review for review in pr.get_reviews()]):
            if review.user.login == ME and review.state == APPROVED:
                return True
        return False

    def select(self, position):
        self.selected_number = position - 1

    @property
    def selected_pr(self):
        if self.selected_number is None:
            raise "Ooops! There was no selected PR"

        return self.prs[self.selected_number]

    def add(self, pr):
        self.prs.append(pr)

    def print_prs(self):
        if not self.prs:
            print("There are no PRs matching your filter")

        for index, pr in enumerate(self.prs):
            print(f"[{index + 1}] {pr.title} [{pr.user.login}]")

    def print_selected(self):
        pr = self.selected_pr
        print(f"\n[{pr.number}] {pr.title} [{pr.user.login}]")

    def open_selected(self):
        webbrowser.open_new_tab(self.repo.get_pull(self.selected_pr.number).html_url)

    def approve_selected(self):
        pull = self.repo.get_pull(self.selected_pr.number)
        event = "COMMENT" if pull.state == "open" else "APPROVE"
        body = ":+1:" if pull.state == "open" else "LGTM"
        pull.create_review(body=body, event=event)
