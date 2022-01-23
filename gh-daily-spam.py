from src.pull_requests import PullRequests
from src.pr_user_interaction import PrUserInteraction

from rich.console import Console

import os

console = Console()


def main():
    prs = PullRequests()
    while prs.number_of_prs_to_be_reviewed:
        os.system("clear")
        print_pending_prs_message(prs)
        PrUserInteraction(prs.pop_first_pr()).operate_with_pr()


def print_pending_prs_message(pending_reviews_list):
    message = "[bold green]You still need to review[/bold green]"
    message += f" [underline bold green]{pending_reviews_list.number_of_prs_to_be_reviewed}[/underline bold green]"
    message += f" [green bold]PRs[/green bold]\n"
    console.print(message)


if __name__ == "__main__":
    main()
