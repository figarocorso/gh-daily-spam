from .config import Config

from github import Github

import webbrowser

REPO = "draios/automation"
ME = "figarocorso"
APPROVED = "APPROVED"
COMMENT = "COMMENT"


class PullRequests:
    filters = [
        {"method": "retrieve_open_by_team", "description": "Opened PRs by team not yet reviewed"},
        {"method": "retrieve_closed_by_team", "description": "Closed PRs by team not yet reviewed"},
        {"method": "retrieve_open_at_onprem", "description": "Opened PRs at onprem folder not yet reviewed"},
        {
            "method": "retrieve_closed_at_onprem",
            "description": "Closed PRs at onprem folder not yet reviewed"
        },
        {
            "method": "retrieve_open_at_jenkins",
            "description": "Opened PRs at jenkins folder not yet reviewed"
        },
    ]

    def __init__(self):
        self.prs = []
        self.selected_number = None
        self.current_filter = 0
        self.config = Config()
        self.repo = Github(self.config.github_token).get_repo(REPO)

    def print_prs(self):
        while not self.prs and self.current_filter < len(self.filters):
            print(f"Retrieving: {self.filters[self.current_filter]['description']}")
            getattr(self, self.filters[self.current_filter]["method"])()
            if not self.prs:
                self.current_filter += 1

            if not self.prs:
                print("Job is over")
                print("Bye!")
                exit()

            for index, pr in enumerate(self.prs):
                print(f"[{index + 1}] {pr.title} [{pr.user.login}]")

    def retrieve_open_by_team(self):
        self.prs = [pr for pr in self.repo.get_pulls(state='open', sort='created', base='staging')
                    if pr.user.login in self.config.team and self.pending_review(pr)]

    def retrieve_closed_by_team(self):
        self.prs = [pr for pr in self.repo.get_pulls(state="closed", sort="created", direction="desc",
                                                     base="staging").get_page(0)
                    if pr.user.login in self.config.team and self.pending_review(pr)]

    def retrieve_open_at_onprem(self):
        self.prs = [pr for pr in self.repo.get_pulls(state='open', sort='created', base='staging')
                    if "onprem" in [label.name for label in pr.labels] and self.pending_review(pr)]

    def retrieve_closed_at_onprem(self):
        self.prs = [pr for pr in self.repo.get_pulls(state="closed", sort="created", direction="desc",
                                                     base="staging").get_page(0)
                    if "onprem" in [label.name for label in pr.labels] and self.pending_review(pr)]

    def retrieve_open_at_jenkins(self):
        self.prs = [pr for pr in self.repo.get_pulls(state='open', sort='created', base='staging')
                    if "jenkins" in [label.name for label in pr.labels] and self.pending_review(pr)]

    def pending_review(self, pr):
        for review in reversed([review for review in pr.get_reviews()]):
            if review.user.login == ME:
                return False
        return True

    def select_pr(self, position):
        self.selected_number = position - 1

    @property
    def selected_pr(self):
        if self.selected_number is None:
            raise "Ooops! There was no selected PR"

        return self.prs[self.selected_number]

    def print_selected(self):
        pr = self.selected_pr
        print(f"\n[{pr.number}] {pr.title} [{pr.user.login}]")

    def open_selected(self):
        webbrowser.open_new_tab(self.repo.get_pull(self.selected_pr.number).html_url)

    def approve_selected(self):
        pull = self.repo.get_pull(self.selected_pr.number)
        event = COMMENT if pull.state == "open" else APPROVED
        body = "" if pull.state == "open" else "Just passing by, LGTM"
        pull.create_review(body=body, event=event)
