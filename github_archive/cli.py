import argparse
from typing import get_args

from github_archive import GithubArchive
from github_archive._version import __version__
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
                "A powerful tool to concurrently clone or pull user and org repos and gists to create a GitHub archive."
            )
        )
        parser.add_argument(
            "-t",
            "--token",
            type=str,
            required=False,
            default=None,
            help=(
                "Provide your GitHub token to authenticate with the GitHub API and gain access to private repos and"
                " gists."
            ),
        )
        parser.add_argument(
            "-u",
            "--users",
            type=str,
            required=False,
            default=None,
            help="Pass a comma separated list of users to get repos for.",
        )
        parser.add_argument(
            "-o",
            "--orgs",
            type=str,
            required=False,
            default=None,
            help="Pass a comma separated list of orgs to get repos for.",
        )
        parser.add_argument(
            "-g",
            "--gists",
            type=str,
            required=False,
            default=None,
            help="Pass a comma separated list of users to get gists for.",
        )
        parser.add_argument(
            "-s",
            "--stars",
            type=str,
            required=False,
            default=None,
            help="Pass a comma separated list of users to get starred repos for.",
        )
        parser.add_argument(
            "-v",
            "--view",
            action="store_true",
            required=False,
            default=False,
            help="Pass this flag to view git assets (dry run).",
        )
        parser.add_argument(
            "-c",
            "--clone",
            action="store_true",
            required=False,
            default=False,
            help="Pass this flag to clone git assets.",
        )
        parser.add_argument(
            "-p",
            "--pull",
            action="store_true",
            required=False,
            default=False,
            help="Pass this flag to pull git assets.",
        )
        parser.add_argument(
            "-f",
            "--fork",
            action="store_true",
            required=False,
            default=False,
            help="Pass this flag to fork git assets.",
        )
        parser.add_argument(
            "--include",
            type=str,
            required=False,
            default=None,
            help="Pass a comma separated list of repos to filter what is included in the Archive.",
        )
        parser.add_argument(
            "--exclude",
            type=str,
            required=False,
            default=None,
            help="Pass a comma separated list of repos to filter what is excluded from the Archive.",
        )
        parser.add_argument(
            "--languages",
            type=str,
            required=False,
            default=None,
            help="Pass a comma separated list of languages to filter what is included in the Archive.",
        )
        parser.add_argument(
            "--forks",
            action="store_true",
            required=False,
            default=False,
            help="Pass this flag to include forked git assets (when cloning or pulling).",
        )
        parser.add_argument(
            "--location",
            type=str,
            required=False,
            default=DEFAULT_LOCATION,
            help=f"The location where you want your GitHub Archive to be stored. Default: {DEFAULT_LOCATION}",
        )
        parser.add_argument(
            "--https",
            action="store_true",
            required=False,
            default=False,
            help="Use HTTPS URLs instead of SSH.",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            required=False,
            default=DEFAULT_TIMEOUT,
            help=f"The number of seconds before a git operation times out. Default: {DEFAULT_TIMEOUT}",
        )
        parser.add_argument(
            "--threads",
            type=int,
            required=False,
            default=DEFAULT_NUM_THREADS,
            help=f"The number of concurrent threads to run. Default: {DEFAULT_NUM_THREADS}",
        )
        parser.add_argument(
            "--base_url",
            type=str,
            required=False,
            default=DEFAULT_BASE_URL,
            help=(  # noqa
                "The base URL of your GitHub instance (useful for enterprise users with custom hostnames). Default:"
                f" {DEFAULT_BASE_URL}"
            ),
        )
        parser.add_argument(
            "--log_level",
            type=str,
            required=False,
            default=DEFAULT_LOG_LEVEL,
            choices=set(get_args(LOG_LEVEL_CHOICES)),
            help=f"The log level used for the tool. Default: {DEFAULT_LOG_LEVEL}",
        )
        parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {__version__}",
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
            fork=self.fork,
            include=self.include,
            exclude=self.exclude,
            languages=self.languages,
            forks=self.forks,
            location=self.location,
            use_https=self.https,
            timeout=self.timeout,
            threads=self.threads,
            base_url=self.base_url,
            log_level=self.log_level,
        )
        github_archive.run()


def main():
    GithubArchiveCli().run()


if __name__ == "__main__":
    main()
