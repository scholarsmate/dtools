import logging

# --- logging --- #
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)-8s %(asctime)s %(name)-12s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# --- settings --- #
DTOOLS_LIB_RELATIVE_PATH = '..'
DEFAULT_DELIMITER = '~'
DEFAULT_LOCALE = 'en_US'
DEFAULT_DOMESTIC_COUNTRY_CODE = 'US'
