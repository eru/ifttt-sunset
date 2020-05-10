#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Kazuki Hashimoto <eru.tndl@gmail.com>
#
# Distributed under terms of the MIT license.

import argparse
from datetime import datetime, timedelta, timezone
import os
import requests
from suntime import Sun


ONCE_A_DAY_FILE = os.path.dirname(os.path.abspath(__file__)) + os.sep + '.last'


parser = argparse.ArgumentParser(description='This script calls the Maker event API of ifttt at sunset time.')
parser.add_argument('--latitude', '-lat', action='store', type=float, required=True, help='Latitude')
parser.add_argument('--longitude', '-lng', action='store', type=float, required=True, help='Longitude')
parser.add_argument('--event', '-e', action='store', type=str, required=True, help='IFTTT Maker Event API name')
parser.add_argument('--key', '-k', action='store', type=str, required=True, help='IFTTT Maker Event API key')
parser.add_argument('--add', '-a', action='store', nargs='?', type=int, help='Additional time (minutes)')
parser.add_argument('--once-a-day', '-once', action='store_true', help='Runs once a day for execution from a job scheduler such as CRON')
args = parser.parse_args()

now = datetime.now(timezone.utc)

if args.once_a_day and os.path.exists(ONCE_A_DAY_FILE):
    with open(ONCE_A_DAY_FILE, 'r') as f:
        line = f.readline()
        try:
            last = datetime.fromisoformat(line)
        except:
            print('The last execution date is an invalid value. Delete the `.last` file.')
            exit(1)

        if now.date() == last.date():
            # Do nothing
            exit(0)

try:
    sun = Sun(args.latitude, args.longitude)
    sunset = sun.get_sunset_time()
except:
    print('Uncalculated latitude and longitude.')
    exit(1)

if args.add:
    try:
        add_timedelta = timedelta(minutes=args.add)
    except:
        print('Uncalculated additional time.')
        exit(1)
    sunset += add_timedelta

if now < sunset:
    # Do nothing
    exit(0)

url = 'https://maker.ifttt.com/trigger/{event}/with/key/{key}'.format(event=args.event, key=args.key)
response = requests.post(url)
if response.status_code != 200:
    print('Failed to post to `{url}`.'.format(url=response.url))
    exit(1)

if args.once_a_day:
    with open(ONCE_A_DAY_FILE, 'w') as f:
        f.write(now.isoformat())
