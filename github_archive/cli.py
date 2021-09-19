import argparse

from github_archive import GithubArchive
from github_archive.constants import DEFAULT_LOCATION, DEFAULT_NUM_THREADS, DEFAULT_TIMEOUT


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
            '-l',
            '--location',
            type=str,  # TODO: Create a custom `path` type here
            required=False,
            default=DEFAULT_LOCATION,
            help='The location where you want your GitHub Archive to be stored.',
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
            use_https=self.https,
            timeout=self.timeout,
            threads=self.threads,
        )
        github_archive.run()


def main():
    GithubArchiveCli().run()


if __name__ == '__main__':
    main()
