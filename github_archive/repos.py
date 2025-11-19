from __future__ import annotations

import os
import subprocess  # nosec
from concurrent.futures import (
    ALL_COMPLETED,
    ThreadPoolExecutor,
    wait,
)
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
)

import woodchips
from github import Repository


if TYPE_CHECKING:
    # This is needed to get around circular imports while allowing `mypy` to be happy
    from github_archive.archive import GithubArchive  # pragma: no cover

from github_archive.constants import (
    CLONE_OPERATION,
    LOGGER_NAME,
    PULL_OPERATION,
)


def iterate_repos_to_archive(
    github_archive: GithubArchive, repos: List[Repository.Repository], operation: str
) -> List[Optional[str]]:
    """Iterate over each repository and start a thread after filtering based on the
    user input and attempt to archive it.

    We ignore repos not in the include or in the exclude list if either are present.
    """
    logger = woodchips.get(LOGGER_NAME)
    pool = ThreadPoolExecutor(github_archive.threads)
    thread_list = []

    for repo in repos:
        if (
            (
                github_archive.languages
                and repo.language
                and repo.language.lower() in github_archive.languages
                and not github_archive.include
                and not github_archive.exclude
            )
            or (not github_archive.languages and not github_archive.include and not github_archive.exclude)
            or (github_archive.include and repo.name in github_archive.include)
            or (github_archive.exclude and repo.name not in github_archive.exclude)
        ):
            repo_owner_username = repo.owner.login.lower()
            repo_path = os.path.join(github_archive.location, "repos", repo_owner_username, repo.name)
            thread_list.append(
                pool.submit(
                    _archive_repo,
                    github_archive=github_archive,
                    repo=repo,
                    repo_path=repo_path,
                    operation=operation,
                )
            )
        else:
            logger.debug(f"{repo.name} skipped due to filtering")

    wait(thread_list, return_when=ALL_COMPLETED)
    failed_repos = [repo.result() for repo in thread_list if repo.result()]

    return failed_repos


def view_repos(repos: List[Repository.Repository]):
    """View a list of repos that will be cloned/pulled."""
    logger = woodchips.get(LOGGER_NAME)

    for repo in repos:
        repo_name = f"{repo.owner.login}/{repo.name}"
        logger.info(repo_name)


def iterate_repos_to_fork(github_archive: GithubArchive, repos: List[Repository.Repository]) -> None:
    """Iterates through a list of repos and attempts to fork them."""
    pool = ThreadPoolExecutor(github_archive.threads)
    thread_list = []

    for repo in repos:
        thread_list.append(
            pool.submit(
                _fork_repo,
                repo=repo,
            )
        )

    wait(thread_list, return_when=ALL_COMPLETED)


def _fork_repo(repo: Repository.Repository):
    """Forks a repository to the authenticated user's GitHub instance."""
    logger = woodchips.get(LOGGER_NAME)

    repo_name = f"{repo.owner.login}/{repo.name}"

    try:
        repo.create_fork()
        logger.info(f"{repo_name} forked!")
    except Exception:
        logger.error(f"{repo_name} failed to fork!")


def _archive_repo(
    github_archive: GithubArchive, repo: Repository.Repository, repo_path: str, operation: str
) -> Optional[str]:
    """Clone and pull repos based on the operation passed.

    We return the name of the repo if its git operation fails, otherwise return None.
    """
    logger = woodchips.get(LOGGER_NAME)
    failed_repo = None
    full_repo_name = os.path.join(repo.owner.login, repo.name)  # We use a path here to properly remove failed dirs

    if (os.path.exists(repo_path) and operation == CLONE_OPERATION) or (
        not os.path.exists(repo_path) and operation == PULL_OPERATION
    ):
        pass
    else:
        commands = {
            PULL_OPERATION: ["git", "-C", repo_path, "pull", "--rebase"],
        }

        if github_archive.use_https or not github_archive.token:
            # Will be used for unauthenticated requests or with items like GCM
            commands.update({CLONE_OPERATION: ["git", "clone", repo.html_url, repo_path]})
        else:
            # Will be used for SSH authenticated requests
            commands.update({CLONE_OPERATION: ["git", "clone", repo.ssh_url, repo_path]})

        git_command = commands[operation]

        try:
            subprocess.check_output(  # nosec
                git_command,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=github_archive.timeout,
            )
            logger.info(f"Repo: {full_repo_name} {operation} success!")
        except subprocess.TimeoutExpired:
            logger.error(f"Git operation timed out archiving {repo.name}.")
            failed_repo = full_repo_name
        except subprocess.CalledProcessError as error:
            logger.error(f"Failed to {operation} {repo.name}\n{error.output}")
            failed_repo = full_repo_name

    return failed_repo
