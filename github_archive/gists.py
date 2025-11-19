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
from github import Gist


if TYPE_CHECKING:
    # This is needed to get around circular imports while allowing `mypy` to be happy
    from github_archive.archive import GithubArchive  # pragma: no cover

from github_archive.constants import (
    CLONE_OPERATION,
    LOGGER_NAME,
    PULL_OPERATION,
)


def iterate_gists_to_archive(github_archive: GithubArchive, gists: List[Gist.Gist], operation: str) -> None:
    """Iterate over each gist and start a thread if it can be archived."""
    pool = ThreadPoolExecutor(github_archive.threads)
    thread_list = []

    for gist in gists:
        gist_path = os.path.join(github_archive.location, "gists", gist.id)
        thread_list.append(
            pool.submit(
                _archive_gist,
                github_archive=github_archive,
                gist=gist,
                gist_path=gist_path,
                operation=operation,
            )
        )

    wait(thread_list, return_when=ALL_COMPLETED)


def view_gists(gists: List[Gist.Gist]):
    """View a list of gists that will be cloned/pulled."""
    logger = woodchips.get(LOGGER_NAME)

    for gist in gists:
        gist_id = f"{gist.owner.login}/{gist.id}"
        logger.info(gist_id)


def iterate_gists_to_fork(github_archive: GithubArchive, gists: List[Gist.Gist]) -> List[Optional[str]]:
    """Iterates through a list of gists and attempts to fork them."""
    pool = ThreadPoolExecutor(github_archive.threads)
    thread_list = []

    for gist in gists:
        thread_list.append(
            pool.submit(
                _fork_gist,
                gist=gist,
            )
        )

    wait(thread_list, return_when=ALL_COMPLETED)
    failed_gists = [gist.result() for gist in thread_list if gist.result()]

    return failed_gists


def _fork_gist(gist: Gist.Gist):
    """Forks a gist to the authenticated user's GitHub instance."""
    logger = woodchips.get(LOGGER_NAME)

    gist_id = f"{gist.owner.login}/{gist.id}"

    try:
        gist.create_fork()
        logger.info(f"{gist_id} forked!")
    except Exception:
        logger.warning(f"{gist_id} failed to fork!")


def _archive_gist(github_archive: GithubArchive, gist: Gist.Gist, gist_path: str, operation: str) -> Optional[str]:
    """Clone and pull gists based on the operation passed.

    We return the name of the gist if its git operation fails, otherwise return None.
    """
    logger = woodchips.get(LOGGER_NAME)
    failed_gist = None
    full_gist_id = os.path.join(gist.owner.login, gist.id)  # We use a path here to properly remove failed dirs

    if (os.path.exists(gist_path) and operation == CLONE_OPERATION) or (
        not os.path.exists(gist_path) and operation == PULL_OPERATION
    ):
        pass
    else:
        commands = {
            CLONE_OPERATION: ["git", "clone", gist.html_url, gist_path],
            PULL_OPERATION: ["git", "-C", gist_path, "pull", "--rebase"],
        }
        git_command = commands[operation]

        try:
            subprocess.check_output(  # nosec
                git_command,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=github_archive.timeout,
            )
            logger.info(f"Gist: {full_gist_id} {operation} success!")
        except subprocess.TimeoutExpired:
            logger.error(f"Git operation timed out archiving {gist.id}.")
            failed_gist = full_gist_id
        except subprocess.CalledProcessError as error:
            logger.error(f"Failed to {operation} {gist.id}\n{error.output}")
            failed_gist = full_gist_id

    return failed_gist
