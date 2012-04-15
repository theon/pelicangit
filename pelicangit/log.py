import logging

def setup_logging():
    home_dir = os.path.expanduser("~")
    log_file = os.path.join(home_dir, 'pelicangit.log')
    
    logger = logging.getLogger('pelicangit')
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(levelname)s %(asctime)s :: %(message)s')
    logger.setFormatter(formatter)
    
    file_handler = logging.FileHandler(filename=log_file)
    logger.addHandler(file_handler)