import os
import shutil
import subprocess

GITHUB_REPO = os.environ["GITHUB_REPO"]
GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

WORKDIR = "/tmp/repo"
REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)

subprocess.run(["git", "clone", REPO_URL, WORKDIR], check=True)
os.chdir(WORKDIR)

subprocess.run(["python", "auto_run.py"], check=True)

subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
subprocess.run(["git", "config", "user.email", "actions@github.com"], check=True)

subprocess.run(["git", "add", "results"], check=True)
commit = subprocess.run(["git", "commit", "-m", "Data Sync: Add hourly artifacts"], check=False)

if commit.returncode == 0:
    subprocess.run(["git", "push", "origin", "main"], check=True)
else:
    print("No changes to commit.")
