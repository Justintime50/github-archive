import os
from datetime import datetime
import sys
import subprocess
import time
import argparse
import logging
from threading import Thread
from github import Github

# Environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORG_LIST = os.getenv('GITHUB_ARCHIVE_ORGS', '')
ORGS = ORG_LIST.split(', ')
GITHUB_ARCHIVE_LOCATION = os.path.expanduser(
    os.getenv('GITHUB_ARCHIVE_LOCATION', '~/github-archive')
)

# Reusable variables
USER = Github(GITHUB_TOKEN)
USER_REPOS = USER.get_user().get_repos()
USER_GISTS = USER.get_user().get_gists()
LOG_PATH = os.path.join(GITHUB_ARCHIVE_LOCATION, 'logs')
LOG_FILE = os.path.join(LOG_PATH, f'{datetime.now()}.log')
BUFFER = 0.1  # Buffer time in between each request - helps with rate limiting
GIT_TIMEOUT = 180  # Number of seconds before a git operation will timeout


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
            help='Clone personal repos.',
        )
        parser.add_argument(
            '-up',
            '--user-pull',
            action='store_true',
            help='Pull personal repos',
        )
        parser.add_argument(
            '-gc',
            '--gists-clone',
            action='store_true',
            help='Clone personal gists',
        )
        parser.add_argument(
            '-gp',
            '--gists-pull',
            action='store_true',
            help='Pull personal gists.',
        )
        parser.add_argument(
            '-oc',
            '--orgs-clone',
            action='store_true',
            help='Clone organization repos.',
        )
        parser.add_argument(
            '-op',
            '--orgs-pull',
            action='store_true',
            help='Pull organization repos.',
        )
        parser.add_argument(
            '-b',
            '--branch',
            default='master',
            help='Which branch to pull from.',
        )
        parser.parse_args(namespace=self)
        logging.basicConfig(level=logging.INFO)

    def run(self):
        GitHubArchive.run(
            self.user_clone,
            self.user_pull,
            self.gists_clone,
            self.gists_pull,
            self.orgs_clone,
            self.orgs_pull,
            self.branch,
        )


class GitHubArchive():
    @classmethod
    def run(
        cls, user_clone, user_pull, gists_clone, gists_pull,
            orgs_clone, orgs_pull, branch):
        """Run the based on configuration script
        """
        # Ensure everything is in order before running the tool
        if not os.path.exists(GITHUB_ARCHIVE_LOCATION):
            os.makedirs(os.path.join(GITHUB_ARCHIVE_LOCATION, 'repos'))
        if not os.path.exists(GITHUB_ARCHIVE_LOCATION):
            os.makedirs(os.path.join(GITHUB_ARCHIVE_LOCATION, 'gists'))
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        if not GITHUB_TOKEN:
            sys.exit(
                'Error: GitHub GITHUB_TOKEN must be present to run github-archive.'
            )

        logging.info('# GitHub Archive started...\n')
        start_time = datetime.now()
        cls.generate_log(start_time)

        # Iterate over each personal repo and concurrently clone it
        if user_clone is True:
            message = '# Cloning personal repos...\n'
            logging.info(message)
            cls.generate_log(message)
            switch = 'clone'
            repos = cls.iterate_repos(switch, branch)
        else:
            message = '# Skipping cloning user repos...\n'
            logging.info(message)
            cls.generate_log(message)

        # Iterate over each personal repo and concurrently pull it
        if user_pull is True:
            message = '# Pulling personal repos...\n'
            logging.info(message)
            cls.generate_log(message)
            switch = 'pull'
            repos = cls.iterate_repos(switch, branch)
        else:
            message = '# Skipping pulling user repos...\n'
            logging.info(message)
            cls.generate_log(message)

        # Check if org variable is set
        if ORG_LIST == '':
            message = '# Skipping org repos, no orgs configured...\n'
            logging.info(message)
            cls.generate_log(message)

        # Iterate over each org repo and concurrently clone it
        if orgs_clone is True:
            message = '# Cloning org repos...\n'
            logging.info(message)
            cls.generate_log(message)
            switch = 'clone'
            orgs = cls.iterate_orgs(switch, branch)
        else:
            data = '# Skipping cloning org repos...\n'
            print(data)
            cls.generate_log(data)

        # Iterate over each org repo and concurrently pull it
        if orgs_pull is True:
            message = '# Pulling org repos...\n'
            logging.info(message)
            cls.generate_log(message)
            switch = 'pull'
            orgs = cls.iterate_orgs(switch, branch)
        else:
            data = '# Skipping cloning org repos...\n'
            print(data)
            cls.generate_log(data)

        # Iterate over each gist and concurrently clone it
        if gists_clone is True:
            message = '# Cloning gists...\n'
            logging.info(message)
            cls.generate_log(message)
            switch = 'clone'
            gists = cls.iterate_gists(switch)
        else:
            data = '# Skipping cloning gists...\n'
            logging.info(data)
            cls.generate_log(data)

        # Iterate over each gist and concurrently pull it
        if gists_pull is True:
            message = '# Pulling gists...\n'
            logging.info(message)
            cls.generate_log(message)
            switch = 'pull'
            gists = cls.iterate_gists(switch)
        else:
            data = '# Skipping pulling gists...\n'
            logging.info(data)
            cls.generate_log(data)

        execution_time = f'Execution time: {datetime.now() - start_time}.'
        finish_message = f'GitHub Archive complete! {execution_time}'
        logging.info(finish_message)
        cls.generate_log(finish_message)

    @classmethod
    def iterate_repos(cls, switch, branch):
        """Iterate over each repository
        """
        thread_list = []
        for repo in USER_REPOS:
            if repo.owner.name == USER.get_user().name:
                time.sleep(BUFFER)
                path = os.path.join(
                    GITHUB_ARCHIVE_LOCATION, 'repos', repo.owner.login, repo.name
                )
                repo_thread = Thread(
                    target=cls.archive_repo,
                    args=(
                        repo,
                        branch,
                        path,
                        switch,
                    )
                )
                thread_list.append(repo_thread)
                repo_thread.start()
        for thread in thread_list:
            thread.join()
        return True

    @classmethod
    def iterate_orgs(cls, switch, branch):
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
                    GITHUB_ARCHIVE_LOCATION, 'repos', repo.owner.login, repo.name
                )
                repo_thread = Thread(
                    target=cls.archive_repo,
                    args=(
                        repo,
                        branch,
                        path,
                        switch,
                    )
                )
                thread_list.append(repo_thread)
                repo_thread.start()
        for thread in thread_list:
            thread.join()
        return True

    @classmethod
    def iterate_gists(cls, switch):
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
                    switch,
                )
            )
            thread_list.append(repo_thread)
            repo_thread.start()
        for thread in thread_list:
            thread.join()
        return True

    @classmethod
    def archive_repo(cls, repo, branch, path, switch):
        """Clone and pull repos based on the switch passed
        """
        if switch == 'clone':
            command = (
                f'git clone --branch={branch}'
                f' {repo.ssh_url} {path}'
            )
        elif switch == 'pull':
            command = f'cd {path} && git pull --rebase'
        else:
            sys.exit(f'Could not determine what action to take with {repo}.')

        try:
            subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
                check=True,
                timeout=int(GIT_TIMEOUT)
            )
            message = f'Repo: {repo.name} {switch} success!'
            logging.info(message)
            cls.generate_log(message)
        except subprocess.TimeoutExpired:
            # TODO: Why do we sys.exit here but log and keep going below?
            sys.exit(
                f'Error: github-archive timed out archiving {repo.name}.'
            )
        except subprocess.CalledProcessError as error:
            # TODO: If it cannot clone due to the folder being there, show a better error
            data = f'Failed to {switch} {repo.name}\n{error}'
            logging.error(data)
            cls.generate_log(data)
        return True

    @classmethod
    def archive_gist(cls, gist, path, switch):
        """Clone and pull gists based on the switch passed
        """
        if switch == 'clone':
            command = f'git clone {gist.html_url} {path}'
        elif switch == 'pull':
            command = f'cd {path} && git pull --rebase'
        else:
            sys.exit(f'Could not determine what action to take with {gist}.')

        try:
            subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
                check=True,
                timeout=int(GIT_TIMEOUT)
            )
            message = f'Gist: {gist.id} {switch} success!'
            logging.info(message)
            cls.generate_log(message)
        except subprocess.TimeoutExpired:
            # TODO: Why do we sys.exit here but log and keep going below?
            sys.exit(f'Error: github-archive timed out archiving {gist.id}.')
        except subprocess.CalledProcessError as error:
            message = f'Failed to {switch} {gist.id}\n{error}'
            logging.error(message)
            cls.generate_log(message)
        return True

    @classmethod
    def generate_log(cls, data):
        """Write output to a log
        """
        with open(LOG_FILE, 'a') as log:
            # TODO: CHANGE THE LOG FILENAME TO WORK ON WINDOWS
            log.write(f'\n{data}')
        return log


def main():
    GitHubArchiveCLI().run()


if __name__ == '__main__':
    main()
