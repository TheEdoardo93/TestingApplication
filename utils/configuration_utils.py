import configparser


class ConfigurationsUtils(object):
    def __init__(self, config_file='./utils/init_config_test.cfg'):
        config = configparser.ConfigParser()
        config.read(config_file)

        # Read the path to the SQLite database
        self._path_to_sqlite_database = config.get('DATABASE', 'PathToDatabase')
        self._database_name = config.get('DATABASE', 'DatabaseName')
