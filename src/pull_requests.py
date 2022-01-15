from .config import Config
from .filter_methods import FilterMethods
from .pull_request import PullRequest

from github import Github

REPO = "draios/automation"


class PullRequests:

    def __init__(self):
        self.prs = []
        self.config = Config()
        self.repo = Github(self.config.github_token).get_repo(REPO)
        self.filter_methods = FilterMethods(self.repo, self.config)
        self.prs = []
        self.retrieve_all_prs()

    @property
    def number_of_prs_to_be_reviewed(self):
        return len(self.prs)

    def pop_first_pr(self):
        return self.prs.pop(0)

    def retrieve_all_prs(self):
        for pr_filter in self.filter_methods.default_filters:
            print(f"Retrieving: {pr_filter.description}")
            self.add_prs_from_filter(pr_filter)

    def add_prs_from_filter(self, pr_filter):
        prs = getattr(self.filter_methods, pr_filter.method)()
        for pr in prs:
            if pr.number not in [pull_request.number for pull_request in self.prs]:
                self.prs.append(PullRequest(pr, pr_filter, self.repo))
