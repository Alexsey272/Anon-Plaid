import logging

#логирование
logging.basicConfig(filename="all_log.log", level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')
warning_log = logging.getLogger("warning_log")
warning_log.setLevel(logging.WARNING)

fh = logging.FileHandler("warning_log.log")

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

warning_log.addHandler(fh)