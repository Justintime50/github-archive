import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

REQUIREMENTS = [
    'PyGithub == 1.*',
    'woodchips == 0.2.*',
]

DEV_REQUIREMENTS = [
    'bandit == 1.7.*',
    'black == 23.*',
    'build == 0.10.*',
    'flake8 == 6.*',
    'isort == 5.*',
    'mypy == 1.3.*',
    'pytest == 7.*',
    'pytest-cov == 4.*',
    'twine == 4.*',
]

setuptools.setup(
    name='github-archive',
    version='6.0.0',
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
            'test',
        ]
    ),
    package_data={
        'github_archive': [
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
    python_requires='>=3.8, <4',
)
