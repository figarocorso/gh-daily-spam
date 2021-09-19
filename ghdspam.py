from github import Github
from invoke import Context

import json
import os
import webbrowser


CONFIG_FILE = "config.json"
REPO = "draios/automation"

invoke = Context()

config = json.loads(invoke.run(f"AWS_PROFILE=figarocorso sops -d {CONFIG_FILE} | jq -c",
                               hide=True, warn=True, echo=False).stdout)
gh = Github(config["github_token"])
repo = gh.get_repo(REPO)
while(True):
    os.system("clear")
    for pr in repo.get_pulls(state='open', sort='created', base='staging'):
        if pr.user.login in config["team"]:
            print(f"[{pr.number}] {pr.title} [{pr.user.login}]")
    pr_number = int(input("\nPR number: "))
    webbrowser.open_new_tab(repo.get_pull(pr_number).html_url)
