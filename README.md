Slurm CLI
=========

The Slurm CLI is used to manage users and jobs from the command line.
It requires Python 3.6 or higher.

## Quick Start

First, install the library:
```sh
$ pip install git+https://github.com/peter-evolent/slurm-cli.git
```

Then, verify the installation

```sh
$ slurm version
0.0.1
```

## Development

#### Gettinger Started

Assuming that you have Python and virtualenv installed, set up your environment and install the required dependencies:
```sh
$ git clone https://github.com/peter-evolent/slurm-cli.git
$ cd slurm-cli
$ virtualenv venv -p python3
...
$ source venv/bin/activate
$ make init
```

#### Running Tests

```sh
$ make test
```

#### Running Lint

```sh
$ make lint
```