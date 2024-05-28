import asyncio
import constants
import logging
import traceback
import argparse
from run import showdown


logger = logging.getLogger(__name__)


def main():
    """Run this on two terminals to make bots battle each other. One bot
    should be set to accept challenges, and the second bot should be set to
    challenge the other.
    Usage: python3 bot_match.py [-e ENV_PATH] [-t TEAM_PATH] [--log-record]
    """
    try:
        parser = argparse.ArgumentParser(description="Pit two battle bots against each other.")
        parser.add_argument("-e", dest="env",
                            type=str, nargs=1, default=constants.DEFAULT_ENV,
                            help="path to environment file, relative to this file's parent directory")
        parser.add_argument("-t", dest="team",
                            type=str, nargs=1, default=None,
                            help="path to teams file, relative to teams/teams/")
        parser.add_argument("--log-record", dest="log_record",
                            type=str, nargs=1, default=None,
                            help="name of file to log wins and losses (writes W or L on each line)")
        args = parser.parse_args()

        # sometimes it's a list and sometimes it's the default value?
        if type(args.env) == list and len(args.env) > 0:
            env = args.env[0]
        else:
            env = args.env
        if args.team is not None and type(args.team) == list and len(args.team) > 0:
            team = args.team[0]
        else:
            team = None
        if args.log_record is not None and type(args.log_record) == list and len(args.log_record) > 0:
            log_record = args.log_record[0]
        else:
            log_record = None

        # run the bot
        logger.debug("Setting up using environment {e} and team {t}".format(e=env, t=team))
        asyncio.run(showdown(env_path=env, team=team, log_record=log_record))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
