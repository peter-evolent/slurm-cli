import json

from click.testing import CliRunner
import pytest

from slurmcli import cli, __version__


class FakeConfig:
    def __init__(self, fpath=None):
        self.fpath = fpath
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def put(self, key, value):
        self.data[key] = value

    @classmethod
    def from_json(cls, fpath):
        raise FileNotFoundError('FakeConfig do not use file')


def handle_action(self, job_id):
    return job_id


def print_error(result):
    if result.exception:
        print(result.exception)
    if result.output:
        print(result.output)


@pytest.fixture
def clictx():
    api = cli.API('https://api.fake.com')
    config = FakeConfig()
    return cli.Context(api, config)


@pytest.fixture
def fakeconfig(monkeypatch):
    monkeypatch.setattr(cli, 'Config', FakeConfig)


@pytest.fixture
def config_fpath(jsonfile, monkeypatch):
    fpath = str(jsonfile)
    monkeypatch.setattr(cli, 'CONFIG_FPATH', fpath)
    return fpath


def test_root_api(fakeconfig):
    @cli.root.command()
    @cli.click.pass_obj
    def cmd(ctx):
        assert ctx.api.base_url == 'https://slurm.evolent.io/api'

    runner = CliRunner()
    result = runner.invoke(cli.root, 'cmd')

    print_error(result)
    assert result.exit_code == 0


def test_root_dev_api(fakeconfig):
    @cli.root.command()
    @cli.click.pass_obj
    def cmd(ctx):
        assert ctx.api.base_url == 'https://slurm-dev.evolent.io/api'

    runner = CliRunner()
    result = runner.invoke(cli.root, '--dev cmd')

    print_error(result)
    assert result.exit_code == 0


def test_root_custom_api(fakeconfig):
    @cli.root.command()
    @cli.click.pass_obj
    def cmd(ctx):
        assert ctx.api.base_url == 'http://localhost:5000'

    runner = CliRunner()
    result = runner.invoke(cli.root, '--base_url http://localhost:5000 cmd')

    print_error(result)
    assert result.exit_code == 0


def test_root_access_token_from_file(jsonfile, config_fpath):
    data = {
        'auth': {
            'access_token': 'token'
        }
    }
    jsonfile.write(json.dumps(data))

    @cli.root.command()
    @cli.click.pass_obj
    def cmd(ctx):
        assert ctx.api.access_token == 'token'

    runner = CliRunner()
    result = runner.invoke(cli.root, 'cmd')

    print_error(result)
    assert result.exit_code == 0


def test_root_access_token_no_file(jsonfile, config_fpath):
    @cli.root.command()
    @cli.click.pass_obj
    def cmd(ctx):
        assert ctx.api.access_token is None

    runner = CliRunner()
    result = runner.invoke(cli.root, 'cmd')

    print_error(result)
    assert result.exit_code == 0


def test_version(clictx):
    runner = CliRunner()
    result = runner.invoke(cli.version, obj=clictx)

    print_error(result)
    assert result.exit_code == 0
    assert result.output.endswith(__version__ + '\n')


def test_login(monkeypatch, clictx):
    auth = {
        'access_token': 'token',
        'expire_at': '2019-01-01T01:00:00+00:00'
    }

    def authenticate(self, username, password):
        assert username == 'user@test.com'
        assert password == 'pass'
        return auth
    monkeypatch.setattr(cli.API, 'authenticate', authenticate)

    runner = CliRunner()
    result = runner.invoke(cli.login, '--username user@test.com', input='pass\n', obj=clictx)

    print_error(result)
    assert result.exit_code == 0
    assert clictx.config.get('auth') == auth
    assert result.output.endswith('Login Succeeded\n')


def test_adduser(monkeypatch, clictx):
    resp = {
        'data': {'created_at': '2019-02-19T16:39:24+00:00', 'id': 4, 'username': 'user@test.com'},
        'meta': {}
    }

    def create_user(self, username, password):
        assert username == 'user@test.com'
        assert password == 'pass'
        return resp
    monkeypatch.setattr(cli.API, 'create_user', create_user)

    runner = CliRunner()
    result = runner.invoke(cli.adduser, '--username user@test.com', input='pass\n', obj=clictx)

    print_error(result)
    assert result.exit_code == 0
    assert json.dumps(resp['data']) in result.output


def test_users(monkeypatch, clictx):
    def list_users(self):
        return {
            'data': [],
            'meta': {'total_count': 0}
        }
    monkeypatch.setattr(cli.API, 'list_users', list_users)

    def format_user(result):
        return 'users'
    monkeypatch.setattr(cli.formatter, 'format_users', format_user)

    runner = CliRunner()
    result = runner.invoke(cli.users, obj=clictx)

    print_error(result)
    assert result.exit_code == 0
    assert result.output == 'users\n'


def test_jobs(monkeypatch, clictx):
    def list_jobs(self, q=None, offset=None, limit=None):
        return {
            'data': [],
            'meta': {'total_count': 0}
        }
    monkeypatch.setattr(cli.API, 'list_jobs', list_jobs)

    def format_jobs(result, offset, limit):
        return 'jobs'
    monkeypatch.setattr(cli.formatter, 'format_jobs', format_jobs)

    runner = CliRunner()
    result = runner.invoke(cli.jobs, obj=clictx)

    print_error(result)
    assert result.exit_code == 0
    assert result.output == 'jobs\n'


def test_jobs_default(monkeypatch, clictx):
    def list_jobs(self, q=None, offset=None, limit=None):
        assert q is None
        assert offset == 0
        assert limit == 20

        return {
            'data': [],
            'meta': {'total_count': 0}
        }
    monkeypatch.setattr(cli.API, 'list_jobs', list_jobs)

    runner = CliRunner()
    result = runner.invoke(cli.jobs, obj=clictx)

    print_error(result)
    assert result.exit_code == 0


def test_jobs_pause(monkeypatch, clictx):
    monkeypatch.setattr(cli.API, 'pause_job', handle_action)

    runner = CliRunner()
    result = runner.invoke(cli.pause, '11', obj=clictx)

    print_error(result)
    assert result.exit_code == 0
    assert result.output == '11\n'


def test_jobs_resume(monkeypatch, clictx):
    monkeypatch.setattr(cli.API, 'resume_job', handle_action)

    runner = CliRunner()
    result = runner.invoke(cli.resume, '11', obj=clictx)

    print_error(result)
    assert result.exit_code == 0
    assert result.output == '11\n'


def test_jobs_retry(monkeypatch, clictx):
    monkeypatch.setattr(cli.API, 'retry_job', handle_action)

    runner = CliRunner()
    result = runner.invoke(cli.retry, '11', obj=clictx)

    print_error(result)
    assert result.exit_code == 0
    assert result.output == '11\n'


def test_jobs_delete(monkeypatch, clictx):
    monkeypatch.setattr(cli.API, 'delete_job', handle_action)

    runner = CliRunner()
    result = runner.invoke(cli.delete, '11', obj=clictx)

    print_error(result)
    assert result.exit_code == 0
    assert result.output == '11\n'
