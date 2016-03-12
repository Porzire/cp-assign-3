import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')
print config.sections()
print config.options('Network')
print config.options('Handlers')
print config.get('Network', 'port')
print config.get('Network', 'handlers[]')
