from slurmcli.config import Config


def test_from_json(jsonfile):
    jsonfile.write('{"k": "v"}')

    config = Config.from_json(str(jsonfile))

    assert config.get('k') == 'v'


def test_persistence(jsonfile):
    config = Config(fpath=str(jsonfile))
    config.put('k', 'v')

    assert jsonfile.read() == '{"k": "v"}'
