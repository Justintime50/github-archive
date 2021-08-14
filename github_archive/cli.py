import argparse

from github_archive import GithubArchive


class CLI:
    def __init__(self):
        """Setup the CLI arguments"""
        parser = argparse.ArgumentParser(
            description=(
                'A powerful script to concurrently clone your entire GitHub instance or save it as an archive.'
            )
        )
        parser.add_argument(
            '-pc',
            '--personal_clone',
            action='store_true',
            required=False,
            default=False,
            help='Clone personal repos.',
        )
        parser.add_argument(
            '-pp',
            '--personal_pull',
            action='store_true',
            required=False,
            default=False,
            help='Pull personal repos',
        )
        parser.add_argument(
            '-uc',
            '--users_clone',
            action='store_true',
            required=False,
            default=False,
            help='Clone user repos.',
        )
        parser.add_argument(
            '-up',
            '--users_pull',
            action='store_true',
            required=False,
            default=False,
            help='Pull user repos.',
        )
        parser.add_argument(
            '-gc',
            '--gists_clone',
            action='store_true',
            required=False,
            default=False,
            help='Clone personal gists.',
        )
        parser.add_argument(
            '-gp',
            '--gists_pull',
            action='store_true',
            required=False,
            default=False,
            help='Pull personal gists.',
        )
        parser.add_argument(
            '-oc',
            '--orgs_clone',
            action='store_true',
            required=False,
            default=False,
            help='Clone organization repos.',
        )
        parser.add_argument(
            '-op',
            '--orgs_pull',
            action='store_true',
            required=False,
            default=False,
            help='Pull organization repos.',
        )
        parser.parse_args(namespace=self)

    def _run(self):
        GithubArchive.run(
            personal_clone=self.personal_clone,
            personal_pull=self.personal_pull,
            users_clone=self.users_clone,
            users_pull=self.users_pull,
            gists_clone=self.gists_clone,
            gists_pull=self.gists_pull,
            orgs_clone=self.orgs_clone,
            orgs_pull=self.orgs_pull,
        )


def main():
    CLI()._run()


if __name__ == '__main__':
    main()
