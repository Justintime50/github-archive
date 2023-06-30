name: build

on:
  push:
    paths:
      - '.github/workflows/build.yml'
      - '**/*.py'
    branches:
      - '**'
    tags:
      - '!**'
  pull_request:
    paths:
      - '.github/workflows/build.yml'
      - '**/*.py'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: extractions/setup-just@v1
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: just install lint
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        pythonversion: ['3.8', '3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v3
      - uses: extractions/setup-just@v1
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.pythonversion }}
      - run: just install coverage
  coverage:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: extractions/setup-just@v1
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: just install coverage
      - uses: coverallsapp/github-action@v2
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          path-to-lcov: './coverage.lcov'
