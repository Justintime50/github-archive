import argparse

from github_archive import GithubArchive
from github_archive.constants import DEFAULT_NUM_THREADS, DEFAULT_TIMEOUT, DEFAULT_LOCATION


class GithubArchiveCli:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description=(
                'A powerful script to concurrently clone your entire GitHub instance or save it as an archive.'
            )
        )
        parser.add_argument(
            '-v',
            '--view',
            action='store_true',
            required=False,
            default=False,
            help='Pass this flag to view git assets.',
        )
        parser.add_argument(
            '-c',
            '--clone',
            action='store_true',
            required=False,
            default=False,
            help='Pass this flag to clone git assets.',
        )
        parser.add_argument(
            '-p',
            '--pull',
            action='store_true',
            required=False,
            default=False,
            help='Pass this flag to pull git assets.',
        )
        parser.add_argument(
            '-u',
            '--users',
            type=str,
            required=False,
            default=None,
            help='Pass a comma separated list of users to get repos for.',
        )
        parser.add_argument(
            '-o',
            '--orgs',
            type=str,
            required=False,
            default=None,
            help='Pass a comma separated list of orgs to get repos for.',
        )
        parser.add_argument(
            '-g',
            '--gists',
            type=str,
            required=False,
            default=None,
            help='Pass a comma separated list of users to get gists for.',
        )
        parser.add_argument(
            '-to',
            '--timeout',
            type=int,
            required=False,
            default=DEFAULT_TIMEOUT,
            help='The number of seconds before a git operation times out.',
        )
        parser.add_argument(
            '-th',
            '--threads',
            type=int,
            required=False,
            default=DEFAULT_NUM_THREADS,
            help='The number of concurrent threads to run.',
        )
        parser.add_argument(
            '-t',
            '--token',
            type=str,
            required=False,
            default=None,
            help='Provide your GitHub token to authenticate with the GitHub API and gain access to private repos and gists.',  # noqa
        )
        parser.add_argument(
            '-l',
            '--location',
            type=str,  # TODO: Create a custom `path` type here
            required=False,
            default=DEFAULT_LOCATION,
            help='The location where you want your GitHub Archive to be stored.',
        )
        parser.parse_args(namespace=self)

    def run(self):
        github_archive = GithubArchive(
            view=self.view,
            clone=self.clone,
            pull=self.pull,
            users=self.users,
            orgs=self.orgs,
            gists=self.gists,
            timeout=self.timeout,
            threads=self.threads,
            token=self.token,
            location=self.location,
        )
        github_archive.run()


def main():
    GithubArchiveCli().run()


if __name__ == '__main__':
    main()
