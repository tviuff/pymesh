# GIT Commands and Best Practice

## GIT Best Practice

The [Seven Rules](https://cbea.ms/git-commit/#seven-rules) of a great Git Commit message:
    1. Separate subject from body with a blank line
    1. Limit the subject line to 50 characters
    1. Capitalize the subject line
    1. Do not end the subject line with a period
    1. Use the imperative mood in the subject line, i.e. "Clean your room"
    1. Wrap the body at 72 characters
    1. Use the body to explain what and why vs. how


## Standard workflow using branches

```Shell
git switch -c <new-branch>
git push -u origin <new-branch>
git branch -a
git commit -am "Final commit in <new-branch>"
git switch main
git pull origin main
git branch --merged
git merge <new-branch>
git push origin main
git branch --merged
git branch -d <new-branch>
git branch -a
git push origin --delete <new-branch>
git branch -a
```
[source](https://youtu.be/HVsySz-h9r4?feature=shared&t=1270)

## GIT Cheat Sheet

```Shell
git status  # see status between working directory, staged and last commit
```
