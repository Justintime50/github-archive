"""Import modules"""
import os
from datetime import datetime
import sys
import subprocess
import time
from threading import Thread
from github import Github
from dotenv import load_dotenv


class Archive():
    load_dotenv()
    # GitHub Archive Variables
    TOKEN = os.getenv('TOKEN')
    USER = Github(TOKEN)
    USER_REPOS = USER.get_user().get_repos()
    USER_GISTS = USER.get_user().get_gists()
    BUFFER = 0.1  # Buffer time in between each request

    # Configuration Variables
    LOCATION = os.path.expanduser(os.getenv('LOCATION'))
    LOG_PATH = os.path.join(LOCATION, 'logs')
    LOG_FILE = os.path.join(LOG_PATH, f'{datetime.now()}.log')
    GIT_TIMEOUT = os.getenv('GIT_TIMEOUT')
    BRANCH = os.getenv('BRANCH')
    LOG_LIFE = os.getenv('LOG_LIFE')

    # User Variables
    USER_CLONE_ON = os.getenv('USER_CLONE_ON')
    USER_PULL_ON = os.getenv('USER_PULL_ON')
    GISTS_CLONE_ON = os.getenv('GISTS_CLONE_ON')
    GISTS_PULL_ON = os.getenv('GISTS_PULL_ON')
    ORGS = os.getenv('ORGS').split(', ')
    ORGS_CLONE_ON = os.getenv('ORGS_CLONE_ON')
    ORGS_PULL_ON = os.getenv('ORGS_PULL_ON')
    # TODO: Log life

    @classmethod
    def clone_repos(cls, repo, path):
        if not os.path.exists(path):
            # Clone repos that don't exist
            try:
                git = subprocess.check_output(
                    f'git clone --branch={Archive.BRANCH} {repo.ssh_url} {path}',
                    stdin=None, stderr=None, shell=True, timeout=int(Archive.GIT_TIMEOUT))
                data = f'{repo.name}\n{git.decode("UTF-8")}'
                print(data)
                Archive.logs(data)
            except subprocess.TimeoutExpired:
                sys.exit(
                    f'Error: github-archive timed out cloning {repo.name}.')
            except subprocess.CalledProcessError as error:
                data = f'{repo.name}\n{error}'
                print(data)
                Archive.logs(data)

    @classmethod
    def pull_repos(cls, repo, path):
        # Pull changes for projects that are cloned
        try:
            git = subprocess.check_output(
                f'cd {path} && git pull',
                stdin=None, stderr=None, shell=True, timeout=int(Archive.GIT_TIMEOUT))
            data = f'{repo.name}\n{git.decode("UTF-8")}'
            print(data)
            Archive.logs(data)
        except subprocess.TimeoutExpired:
            sys.exit(f'Error: github-archive timed out pulling {repo.name}.')
        except subprocess.CalledProcessError as error:
            data = f'{repo.name}\n{error}'
            print(data)
            Archive.logs(data)

    @classmethod
    def clone_gists(cls, gist, path):
        # Pull changes for projects that are cloned
        if not os.path.exists(os.path.join(Archive.LOCATION, 'gists')):
            os.makedirs(os.path.join(Archive.LOCATION, 'gists'))
        try:
            git = subprocess.check_output(
                f'git clone {gist.html_url} {path}',
                stdin=None, stderr=None, shell=True, timeout=int(Archive.GIT_TIMEOUT))
            data = f'{gist.id}\n{git.decode("UTF-8")}'
            print(data)
            Archive.logs(data)
        except subprocess.TimeoutExpired:
            sys.exit(f'Error: github-archive timed out cloning {gist.id}.')
        except subprocess.CalledProcessError as error:
            data = f'{gist.id}\n{error}'
            print(data)
            Archive.logs(data)

    @classmethod
    def pull_gists(cls, gist, path):
        # Pull changes for projects that are cloned
        if not os.path.exists(os.path.join(Archive.LOCATION, 'gists')):
            os.makedirs(os.path.join(Archive.LOCATION, 'gists'))
        try:
            git = subprocess.check_output(
                f'cd {path} && git pull',
                stdin=None, stderr=None, shell=True, timeout=int(Archive.GIT_TIMEOUT))
            data = f'{gist.id}\n{git.decode("UTF-8")}'
            print(data)
            Archive.logs(data)
        except subprocess.TimeoutExpired:
            sys.exit(f'Error: github-archive timed out pulling {gist.id}.')
        except subprocess.CalledProcessError as error:
            data = f'{gist.id}\n{error}'
            print(data)
            Archive.logs(data)

    @classmethod
    def run(cls):
        """Run the script"""
        if not os.path.exists(Archive.LOCATION):
            os.makedirs(Archive.LOCATION)
        if not Archive.TOKEN:
            sys.exit('Error: GitHub token must be present to run github-archive.')
        if not Archive.LOCATION or not Archive.GIT_TIMEOUT or not Archive.BRANCH or not Archive.LOG_LIFE or not Archive.USER_CLONE_ON or not Archive.USER_PULL_ON or not Archive.GISTS_CLONE_ON or not Archive.GISTS_PULL_ON or not Archive.ORGS_CLONE_ON or not Archive.ORGS_PULL_ON:
            sys.exit(
                'Error: You have variables that have no values, please set them in the ".env" file before continuing.')

        # TODO: Fix timer and printing
        # start_time = datetime.now()
        # count = 0
        print('GitHub Archive started...')

        # Iterate over each personal repo and concurrently start cloning
        if Archive.USER_CLONE_ON == 'enable':
            for repo in Archive.USER_REPOS:
                if repo.owner.name == Archive.USER.get_user().name:
                    time.sleep(Archive.BUFFER)
                    path = os.path.join(
                        Archive.LOCATION, 'repos', repo.owner.login, repo.name)
                    Thread(target=Archive.clone_repos, args=(
                        repo, path,)).start()
        else:
            print('Skipping cloning user repos...')

        # Iterate over each personal repo and concurrently start pulling
        if Archive.USER_PULL_ON == 'enable':
            for repo in Archive.USER_REPOS:
                if repo.owner.name == Archive.USER.get_user().name:
                    time.sleep(Archive.BUFFER)
                    path = os.path.join(
                        Archive.LOCATION, 'repos', repo.owner.login, repo.name)
                    Thread(target=Archive.pull_repos, args=(
                        repo, path,)).start()
        else:
            print('Skipping pulling user repos...')

        # Iterate over each personal gist and concurrently start cloning
        if Archive.GISTS_CLONE_ON == 'enable':
            for gist in Archive.USER_GISTS:
                time.sleep(Archive.BUFFER)
                path = os.path.join(
                    Archive.LOCATION, 'gists', gist.id)
                Thread(target=Archive.clone_gists, args=(
                    gist, path,)).start()
        else:
            print('Skipping cloning user gists...')

        # Iterate over each personal gist and concurrently start pulling
        if Archive.GISTS_PULL_ON == 'enable':
            for gist in Archive.USER_GISTS:
                time.sleep(Archive.BUFFER)
                path = os.path.join(
                    Archive.LOCATION, 'gists', gist.id)
                Thread(target=Archive.pull_gists, args=(
                    gist, path,)).start()
        else:
            print('Skipping cloning user gists...')

        # Iterate over each organization repo and concurrently start cloning
        if Archive.ORGS and Archive.ORGS_CLONE_ON == 'enable':
            for org in Archive.ORGS:
                git_org = Archive.USER.get_organization(
                    org.strip()).get_repos()
                for repo in git_org:
                    time.sleep(Archive.BUFFER)
                    path = os.path.join(
                        Archive.LOCATION, 'repos', repo.owner.login, repo.name)
                    Thread(target=Archive.clone_repos, args=(
                        repo, path,)).start()
        else:
            print('Skipping cloning org repos...')

        # Iterate over each organization repo and concurrently start pulling
        if Archive.ORGS and Archive.ORGS_PULL_ON == 'enable':
            for org in Archive.ORGS:
                git_org = Archive.USER.get_organization(
                    org.strip()).get_repos()
                for repo in git_org:
                    time.sleep(Archive.BUFFER)
                    path = os.path.join(
                        Archive.LOCATION, 'repos', repo.owner.login, repo.name)
                    Thread(target=Archive.pull_repos, args=(
                        repo, path,)).start()
        else:
            print('Skipping pulling org repos...')

        # TODO: Fix this as it will print without checking if each child process is finished.
        # count += 1
        # execution_time = f'Execution time: {datetime.now() - start_time}. Items iterated: {count}'
        # print('Script complete!', execution_time)

    @classmethod
    def logs(cls, data):
        """Write output to a log"""
        if not os.path.exists(Archive.LOG_PATH):
            os.makedirs(Archive.LOG_PATH)
        with open(Archive.LOG_FILE, 'a') as log:
            log.write(f'\n{data}\n')


Archive.run()
