#!/usr/bin/env python3
"""A small app to log the productivity of a fellow student."""

import datetime
import distutils.util
import os
import pickle
import sys


DATAFILE = 'brankotimelog.pickle'
NO_STATUS = 0
PRODUCTIVE = 1
UNPRODUCTIVE = 2

def prompt(query):
    """Prompt a yes/no question and get an answer.

    A simple function to ask yes/no questions on the command line.
    Credit goes to Matt Stevenson. See:
    http://mattoc.com/python-yes-no-prompt-cli.html

    Args:
        query: A string containing a question.

    Returns:
        A boolean corresponding to the answer to the question asked.
    """
    sys.stdout.write("%s [y/n]: " % query)
    val = input().lower()
    try:
        result = distutils.util.strtobool(val)
    except ValueError:
        # Result no good! Ask again.
        sys.stdout.write("Please answer with y/n\n")
        return prompt(query)
    return result

if __name__ == '__main__':
    # Check if datafile exists and load it if so
    if not os.path.exists(DATAFILE):
        # Make the data object
        timelog = {'timeproductive': datetime.timedelta(),
                   'timeunproductive': datetime.timedelta(),
                   'lasttime': datetime.datetime.now(),
                   'lasttimestatus': NO_STATUS
                  }
    else:
        # Load the datefile
        with open(DATAFILE, 'rb') as f:
            timelog = pickle.load(f)

    # Get current time
    now = datetime.datetime.now()

    # Finish a productive or unproductive session
    if timelog['lasttimestatus'] != NO_STATUS:
        if timelog['lasttimestatus'] == PRODUCTIVE:
            message = "Has Branko stopped being productive?"
        else:
            message = "Has Branko stopped being unproductive?"

        if prompt(message):
            if timelog['lasttimestatus'] == PRODUCTIVE:
                timelog['timeproductive'] += now - timelog['lasttime']
            else:
                timelog['timeunproductive'] += now - timelog['lasttime']

            timelog['lasttimestatus'] = NO_STATUS
        else:
            # Leave if session not over
            sys.exit(0)

    # Add new status
    if prompt("Has Branko started being productive?"):
        timelog['lasttimestatus'] = PRODUCTIVE
        timelog['lasttime'] = now
    elif prompt("Has Brakno started being unproductive?"):
        timelog['lasttimestatus'] = UNPRODUCTIVE
        timelog['lasttime'] = now
    else:
        timelog['lasttimestatus'] = NO_STATUS

    # Write to file
    with open(DATAFILE, 'wb') as f:
        pickle.dump(timelog, f, pickle.HIGHEST_PROTOCOL)

    # Show stats
    print()
    print("So far, Branko has allocated his study time as follows:")
    print("Productive:\t%s" % timelog['timeproductive'])
    print("Unproductive:\t%s" % timelog['timeunproductive'])
