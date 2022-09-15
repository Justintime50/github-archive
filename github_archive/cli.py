import argparse
from typing import (
    get_args,
)

from github_archive import (
    GithubArchive,
)
from github_archive.constants import (
    DEFAULT_BASE_URL,
    DEFAULT_LOCATION,
    DEFAULT_LOG_LEVEL,
    DEFAULT_NUM_THREADS,
    DEFAULT_TIMEOUT,
    LOG_LEVEL_CHOICES,
)


class GithubArchiveCli:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description=(
                'A powerful tool to concurrently clone or pull user and org repos and gists to create a GitHub archive.'
            )
        )
        parser.add_argument(
            '-t',
            '--token',
            type=str,
            required=False,
            default=None,
            help=(
                'Provide your GitHub token to authenticate with the GitHub API and gain access to private repos and'
                ' gists.'
            ),
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
            '-s',
            '--stars',
            type=str,
            required=False,
            default=None,
            help='Pass a comma separated list of users to get starred repos for.',
        )
        parser.add_argument(
            '-v',
            '--view',
            action='store_true',
            required=False,
            default=False,
            help='Pass this flag to view git assets (dry run).',
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
            '-f',
            '--forks',
            action='store_true',
            required=False,
            default=False,
            help='Pass this flag to include forked git assets.',
        )
        parser.add_argument(
            '-i',
            '--include',
            type=str,
            required=False,
            default=None,
            help='Pass a comma separated list of repos to filter what is included in the Archive.',
        )
        parser.add_argument(
            '-e',
            '--exclude',
            type=str,
            required=False,
            default=None,
            help='Pass a comma separated list of repos to filter what is excluded from the Archive.',
        )
        parser.add_argument(
            '-l',
            '--location',
            type=str,
            required=False,
            default=DEFAULT_LOCATION,
            help=(
                f'The location where you want your GitHub Archive to be stored. By default, this is: {DEFAULT_LOCATION}'
            ),
        )
        parser.add_argument(
            '-ht',
            '--https',
            action='store_true',
            required=False,
            default=False,
            help='Use HTTPS URLs instead of SSH.',
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
            '--base_url',
            type=str,
            required=False,
            default=DEFAULT_BASE_URL,
            help='The base URL of your GitHub instance (useful for enterprise users with custom hostnames).',
        )
        parser.add_argument(
            '--log_level',
            type=str,
            required=False,
            default=DEFAULT_LOG_LEVEL,
            choices=set(get_args(LOG_LEVEL_CHOICES)),
            help='The log level used for the tool.',
        )
        parser.parse_args(namespace=self)

    def run(self):
        github_archive = GithubArchive(
            token=self.token,
            users=self.users,
            orgs=self.orgs,
            gists=self.gists,
            stars=self.stars,
            view=self.view,
            clone=self.clone,
            pull=self.pull,
            forks=self.forks,
            location=self.location,
            include=self.include,
            exclude=self.exclude,
            use_https=self.https,
            timeout=self.timeout,
            threads=self.threads,
            base_url=self.base_url,
            log_level=self.log_level,
        )
        github_archive.run()


def main():
    GithubArchiveCli().run()


if __name__ == '__main__':
    main()
