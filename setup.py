import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

REQUIREMENTS = [
    'PyGithub == 1.*',
    'typing_extensions',  # TODO: Remove once we drop support for Python 3.7 (used for Literal type hint)
    'woodchips == 0.2.*',
]

DEV_REQUIREMENTS = [
    'bandit == 1.7.*',
    'black == 22.*',
    'build == 0.10.*',
    'flake8 == 5.*',  # TODO: Bump once we drop support for Python 3.7
    'isort == 5.*',
    'mypy == 1.1.*',
    'pytest == 7.*',
    'pytest-cov == 4.*',
    'twine == 4.*',
]

setuptools.setup(
    name='github-archive',
    version='5.0.2',
    description=(
        'A powerful tool to concurrently clone, pull, or fork user and org repos and gists to create a GitHub archive.'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/justintime50/github-archive',
    author='Justintime50',
    license='MIT',
    packages=setuptools.find_packages(
        exclude=[
            'examples',
            'test',
        ]
    ),
    package_data={
        'github-archive': [
            'py.typed',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': DEV_REQUIREMENTS,
    },
    entry_points={
        'console_scripts': [
            'github-archive=github_archive.cli:main',
        ]
    },
    python_requires='>=3.7, <4',
)
