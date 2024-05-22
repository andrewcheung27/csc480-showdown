import asyncio
import logging
import traceback
from run import showdown
import sys


logger = logging.getLogger(__name__)


def main():
    # run this on two terminals to make bots battle each other,
    # one bot should be set to accept challenges, the other bot should be set to challenge
    try:
        if len(sys.argv) <= 1:
            logger.debug("Setting up default environment")
            asyncio.run(showdown())  # default to env
        else:
            env_path = sys.argv[1]
            logger.debug("Setting up using environment: " + env_path)
            asyncio.run(showdown(env_path))  # specify env
    except Exception as e:
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
