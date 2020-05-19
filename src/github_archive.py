"""Import modules"""
# pylint: disable=W0511,R0916,R0912,R0915,R0914
# TODO: Restructure the code to align with what Pylint wants ^
import os
from datetime import datetime
import sys
import subprocess
import time
from threading import Thread
from github import Github
from dotenv import load_dotenv


class Archive():
    """All GitHub Archive methods"""
    load_dotenv()
    # GitHub Archive Variables
    TOKEN = os.getenv('TOKEN')
    USER = Github(TOKEN)
    USER_REPOS = USER.get_user().get_repos()
    USER_GISTS = USER.get_user().get_gists()
    BUFFER = 0.1  # Buffer time in between each request
    GIT_TIMEOUT = 120  # Number of seconds before a git operation will timeout

    # Configuration Variables
    LOCATION = os.path.expanduser(os.getenv('LOCATION'))
    LOG_PATH = os.path.join(LOCATION, 'logs')
    LOG_FILE = os.path.join(LOG_PATH, f'{datetime.now()}.log')
    BRANCH = os.getenv('BRANCH')
    LOG_LIFE = time.time() - int(os.getenv('LOG_LIFE')) * 86400

    # User Variables
    USER_CLONE_ON = os.getenv('USER_CLONE_ON')
    USER_PULL_ON = os.getenv('USER_PULL_ON')
    GISTS_CLONE_ON = os.getenv('GISTS_CLONE_ON')
    GISTS_PULL_ON = os.getenv('GISTS_PULL_ON')
    ORGS = os.getenv('ORGS').split(', ')
    ORGS_CLONE_ON = os.getenv('ORGS_CLONE_ON')
    ORGS_PULL_ON = os.getenv('ORGS_PULL_ON')

    @classmethod
    def clone_repos(cls, repo, path):
        """Clone repos that don't exist"""
        if not os.path.exists(path):
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
        else:
            data = f'{repo.name}\nAlready cloned, skipping...\n'
            print(data)
            Archive.logs(data)

    @classmethod
    def pull_repos(cls, repo, path):
        """Pull changes for projects that are cloned"""
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
        """Clone gists"""
        if not os.path.exists(os.path.join(Archive.LOCATION, 'gists')):
            os.makedirs(os.path.join(Archive.LOCATION, 'gists'))
        if not os.path.exists(path):
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
        else:
            data = f'{gist.id}\nAlready cloned, skipping...\n'
            print(data)
            Archive.logs(data)

    @classmethod
    def pull_gists(cls, gist, path):
        """Pull Gists"""
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
        """Run the based on configuration script"""
        if not os.path.exists(Archive.LOCATION):
            os.makedirs(Archive.LOCATION)
        if not Archive.TOKEN:
            sys.exit('Error: GitHub token must be present to run github-archive.')
        if not Archive.LOCATION or not Archive.GIT_TIMEOUT or not Archive.BRANCH \
                or not Archive.LOG_LIFE or not Archive.USER_CLONE_ON or not Archive.USER_PULL_ON \
                or not Archive.GISTS_CLONE_ON or not Archive.GISTS_PULL_ON \
                or not Archive.ORGS_CLONE_ON or not Archive.ORGS_PULL_ON:
            sys.exit(
                'Error: You have variables that have no values,' +
                'please set them in the ".env" file before continuing.')

        start_message = 'GitHub Archive started...'
        start_time = datetime.now()
        preamble = f'{start_message}\n{start_time}\n'
        print(preamble)
        Archive.logs(preamble)

        # Iterate over each personal repo and concurrently start cloning
        if Archive.USER_CLONE_ON == 'enable':
            message = '## Cloning personal repos... ##\n'
            print(message)
            Archive.logs(message)
            for repo in Archive.USER_REPOS:
                if repo.owner.name == Archive.USER.get_user().name:
                    time.sleep(Archive.BUFFER)
                    path = os.path.join(
                        Archive.LOCATION, 'repos', repo.owner.login, repo.name)
                    Thread(target=Archive.clone_repos, args=(
                        repo, path,)).start()
        else:
            data = '## Skipping cloning user repos... ##'
            print(data)
            Archive.logs(data)

        # Iterate over each personal repo and concurrently start pulling
        if Archive.USER_PULL_ON == 'enable':
            message = '## Pulling personal repos... ##\n'
            print(message)
            Archive.logs(message)
            for repo in Archive.USER_REPOS:
                if repo.owner.name == Archive.USER.get_user().name:
                    time.sleep(Archive.BUFFER)
                    path = os.path.join(
                        Archive.LOCATION, 'repos', repo.owner.login, repo.name)
                    Thread(target=Archive.pull_repos, args=(
                        repo, path,)).start()
        else:
            data = '## Skipping pulling user repos...## '
            print(data)
            Archive.logs(data)

        # Iterate over each gist and concurrently start cloning
        if Archive.GISTS_CLONE_ON == 'enable':
            message = 'Cloning gists...\n'
            print(message)
            Archive.logs(message)
            for gist in Archive.USER_GISTS:
                time.sleep(Archive.BUFFER)
                path = os.path.join(
                    Archive.LOCATION, 'gists', gist.id)
                Thread(target=Archive.clone_gists, args=(
                    gist, path,)).start()
        else:
            data = '## Skipping cloning gists... ##'
            print(data)
            Archive.logs(data)

        # Iterate over each gist and concurrently start pulling
        if Archive.GISTS_PULL_ON == 'enable':
            message = '## Pulling gists... ##\n'
            print(message)
            Archive.logs(message)
            for gist in Archive.USER_GISTS:
                time.sleep(Archive.BUFFER)
                path = os.path.join(
                    Archive.LOCATION, 'gists', gist.id)
                Thread(target=Archive.pull_gists, args=(
                    gist, path,)).start()
        else:
            data = '##Skipping pulling gists... ##'
            print(data)
            Archive.logs(data)

        # Iterate over each organization repo and concurrently start cloning
        if Archive.ORGS and Archive.ORGS_CLONE_ON == 'enable':
            for org in Archive.ORGS:
                message = f'## Cloning {org} repos... ##\n'
                print(message)
                Archive.logs(message)
                git_org = Archive.USER.get_organization(
                    org.strip()).get_repos()
                for repo in git_org:
                    time.sleep(Archive.BUFFER)
                    path = os.path.join(
                        Archive.LOCATION, 'repos', repo.owner.login, repo.name)
                    Thread(target=Archive.clone_repos, args=(
                        repo, path,)).start()
        else:
            data = '## Skipping cloning org repos... ##'
            print(data)
            Archive.logs(data)

        # Iterate over each organization repo and concurrently start pulling
        if Archive.ORGS and Archive.ORGS_PULL_ON == 'enable':
            for org in Archive.ORGS:
                message = f'## Pulling {org} repos... ##\n'
                print(message)
                Archive.logs(message)
                git_org = Archive.USER.get_organization(
                    org.strip()).get_repos()
                for repo in git_org:
                    time.sleep(Archive.BUFFER)
                    path = os.path.join(
                        Archive.LOCATION, 'repos', repo.owner.login, repo.name)
                    Thread(target=Archive.pull_repos, args=(
                        repo, path,)).start()
        else:
            data = '## Skipping pulling org repos... ##'
            print(data)
            Archive.logs(data)

        # Clean up logs before finishing)
        for root, dirs, files in os.walk(Archive.LOG_PATH):  # pylint: disable=W0612
            for file in files:
                if file.mtime < Archive.LOG_LIFE:
                    os.remove(file)
                    print('Logs cleaned up')

        # TODO: Use threading.wait to check if all processes are finished
        time.sleep(6)
        execution_time = f'Execution time: {datetime.now() - start_time}.'
        finish_message = f'GitHub Archive complete! {execution_time}'
        print(finish_message)
        Archive.logs(finish_message)

    @classmethod
    def logs(cls, data):
        """Write output to a log"""
        if not os.path.exists(Archive.LOG_PATH):
            os.makedirs(Archive.LOG_PATH)
        with open(Archive.LOG_FILE, 'a') as log:
            log.write(f'\n{data}')


Archive.run()
