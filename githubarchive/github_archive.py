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
TOKEN = os.getenv('GITHUB_ARCHIVE_TOKEN')
ORG_LIST = os.getenv('GITHUB_ARCHIVE_ORGS', '')
ORGS = ORG_LIST.split(', ')
LOCATION = os.path.expanduser(
    os.getenv('GITHUB_ARCHIVE_LOCATION', '~/github-archive')
)

# Reusable variables
USER = Github(TOKEN)
USER_REPOS = USER.get_user().get_repos()
USER_GISTS = USER.get_user().get_gists()
LOG_PATH = os.path.join(LOCATION, 'logs')
LOG_FILE = os.path.join(LOG_PATH, f'{datetime.now()}.log')
BUFFER = 0.1  # Buffer time in between each request - helps with rate limiting
GIT_TIMEOUT = 180  # Number of seconds before a git operation will timeout


class GitHubArchiveCLI():
    def __init__(self):
        """Setup the CLI arguments for the project
        """
        parser = argparse.ArgumentParser(
            description=('A powerful script to concurrently clone your entire'
                         ' GitHub instance or save it as an cls.')
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

        # def run(self):
        #     # TODO: ADD STUFF HERE


class GitHubArchive():
    @classmethod
    def run(cls):
        """Run the based on configuration script
        """
        # Ensure everything is in order before running the tool
        if not os.path.exists(cls.LOCATION):
            os.makedirs(os.path.join(cls.LOCATION, 'repos'))
        if not os.path.exists(cls.LOCATION):
            os.makedirs(os.path.join(cls.LOCATION, 'gists'))
        if not cls.TOKEN:
            sys.exit(
                'Error: GitHub token must be present to run github-cls.'
            )

        logging.info('GitHub Archive started...')
        start_time = datetime.now()
        cls.generate_log(start_time)
        thread_list = []

        # Iterate over each personal repo and concurrently start cloning
        if cls.args.user_clone is True:
            message = '## Cloning personal repos... ##\n'
            logging.info(message)
            cls.generate_log(message)
            switch = 'clone'
            repos = cls.iterate_repos(switch, thread_list)
        else:
            message = '## Skipping cloning user repos... ##'
            logging.info(message)
            cls.generate_log(message)

        # Iterate over each personal repo and concurrently start pulling
        if cls.args.user_pull is True:
            message = '## Pulling personal repos... ##\n'
            logging.info(message)
            cls.generate_log(message)
            switch = 'pull'
            repos = cls.iterate_repos(switch, thread_list)
        else:
            message = '## Skipping pulling user repos...## '
            logging.info(message)
            cls.generate_log(message)

        # Iterate over each gist and concurrently start cloning
        if cls.args.gists_clone is True:
            message = '## Cloning gists... ##\n'
            logging.info(message)
            cls.generate_log(message)
            switch = 'clone'
            gists = cls.iterate_gists(switch, thread_list)
        else:
            data = '## Skipping cloning gists... ##'
            logging.info(data)
            cls.generate_log(data)

        # Iterate over each gist and concurrently start pulling
        if cls.args.gists_pull is True:
            message = '## Pulling gists... ##\n'
            logging.info(message)
            cls.generate_log(message)
            switch = 'pull'
            gists = cls.iterate_gists(switch, thread_list)
        else:
            data = '## Skipping pulling gists... ##'
            logging.info(data)
            cls.generate_log(data)

        # # Check if org variable is set
        # if cls.ORG_LIST == '':
        #     data = '## Skipping org repos, no organizations specified... ##'
        #     print(data)
        #     cls.generate_log(data)
        # else:
        #     # Iterate over each organization repo and concurrently start cloning
        #     if cls.args.orgs_clone is True:
        #         for org in cls.ORGS:
        #             message = f'## Cloning {org} repos... ##\n'
        #             print(message)
        #             cls.generate_log(message)
        #             git_org = cls.USER.get_organization(
        #                 org.strip()).get_repos()
        #             for repo in git_org:
        #                 time.sleep(cls.BUFFER)
        #                 path = os.path.join(
        #                     cls.LOCATION, 'repos', repo.owner.login, repo.name)
        #                 repo_thread = Thread(target=cls.clone_repos, args=(
        #                     repo, path,))
        #                 thread_list.append(repo_thread)
        #                 repo_thread.start()
        #     else:
        #         data = '## Skipping cloning org repos... ##'
        #         print(data)
        #         cls.generate_log(data)

        #     # Iterate over each organization repo and concurrently start pulling
        #     if cls.args.orgs_pull is True:
        #         for org in cls.ORGS:
        #             message = f'## Pulling {org} repos... ##\n'
        #             print(message)
        #             cls.generate_log(message)
        #             git_org = cls.USER.get_organization(
        #                 org.strip()).get_repos()
        #             for repo in git_org:
        #                 time.sleep(cls.BUFFER)
        #                 path = os.path.join(
        #                     cls.LOCATION, 'repos', repo.owner.login, repo.name)
        #                 repo_thread = Thread(target=cls.pull_repos, args=(
        #                     repo, path,))
        #                 thread_list.append(repo_thread)
        #                 repo_thread.start()
        #     else:
        #         data = '## Skipping pulling org repos... ##'
        #         print(data)
        #         cls.generate_log(data)

        for thread in thread_list:
            thread.join()
        execution_time = f'Execution time: {datetime.now() - start_time}.'
        finish_message = f'GitHub Archive complete! {execution_time}'
        print(finish_message)
        cls.generate_log(finish_message)

    @classmethod
    def iterate_repos(cls, switch, thread_list):
        """Iterate over each repository
        """
        for repo in cls.USER_REPOS:
            if repo.owner.name == cls.USER.get_user().name:
                time.sleep(cls.BUFFER)
                path = os.path.join(
                    cls.LOCATION, 'repos', repo.owner.login, repo.name
                )
                repo_thread = Thread(
                    target=cls.archive_repo,
                    args=(
                        repo,
                        path,
                        switch,
                    )
                )
                thread_list.append(repo_thread)
                repo_thread.start()
        # TODO: Return something meaningful
        # return 

    @classmethod
    def archive_repo(cls, repo, path, switch):
        """Clone and pull repos based on the switch passed
        """
        if switch == 'clone':
            command = (
                f'git clone --branch={cls.args.branch}'
                f' {repo.ssh_url} {path}'
            )
        elif switch == 'pull':
            command = f'cd {path} && git pull --rebase'
        else:
            sys.exit(f'Could not determine what action to take with {repo}.')

        try:
            git = subprocess.check_output(
                command,
                stdin=None,
                stderr=None,
                shell=True,
                timeout=int(cls.GIT_TIMEOUT)
            )
            data = f'{repo.name}\n{git.decode("UTF-8")}'
            logging.info(data)
            cls.generate_log(data)
        except subprocess.TimeoutExpired:
            # TODO: Why do we sys.exit here but log and keep going below?
            sys.exit(
                f'Error: github-archive timed out archiving {repo.name}.'
            )
        except subprocess.CalledProcessError as error:
            data = f'{repo.name}\n{error}'
            logging.error(data)
            cls.generate_log(data)
        return git

    @classmethod
    def iterate_gists(cls, switch, thread_list):
        """Iterate over each gist
        """
        for gist in cls.USER_GISTS:
            time.sleep(cls.BUFFER)
            path = os.path.join(
                cls.LOCATION, 'gists', gist.id)
            repo_thread = Thread(
                target=cls.clone_gists, 
                args=(
                    gist,
                    path,
                    switch,
                )
            )
            thread_list.append(repo_thread)
            repo_thread.start()
        # TODO: Return something meaningful
        # return

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
            git = subprocess.check_output(
                command,
                stdin=None,
                stderr=None,
                shell=True,
                timeout=int(cls.GIT_TIMEOUT)
            )
            data = f'{gist.id}\n{git.decode("UTF-8")}'
            logging.info(data)
            cls.generate_log(data)
        except subprocess.TimeoutExpired:
            # TODO: Why do we sys.exit here but log and keep going below?
            sys.exit(f'Error: github-archive timed out cloning {gist.id}.')
        except subprocess.CalledProcessError as error:
            data = f'{gist.id}\n{error}'
            logging.error(data)
            cls.generate_log(data)
        return git

    @classmethod
    def generate_log(cls, data):
        """Write output to a log
        """
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        with open(LOG_FILE, 'a') as log:
            # TODO: CHANGE THE LOG FILENAME TO WORK ON WINDOWS
            log.write(f'\n{data}')
        return log


def main():
    GitHubArchive().run()


if __name__ == '__main__':
    main()
