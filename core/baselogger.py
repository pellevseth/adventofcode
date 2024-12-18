import os

__author__ = 'pel'

# Logging stuff
import logging
import logging.config


class SafeLogger(logging.Logger):
    """
    Logger with qa logging
    """
    LOG_LEVEL_QA = 25

    def qa(self, msg, *args, **kwargs):
        self.log(self.LOG_LEVEL_QA, msg, *args, **kwargs)

logging.setLoggerClass(SafeLogger)
logging.addLevelName(SafeLogger.LOG_LEVEL_QA, 'QA')


def init_logger(level='DEBUG'):
    """
    Set up logging for commands
    Adds qa logging to file
    """
    LOGGING['handlers']['console']['level'] = level
    if level == 0:
        LOGGING['handlers']['console']['formatter'] = 'verbose'
    logging.config.dictConfig(LOGGING)


def getLogger(name):
    """
    :param name: Name of logger, typiccal name of file
    :return: Logger
    """
    logger = logging.getLogger(name)
    return logger

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            #'format': '%(levelname)-10s: SOURCE: %(name)-20s %(funcName)-10s MESSAGE: %(message)s'
            'format': '%(asctime)s %(levelname)-10s: SOURCE: %(name)-20s %(funcName)-10s MESSAGE: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
        'qa_format': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'qafile': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.curdir, 'QA_LOG'),
            'formatter': 'qa_format',
            'level': SafeLogger.LOG_LEVEL_QA,
        },
        'logfile': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.curdir, 'Log'),
            'formatter': 'simple',
            'level': 'DEBUG',
        },

    },
    'loggers': {
        '': {
            'handlers': ['qafile', 'logfile', 'console'],
            'level': 0,  #This ensures that everything is logged. Only handlers with level>the loggers level will logg
            'propagate': True,
        },
    },
}