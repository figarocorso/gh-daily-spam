from .filter import Filter


class FilterMethods:
    def __init__(self, repo, config):
        self.repo = repo
        self.config = config

    @property
    def default_filters(self):
        return [
            Filter("retrieve_open_by_team", "Opened PRs by team not yet reviewed"),
            Filter("retrieve_closed_by_team", "Closed PRs by team not yet reviewed"),
            Filter("retrieve_open_at_onprem", "Opened PRs at onprem folder not yet reviewed"),
            Filter("retrieve_closed_at_onprem", "Closed PRs at onprem folder not yet reviewed"),
            Filter("retrieve_open_at_jenkins", "Opened PRs at jenkins folder not yet reviewed"),
        ]

    def retrieve_open_by_team(self):
        return [pr for pr in self.repo.get_pulls(state='open', sort='created', base='staging')
                    if pr.user.login in self.config.team and self.pending_review(pr)]

    def retrieve_closed_by_team(self):
        return [pr for pr in self.repo.get_pulls(state="closed", sort="created", direction="desc",
                                                     base="staging").get_page(0)
                    if pr.user.login in self.config.team and self.pending_review(pr)]

    def retrieve_open_at_onprem(self):
        return [pr for pr in self.repo.get_pulls(state='open', sort='created', base='staging')
                    if "onprem" in [label.name for label in pr.labels] and self.pending_review(pr)]

    def retrieve_closed_at_onprem(self):
        return [pr for pr in self.repo.get_pulls(state="closed", sort="created", direction="desc",
                                                     base="staging").get_page(0)
                    if "onprem" in [label.name for label in pr.labels] and self.pending_review(pr)]

    def retrieve_open_at_jenkins(self):
        return [pr for pr in self.repo.get_pulls(state='open', sort='created', base='staging')
                    if "jenkins" in [label.name for label in pr.labels] and self.pending_review(pr)]

    def pending_review(self, pr):
        for review in reversed([review for review in pr.get_reviews()]):
            if review.user.login == self.config.me:
                return False
        return True
