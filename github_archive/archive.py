import os
from datetime import datetime
import subprocess
import time
import logging
from threading import Thread
from github import Github
from github_archive.logger import Logger


# Environment global variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORG_LIST = os.getenv('GITHUB_ARCHIVE_ORGS', '')
ORGS = ORG_LIST.split(', ')
GITHUB_ARCHIVE_LOCATION = os.path.expanduser(
    os.getenv('GITHUB_ARCHIVE_LOCATION', '~/github-archive')
)
LOGGER = logging.getLogger(__name__)

# Reusable global variables
USER = Github(GITHUB_TOKEN).get_user()
# TODO: Add user/password authentication (will need to pull from non-ssh url)
# BUFFER is the time in between each request - helps with rate limiting
BUFFER = float(os.getenv('GITHUB_ARCHIVE_BUFFER', 0.1))
# GIT_TIMEOUT is the number of seconds before a git operation will timeout
GIT_TIMEOUT = int(os.getenv('GITHUB_ARCHIVE_TIMEOUT', 180))


class GithubArchive():
    @classmethod
    def run(cls, user_clone, user_pull, gists_clone, gists_pull, orgs_clone, orgs_pull, branch):
        """Run the tool based on the arguments passed
        """
        cls.initialize_project()
        Logger._setup_logging(LOGGER)
        clone = 'clone'
        pull = 'pull'
        LOGGER.info('# GitHub Archive started...\n')
        start_time = datetime.now()

        if user_clone or user_pull:
            repos = cls.get_repos()

        # Iterate over each personal repo and concurrently clone it
        if user_clone is True:
            LOGGER.info('# Cloning personal repos...\n')
            cls.determine_repo_context(repos, 'user', clone, branch)
        else:
            LOGGER.info('# Skipping cloning user repos...\n')

        # Iterate over each personal repo and concurrently pull it
        if user_pull is True:
            LOGGER.info('# Pulling personal repos...\n')
            cls.determine_repo_context(repos, 'user', pull, branch)
        else:
            LOGGER.info('# Skipping pulling user repos...\n')

        # Check if org list is populated
        if ORG_LIST != '':
            if orgs_clone or orgs_pull:
                org_repos = cls.get_all_org_repos()
            # Iterate over each org repo and concurrently clone it
            if orgs_clone is True:
                LOGGER.info('# Cloning org repos...\n')
                cls.determine_repo_context(org_repos, 'orgs', clone, branch)
            else:
                LOGGER.info('# Skipping cloning org repos...\n')
            # Iterate over each org repo and concurrently pull it
            if orgs_pull is True:
                LOGGER.info('# Pulling org repos...\n')
                cls.determine_repo_context(org_repos, 'orgs', pull, branch)
            else:
                LOGGER.info('# Skipping cloning org repos...\n')
        else:
            LOGGER.info('# Skipping org repos, no orgs configured...\n')

        if gists_clone or gists_pull:
            gists = cls.get_gists()

        # Iterate over each gist and concurrently clone it
        if gists_clone is True:
            LOGGER.info('# Cloning gists...\n')
            cls.iterate_gists(gists, clone)
        else:
            LOGGER.info('# Skipping cloning gists...\n')

        # Iterate over each gist and concurrently pull it
        if gists_pull is True:
            LOGGER.info('# Pulling gists...\n')
            cls.iterate_gists(gists, pull)
        else:
            LOGGER.info('# Skipping pulling gists...\n')

        execution_time = f'Execution time: {datetime.now() - start_time}.'
        finish_message = f'GitHub Archive complete! {execution_time}\n'
        LOGGER.info(finish_message)

    @classmethod
    def initialize_project(cls):
        """Initialize the tool and ensure everything is
        in order before running any logic
        """
        if not GITHUB_TOKEN:
            message = 'GITHUB_TOKEN must be present to run github-archive.'
            LOGGER.critical(message)
            raise ValueError(message)
        if not os.path.exists(GITHUB_ARCHIVE_LOCATION):
            os.makedirs(os.path.join(GITHUB_ARCHIVE_LOCATION, 'repos'))
        if not os.path.exists(GITHUB_ARCHIVE_LOCATION):
            os.makedirs(os.path.join(GITHUB_ARCHIVE_LOCATION, 'gists'))

    @classmethod
    def get_repos(cls):
        """Retrieve repos of a given user
        """
        repos = USER.get_repos()
        return repos

    @classmethod
    def get_all_org_repos(cls):
        """Retrieve repos of all orgs in the orgs list
        """
        all_org_repos = []
        for org in ORGS:
            all_org_repos.append(Github(GITHUB_TOKEN).get_organization(org.strip()).get_repos())
        return all_org_repos

    @classmethod
    def get_gists(cls):
        """Retrieve gists of a given user
        """
        gists = USER.get_gists()
        return gists

    @classmethod
    def determine_repo_context(cls, repos, context, operation, branch):
        """Determine if a repo is from a user or org
        and route the logic accordingly
        """
        if context == 'orgs':
            for single_org_repos in repos:
                cls.iterate_repos(single_org_repos, context, operation, branch)
        elif context == 'user':
            cls.iterate_repos(repos, context, operation, branch)
        else:
            message = f'Could not determine what action to take with {context}.'
            LOGGER.error(message)
            raise ValueError(message)

    @classmethod
    def iterate_repos(cls, repos, context, operation, branch):
        """Iterate over each repository
        """
        thread_list = []
        for repo in repos:
            # We check the owner name here to ensure that we only iterate
            # through the user's personal repos which will exclude orgs
            # that can instead be iterated by passing the "--clone_orgs"
            # or "--pull_orgs" flags to allow for granular control
            if repo.owner.name != USER.name and context == 'user':
                continue
            else:
                time.sleep(BUFFER)
                path = os.path.join(GITHUB_ARCHIVE_LOCATION, 'repos', repo.owner.login, repo.name)
                repo_thread = Thread(
                    target=cls.archive_repo,
                    args=(
                        repo,
                        branch,
                        path,
                        operation,
                    )
                )
                thread_list.append(repo_thread)
                repo_thread.start()
        for thread in thread_list:
            thread.join()

    @classmethod
    def iterate_gists(cls, gists, operation):
        """Iterate over each gist
        """
        thread_list = []
        for gist in gists:
            time.sleep(BUFFER)
            path = os.path.join(GITHUB_ARCHIVE_LOCATION, 'gists', gist.id)
            repo_thread = Thread(
                target=cls.archive_gist,
                args=(
                    gist,
                    path,
                    operation,
                )
            )
            thread_list.append(repo_thread)
            repo_thread.start()
        for thread in thread_list:
            thread.join()

    @classmethod
    def archive_repo(cls, repo, branch, path, operation):
        """Clone and pull repos based on the operation passed
        """
        if os.path.exists(path) and operation == 'clone':
            LOGGER.info(f'Repo: {repo.name} already cloned, skipping clone operation.')
        else:
            if operation == 'clone':
                command = (f'git clone --branch={branch} {repo.ssh_url} {path}')
            elif operation == 'pull':
                command = f'cd {path} && git pull --rebase'
            else:
                message = f'Could not determine what action to take with {repo.name} based on {operation}.'
                LOGGER.error(message)
                raise ValueError(message)

            try:
                subprocess.run(
                    command,
                    stdin=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True,
                    check=True,
                    timeout=int(GIT_TIMEOUT)
                )
                LOGGER.info(f'Repo: {repo.name} {operation} success!')
            except subprocess.TimeoutExpired:
                LOGGER.error(f'Git operation timed out archiving {repo.name}.')
            except subprocess.CalledProcessError as error:
                LOGGER.error(f'Failed to {operation} {repo.name}\n{error}')

    @classmethod
    def archive_gist(cls, gist, path, operation):
        """Clone and pull gists based on the operation passed
        """
        if os.path.exists(path) and operation == 'clone':
            LOGGER.info(f'Gist: {gist.id} already cloned, skipping clone operation.')
        else:
            if operation == 'clone':
                command = f'git clone {gist.html_url} {path}'
            elif operation == 'pull':
                command = f'cd {path} && git pull --rebase'
            else:
                message = f'Could not determine what action to take with {gist.id} based on {operation}.'
                LOGGER.error(message)
                raise ValueError(message)

            try:
                subprocess.run(
                    command,
                    stdin=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True,
                    check=True,
                    timeout=int(GIT_TIMEOUT)
                )
                LOGGER.info(f'Gist: {gist.id} {operation} success!')
            except subprocess.TimeoutExpired:
                LOGGER.error(f'Git operation timed out archiving {gist.id}.')
            except subprocess.CalledProcessError as error:
                LOGGER.error(f'Failed to {operation} {gist.id}\n{error}')
