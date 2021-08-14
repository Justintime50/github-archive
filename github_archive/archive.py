import logging
import os
import subprocess
import time
from datetime import datetime
from threading import Thread

from github import Github

from github_archive.logger import Logger

# TODO: Add user/password authentication (will need to pull from non-ssh url)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USER = Github(GITHUB_TOKEN).get_user()
ORG_LIST = os.getenv('GITHUB_ARCHIVE_ORGS', '')
ORGS = ORG_LIST.split(',')

GIT_TIMEOUT = int(os.getenv('GITHUB_ARCHIVE_TIMEOUT', 180))
GITHUB_ARCHIVE_LOCATION = os.path.expanduser(os.getenv('GITHUB_ARCHIVE_LOCATION', '~/github-archive'))
SUBPROCESS_BUFFER = float(
    os.getenv('GITHUB_ARCHIVE_BUFFER', 0.1)
)  # TODO: This can most likely be removed once we limit the number of open threads at once

LOGGER = logging.getLogger(__name__)
CLONE_OPERATION = 'clone'
ORG_CONTEXT = 'orgs'
PULL_OPERATION = 'pull'
USER_CONTEXT = 'user'


class GithubArchive:
    @staticmethod
    def run(user_clone=False, user_pull=False, gists_clone=False, gists_pull=False, orgs_clone=False, orgs_pull=False):
        """Run the tool based on the arguments passed."""
        GithubArchive.initialize_project(orgs_clone, orgs_pull)
        Logger._setup_logging(LOGGER)
        LOGGER.info('# GitHub Archive started...\n')
        start_time = datetime.now()

        # Make API calls
        if user_clone or user_pull:
            LOGGER.info('# Making API call to GitHub for personal repos...\n')
            repos = GithubArchive.get_repos()
        if orgs_clone or orgs_pull:
            LOGGER.info('# Making API calls to GitHub for org repos...\n')
            org_repos = GithubArchive.get_all_org_repos()
        if gists_clone or gists_pull:
            LOGGER.info('# Making API call to GitHub for personal gists...\n')
            gists = GithubArchive.get_gists()

        # Git operations
        if user_clone is True:
            LOGGER.info('# Cloning missing personal repos...\n')
            GithubArchive.iterate_repos_to_archive(repos, USER_CONTEXT, CLONE_OPERATION)
        if user_pull is True:
            LOGGER.info('# Pulling personal repos...\n')
            GithubArchive.iterate_repos_to_archive(repos, USER_CONTEXT, PULL_OPERATION)

        if orgs_clone is True:
            LOGGER.info('# Cloning missing org repos...\n')
            GithubArchive.iterate_repos_to_archive(org_repos, ORG_CONTEXT, CLONE_OPERATION)
        if orgs_pull is True:
            LOGGER.info('# Pulling org repos...\n')
            GithubArchive.iterate_repos_to_archive(org_repos, ORG_CONTEXT, PULL_OPERATION)

        if gists_clone is True:
            LOGGER.info('# Cloning missing gists...\n')
            GithubArchive.iterate_gists_to_archive(gists, CLONE_OPERATION)
        if gists_pull is True:
            LOGGER.info('# Pulling gists...\n')
            GithubArchive.iterate_gists_to_archive(gists, PULL_OPERATION)

        execution_time = f'Execution time: {datetime.now() - start_time}.'
        finish_message = f'GitHub Archive complete! {execution_time}\n'
        LOGGER.info(finish_message)

    @staticmethod
    def initialize_project(orgs_clone, orgs_pull):
        """Initialize the tool and ensure everything is in order before running any logic."""
        if not GITHUB_TOKEN:
            message = 'GITHUB_TOKEN must be present to run github-archive.'
            LOGGER.critical(message)
            raise ValueError(message)

        if not ORG_LIST and (orgs_clone or orgs_pull):
            message = 'GITHUB_ARCHIVE_ORGS must be present when passing org flags.'
            LOGGER.critical(message)
            raise ValueError(message)

        if not os.path.exists(GITHUB_ARCHIVE_LOCATION):
            os.makedirs(os.path.join(GITHUB_ARCHIVE_LOCATION, 'repos'))

        if not os.path.exists(GITHUB_ARCHIVE_LOCATION):
            os.makedirs(os.path.join(GITHUB_ARCHIVE_LOCATION, 'gists'))

    @staticmethod
    def get_repos():
        """Retrieve all repos of the authenticated user."""
        repos = USER.get_repos()
        LOGGER.debug('User repos retrieved!')

        return repos

    @staticmethod
    def get_all_org_repos():
        """Retrieve repos of all orgs in the orgs list provided and return a single list
        including every repo from each org flattened.
        """
        all_org_repos = []
        for org in ORGS:
            org_repos = Github(GITHUB_TOKEN).get_organization(org.strip()).get_repos()
            all_org_repos.append(org_repos)
            LOGGER.debug(f'{org.strip()} repos retrieved!')

        flattened_org_repos_list = [repo for org_repos in all_org_repos for repo in org_repos]

        return flattened_org_repos_list

    @staticmethod
    def get_gists():
        """Retrieve all gists of the authenticated user."""
        gists = USER.get_gists()
        LOGGER.debug('User gists retrieved!')

        return gists

    @staticmethod
    def iterate_repos_to_archive(repos, context, operation):
        """Iterate over each repository and start a thread if it can be archived."""
        thread_list = []
        for repo in repos:
            # We check the owner name here to ensure that we only iterate
            # through the user's personal repos which will exclude orgs
            # that can instead be iterated by passing the "--clone_orgs"
            # or "--pull_orgs" flags to allow for more granular control.
            if repo.owner.name != USER.name and context == USER_CONTEXT:
                continue
            else:
                time.sleep(SUBPROCESS_BUFFER)
                repo_path = os.path.join(GITHUB_ARCHIVE_LOCATION, 'repos', repo.owner.login, repo.name)
                repo_thread = Thread(
                    target=GithubArchive.archive_repo,
                    args=(
                        repo,
                        repo_path,
                        operation,
                    ),
                )
                thread_list.append(repo_thread)
                repo_thread.start()
        for thread in thread_list:
            thread.join()

    @staticmethod
    def iterate_gists_to_archive(gists, operation):
        """Iterate over each gist and start a thread if it can be archived."""
        thread_list = []
        for gist in gists:
            time.sleep(SUBPROCESS_BUFFER)
            gist_path = os.path.join(GITHUB_ARCHIVE_LOCATION, 'gists', gist.id)
            gist_thread = Thread(
                target=GithubArchive.archive_gist,
                args=(
                    gist,
                    gist_path,
                    operation,
                ),
            )
            thread_list.append(gist_thread)
            gist_thread.start()
        for thread in thread_list:
            thread.join()

    @staticmethod
    def archive_repo(repo, repo_path, operation):
        """Clone and pull repos based on the operation passed"""
        if os.path.exists(repo_path) and operation == CLONE_OPERATION:
            LOGGER.debug(f'Repo: {repo.name} already cloned, skipping clone operation.')
        else:
            commands = {
                CLONE_OPERATION: f'git clone {repo.ssh_url} {repo_path}',
                PULL_OPERATION: f'cd {repo_path} && git pull --rebase',
            }
            git_command = commands[operation]

            try:
                subprocess.run(
                    git_command,
                    stdin=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True,
                    check=True,
                    timeout=GIT_TIMEOUT,
                )
                # TODO: If the response of pulling is `Already up to date.`, skip outputting to the logger
                LOGGER.info(f'Repo: {repo.name} {operation} success!')
            except subprocess.TimeoutExpired:
                LOGGER.error(f'Git operation timed out archiving {repo.name}.')
            except subprocess.CalledProcessError as error:
                LOGGER.error(f'Failed to {operation} {repo.name}\n{error}')

    @staticmethod
    def archive_gist(gist, gist_path, operation):
        """Clone and pull gists based on the operation passed"""
        if os.path.exists(gist_path) and operation == CLONE_OPERATION:
            LOGGER.debug(f'Gist: {gist.id} already cloned, skipping clone operation.')
        else:
            commands = {
                CLONE_OPERATION: f'git clone {gist.html_url} {gist_path}',
                PULL_OPERATION: f'cd {gist_path} && git pull --rebase',
            }
            git_command = commands[operation]

            try:
                subprocess.run(
                    git_command,
                    stdin=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True,
                    check=True,
                    timeout=GIT_TIMEOUT,
                )
                # TODO: If the response of pulling is `Already up to date.`, skip outputting to the logger
                LOGGER.info(f'Gist: {gist.id} {operation} success!')
            except subprocess.TimeoutExpired:
                LOGGER.error(f'Git operation timed out archiving {gist.id}.')
            except subprocess.CalledProcessError as error:
                LOGGER.error(f'Failed to {operation} {gist.id}\n{error}')
