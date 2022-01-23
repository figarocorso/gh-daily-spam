# gh-daily-spam

This is a small and ugly Python CLI tool to review and, approve or comment, Github pull requests from a single repo.

Why? Because GH notifications could be overwhelming and you would like to review few specific PRs with more attention. Also default messages and "approval by single `<enter>` key" will save you a bunch of time.

### Contributing

PRs are more than welcome. Color schema, filters, GH API usage, user interaction, tests coverage, ... everything can be improved. Any big feature (like showing the diff at the terminal) should probably be better under a feature flag. As tool is working fine for me, if you are considering adding any code, contact me anyhow so we avoid conflicts (or developing the same fix/feature).

### How to run

First things first: edit your [config.json](config.json) file with your customizations

Then you just need to download the [dependencies](requirements.txt) (consider using a virtualenv) and run the tool:

```python
python gh-daily-spam.py
```

You can `<CONTROL>+c` at any time, CLI should exit, most of the times, in a exception-less way.

### Current workflow

* Tool retrieves PRs from the last week (depending on filters available)
* Then iterates over every one of all those PRs:
  * Show PR info and asks if you want to open it at your default browser
  * If affirmative you should be able to review it at your browser and Approve/Comment/Skip the PR
  * For approval and comment you will be asked for default comment or custom one

No info is stored (beyond your own `config.json`) so do not expect any magic with the skip option.

### Filters

Current MVP has hardcoded at [filter_methods.py](src/filter_methods.py) those filters that were useful to the author. Feel free to edit that file (it should be pretty straighforward) commenting the dict we are iterating at or changing/adding methods. After updating this readme, next task is to describe the desired filters at the [config.json](config.json) file.
