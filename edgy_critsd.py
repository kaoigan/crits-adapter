#!/usr/bin/env python2.7
from docopt import docopt
import os.path
from sys import path as python_path
python_path.append('./lib_')
import util_
import log_
import db_
import signal

__version__ = '0.2'
app_path = os.path.split(os.path.abspath(__file__))[0]
default_config = os.path.join(app_path, 'config.yaml')
__doc__ = '''edgy_critsd.py: a daemon to drive edgy_crits

Usage:
    edgy_crits.py start [--config=CONFIG]
    edgy_crits.py stop [--config=CONFIG]
    edgy_crits.py restart [--config=CONFIG]
    edgy_crits.py status [--config=CONFIG]

    edgy_crits.py --help
    edgy_crits.py --version


Options:
    -c CONFIG --config=CONFIG         Specify config file to use [default: %s].
    -h --help                         Show this screen.
    -V --version                      Show version.

Please report bugs to support@soltra.com
''' % (default_config)

def main():
    args = docopt(__doc__, version=__version__)
    config = util_.parse_config(args['--config'])
    config['config_file'] = args['--config']
    config['daemon']['app_path'] = app_path
    logger = log_.setup_logging(config)
    config['logger'] = logger
    db = db_.DB(config)
    config['db'] = db
    daemon = util_.Daemon(config)
    if args['start']:
        logger.info('edgy_critsd starting...')
        signal.signal(signal.SIGTERM, util_.signal_handler)
        daemon.start()
    elif args['stop']:
        logger.info('edgy_critsd stopping...')
        daemon.stop()
    elif args['restart']:
        logger.info('edgy_critsd restarting...')
        daemon.restart()

if __name__ == '__main__':
    main()
