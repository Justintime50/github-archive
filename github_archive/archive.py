import logging
import os
import shutil
import subprocess
from datetime import datetime
from threading import BoundedSemaphore, Thread

from github import Github

from github_archive.constants import DEFAULT_LOCATION, DEFAULT_NUM_THREADS, DEFAULT_TIMEOUT
from github_archive.logger import Logger

LOGGER = logging.getLogger(__name__)

CLONE_OPERATION = 'clone'
PULL_OPERATION = 'pull'

GIST_CONTEXT = 'gist'
ORG_CONTEXT = 'org'
PERSONAL_CONTEXT = 'personal'
STAR_CONTEXT = 'star'
USER_CONTEXT = 'user'


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
        forks=False,
        location=DEFAULT_LOCATION,
        use_https=False,
        timeout=DEFAULT_TIMEOUT,
        threads=DEFAULT_NUM_THREADS,
    ):
        # Parameter variables
        self.token = token
        self.users = users.lower().split(',') if users else ''
        self.orgs = orgs.lower().split(',') if orgs else ''
        self.gists = gists.lower().split(',') if gists else ''
        self.stars = stars.lower().split(',') if stars else ''
        self.view = view
        self.clone = clone
        self.pull = pull
        self.forks = forks
        self.location = location
        self.use_https = use_https
        self.timeout = timeout
        self.threads = threads

        # Internal variables
        self.github_instance = Github(self.token) if self.token else Github()
        self.authenticated_user = self.github_instance.get_user() if self.token else None
        self.authenticated_username = self.authenticated_user.login.lower() if self.token else None

    def run(self):
        """Run the tool based on the arguments passed via the CLI."""
        self.initialize_project()
        Logger.setup_logging(LOGGER, self.location)
        LOGGER.info('# GitHub Archive started...\n')
        start_time = datetime.now()

        # Personal (includes personal authenticated items)
        if self.token and self.authenticated_user_in_users and self.users:
            LOGGER.info('# Making API call to GitHub for personal repos...\n')
            personal_repos = self.get_all_git_assets(PERSONAL_CONTEXT)

            if self.view:
                LOGGER.info('# Viewing user repos...\n')
                self.view_repos(personal_repos)
            if self.clone:
                LOGGER.info('# Cloning missing personal repos...\n')
                self.iterate_repos_to_archive(personal_repos, CLONE_OPERATION)
            if self.pull:
                LOGGER.info('# Pulling changes to personal repos...\n')
                self.iterate_repos_to_archive(personal_repos, PULL_OPERATION)

            # We remove the authenticated user from the list so that we don't double pull their
            # repos for the `users` logic.
            self.users.remove(self.authenticated_username)

        # Users (can include personal non-authenticated items, excludes personal authenticated calls)
        if self.users and len(self.users) > 0:
            LOGGER.info('# Making API calls to GitHub for user repos...\n')
            user_repos = self.get_all_git_assets(USER_CONTEXT)

            if self.view:
                LOGGER.info('# Viewing user repos...\n')
                self.view_repos(user_repos)
            if self.clone:
                LOGGER.info('# Cloning missing user repos...\n')
                self.iterate_repos_to_archive(user_repos, CLONE_OPERATION)
            if self.pull:
                LOGGER.info('# Pulling changes to user repos...\n')
                self.iterate_repos_to_archive(user_repos, PULL_OPERATION)

        # Orgs
        if self.orgs:
            LOGGER.info('# Making API calls to GitHub for org repos...\n')
            org_repos = self.get_all_git_assets(ORG_CONTEXT)

            if self.view:
                LOGGER.info('# Viewing org repos...\n')
                self.view_repos(org_repos)
            if self.clone:
                LOGGER.info('# Cloning missing org repos...\n')
                self.iterate_repos_to_archive(org_repos, CLONE_OPERATION)
            if self.pull:
                LOGGER.info('# Pulling changes to org repos...\n')
                self.iterate_repos_to_archive(org_repos, PULL_OPERATION)

        # Gists
        if self.gists:
            LOGGER.info('# Making API call to GitHub for gists...\n')
            gists = self.get_all_git_assets(GIST_CONTEXT)

            if self.view:
                LOGGER.info('# Viewing gists...\n')
                self.view_gists(gists)
            if self.clone:
                LOGGER.info('# Cloning missing gists...\n')
                self.iterate_gists_to_archive(gists, CLONE_OPERATION)
            if self.pull:
                LOGGER.info('# Pulling changes to gists...\n')
                self.iterate_gists_to_archive(gists, PULL_OPERATION)

        # Stars
        if self.stars:
            LOGGER.info('# Making API call to GitHub for starred repos...\n')
            starred_repos = self.get_all_git_assets(STAR_CONTEXT)

            if self.view:
                LOGGER.info('# Viewing stars...\n')
                self.view_repos(starred_repos)
            if self.clone:
                LOGGER.info('# Cloning missing starred repos...\n')
                self.iterate_repos_to_archive(starred_repos, CLONE_OPERATION)
            if self.pull:
                LOGGER.info('# Pulling changes to starred repos...\n')
                self.iterate_repos_to_archive(starred_repos, PULL_OPERATION)

        execution_time = f'Execution time: {datetime.now() - start_time}.'
        finish_message = f'GitHub Archive complete! {execution_time}\n'
        LOGGER.info(finish_message)

    def initialize_project(self):
        """Initialize the tool and ensure everything is in order before running any logic.

        This function ensures the minimum set of requirements are passed in to run the tool:
        1. a git operation
        2. a list of assets to run operations on
        """
        if not os.path.exists(self.location):
            os.makedirs(os.path.join(self.location, 'repos'))
            os.makedirs(os.path.join(self.location, 'gists'))

        if (self.users or self.orgs or self.gists or self.stars) and not (self.view or self.clone or self.pull):
            message = 'A git operation must be specified when a list of users or orgs is provided.'
            LOGGER.critical(message)
            raise ValueError(message)
        elif not (self.users or self.orgs or self.gists or self.stars) and (self.view or self.clone or self.pull):
            message = 'A list must be provided when a git operation is specified.'
            LOGGER.critical(message)
            raise ValueError(message)

    def authenticated_user_in_users(self):
        return self.authenticated_user.login.lower() in self.users

    def get_all_git_assets(self, context):
        """Retrieve a list of lists via API of git assets (repos, gists) of the
        specified owner(s) (users, orgs). Return a sorted, flat, sorted list of git assets.
        """
        get_org_repos = lambda owner: self.github_instance.get_organization(owner).get_repos()  # noqa
        get_personal_repos = lambda owner: self.authenticated_user.get_repos(affiliation='owner')  # noqa
        get_starred_repos = lambda owner: self.github_instance.get_user(owner).get_starred()  # noqa
        get_user_gists = lambda owner: self.github_instance.get_user(owner).get_gists()  # noqa
        get_user_repos = lambda owner: self.github_instance.get_user(owner).get_repos()  # noqa

        context_manager = {
            GIST_CONTEXT: [self.gists, get_user_gists, 'gists'],
            ORG_CONTEXT: [self.orgs, get_org_repos, 'repos'],
            PERSONAL_CONTEXT: [self.users, get_personal_repos, 'repos'],
            STAR_CONTEXT: [self.stars, get_starred_repos, 'starred repos'],
            USER_CONTEXT: [self.users, get_user_repos, 'repos'],
        }

        all_git_assets = []
        owner_list = context_manager[context][0]
        git_asset_string = context_manager[context][2]

        for owner in owner_list:
            formatted_owner_name = owner.strip()
            git_assets = context_manager[context][1](owner)
            LOGGER.debug(f'{formatted_owner_name} {git_asset_string} retrieved!')

            for item in git_assets:
                if self.forks or (self.forks is False and item.fork is False):
                    all_git_assets.append(item)
                else:
                    # Do not include this forked asset
                    pass

        final_sorted_list = sorted(all_git_assets, key=lambda item: item.owner.login)

        return final_sorted_list

    def iterate_repos_to_archive(self, repos, operation):
        """Iterate over each repository and start a thread if it can be archived."""
        thread_limiter = BoundedSemaphore(self.threads)
        thread_list = []

        for repo in repos:
            repo_owner_username = repo.owner.login.lower()
            repo_path = os.path.join(self.location, 'repos', repo_owner_username, repo.name)
            repo_thread = Thread(
                target=self.archive_repo,
                args=(
                    thread_limiter,
                    repo,
                    repo_path,
                    operation,
                ),
            )
            thread_list.append(repo_thread)
            repo_thread.start()
        for thread in thread_list:
            thread.join()

    def iterate_gists_to_archive(self, gists, operation):
        """Iterate over each gist and start a thread if it can be archived."""
        thread_limiter = BoundedSemaphore(self.threads)
        thread_list = []

        for gist in gists:
            gist_path = os.path.join(self.location, 'gists', gist.id)
            gist_thread = Thread(
                target=self.archive_gist,
                args=(
                    thread_limiter,
                    gist,
                    gist_path,
                    operation,
                ),
            )
            thread_list.append(gist_thread)
            gist_thread.start()
        for thread in thread_list:
            thread.join()

    def view_repos(self, repos):
        """View a list of repos that will be cloned/pulled."""
        for repo in repos:
            repo_name = f'{repo.owner.login}/{repo.name}'
            LOGGER.info(repo_name)

    def view_gists(self, gists):
        """View a list of gists that will be cloned/pulled."""
        for gist in gists:
            gist_id = f'{gist.owner.login}/{gist.id}'
            LOGGER.info(gist_id)

    def archive_repo(self, thread_limiter, repo, repo_path, operation):
        """Clone and pull repos based on the operation passed"""
        if (os.path.exists(repo_path) and operation == CLONE_OPERATION) or (
            not os.path.exists(repo_path) and operation == PULL_OPERATION
        ):
            pass
        else:
            commands = {
                PULL_OPERATION: f'cd {repo_path} && git pull --rebase',
            }

            if self.use_https:
                commands.update({CLONE_OPERATION: f'git clone {repo.html_url} {repo_path}'})
            else:
                commands.update({CLONE_OPERATION: f'git clone {repo.ssh_url} {repo_path}'})
            git_command = commands[operation]

            try:
                thread_limiter.acquire()
                subprocess.run(
                    git_command,
                    stdout=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True,
                    check=True,
                    timeout=self.timeout,
                )
                LOGGER.info(f'Repo: {repo.owner.login}/{repo.name} {operation} success!')
            except subprocess.TimeoutExpired:
                LOGGER.error(f'Git operation timed out archiving {repo.name}.')
                if os.path.exists(repo_path):
                    shutil.rmtree(repo_path)
            except subprocess.CalledProcessError as error:
                LOGGER.error(f'Failed to {operation} {repo.name}\n{error}')
                if os.path.exists(repo_path):
                    shutil.rmtree(repo_path)
            finally:
                thread_limiter.release()

    def archive_gist(self, thread_limiter, gist, gist_path, operation):
        """Clone and pull gists based on the operation passed"""
        if (os.path.exists(gist_path) and operation == CLONE_OPERATION) or (
            not os.path.exists(gist_path) and operation == PULL_OPERATION
        ):
            pass
        else:
            commands = {
                CLONE_OPERATION: f'git clone {gist.html_url} {gist_path}',
                PULL_OPERATION: f'cd {gist_path} && git pull --rebase',
            }
            git_command = commands[operation]

            try:
                thread_limiter.acquire()
                subprocess.run(
                    git_command,
                    stdout=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True,
                    check=True,
                    timeout=self.timeout,
                )
                LOGGER.info(f'Gist: {gist.owner.login}/{gist.id} {operation} success!')
            except subprocess.TimeoutExpired:
                LOGGER.error(f'Git operation timed out archiving {gist.id}.')
                if os.path.exists(gist_path):
                    shutil.rmtree(gist_path)
            except subprocess.CalledProcessError as error:
                LOGGER.error(f'Failed to {operation} {gist.id}\n{error}')
                if os.path.exists(gist_path):
                    shutil.rmtree(gist_path)
            finally:
                thread_limiter.release()
