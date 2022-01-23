from src.pull_requests import PullRequests

from rich.console import Console

import os

console = Console()


class PrUserInteraction:

    def __init__(self, pr):
        self.pr = pr

    def operate_with_pr(self):
        self.print_pr()
        opened = self.open_in_browser_workflow()
        if not opened:
            return
        self.approve_workflow()

    def print_pr(self):
        console.print(str(self.pr))

    def open_in_browser_workflow(self):
        should_open = self.custom_input("\n[bold]Should open in browser? [reverse](Y/n)[/reverse]:[/bold] ")
        should_open = not should_open or should_open.lower() == "y"
        if should_open:
            self.pr.open_in_browser()
        return should_open

    def approve_workflow(self):
        action = self.custom_input("\n[bold](A)pprove/(C)omment/(S)kip? [reverse](A/c/s)[/reverse]:[/bold] ")
        action = action.lower() if action else "a"

        if action == "s":
            return

        if action == "c":
            message = self.custom_input("\n[bold]Type custom message:[/bold] ")
            self.pr.comment(message)
            return

        if action == "a":
            should_custom_message = self.custom_input("\n[bold]Do you want custom message [reverse](y/N)[/reverse]:[/bold] ")
            should_custom_message = should_custom_message and should_custom_message.lower() == "y"
            message = self.custom_input("\n[bold]Type custom message:[/bold] ") if should_custom_message else ""
            self.pr.approve(message)

    @classmethod
    def custom_input(cls, message):
        try:
            return console.input(message)
        except:  # noqa
            console.print("\n\n[bold red]Bye![/bold red]\n")
            exit()
