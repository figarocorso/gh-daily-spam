from src.pull_requests import PullRequests

import os


def main():
    prs = PullRequests()
    while(True):
        os.system("clear")
        prs.retrieve_open_by_team()
        prs.print_prs()
        pr_number = custom_input("\nPR number (0: exit | r: refresh) ")

        if not pr_number:
            pr_number = "1"

        if pr_number == "r":
            continue

        if pr_number == "0":
            exit()

        pr_number = int(pr_number)
        prs.select(pr_number)
        prs.open_selected()
        prs.print_selected()

        should_approve = custom_input("\nShould approve? (Y/n): ")
        should_approve = not should_approve or should_approve != "n"
        prs.approve_selected()


def custom_input(message):
    try:
        return input(message)
    except:
        print("\nBye!\n")
        exit()


if __name__ == "__main__":
    main()
