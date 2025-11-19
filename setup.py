import re

import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

# Inspiration: https://stackoverflow.com/a/7071358/6064135
with open('github_archive/_version.py', 'r') as version_file:
    version_groups = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_groups:
        version = version_groups.group(1)
    else:
        raise RuntimeError('Unable to find version string!')

REQUIREMENTS = [
    'PyGithub == 2.8.*',
    'woodchips == 2.*',
]

DEV_REQUIREMENTS = [
    'bandit == 1.9.*',
    'black == 25.*',
    'build == 1.3.*',
    'flake8 == 7.*',
    'isort == 7.*',
    'mypy == 1.18.*',
    'pytest == 9.*',
    'pytest-cov == 7.*',
]

setuptools.setup(
    name='github-archive',
    version=version,
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
    python_requires='>=3.10, <4',
)
