import sys, os
from logging import getLogger


def debug_requests(f):
    """ Декоратор для отладки событий от телеграма
        Логгер подключается в самый последний момент чтобы быть уверенными в том, что конфиг логирования уже загружен
    """
    logger = getLogger(__name__)

    def inner(*args, **kwargs):
        try:
            logger.info('Обращение в функцию {}'.format(f.__name__))
            return f(*args, **kwargs)
        except Exception:
            logger.exception('Ошибка в обработчике {}'.format(f.__name__))
            raise

    return inner

def load_config(logger):
    conf_name = os.environ.get("TG_CONF")
    if conf_name is None:
        conf_name = "development"
    try:
        return logger.debug("Loaded config \"{}\" - OK".format(conf_name))
    except (TypeError, ValueError, ImportError):
        logger.error("Invalid config \"{}\"".format(conf_name))
        sys.exit(1)