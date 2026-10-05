# /// script
# dependencies = [
#   "requests >=2.34.2, <2.35.0",
# ]
# ///
import shlex
import subprocess
import sys

import requests

REMOTE_REPO_OWNER = "allen-cell-animated"
REMOTE_REPO_NAME = "vole-app"
LOCAL_REPO_NAME = "vole-app-builds-test"

_run = lambda cmd: subprocess.run(
    shlex.split(cmd),
    capture_output=True,
    encoding="utf-8",
    check=True,
)

# Fail for dirty status
_run("git pull --tags")
res = _run("git status --porcelain")
if res.stdout.strip() != "":
    print(res.stdout, file=sys.stderr)
    sys.exit("Status not clean. Exit.")
print("Status is clean, proceed.")

# Local-repository info
res = _run("git tag --list")
local_tag_list = res.stdout.splitlines()
print(f"Local repository has tag list: {local_tag_list}")

# Fetch and parse GitHub information
github_api_url = (
    "https://api.github.com/repos/"
    f"{REMOTE_REPO_OWNER}/{REMOTE_REPO_NAME}/releases/latest"
)
response = requests.get(
    github_api_url,
    headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    },
    timeout=10,
)
if response.status_code != 200:
    sys.exit(f"\nInvalid response from {github_api_url}:\n{response}")
response_data = response.json()
remote_latest_tag = response_data["tag_name"]
print(
    f"Latest tag of remote repository "
    f"{REMOTE_REPO_OWNER}/{REMOTE_REPO_NAME}: "
    f"{remote_latest_tag}"
)

if remote_latest_tag in local_tag_list:
    print(f"{remote_latest_tag} already exists, exit.")
else:
    print("Now creating new local tag")
    # _run(f"git tag -m {remote_latest_tag} -a {remote_latest_tag}") # FIXME
    # _run("git push --tags") # FIXME
    res = _run("git tag --list")
    local_tag_list = res.stdout.splitlines()
    print(f"Local repository now has tag list: {local_tag_list}")
    print("All OK, exit")

