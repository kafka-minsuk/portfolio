#!/usr/bin/env bash
# One-shot publish to GitHub Pages.
#   ./deploy.sh <github-account> [repo-name] [--private]
# Creates the repo if needed, commits everything, pushes to main and serves /docs with GitHub Pages.
# Site URL: https://<github-account>.github.io/<repo-name>/
set -euo pipefail

GH_ACCOUNT="${1:-}"
REPO="${2:-portfolio}"
VISIBILITY="--public"
[[ "${3:-}" == "--private" ]] && VISIBILITY="--private"   # Pages on private repos needs a paid plan
EMAIL="minsuk0504@snu.ac.kr"
NAME="${GIT_NAME:-Minsuk Kim}"

if [[ -z "$GH_ACCOUNT" ]]; then
  echo "usage: ./deploy.sh <github-account> [repo-name] [--private]"
  echo "logged-in accounts:"; gh auth status 2>&1 | grep -o 'account [^ ]*' | sed 's/account /  /'
  exit 1
fi
cd "$(dirname "$0")"

# use the requested gh account for this run, restore the previous one afterwards
PREV=$(gh api user --jq .login 2>/dev/null || true)
gh auth switch --hostname github.com --user "$GH_ACCOUNT"
trap '[[ -n "$PREV" && "$PREV" != "$GH_ACCOUNT" ]] && gh auth switch --hostname github.com --user "$PREV" >/dev/null 2>&1 || true' EXIT
gh auth setup-git >/dev/null

[[ -d .git ]] || git init -q -b main
git config user.email "$EMAIL"
git config user.name "$NAME"
git config http.postBuffer 524288000   # large data folder: avoid HTTP 408 on push
git add -A
git commit -q -m "${COMMIT_MSG:-Update demography pyramid app}" || echo "nothing new to commit"
git branch -M main

URL="https://github.com/$GH_ACCOUNT/$REPO.git"
if gh repo view "$GH_ACCOUNT/$REPO" >/dev/null 2>&1; then
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "$URL"
  git remote set-url origin "$URL"
  git push -u origin main
else
  gh repo create "$GH_ACCOUNT/$REPO" $VISIBILITY --source=. --remote=origin --push \
    --description "Interactive population pyramids by birth year with shocks, productivity and retirement cost estimates"
fi

# enable (or update) GitHub Pages: branch main, folder /docs
if ! gh api "repos/$GH_ACCOUNT/$REPO/pages" >/dev/null 2>&1; then
  gh api -X POST "repos/$GH_ACCOUNT/$REPO/pages" -f "source[branch]=main" -f "source[path]=/docs" >/dev/null
else
  gh api -X PUT "repos/$GH_ACCOUNT/$REPO/pages" -f "source[branch]=main" -f "source[path]=/docs" >/dev/null
fi
echo
echo "Pushed. The site will be live in ~1 minute at: https://$(echo "$GH_ACCOUNT" | tr "[:upper:]" "[:lower:]").github.io/$REPO/"
