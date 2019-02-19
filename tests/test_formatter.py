from textwrap import dedent

import pytest

from slurmcli import formatter


@pytest.fixture
def empty_result():
    return {
        'data': [],
        'meta': {'total_count': 0}
    }


def test_format_users_empty(empty_result):
    result = formatter.format_users(empty_result)

    assert result == dedent('''\
    id   username   created_at
    ==========================
    0 - 0 of 0''')


def test_format_users():
    result = {
        'data': [
            {'id': 1, 'username': 'user1@test.com', 'created_at': '2019-01-01T01:00:00+00:00'},
            {'id': 11, 'username': 'user2@test.com', 'created_at': '2019-01-01T01:00:00+00:00'}
        ],
        'meta': {'total_count': 2}
    }
    result = formatter.format_users(result)

    assert result == dedent('''\
    id      username             created_at        
    ===============================================
     1   user1@test.com   2019-01-01T01:00:00+00:00
    11   user2@test.com   2019-01-01T01:00:00+00:00
    0 - 2 of 2''')  # noqa: W291


def test_format_jobs_empty(empty_result):
    result = formatter.format_jobs(empty_result, 0, 0)

    assert result == dedent('''\
    id   name   owner   member_count   duration (min)   status   created_at
    =======================================================================
    0 - 0 of 0''')


def test_format_jobs():
    data = {
        'data': [
            {
                'id': 1,
                'name': 'job1',
                'owner': 'owner@test.com',
                'member_count': 3000,
                'duration': 120,
                'status': 'done',
                'created_at': '2019-01-01T01:00:00+00:00'
            },
            {
                'id': 11,
                'name': 'job2',
                'owner': 'owner@test.com',
                'member_count': 3000,
                'duration': 30,
                'status': 'done',
                'created_at': '2019-01-01T01:00:00+00:00'
            },
        ],
        'meta': {'total_count': 2}
    }
    result = formatter.format_jobs(data, 0, 10)

    assert result == dedent('''\
    id   name       owner        member_count   duration (min)   status          created_at        
    ===============================================================================================
     1   job1   owner@test.com           3000                2    done    2019-01-01T01:00:00+00:00
    11   job2   owner@test.com           3000            0.500    done    2019-01-01T01:00:00+00:00
    0 - 2 of 2''')  # noqa: W291


def test_format_jobs_duration_none():
    data = {
        'data': [
            {
                'id': 1,
                'name': 'job1',
                'owner': 'owner@test.com',
                'member_count': 3000,
                'duration': None,
                'status': 'queued',
                'created_at': '2019-01-01T01:00:00+00:00'
            },
        ],
        'meta': {'total_count': 1}
    }
    result = formatter.format_jobs(data, 0, 10)

    assert result == dedent('''\
    id   name       owner        member_count   duration (min)   status          created_at        
    ===============================================================================================
     1   job1   owner@test.com           3000             None   queued   2019-01-01T01:00:00+00:00
    0 - 1 of 1''')  # noqa: W291


def test_format_jobs_member_count_none():
    data = {
        'data': [
            {
                'id': 1,
                'name': 'job1',
                'owner': 'owner@test.com',
                'member_count': None,
                'duration': 60,
                'status': 'done',
                'created_at': '2019-01-01T01:00:00+00:00'
            },
        ],
        'meta': {'total_count': 1}
    }
    result = formatter.format_jobs(data, 0, 10)

    assert result == dedent('''\
    id   name       owner        member_count   duration (min)   status          created_at        
    ===============================================================================================
     1   job1   owner@test.com           None                1    done    2019-01-01T01:00:00+00:00
    0 - 1 of 1''')  # noqa: W291


def test_format_jobs_page():
    data = {
        'data': [],
        'meta': {'total_count': 100}
    }
    result = formatter.format_jobs(data, 1, 10)

    assert result.endswith('1 - 11 of 100')
