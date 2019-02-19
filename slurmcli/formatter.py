"""Format outputs"""
from texttable import Texttable


def format_users(result: dict) -> str:
    """Returns formatted users"""
    data = result['data']

    headers = ('id', 'username', 'created_at')
    rows = [headers]
    for record in data:
        row = [record[col] for col in headers]
        rows.append(row)

    table = Texttable(max_width=250)
    table.set_deco(Texttable.HEADER)
    table.set_cols_align(['r', 'l', 'r'])
    table.add_rows(rows)
    table_text = table.draw()

    total_count = result['meta']['total_count']
    fmt = '{} - {} of {}'
    page = fmt.format(0, total_count, total_count)

    return table_text + '\n' + page


def format_jobs(result: dict, offset: int, limit: int):
    """Returns formatted users"""
    data = result['data']

    headers = ['id', 'name', 'owner', 'member_count', 'duration', 'status', 'created_at']
    idx_duration = headers.index('duration')
    rows = [headers]
    for record in data:
        row = [record[col] for col in headers]
        if row[idx_duration] is not None:
            row[idx_duration] /= 60.0
        rows.append(row)
    headers[idx_duration] = headers[idx_duration] + ' (min)'

    table = Texttable(max_width=250)
    table.set_deco(Texttable.HEADER)
    table.set_cols_align(['r', 'l', 'l', 'r', 'r', 'c', 'r'])
    table.add_rows(rows)
    table_text = table.draw()

    total_count = result['meta']['total_count']
    fmt = '{} - {} of {}'
    page = fmt.format(min(offset, total_count), min(offset + limit, total_count), total_count)

    return table_text + '\n' + page
