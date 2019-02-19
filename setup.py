from setuptools import setup, find_packages


requires = [
    'click>=7.0',
    'texttable',
    'slurmsdk@git+https://github.com/peter-evolent/slurm-sdk.git@v0.0.1'
]

def get_version():
    with open('slurmcli/version.py') as f:
        ns = {}
        exec(f.read(), ns)
        version = ns['__version__']
        return version


setup(
    name='SlurmCLI',
    version=get_version(),
    description='A command line interface to Slurm REST API',
    license='MIT',
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'slurm = slurmcli.__main__:main',
        ],
    },
)
