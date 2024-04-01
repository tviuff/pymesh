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
Source: [https://youtu.be/HVsySz-h9r4?feature=shared&t=1270](https://youtu.be/HVsySz-h9r4?feature=shared&t=1270)

```
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

## GIT Cheat Sheet

```
git status                          # see status between  working directory, staged and last commit
    -s                              # same as git status but showing only two-column info (left=staged, right=working directory) with A and M for added and modified:
                                    #   M  readme
                                    #    M config
                                    # the file 'readme' is modified and staged, while 'config' is modified but not staged
git add                             # “add precisely this content to the next commit” rather than “add this file to the project”
git diff                            # compares staged files to last commit
    --staged                        # compares working directory to staged files
git commit -a -m "message"          # commits all modified files in the working directory (-a) and ads a commit message (-m)
git rm <file>                       # removes <file> from the staging area and working directory and commits
git rm                              # used if you have deleted files (in the "normal" way), thins command will stage the files removal
git log
    --all                           # includes all branches in the shown log (not only the one you're in)
    -<n>                            # show only the last n commits.
    --since, --after                # limit the commits to those made after the specified date.
    --until, --before               # limit the commits to those made before the specified date.
                                    #   2.weeks
                                    #   "2024-03-27"
                                    #   "1 day 3 hours ago"
    --author                        # only show commits in which the author entry matches the specified string.
    --committer                     # only show commits in which the committer entry matches the specified string.
    --grep                          # only show commits with a commit message containing the string.
    -S                              # only show commits adding or removing code matching the string.
    --stat                          # show commits with extra stat info
    -p                              # shows log with diff for each commit
    --pretty=oneline                # shows commit SHA-1 and their first line of the commit message
    --pretty="%h %s" --graph        # shows branches with commit hash (%h) and subject (%s)
    --decorate                      # also shows the HEAD pointer (use git log --oneline --decorate)
    -- path/to/file/or/dir          # only show commits that introduced a change to file or files in dir. This log option must always be the last if concatenating options
git log --oneline --decorate --graph --all
git commit
    -a
    -m
    -am                             # stage all and add message
    --amend                         # ammends (replaces) a previous commit with a new and imporoved oneline, i.e:
                                    #   git commit -m 'Initial commit'
                                    #   git add forgotten_file
                                    #   git commit --amend
                                    # only amend commits that are still local and have not been pushed somewhere.
git restore --staged <file>         # used for unstaging a staged <file>
git restore <file>                  # used to discard changes in working directory <file  !!! CAN BE DANGEREOUS AND LOCAL DATA LOSED !!!
git remote -v                       # see which remote servers you have configured and its urls (-v)

git pull                            # automatically fetch and then merge that remote branch into your current branch

git push -u origin <local-branch>       # push your commits to the server. -u associates the remote and local branches, so in the future you can run
                                        #   git pull
                                        #   git push
                                        # when inside the branch, thereby omitting extra text

git remote show origin              # lists the URL for the remote repository as well as the tracking branch information
git branch                          # lists all branches locally
git branch -r                       # lists all branches remote
git branch <newbranchname>          # creates a new git branch

git switch <newbranchname>          # switch to existing branch
git switch -c <newbranchname>       # create (-c) and switch to new branch in a single command

git merge <branchname>              # merges <branchname> into existing branch, e.g. main
git branch -d <branchname>          # deletes branch (usually dine after a merge)
```
