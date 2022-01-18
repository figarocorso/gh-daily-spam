from src.pull_requests import PullRequests

from rich.console import Console

import os

console = Console()


def main():
    prs = PullRequests()
    while prs.number_of_prs_to_be_reviewed:
        os.system("clear")
        message = "[bold green]You still need to review[/bold green]"
        message += f" [underline bold green]{prs.number_of_prs_to_be_reviewed}[/underline bold green]"
        message += f" [green bold]PRs[/green bold]\n"
        console.print(message)
        pr = prs.pop_first_pr()
        operate_with_pr(pr)


def operate_with_pr(pr):
    console.print(str(pr))
    opened = open_in_browser_workflow(pr)
    if not opened:
        return
    approve_workflow(pr)


def open_in_browser_workflow(pr):
    should_open = custom_input("\n[bold]Should open in browser? [reverse](Y/n)[/reverse]:[/bold] ")
    should_open = not should_open or should_open.lower() == "y"
    if should_open:
        pr.open_in_browser()
    return should_open


def approve_workflow(pr):
    action = custom_input("\n[bold](A)pprove/(C)omment/(S)kip? [reverse](A/c/s)[/reverse]:[/bold] ")
    action = action.lower() if action else "a"

    if action == "s":
        return

    if action == "c":
        message = custom_input("\n[bold]Type custom message:[/bold] ")
        pr.comment(message)
        return

    if action == "a":
        should_custom_message = custom_input("\n[bold]Do you want custom message [reverse](y/N)[/reverse]:[/bold] ")
        should_custom_message = should_custom_message and should_custom_message.lower() == "y"
        message = custom_input("\n[bold]Type custom message:[/bold] ") if should_custom_message else ""
        pr.approve(message)


def custom_input(message):
    try:
        return console.input(message)
    except:  # noqa
        console.print("\n[bold red]Bye![/bold red]\n")
        exit()


if __name__ == "__main__":
    main()
