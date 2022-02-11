from .filter import Filter


class FilterMethods:
    def __init__(self, repo, config):
        self.repo = repo
        self.config = config
        self._open_prs = None
        self._closed_prs = None

    @property
    def open_prs(self):
        if self._open_prs is None:
            self._open_prs = self.repo.get_pulls(state='open', sort='created', base='staging')
        return self._open_prs

    @property
    def closed_prs(self):
        if self._closed_prs is None:
            self._closed_prs = self.repo.get_pulls(state="closed", sort="created", direction="desc",
                                                   base="staging").get_page(0)
        return self._closed_prs

    @property
    def default_filters(self):
        return [
            Filter("retrieve_open_by_team", "Opened PRs by team not yet reviewed"),
            Filter("retrieve_merged_by_team", "Closed PRs by team not yet reviewed"),
            Filter("retrieve_open_at_onprem", "Opened PRs at onprem folder not yet reviewed"),
            Filter("retrieve_merged_at_onprem", "Closed PRs at onprem folder not yet reviewed"),
            Filter("retrieve_open_at_jenkins", "Opened PRs at jenkins folder not yet reviewed"),
        ]

    def retrieve_open_by_team(self):
        return [pr for pr in self.open_prs
                if pr.user.login in self.config.team and self.pending_review(pr)]

    def retrieve_merged_by_team(self):
        return [pr for pr in self.closed_prs
                if pr.user.login in self.config.team and self.pending_review(pr) and pr.merged]

    def retrieve_open_at_onprem(self):
        return [pr for pr in self.open_prs
                if "onprem" in [label.name for label in pr.labels] and self.pending_review(pr)
                and not self.author_is_me(pr)]

    def retrieve_merged_at_onprem(self):
        return [pr for pr in self.closed_prs
                if "onprem" in [label.name for label in pr.labels] and self.pending_review(pr)
                and not self.author_is_me(pr) and pr.merged]

    def retrieve_open_at_jenkins(self):
        return [pr for pr in self.open_prs
                if "jenkins" in [label.name for label in pr.labels] and self.pending_review(pr)
                and not self.author_is_me(pr)]

    def pending_review(self, pr):
        for review in reversed([review for review in pr.get_reviews()]):
            if review.user.login == self.config.me:
                return False
        return True

    def author_is_me(self, pr):
        return pr.user.login == self.config.me
