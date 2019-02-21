"""Slurm CLI commands"""
import collections
import json
import os

import click
from slurmsdk import API

from slurmcli import formatter
from slurmcli.config import Config
from slurmcli.version import __version__


CONFIG_FPATH = os.path.expanduser('~/.slurm')


Context = collections.namedtuple('context', 'api config')


@click.group()
@click.option('--dev', is_flag=True, help='Use dev endpoints')
@click.option('--base_url', type=str, default=None, help='Specify Slurm REST API base url')
@click.pass_context
def root(ctx, dev, base_url):
    """Slurm CLI: manage users and jobs from the command line"""
    try:
        config = Config.from_json(CONFIG_FPATH)
    except FileNotFoundError:
        config = Config(fpath=CONFIG_FPATH)

    # TODO: warn the user if access_token is expiring

    if not base_url:
        base_url = 'https://slurm.evolent.io/api' if not dev else 'https://slurm-dev.evolent.io/api'

    auth = config.get('auth')
    access_token = auth['access_token'] if auth else None
    ctx.obj = Context(API(base_url, access_token), config)


@root.command(short_help='Show the Slurm CLI version information')
def version():
    click.echo(__version__)


@root.command(short_help='Authenticate using UserCreds')
@click.option('--username', required=True, help='Username')
@click.password_option(confirmation_prompt=False, help='Password')
@click.pass_obj
def login(ctx, username, password):
    result = ctx.api.authenticate(username, password)
    ctx.config.put('auth', result)
    click.echo('Login Succeeded')


@root.command(short_help='Add a new user')
@click.option('--username', required=True, help='Username')
@click.password_option(confirmation_prompt=False, help='Password')
@click.pass_obj
def adduser(ctx, username, password):
    result = ctx.api.create_user(username, password)
    output = result['data']
    click.echo(json.dumps(output))


@root.command(short_help='List available users')
@click.pass_obj
def users(ctx):
    result = ctx.api.list_users()
    output = formatter.format_users(result)
    click.echo(output)


@root.command(short_help='List available jobs')
@click.option('--query', type=str, default=None, help='Search query')
@click.option('--offset', type=int, default=0, help='Offset of the first row')
@click.option('--limit', type=int, default=20, help='Limit the number of rows returned')
@click.pass_obj
def jobs(ctx, query, offset, limit):
    result = ctx.api.list_jobs(query, offset, limit)
    output = formatter.format_jobs(result, offset, limit)
    click.echo(output)


@root.command(short_help='Pause a job')
@click.argument('job_id', type=int)
@click.pass_obj
def pause(ctx, job_id):
    ctx.api.pause_job(job_id)
    click.echo(job_id)


@root.command(short_help='Resume a paused job')
@click.argument('job_id', type=int)
@click.pass_obj
def resume(ctx, job_id):
    ctx.api.resume_job(job_id)
    click.echo(job_id)


@root.command(short_help='Change the job status to queued')
@click.argument('job_id', type=int)
@click.pass_obj
def retry(ctx, job_id):
    ctx.api.retry_job(job_id)
    click.echo(job_id)


@root.command(short_help='Delete a job')
@click.argument('job_id', type=int)
@click.pass_obj
def delete(ctx, job_id):
    ctx.api.delete_job(job_id)
    click.echo(job_id)
