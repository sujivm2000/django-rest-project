import os, logging
import errno, time, datetime

from importlib import import_module

def standalone_main(cls, *args, **kwargs):
    s = time.time()
    status = 0

    obj = cls(*args, **kwargs)
    obj.parse()

    status = obj.process()
    if status:
        msg = '%s process failed with status: %s' % (cls.__name__, status)
        obj.log.ERROR(msg)
        print(msg)

    obj.close()

    obj.log.info('Time Taken: %s' % datetime.timedelta(seconds=round((time.time()-s))))

def init_logger(filename, level=logging.INFO, frmt=None, maxbytes=104857600, backupcount=5):
    site_name       = os.environ.get('SITE')
    env_home        = os.environ.get('ENV_HOME')

    if site_name and env_home:
        log_dir_path    = "/".join([env_home, site_name+"_logs"])
        filename        = filename.split('/')[-1]
        filename        = os.path.join(log_dir_path, filename)
        makedir_p(os.path.dirname(filename))
    if os.environ.get('DJANGO_LOGS'):
        filename = os.environ.get('DJANGO_LOGS')
    log = logging.getLogger(filename)
    log.setLevel(level)
    handler = logging.handlers.RotatingFileHandler(filename, maxBytes=maxbytes, backupCount=backupcount)
    log.addHandler(handler)

    frmt = frmt if frmt else '%(asctime)s %(filename)s:%(lineno)s %(levelname)s: %(process)d: %(message)s'
    formatter = logging.Formatter(frmt)
    handler.setFormatter(formatter)

    return log

def close_logger(log):
    logging.shutdown()

def makedir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def import_module_var(path, default):
    module_name, var_name = path.rsplit('.', 1)
    return getattr(import_module(module_name), var_name, default)

MEDIA_PREFIX = 'media://'
def get_media_path(url):
    if url.startswith(MEDIA_PREFIX):
        return url[len(MEDIA_PREFIX):]
    return url

def get_media_url(path):
    return MEDIA_PREFIX + path

def get_parent(obj):
    for rel_obj in obj._meta._relation_tree:
        field = rel_obj.remote_field
        if field.parent_link:
            parent_obj = getattr(obj, field.name, None)
            if parent_obj:
                return parent_obj

def upload_path(obj, filepath):
    return obj.upload_path(filepath)



