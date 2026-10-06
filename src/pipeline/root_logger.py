import sys
import logging

def setup_logger():
    root_logger = logging.getLogger()

    if not root_logger.handlers:
#pipeline logs
        pipeline_handler = logging.FileHandler('logs/pipeline.log', mode='a', encoding='utf-8')
        pipeline_handler_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] - %(message)s")
        pipeline_handler.setFormatter(pipeline_handler_formatter)
        pipeline_handler.setLevel(logging.DEBUG)


        root_logger.addHandler(pipeline_handler)
#error logs
        error_handler = logging.FileHandler('logs/error.log', mode='a', encoding='utf-8')
        error_handler_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] - %(message)s")
        error_handler.setFormatter(error_handler_formatter)
        error_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(error_handler)
#change logs
        change_handler = logging.FileHandler('logs/change.log', mode='a', encoding='utf-8')
        change_handler_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] - %(message)s")
        change_handler.setFormatter(change_handler_formatter)
        change_handler.setLevel(logging.DEBUG)

        root_logger.addHandler(change_handler)
#stream handler
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler_formatter = logging.Formatter("%(levelname)s, %(module)s:%(lineno)d, - %(message)s")
        stream_handler.setFormatter(stream_handler_formatter)

        root_logger.addHandler(stream_handler)