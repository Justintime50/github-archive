import os
from datetime import datetime
import subprocess
import time
import argparse
import logging
import logging.handlers
from threading import Thread
from github import Github

# Environment global variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORG_LIST = os.getenv('GITHUB_ARCHIVE_ORGS', '')
ORGS = ORG_LIST.split(', ')
GITHUB_ARCHIVE_LOCATION = os.path.expanduser(
    os.getenv('GITHUB_ARCHIVE_LOCATION', '~/github-archive')
)
LOGGER = logging.getLogger(__name__)

# Reusable global variables
USER = Github(GITHUB_TOKEN)
# TODO: Add user/password authentication (will need to pull from non-ssh url)
USER_REPOS = USER.get_user().get_repos()
USER_GISTS = USER.get_user().get_gists()
LOG_PATH = os.path.join(GITHUB_ARCHIVE_LOCATION, 'logs')
LOG_FILE = os.path.join(LOG_PATH, 'github-archive.log')
LOG_MAX_BYTES = int(os.getenv('GITHUB_ARCHIVE_LOG_MAX_BYTES', 1000000))  # 1mb
LOG_BACKUP_COUNT = int(os.getenv('GITHUB_ARCHIVE_LOG_BACKUP_COUNT', 5))
# BUFFER = Buffer time in between each request - helps with rate limiting
BUFFER = float(os.getenv('GITHUB_ARCHIVE_BUFFER', 0.1))
# GIT_TIMEOUT = Number of seconds before a git operation will timeout
GIT_TIMEOUT = int(os.getenv('GITHUB_ARCHIVE_TIMEOUT', 180))


class GitHubArchiveCLI():
    def __init__(self):
        """Setup the CLI arguments for the project
        """
        parser = argparse.ArgumentParser(
            description=('A powerful script to concurrently clone your entire'
                         ' GitHub instance or save it as an archive.')
        )
        parser.add_argument(
            '-uc',
            '--user-clone',
            action='store_true',
            required=False,
            help='Clone personal repos.',
        )
        parser.add_argument(
            '-up',
            '--user-pull',
            action='store_true',
            required=False,
            help='Pull personal repos',
        )
        parser.add_argument(
            '-gc',
            '--gists-clone',
            action='store_true',
            required=False,
            help='Clone personal gists',
        )
        parser.add_argument(
            '-gp',
            '--gists-pull',
            action='store_true',
            required=False,
            help='Pull personal gists.',
        )
        parser.add_argument(
            '-oc',
            '--orgs-clone',
            action='store_true',
            required=False,
            help='Clone organization repos.',
        )
        parser.add_argument(
            '-op',
            '--orgs-pull',
            action='store_true',
            required=False,
            help='Pull organization repos.',
        )
        parser.add_argument(
            '-b',
            '--branch',
            default='master',
            required=False,
            help='Which branch to pull from.',
        )
        parser.parse_args(namespace=self)

    def run(self):
        GitHubArchive().run(
            self.user_clone,
            self.user_pull,
            self.gists_clone,
            self.gists_pull,
            self.orgs_clone,
            self.orgs_pull,
            self.branch,
        )


class GitHubArchive():
    def __init__(self):
        """Initialize the tool and ensure everything is
        in order before running any logic
        """
        if not GITHUB_TOKEN:
            message = 'GITHUB_TOKEN must be present to run github-archive.'
            LOGGER.critical(message)
            raise ValueError(message)
        # Setup project directories
        if not os.path.exists(GITHUB_ARCHIVE_LOCATION):
            os.makedirs(os.path.join(GITHUB_ARCHIVE_LOCATION, 'repos'))
        if not os.path.exists(GITHUB_ARCHIVE_LOCATION):
            os.makedirs(os.path.join(GITHUB_ARCHIVE_LOCATION, 'gists'))
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        # Setup project logging (to console and log file)
        LOGGER.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        LOGGER.addHandler(logging.StreamHandler())
        LOGGER.addHandler(handler)

    @ classmethod
    def run(
        cls, user_clone, user_pull, gists_clone, gists_pull,
            orgs_clone, orgs_pull, branch):
        """Run the tool based on the arguments passed
        """
        clone = 'clone'
        pull = 'pull'
        LOGGER.info('# GitHub Archive started...\n')
        start_time = datetime.now()

        # Iterate over each personal repo and concurrently clone it
        if user_clone is True:
            LOGGER.info('# Cloning personal repos...\n')
            cls.iterate_repos(clone, branch)
        else:
            LOGGER.info('# Skipping cloning user repos...\n')

        # Iterate over each personal repo and concurrently pull it
        if user_pull is True:
            LOGGER.info('# Pulling personal repos...\n')
            cls.iterate_repos(pull, branch)
        else:
            LOGGER.info('# Skipping pulling user repos...\n')

        # Check if org variable is set
        if ORG_LIST == '':
            LOGGER.info('# Skipping org repos, no orgs configured...\n')

        # Iterate over each org repo and concurrently clone it
        if orgs_clone is True:
            LOGGER.info('# Cloning org repos...\n')
            cls.iterate_orgs(clone, branch)
        else:
            LOGGER.info('# Skipping cloning org repos...\n')

        # Iterate over each org repo and concurrently pull it
        if orgs_pull is True:
            LOGGER.info('# Pulling org repos...\n')
            cls.iterate_orgs(pull, branch)
        else:
            LOGGER.info('# Skipping cloning org repos...\n')

        # Iterate over each gist and concurrently clone it
        if gists_clone is True:
            LOGGER.info('# Cloning gists...\n')
            cls.iterate_gists(clone)
        else:
            LOGGER.info('# Skipping cloning gists...\n')

        # Iterate over each gist and concurrently pull it
        if gists_pull is True:
            LOGGER.info('# Pulling gists...\n')
            cls.iterate_gists(pull)
        else:
            LOGGER.info('# Skipping pulling gists...\n')

        execution_time = f'Execution time: {datetime.now() - start_time}.'
        finish_message = f'GitHub Archive complete! {execution_time}'
        LOGGER.info(finish_message)

    @ classmethod
    def iterate_repos(cls, operation, branch):
        """Iterate over each repository
        """
        thread_list = []
        for repo in USER_REPOS:
            # We check the owner name here to ensure that we only iterate
            # through the user's personal repos which will excludes orgs
            # that can instead be iterated by passing the "--clone_orgs"
            # or "--pull_orgs" flags to allow for granular usage
            if repo.owner.name == USER.get_user().name:
                time.sleep(BUFFER)
                path = os.path.join(
                    GITHUB_ARCHIVE_LOCATION,
                    'repos',
                    repo.owner.login,
                    repo.name
                )
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
        return True

    @classmethod
    def iterate_orgs(cls, operation, branch):
        """Iterate over each organization and its repos
        """
        thread_list = []
        for org in ORGS:
            git_org = USER.get_organization(
                org.strip()
            ).get_repos()
            for repo in git_org:
                time.sleep(BUFFER)
                path = os.path.join(
                    GITHUB_ARCHIVE_LOCATION,
                    'repos',
                    repo.owner.login,
                    repo.name
                )
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
        return True

    @classmethod
    def iterate_gists(cls, operation):
        """Iterate over each gist
        """
        thread_list = []
        for gist in USER_GISTS:
            time.sleep(BUFFER)
            path = os.path.join(
                GITHUB_ARCHIVE_LOCATION, 'gists', gist.id)
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
        return True

    @classmethod
    def archive_repo(cls, repo, branch, path, operation):
        """Clone and pull repos based on the operation passed
        """
        if operation == 'clone':
            command = (
                f'git clone --branch={branch}'
                f' {repo.ssh_url} {path}'
            )
        elif operation == 'pull':
            command = f'cd {path} && git pull --rebase'
        else:
            LOGGER.error(
                f'Could not determine what action to take with {repo}.'
            )

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
            # TODO: If we cannot clone due to the project already being clone, show a better error  # noqa
            LOGGER.error(f'Failed to {operation} {repo.name}\n{error}')
        return True

    @classmethod
    def archive_gist(cls, gist, path, operation):
        """Clone and pull gists based on the operation passed
        """
        if operation == 'clone':
            command = f'git clone {gist.html_url} {path}'
        elif operation == 'pull':
            command = f'cd {path} && git pull --rebase'
        else:
            LOGGER.warning(
                f'Could not determine what action to take with {gist}.'
            )

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
            LOGGER.error(
                f'Error: github-archive timed out archiving {gist.id}.'
            )
        except subprocess.CalledProcessError as error:
            # TODO: If we cannot clone due to the project already being clone, show a better error  # noqa
            LOGGER.error(f'Failed to {operation} {gist.id}\n{error}')
        return True


def main():
    GitHubArchiveCLI().run()


if __name__ == '__main__':
    main()
