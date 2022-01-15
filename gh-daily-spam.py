from src.pull_requests import PullRequests

import os


def main():
    prs = PullRequests()
    while prs.number_of_prs_to_be_reviewed:
        os.system("clear")
        print(f"You still need to review {prs.number_of_prs_to_be_reviewed} PRs\n")
        pr = prs.pop_first_pr()
        operate_with_pr(pr)


def operate_with_pr(pr):
    print(pr)
    opened = open_in_browser_workflow(pr)
    if not opened:
        return
    approve_workflow(pr)


def open_in_browser_workflow(pr):
    should_open = custom_input("\nShould open in browser? (Y/n): ")
    should_open = not should_open or should_open.lower() == "y"
    if should_open:
        pr.open_in_browser()
    return should_open


def approve_workflow(pr):
    action = custom_input("\n(A)pprove/(C)omment/(S)kip? (A/c/s): ")
    action = action.lower() if action else "a"

    if action == "s":
        return

    if action == "c":
        message = custom_input("\nType custom message: ")
        pr.comment(message)
        return

    if action == "a":
        should_custom_message = custom_input("\nDo you want custom message (y/N): ")
        should_custom_message = should_custom_message and should_custom_message.lower() == "y"
        message = custom_input("\nType custom message: ") if should_custom_message else ""
        pr.approve(message)


def custom_input(message):
    try:
        return input(message)
    except:  # noqa
        print("\nBye!\n")
        exit()


if __name__ == "__main__":
    main()
