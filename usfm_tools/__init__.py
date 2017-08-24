import logging

# set up logging
__logger = logging.getLogger('usfm_tools')
__logger.setLevel(logging.INFO)
__handler = logging.StreamHandler()
__handler.setLevel(logging.INFO)
__formatter = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
__handler.setFormatter(__formatter)
__logger.addHandler(__handler)