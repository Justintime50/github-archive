import logging
import os
import subprocess
from datetime import datetime
from threading import BoundedSemaphore, Thread

from github import Github

from github_archive.logger import Logger

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_LOGIN = Github(GITHUB_TOKEN)
AUTHENTICATED_GITHUB_USER = GITHUB_LOGIN.get_user()
ORG_LIST = os.getenv('GITHUB_ARCHIVE_ORGS', '')
ORGS = ORG_LIST.split(',')
USER_LIST = os.getenv('GITHUB_ARCHIVE_USERS', '')
USERS = USER_LIST.split(',')

GIT_TIMEOUT = int(os.getenv('GITHUB_ARCHIVE_TIMEOUT', 300))
GITHUB_ARCHIVE_LOCATION = os.path.expanduser(os.getenv('GITHUB_ARCHIVE_LOCATION', '~/github-archive'))
DEFAULT_NUM_THREADS = 10

LOGGER = logging.getLogger(__name__)
CLONE_OPERATION = 'clone'
ORG_CONTEXT = 'orgs'
PERSONAL_CONTEXT = 'personal'
PULL_OPERATION = 'pull'
USER_CONTEXT = 'user'


class GithubArchive:
    @staticmethod
    def run(
        personal_clone=False,
        personal_pull=False,
        users_clone=False,
        users_pull=False,
        gists_clone=False,
        gists_pull=False,
        orgs_clone=False,
        orgs_pull=False,
        num_of_threads=DEFAULT_NUM_THREADS,
    ):
        """Run the tool based on the arguments passed."""
        GithubArchive.initialize_project(users_clone, users_pull, orgs_clone, orgs_pull)
        Logger._setup_logging(LOGGER)
        LOGGER.info('# GitHub Archive started...\n')
        start_time = datetime.now()

        # Make API calls
        # TODO: If we decide to remove the `personal` flag here, we need a new way to get private repos
        # for the authenticated user. We could do this by making a separate API call to the get_user endpoint
        # of the users passing the API key based on the name in the `users` list and the authed user.
        if personal_clone or personal_pull:
            LOGGER.info('# Making API call to GitHub for personal repos...\n')
            personal_repos = GithubArchive.get_personal_repos()
        if users_clone or users_pull:
            LOGGER.info('# Making API calls to GitHub for user repos...\n')
            user_repos = GithubArchive.get_all_user_repos()
        if orgs_clone or orgs_pull:
            LOGGER.info('# Making API calls to GitHub for org repos...\n')
            org_repos = GithubArchive.get_all_org_repos()
        if gists_clone or gists_pull:
            LOGGER.info('# Making API call to GitHub for personal gists...\n')
            gists = GithubArchive.get_gists()

        # Git operations
        # TODO: Rework a class that can share all these values so we don't need to pass
        # along all these variables across the app.
        if personal_clone is True:
            LOGGER.info('# Cloning missing personal repos...\n')
            GithubArchive.iterate_repos_to_archive(num_of_threads, personal_repos, PERSONAL_CONTEXT, CLONE_OPERATION)
        if personal_pull is True:
            LOGGER.info('# Pulling personal repos...\n')
            GithubArchive.iterate_repos_to_archive(num_of_threads, personal_repos, PERSONAL_CONTEXT, PULL_OPERATION)

        if users_clone is True:
            LOGGER.info('# Cloning missing user repos...\n')
            GithubArchive.iterate_repos_to_archive(num_of_threads, user_repos, USER_CONTEXT, CLONE_OPERATION)
        if users_pull is True:
            LOGGER.info('# Pulling user repos...\n')
            GithubArchive.iterate_repos_to_archive(num_of_threads, user_repos, USER_CONTEXT, PULL_OPERATION)

        if orgs_clone is True:
            LOGGER.info('# Cloning missing org repos...\n')
            GithubArchive.iterate_repos_to_archive(num_of_threads, org_repos, ORG_CONTEXT, CLONE_OPERATION)
        if orgs_pull is True:
            LOGGER.info('# Pulling org repos...\n')
            GithubArchive.iterate_repos_to_archive(num_of_threads, org_repos, ORG_CONTEXT, PULL_OPERATION)

        if gists_clone is True:
            LOGGER.info('# Cloning missing gists...\n')
            GithubArchive.iterate_gists_to_archive(num_of_threads, gists, CLONE_OPERATION)
        if gists_pull is True:
            LOGGER.info('# Pulling gists...\n')
            GithubArchive.iterate_gists_to_archive(num_of_threads, gists, PULL_OPERATION)

        execution_time = f'Execution time: {datetime.now() - start_time}.'
        finish_message = f'GitHub Archive complete! {execution_time}\n'
        LOGGER.info(finish_message)

    @staticmethod
    def initialize_project(users_clone, users_pull, orgs_clone, orgs_pull):
        """Initialize the tool and ensure everything is in order before running any logic."""
        if not GITHUB_TOKEN:
            message = 'GITHUB_TOKEN must be present to run github-archive.'
            LOGGER.critical(message)
            raise ValueError(message)

        if not USER_LIST and (users_clone or users_pull):
            message = 'GITHUB_ARCHIVE_USERS must be present when passing user flags.'
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
    def get_personal_repos():
        """Retrieve all repos of the authenticated user."""
        repos = AUTHENTICATED_GITHUB_USER.get_repos()
        LOGGER.debug('Personal repos retrieved!')

        return repos

    @staticmethod
    def get_all_user_repos():
        """Retrieve repos of all users in the users list provided and return a single list
        including every repo from each user flattened.
        """
        all_user_repos = []
        for user in USERS:
            formatted_user_name = user.strip()
            user_repos = GITHUB_LOGIN.get_user(formatted_user_name).get_repos()
            all_user_repos.append(user_repos)
            LOGGER.debug(f'{formatted_user_name} repos retrieved!')

        flattened_user_repos_list = [repo for user_repos in all_user_repos for repo in user_repos]

        return flattened_user_repos_list

    @staticmethod
    def get_all_org_repos():
        """Retrieve repos of all orgs in the orgs list provided and return a single list
        including every repo from each org flattened.
        """
        all_org_repos = []
        for org in ORGS:
            formatted_org_name = org.strip()
            org_repos = GITHUB_LOGIN.get_organization(formatted_org_name).get_repos()
            all_org_repos.append(org_repos)
            LOGGER.debug(f'{formatted_org_name} repos retrieved!')

        flattened_org_repos_list = [repo for org_repos in all_org_repos for repo in org_repos]

        return flattened_org_repos_list

    @staticmethod
    def get_gists():
        """Retrieve all gists of the authenticated user."""
        gists = AUTHENTICATED_GITHUB_USER.get_gists()
        LOGGER.debug('User gists retrieved!')

        return gists

    @staticmethod
    def iterate_repos_to_archive(num_of_threads, repos, context, operation):
        """Iterate over each repository and start a thread if it can be archived."""
        thread_list = []
        for repo in repos:
            # We check the owner name here to ensure that we only iterate
            # through the user's personal repos which will exclude orgs.
            #
            # This is important because PyGithub will include a user's org repos
            # in the list of repos for an authenticated user out of the box.
            #
            # Instead, the user can pass the "--clone_orgs" or "--pull_orgs"
            # flags to allow for more granular control over which repos they get.
            if repo.owner.name != AUTHENTICATED_GITHUB_USER.name and context == PERSONAL_CONTEXT:
                continue
            else:
                thread_limiter = BoundedSemaphore(num_of_threads)
                repo_path = os.path.join(GITHUB_ARCHIVE_LOCATION, 'repos', repo.owner.login, repo.name)
                repo_thread = Thread(
                    target=GithubArchive.archive_repo,
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

    @staticmethod
    def iterate_gists_to_archive(num_of_threads, gists, operation):
        """Iterate over each gist and start a thread if it can be archived."""
        thread_limiter = BoundedSemaphore(num_of_threads)
        thread_list = []
        for gist in gists:
            gist_path = os.path.join(GITHUB_ARCHIVE_LOCATION, 'gists', gist.id)
            gist_thread = Thread(
                target=GithubArchive.archive_gist,
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

    @staticmethod
    def archive_repo(thread_limiter, repo, repo_path, operation):
        """Clone and pull repos based on the operation passed"""
        if os.path.exists(repo_path) and operation == CLONE_OPERATION:
            # TODO: There is a bug here if a repo times out or has another error but the folder got created
            # where the repo won't finish getting cloned and therefore can't reliably get pulled in the future.
            # Look into a better way to assert this was successful before skipping.
            # TODO: Move the debug line into the exception block and delete the failed folder so that on a future
            # run, the app will attempt to re-clone the project
            LOGGER.debug(f'Repo: {repo.name} already cloned, skipping clone operation.')
        else:
            commands = {
                CLONE_OPERATION: f'git clone {repo.ssh_url} {repo_path}',
                PULL_OPERATION: f'cd {repo_path} && git pull --rebase',
            }
            git_command = commands[operation]

            try:
                thread_limiter.acquire()
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
            finally:
                thread_limiter.release()

    @staticmethod
    def archive_gist(thread_limiter, gist, gist_path, operation):
        """Clone and pull gists based on the operation passed"""
        if os.path.exists(gist_path) and operation == CLONE_OPERATION:
            # TODO: There is a bug here if a repo times out or has another error but the folder got created
            # where the repo won't finish getting cloned and therefore can't reliably get pulled in the future.
            # Look into a better way to assert this was successful before skipping.
            # TODO: Move the debug line into the exception block and delete the failed folder so that on a future
            # run, the app will attempt to re-clone the project
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
            finally:
                thread_limiter.release()
