from src.pull_requests import PullRequests

import os


def main():
    prs = PullRequests()
    while(True):
        os.system("clear")

        prs.print_prs()

        pr_number = get_pr_number_from_user()
        if pr_number == "0":
            continue

        operate_with_pr(prs, pr_number)


def get_pr_number_from_user():
    pr_number = custom_input("\nPR number (0: refresh): ")

    if not pr_number:
        pr_number = "1"

    return int(pr_number)


def operate_with_pr(prs, pr_number):
    prs.select_pr(pr_number)
    prs.open_selected()
    prs.print_selected()

    should_approve = custom_input("\nShould approve? (Y/n): ")
    should_approve = not should_approve or should_approve != "n"
    prs.approve_selected()


def custom_input(message):
    try:
        return input(message)
    except:  # noqa
        print("\nBye!\n")
        exit()


if __name__ == "__main__":
    main()
