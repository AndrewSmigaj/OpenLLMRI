#!/bin/bash
# Safe push for the solo-dev main-branch workflow.
#   scripts/push.sh            push main if it is a fast-forward
#   scripts/push.sh --rebase   if behind, rebase local commits onto origin/main first, then push
# It never force-pushes and never merges.
set -e
cd "$(git rev-parse --show-toplevel)"
branch=$(git rev-parse --abbrev-ref HEAD)
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  echo "Uncommitted changes to tracked files. Commit or stash first."; git status --short --untracked-files=no; exit 1
fi
git fetch -q origin
ahead=$(git rev-list --count "origin/$branch..$branch")
behind=$(git rev-list --count "$branch..origin/$branch")
echo "branch $branch: ahead $ahead, behind $behind"
if [ "$ahead" -eq 0 ]; then echo "Nothing to push."; exit 0; fi
if [ "$behind" -gt 0 ]; then
  if [ "$1" = "--rebase" ]; then
    echo "Rebasing $ahead local commit(s) onto origin/$branch..."
    git rebase "origin/$branch"
  else
    echo "origin/$branch has $behind commit(s) you do not have. Run: scripts/push.sh --rebase"
    git log --oneline "$branch..origin/$branch"; exit 1
  fi
fi
git log --oneline "origin/$branch..$branch"
git push origin "$branch"
