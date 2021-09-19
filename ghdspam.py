from github import Github
from invoke import Context

import json


CONFIG_FILE = "config.json"
REPO = "draios/automation"

invoke = Context()

config = json.loads(invoke.run(f"AWS_PROFILE=figarocorso sops -d {CONFIG_FILE} | jq -c",
                               hide=True, warn=True, echo=False).stdout)
gh = Github(config["github_token"])
repo = gh.get_repo(REPO)
for pr in repo.get_pulls(state='open', sort='created', base='staging'):
    print(pr.title)
