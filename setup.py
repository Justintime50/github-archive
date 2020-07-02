import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = [
    'PyGithub >= 1.51',
    'python-dotenv >= 0.10.0'
]

setuptools.setup(
    name='github-archive',
    version='2.1.0',
    description='A powerful script to concurrently clone your entire GitHub instance or save it as an archive.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/justintime50/github-archive',
    author='Justintime50',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': [
            'pylint >= 2.5.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'github_archive=githubarchive.github_archive:main'
        ]
    },
    python_requires='>=3.6',
)
