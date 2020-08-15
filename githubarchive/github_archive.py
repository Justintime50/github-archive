"""Import modules"""
# pylint: disable=R0912,R0915
import os
from datetime import datetime
import sys
import subprocess
import time
import argparse
from threading import Thread
from github import Github


class Archive():
    """All GitHub Archive methods
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
    args = parser.parse_args()

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
    BUFFER = 0.1  # Buffer time in between each request
    GIT_TIMEOUT = 180  # Number of seconds before a git operation will timeout

    @classmethod
    def clone_repos(cls, repo, path):
        """Clone repos that don't exist
        """
        if not os.path.exists(path):
            try:
                git = subprocess.check_output(
                    f'git clone --branch={Archive.args.branch} {repo.ssh_url} {path}',
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
        """Pull changes for projects that are cloned
        """
        try:
            git = subprocess.check_output(
                f'cd {path} && git pull --ff-only',
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
        """Clone gists
        """
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
        """Pull Gists
        """
        if not os.path.exists(os.path.join(Archive.LOCATION, 'gists')):
            os.makedirs(os.path.join(Archive.LOCATION, 'gists'))
        try:
            git = subprocess.check_output(
                f'cd {path} && git pull --ff-only',
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
    def logs(cls, data):
        """Write output to a log
        """
        if not os.path.exists(Archive.LOG_PATH):
            os.makedirs(Archive.LOG_PATH)
        with open(Archive.LOG_FILE, 'a') as log:
            log.write(f'\n{data}')


def main():
    """Run the based on configuration script
    """
    if not os.path.exists(Archive.LOCATION):
        os.makedirs(Archive.LOCATION)
    if not Archive.TOKEN:
        sys.exit('Error: GitHub token must be present to run github-archive.')

    start_message = 'GitHub Archive started...'
    start_time = datetime.now()
    preamble = f'{start_message}\n{start_time}\n'
    print(preamble)
    Archive.logs(preamble)
    thread_list = []

    # Iterate over each personal repo and concurrently start cloning
    if Archive.args.user_clone is True:
        message = '## Cloning personal repos... ##\n'
        print(message)
        Archive.logs(message)
        for repo in Archive.USER_REPOS:
            if repo.owner.name == Archive.USER.get_user().name:
                time.sleep(Archive.BUFFER)
                path = os.path.join(
                    Archive.LOCATION, 'repos', repo.owner.login, repo.name)
                repo_thread = Thread(target=Archive.clone_repos, args=(
                    repo, path,))
                thread_list.append(repo_thread)
                repo_thread.start()
    else:
        data = '## Skipping cloning user repos... ##'
        print(data)
        Archive.logs(data)

    # Iterate over each personal repo and concurrently start pulling
    if Archive.args.user_pull is True:
        message = '## Pulling personal repos... ##\n'
        print(message)
        Archive.logs(message)
        for repo in Archive.USER_REPOS:
            if repo.owner.name == Archive.USER.get_user().name:
                time.sleep(Archive.BUFFER)
                path = os.path.join(
                    Archive.LOCATION, 'repos', repo.owner.login, repo.name)
                repo_thread = Thread(target=Archive.pull_repos, args=(
                    repo, path,))
                thread_list.append(repo_thread)
                repo_thread.start()
    else:
        data = '## Skipping pulling user repos...## '
        print(data)
        Archive.logs(data)

    # Iterate over each gist and concurrently start cloning
    if Archive.args.gists_clone is True:
        message = 'Cloning gists...\n'
        print(message)
        Archive.logs(message)
        for gist in Archive.USER_GISTS:
            time.sleep(Archive.BUFFER)
            path = os.path.join(
                Archive.LOCATION, 'gists', gist.id)
            repo_thread = Thread(target=Archive.clone_gists, args=(
                gist, path,))
            thread_list.append(repo_thread)
            repo_thread.start()
    else:
        data = '## Skipping cloning gists... ##'
        print(data)
        Archive.logs(data)

    # Iterate over each gist and concurrently start pulling
    if Archive.args.gists_pull is True:
        message = '## Pulling gists... ##\n'
        print(message)
        Archive.logs(message)
        for gist in Archive.USER_GISTS:
            time.sleep(Archive.BUFFER)
            path = os.path.join(
                Archive.LOCATION, 'gists', gist.id)
            repo_thread = Thread(target=Archive.pull_gists, args=(
                gist, path,))
            thread_list.append(repo_thread)
            repo_thread.start()
    else:
        data = '## Skipping pulling gists... ##'
        print(data)
        Archive.logs(data)

    # Check if org variable is set
    if Archive.ORG_LIST == '':
        data = '## Skipping org repos, no organizations specified... ##'
        print(data)
        Archive.logs(data)
    else:
        # Iterate over each organization repo and concurrently start cloning
        if Archive.args.orgs_clone is True:
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
                    repo_thread = Thread(target=Archive.clone_repos, args=(
                        repo, path,))
                    thread_list.append(repo_thread)
                    repo_thread.start()
        else:
            data = '## Skipping cloning org repos... ##'
            print(data)
            Archive.logs(data)

        # Iterate over each organization repo and concurrently start pulling
        if Archive.args.orgs_pull is True:
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
                    repo_thread = Thread(target=Archive.pull_repos, args=(
                        repo, path,))
                    thread_list.append(repo_thread)
                    repo_thread.start()
        else:
            data = '## Skipping pulling org repos... ##'
            print(data)
            Archive.logs(data)

    for thread in thread_list:
        thread.join()
    execution_time = f'Execution time: {datetime.now() - start_time}.'
    finish_message = f'GitHub Archive complete! {execution_time}'
    print(finish_message)
    Archive.logs(finish_message)


if __name__ == '__main__':
    main()
