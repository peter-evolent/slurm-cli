from setuptools import setup, find_packages


requires = []


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
)
