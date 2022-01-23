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
        should_open = self.custom_input("Should open in browser?", "(Y/n)")
        should_open = not should_open or should_open.lower() == "y"
        if should_open:
            self.pr.open_in_browser()
        return should_open

    def approve_workflow(self):
        action = self.custom_input("(A)pprove/(C)omment/(S)kip?", "(A/c/s)")
        action = action.lower() if action else "a"

        if action == "s":
            return

        if action == "c":
            message = self.custom_input("Type custom message:")
            self.pr.comment(message)
            return

        if action == "a":
            should_custom_message = self.custom_input("Do you want custom message?", "(y/N)")
            should_custom_message = should_custom_message and should_custom_message.lower() == "y"
            message = self.custom_input("Type custom message:") if should_custom_message else ""
            self.pr.approve(message)

    @classmethod
    def custom_input(cls, message, options_message=""):
        space = " " if options_message else ""
        try:
            return console.input(f"\n[bold]{message} [reverse]{options_message}[/reverse][/bold]{space}")
        except:  # noqa
            console.print("\n\n[bold red]Bye![/bold red]\n")
            exit()
