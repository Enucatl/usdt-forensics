import datetime

def log_config(verbose):
    filename = "log_of_session_started_on_{0}.log".format(
        datetime.datetime.now().strftime("%y%m%d.%H%M%S%f"))
    levels = [
        'ERROR',
        'INFO',
        'DEBUG',
    ]
    verbose = min(len(levels) - 1, verbose)
    return dict(
        version = 1,
        disable_existing_loggers = False,
        formatters = {
            'f': {'format':
                  '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
                 }
        },
        handlers = {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'f',
                'level': levels[verbose],
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'f',
                'filename': filename,
                'level': levels[verbose],
            },
        },
        root = {
            'handlers': ['console', 'file'],
            'level': levels[verbose],
        },
    )
