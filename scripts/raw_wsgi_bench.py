"""
    MoinMoin - raw_wsgi_bench

    @copyright: 2008 MoinMoin:FlorianKrupicka
    @license: GNU GPL, see COPYING for details.
"""

import time
import sys
import os

from werkzeug.test import Client

from moin.app import create_app

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tests"))

RUNS = 100
RUNS_MARKER = RUNS // 10
DOTS_MARKER = RUNS_MARKER // 5

PAGES = ("Home", "help-en/moin", "+index/all")

client = Client(create_app())

for page in PAGES:
    print('=== Run with page "%s" ===' % page)
    print("Running %i WSGI-requests:" % RUNS)
    timing = time.time()
    for run in range(RUNS):
        response = client.get(f"/{page}")
        assert response.status_code == 200
        if (run + 1) % RUNS_MARKER == 0:
            sys.stdout.write(f"{run + 1}")
        elif (run + 1) % DOTS_MARKER == 0:
            sys.stdout.write(".")
    timing = time.time() - timing

    print()
    print("Finished %i WSGI-requests in %.2f seconds" % (RUNS, timing))
    print("Time per request: %.4f seconds" % (timing / RUNS))
    print("Requests per second: %.2f" % (RUNS / timing))
