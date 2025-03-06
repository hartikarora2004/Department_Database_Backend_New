import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set Level of logger
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('.dept_db.log')

# Set the level of the file handler
handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add formatter to handler
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)
