import logging
from functools import wraps

def log_actions(start_message: str = "Starting execution of {callable}",
                complete_message: str = "Execution of {callable} completed",
                error_message: str = "Error occurred in {callable}: {exception}"):

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(fn.__module__)

            formatter = logging.Formatter(fmt="%(asctime)s - [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            logger.info(start_message.format(callable=fn.__name__))
            try:
                result = fn(*args, **kwargs)
                logger.info(complete_message.format(callable=fn.__name__))
                return result
            except Exception as e:
                logger.error(error_message.format(callable=fn.__name__, exception=e))
                raise
            finally:
                logger.removeHandler(console_handler)
        return wrapper
    return decorator

# Example usage:
logging.basicConfig(level=logging.DEBUG)

@log_actions(start_message="Processing {callable}...",
             complete_message="Successfully processed {callable}.",
             error_message="Error occurred while processing {callable}: {exception}")
def example_function(x, y):
    if x > y:
        raise ValueError("x should be less than y")
    return x + y

example_function(2, 3)
