#!/usr/bin/env python
import os
import requests
import sys
from tempfile import mkdtemp

from git import Repo
from tqdm import tqdm

from github.repository_query import RepositoryQuery as GithubRepositoryQuery
from sourcehut.client import Client as SourcehutClient


def main():
    github_token = os.getenv("GITHUB_API_KEY")
    sourcehut_token = os.getenv("SOURCEHUT_ACCESS_TOKEN")

    if github_token is None or sourcehut_token is None:
        print(
            "Please ensure GITHUB_API_KEY and SOURCEHUT_API_KEY are exported in the environment."
        )
        sys.exit(1)

    sourcehut_client = SourcehutClient(token=sourcehut_token)
    github_repos = GithubRepositoryQuery(token=github_token)
    tmpd = mkdtemp("-github-repos")

    for repo in tqdm(github_repos.iterator()):
        if not repo["viewerCanAdminister"] or repo["isArchived"] or repo["isDisabled"]:
            pass
        # TODO: Check if repository already exists already in sr.ht

        name = repo["name"]
        clone_to = f"{tmpd}/{name}"
        print(f"Cloning {name} to {clone_to}")

        print(f"Creating new repository in Sourcehut for: {name}")
        res = sourcehut_client.post(
            "/api/repos",
            {
                "name": name,
                "description": repo["description"],
                "visibility": "private" if repo["isPrivate"] else "public",
            },
        )
        # TODO: Handle response errors etc.

        cloned_repo = Repo.clone_from(repo["sshUrl"], f"{tmpd}/{name}")
        remote = cloned_repo.create_remote(
            name="sourcehut",
            # TODO: This shouldn't be hardcoded, we can query the sh API for this
            url=f"git@git.sr.ht:~w1lkins/{name}",
        )

        print(f"Pushing {name} to sourcehut.")
        remote.push(refspec="master:master")

    # TODO: Ask user if they want to cleanup the directory
    os.removedirs(tmpd)


if __name__ == "__main__":
    main()
