import json

CONFIG_FILE = "config.json"


class Config:
    def __init__(self):
        self.config = {}
        with open(CONFIG_FILE, "r") as f:
            self.config = json.load(f)

    @property
    def github_token(self):
        return self.config.get("github_token")

    @property
    def team(self):
        return self.config.get("team")

    @property
    def me(self):
        return self.config.get("me")

    @property
    def default_open_pr_message(self):
        return self.config.get("messages").get("open_pr")

    @property
    def default_closed_pr_message(self):
        return self.config.get("messages").get("closed_pr")
