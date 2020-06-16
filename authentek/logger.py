import os
import logging
import logging.config as sysconf

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
sysconf.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
