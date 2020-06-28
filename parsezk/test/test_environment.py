from parsezk.environment import Config


def test_config_set_get():
    key = 'foo'
    value = 'bar'
    Config.set(key, value)
    assert Config.get(key) == value
