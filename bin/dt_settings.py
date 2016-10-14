import logging

# --- logging --- #
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)-8s %(asctime)s %(name)-12s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# --- settings --- #
DEFAULT_DELIMITER = '|'
DTOOLS_LIB_RELATIVE_PATH = '..'
