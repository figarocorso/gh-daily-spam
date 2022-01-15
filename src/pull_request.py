import webbrowser

APPROVED = "APPROVED"
COMMENT = "COMMENT"


class PullRequest:
    def __init__(self, pr, pr_filter, repo):
        self.pr = pr
        self._full_pr = None
        self.pr_filter = pr_filter
        self.repo = repo

    def __str__(self):
        return f"{self.pr_filter.description}\n\t[{self.pr.number}] {self.pr.title} [{self.pr.user.login}]"

    @property
    def full_pr(self):
        if self._full_pr is None:
            self._full_pr = self.repo.get_pull(self.pr.number)

        return self._full_pr

    @property
    def number(self):
        return self.pr.number

    def open_in_browser(self):
        webbrowser.open_new_tab(self.full_pr.html_url)

    def approve(self, body=""):
        event = APPROVED if self.full_pr.state == "open" else COMMENT
        self._create_review(event, body)

    def comment(self, body=""):
        self._create_review(COMMENT, body)

    def _create_review(self, event, body=""):
        body = body if body else "Quick review, LGTM"
        self.full_pr.create_review(body=body, event=event)
