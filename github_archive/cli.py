import argparse
from github_archive import GithubArchive


class CLI():
    def __init__(self):
        """Setup the CLI arguments
        """
        parser = argparse.ArgumentParser(
            description=('A powerful script to concurrently clone your entire'
                         ' GitHub instance or save it as an archive.')
        )
        parser.add_argument(
            '-uc',
            '--user_clone',
            action='store_true',
            required=False,
            help='Clone personal repos.',
        )
        parser.add_argument(
            '-up',
            '--user_pull',
            action='store_true',
            required=False,
            help='Pull personal repos',
        )
        parser.add_argument(
            '-gc',
            '--gists_clone',
            action='store_true',
            required=False,
            help='Clone personal gists',
        )
        parser.add_argument(
            '-gp',
            '--gists_pull',
            action='store_true',
            required=False,
            help='Pull personal gists.',
        )
        parser.add_argument(
            '-oc',
            '--orgs_clone',
            action='store_true',
            required=False,
            help='Clone organization repos.',
        )
        parser.add_argument(
            '-op',
            '--orgs_pull',
            action='store_true',
            required=False,
            help='Pull organization repos.',
        )
        parser.add_argument(
            '-b',
            '--branch',
            default='master',
            required=False,
            help='Which branch to pull from.',
        )
        parser.parse_args(namespace=self)

    def _run(self):
        GithubArchive.run(
            user_clone=self.user_clone,
            user_pull=self.user_pull,
            gists_clone=self.gists_clone,
            gists_pull=self.gists_pull,
            orgs_clone=self.orgs_clone,
            orgs_pull=self.orgs_pull,
            branch=self.branch,
        )


if __name__ == '__main__':
    CLI()._run()
