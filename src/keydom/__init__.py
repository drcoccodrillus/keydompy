__version__ = "0.1"
__author__ = "dr.coccodrillus"
__email__ = "dr.coccodrillus@gmail.com"
__license__ = "Apache License"


from .keydom import KeydomManager

__all__ = ['KeydomManager']

DEFAULT_CONFIG = {
    "keydom_ip": "172.26.20.100",
    "keydom_port": 443,
    "keydom_protocol": "https",
    "keydom_username": "admin",
    "keydom_password": "admin",
}

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Module loaded")
