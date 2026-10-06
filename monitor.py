# /// script
# dependencies = [
#   "requests >=2.34.2, <2.35.0",
# ]
# ///
import os
import shlex
import subprocess
import sys

import requests

REMOTE_REPO_OWNER = "allen-cell-animated"
REMOTE_REPO_NAME = "vole-app"


# Local-repository info
res = subprocess.run(
    shlex.split("git tag --list"),
    capture_output=True,
    encoding="utf-8",
    check=False,
)
if res.returncode != 0:
    print(f"STDOUT:\n{res.stdout}\n", file=sys.stderr)
    print(f"STDERR:\n{res.stderr}\n", file=sys.stderr)
    sys.exit(f"Command failed with {res.returncode}.")
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
tag_is_new = remote_latest_tag not in local_tag_list
if tag_is_new:
    print(f"{remote_latest_tag} does not exists, create a new issue.")
    issue_title = f"New vole-app release ({remote_latest_tag})"
    issue_body = (
        f"Project {REMOTE_REPO_OWNER}/{REMOTE_REPO_NAME} has a new release, for "
        f"tag {remote_latest_tag} - see "
        f"https://github.com/{REMOTE_REPO_OWNER}/{REMOTE_REPO_NAME}/releases. "
        "You should create a new tag on the current repository via "
        f"`git tag -m {remote_latest_tag} -a {remote_latest_tag} && git push --tags` "
        "to trigger a new build."
    )
    issue_label = remote_latest_tag
else:
    print(f"{remote_latest_tag} already exists, exit.")
    issue_title = ""
    issue_body = ""
    issue_label = ""


if github_output := os.getenv("GITHUB_OUTPUT", None):
    with open(github_output, "a") as writer:
        writer.write(f"tag_is_new={tag_is_new}\n")
        writer.write(f"remote_latest_tag={remote_latest_tag}\n")
        writer.write(f"issue_title={issue_title}\n")
        writer.write(f"issue_body={issue_body}\n")
        writer.write(f"issue_label={remote_latest_tag}")
