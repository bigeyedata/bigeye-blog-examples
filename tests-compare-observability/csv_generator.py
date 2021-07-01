#!/usr/bin/env python

#   Copyright 2021 Toro Data Labs, Inc
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.



import math
import random
import time
from datetime import timedelta, datetime

import numpy

SECONDS_IN_DAY = 60 * 60 * 24

def rand_jitter(arr):
    stdev = .01 * 24 * 60 * 60
    return arr + numpy.random.randn(len(arr)) * stdev


def generate_rows_for_day(num_rows, num_users, null_pct, epoch_seconds_start, duplicate_pct):
    mult = lambda n: n * math.floor(SECONDS_IN_DAY / num_rows) + epoch_seconds_start
    times = map(time.gmtime, rand_jitter(list(map(mult, range(num_rows)))))
    for tm in times:
        if random.randint(0, 100) < null_pct:
            user_id = ''
        else:
            user_id = f"user{random.randrange(0, num_users)}"
        page = random.randint(0, num_rows)
        row = [time.strftime('%Y-%m-%d %H:%M:%S', tm), user_id, f"https://my.company.com/products/{page}"]
        print(",".join(row))
        if random.randint(0, 100) < duplicate_pct:
            print(",".join(row))


def generate_rows(num_rows=10000, num_users=100, null_pct=5, start='2021-06-01', null_days=4, good_days=4,
                  duplicate_days=4, dup_pct=100):
    date = datetime.strptime(start, '%Y-%m-%d')
    for i in range(null_days):
        generate_rows_for_day(num_rows, num_users, null_pct, date.timestamp(), 0)
        date += timedelta(days=1)
    for i in range(good_days):
        generate_rows_for_day(num_rows, num_users, 0, date.timestamp(), 0)
        date += timedelta(days=1)
    for i in range(duplicate_days):
        generate_rows_for_day(num_rows, num_users, 0, date.timestamp(), dup_pct)
        date += timedelta(days=1)


if __name__ == '__main__':
    generate_rows()
