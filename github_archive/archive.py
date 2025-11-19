import os
import shutil
import stat
from datetime import datetime
from typing import (
    List,
    Union,
)

import woodchips
from github import (
    Auth,
    Gist,
    Github,
    Repository,
)

from github_archive.constants import (
    CLONE_OPERATION,
    DEFAULT_BASE_URL,
    DEFAULT_LOCATION,
    DEFAULT_LOG_LEVEL,
    DEFAULT_NUM_THREADS,
    DEFAULT_TIMEOUT,
    GIST_CONTEXT,
    LOGGER_NAME,
    ORG_CONTEXT,
    PERSONAL_CONTEXT,
    PULL_OPERATION,
    STAR_CONTEXT,
    USER_CONTEXT,
)
from github_archive.gists import (
    iterate_gists_to_archive,
    iterate_gists_to_fork,
    view_gists,
)
from github_archive.logger import (
    log_and_raise_value_error,
    setup_logger,
)
from github_archive.repos import (
    iterate_repos_to_archive,
    iterate_repos_to_fork,
    view_repos,
)


class GithubArchive:
    def __init__(
        self,
        token=None,
        users=None,
        orgs=None,
        gists=None,
        stars=None,
        view=False,
        clone=False,
        pull=False,
        fork=False,
        include=None,
        exclude=None,
        languages=None,
        forks=False,
        location=DEFAULT_LOCATION,
        use_https=False,
        timeout=DEFAULT_TIMEOUT,
        threads=DEFAULT_NUM_THREADS,
        base_url=DEFAULT_BASE_URL,
        log_level=DEFAULT_LOG_LEVEL,
    ):
        # Parameter variables
        self.token = token
        self.users = users.lower().split(",") if users else ""
        self.orgs = orgs.lower().split(",") if orgs else ""
        self.gists = gists.lower().split(",") if gists else ""
        self.stars = stars.lower().split(",") if stars else ""
        self.view = view
        self.clone = clone
        self.pull = pull
        self.fork = fork
        self.include = include.lower().split(",") if include else ""
        self.exclude = exclude.lower().split(",") if exclude else ""
        self.languages = languages.lower().split(",") if languages else ""
        self.forks = forks
        self.location = os.path.expanduser(location)
        self.use_https = use_https
        self.timeout = timeout
        self.threads = threads
        self.base_url = base_url
        self.log_level = log_level

        # Internal variables
        self.github_instance = (
            Github(auth=Auth.Token(self.token), base_url=self.base_url)
            if self.token
            else Github(base_url=self.base_url)
        )
        self.authenticated_user = self.github_instance.get_user() if self.token else None
        self.authenticated_username = self.authenticated_user.login.lower() if self.token else None

    def run(self):
        """Run the tool based on the arguments passed via the CLI."""
        self.initialize_project()
        logger = woodchips.get(LOGGER_NAME)
        logger.info("# GitHub Archive started...")
        start_time = datetime.now()
        failed_repo_dirs = []

        # Personal (includes personal authenticated items)
        if self.token and self.users and self.authenticated_user_in_users():
            logger.info("# Making API call to GitHub for personal repos...")
            personal_repos = self.get_all_git_assets(PERSONAL_CONTEXT)

            if self.view:
                logger.info("# Viewing user repos...")
                view_repos(personal_repos)
            if self.clone:
                logger.info("# Cloning missing personal repos...")
                failed_repos = iterate_repos_to_archive(self, personal_repos, CLONE_OPERATION)
                if any(failed_repos):
                    failed_repo_dirs.extend(failed_repos)
            if self.pull:
                logger.info("# Pulling changes to personal repos...")
                _ = iterate_repos_to_archive(self, personal_repos, PULL_OPERATION)
            if self.fork:
                # We can't fork a repo we already have, do nothing
                pass

            # We remove the authenticated user from the list so that we don't double pull their
            # repos for the `users` logic.
            self.users.remove(self.authenticated_username)

        # Users (can include personal non-authenticated items, excludes personal authenticated calls)
        if self.users and len(self.users) > 0:
            logger.info("# Making API calls to GitHub for user repos...")
            user_repos = self.get_all_git_assets(USER_CONTEXT)

            if self.view:
                logger.info("# Viewing user repos...")
                view_repos(user_repos)
            if self.clone:
                logger.info("# Cloning missing user repos...")
                failed_repos = iterate_repos_to_archive(self, user_repos, CLONE_OPERATION)
                if any(failed_repos):
                    failed_repo_dirs.extend(failed_repos)
            if self.pull:
                logger.info("# Pulling changes to user repos...")
                _ = iterate_repos_to_archive(self, user_repos, PULL_OPERATION)
            if self.fork:
                logger.info("# Forking user repos...")
                iterate_repos_to_fork(self, user_repos)

        # Orgs
        if self.orgs:
            logger.info("# Making API calls to GitHub for org repos...")
            org_repos = self.get_all_git_assets(ORG_CONTEXT)

            if self.view:
                logger.info("# Viewing org repos...")
                view_repos(org_repos)
            if self.clone:
                logger.info("# Cloning missing org repos...")
                failed_repos = iterate_repos_to_archive(self, org_repos, CLONE_OPERATION)
                if any(failed_repos):
                    failed_repo_dirs.extend(failed_repos)
            if self.pull:
                logger.info("# Pulling changes to org repos...")
                _ = iterate_repos_to_archive(self, org_repos, PULL_OPERATION)
            if self.fork:
                logger.info("# Forking org repos...")
                iterate_repos_to_fork(self, org_repos)

        # Stars
        if self.stars:
            logger.info("# Making API call to GitHub for starred repos...")
            starred_repos = self.get_all_git_assets(STAR_CONTEXT)

            if self.view:
                logger.info("# Viewing stars...")
                view_repos(starred_repos)
            if self.clone:
                logger.info("# Cloning missing starred repos...")
                failed_repos = iterate_repos_to_archive(self, starred_repos, CLONE_OPERATION)
                if any(failed_repos):
                    failed_repo_dirs.extend(failed_repos)
            if self.pull:
                logger.info("# Pulling changes to starred repos...")
                _ = iterate_repos_to_archive(self, starred_repos, PULL_OPERATION)
            if self.fork:
                logger.info("# Forking starred repos...")
                iterate_repos_to_fork(self, starred_repos)

        if failed_repo_dirs:
            logger.info("Cleaning up repos...")
            self.remove_failed_dirs("repos", failed_repo_dirs)

        # Gists
        if self.gists:
            logger.info("# Making API call to GitHub for gists...")
            gists = self.get_all_git_assets(GIST_CONTEXT)
            failed_gist_dirs = []

            if self.view:
                logger.info("# Viewing gists...")
                view_gists(gists)
            if self.clone:
                logger.info("# Cloning missing gists...")
                failed_gists = iterate_gists_to_archive(self, gists, CLONE_OPERATION)
                if any(failed_gists):
                    failed_gist_dirs.extend(failed_gists)
            if self.pull:
                logger.info("# Pulling changes to gists...")
                _ = iterate_gists_to_archive(self, gists, PULL_OPERATION)
            if self.fork:
                logger.info("# Forking gists...")
                iterate_gists_to_fork(self, gists)

            if failed_gist_dirs:
                logger.info("Cleaning up gists...")
                self.remove_failed_dirs("gists", failed_gist_dirs)

        execution_time = f"Execution time: {datetime.now() - start_time}."
        finish_message = f"GitHub Archive complete! {execution_time}"
        logger.info(finish_message)

    def initialize_project(self):
        """Initialize the tool and ensure everything is in order before moving on:
        1. Directories are setup correctly
        2. A git operation was specified
        3. A list of assets to run operations on is specified
        """
        setup_logger(self)
        logger = woodchips.get(LOGGER_NAME)

        if not os.path.exists(self.location):
            os.makedirs(os.path.join(self.location, "repos"))
            os.makedirs(os.path.join(self.location, "gists"))

        if (self.users or self.orgs or self.gists or self.stars) and not (
            self.view or self.clone or self.pull or self.fork
        ):
            log_and_raise_value_error(
                logger=logger,
                message="A git operation must be specified when a list of users or orgs is provided.",
            )
        elif not (self.users or self.orgs or self.gists or self.stars) and (
            self.view or self.clone or self.pull or self.fork
        ):
            log_and_raise_value_error(
                logger=logger,
                message="A list must be provided when a git operation is specified.",
            )
        elif not (
            self.users or self.orgs or self.gists or self.stars or self.view or self.clone or self.pull or self.fork
        ):
            log_and_raise_value_error(
                logger=logger,
                message="At least one git operation and one list must be provided to run github-archive.",
            )
        elif self.include and self.exclude:
            log_and_raise_value_error(
                logger=logger,
                message="The include and exclude flags are mutually exclusive. Only one can be used on each run.",
            )
        elif (self.include or self.exclude) and self.languages:
            log_and_raise_value_error(
                logger=logger,
                message="The include and exclude flags cannot be used with the languages flag.",
            )

    def authenticated_user_in_users(self) -> bool:
        """Returns True if the authenticated user is in the list of users."""
        return self.authenticated_user.login.lower() in self.users

    def get_all_git_assets(self, context: str) -> List[Union[Repository.Repository, Gist.Gist]]:
        """Retrieve a list of lists via API of git assets (repos, gists) of the
        specified owner(s) (users, orgs). Returns a flattened, sorted list of git assets.
        """
        logger = woodchips.get(LOGGER_NAME)

        get_org_repos = lambda owner: self.github_instance.get_organization(owner).get_repos()  # noqa
        get_personal_repos = lambda _: self.authenticated_user.get_repos(affiliation="owner")  # noqa
        get_starred_repos = lambda owner: self.github_instance.get_user(owner).get_starred()  # noqa
        get_user_gists = lambda owner: self.github_instance.get_user(owner).get_gists()  # noqa
        get_user_repos = lambda owner: self.github_instance.get_user(owner).get_repos()  # noqa

        context_manager = {
            GIST_CONTEXT: [self.gists, get_user_gists, "gists"],
            ORG_CONTEXT: [self.orgs, get_org_repos, "repos"],
            PERSONAL_CONTEXT: [self.users, get_personal_repos, "repos"],
            STAR_CONTEXT: [self.stars, get_starred_repos, "starred repos"],
            USER_CONTEXT: [self.users, get_user_repos, "repos"],
        }

        all_git_assets = []
        owner_list = context_manager[context][0]
        git_asset_string = context_manager[context][2]

        for owner in owner_list:
            formatted_owner_name = owner.strip()
            git_assets = context_manager[context][1](owner)
            logger.debug(f"{formatted_owner_name} {git_asset_string} retrieved!")

            for item in git_assets:
                if context == GIST_CONTEXT:
                    # Automatically add gists since we don't support forked gists
                    all_git_assets.append(item)
                elif self.forks or (self.forks is False and item.fork is False):
                    all_git_assets.append(item)
                else:
                    # Do not include this forked asset
                    pass

        final_sorted_list = sorted(all_git_assets, key=lambda item: item.owner.login)

        return final_sorted_list

    def remove_failed_dirs(self, dirs_location: str, failed_dirs: List[str]):
        """Removes a directory if it fails a git operation due to
        timing out or other errors so it can be retried on the next run.
        """
        logger = woodchips.get(LOGGER_NAME)

        def make_dir_writable(function, path, _):
            """The `.git` folder on Windows cannot be gracefully removed due to being read-only,
            so we make the directory writable on a failure and retry the original function.
            """
            os.chmod(path, stat.S_IWRITE)
            function(path)

        for directory in set(failed_dirs):
            path = os.path.join(self.location, dirs_location, directory)
            if os.path.exists(path):
                logger.debug(f"Removing {directory} due to a failed git operation...")
                shutil.rmtree(path, onerror=make_dir_writable)
