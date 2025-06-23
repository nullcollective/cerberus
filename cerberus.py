#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: nullcollective
# This code is licensed under MIT license (see LICENSE for details)

# cerberus
# Disable Spot Robot \m/
####################################################################
# Usage: ./cerberus.py -h
# Depends on [Spot-SDK from bostondynamics]
# python3 -m pip install --upgrade bosdyn-client bosdyn-mission \
#                                  bosdyn-choreography-client \
#                                  bosdyn-orbit
####################################################################
# Copyright 2025 nullcollective
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import argparse
import bosdyn.client
import bosdyn.client.util

from cerberus_functions import Spot
#-###############################-#
# ░█▀▀░█▀▀░█▀▄░█▀▄░█▀▀░█▀▄░█░█░█▀▀
# ░█░░░█▀▀░█▀▄░█▀▄░█▀▀░█▀▄░█░█░▀▀█
# ░▀▀▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀
#-###############################-#

def main(argv):
    """MAIN"""
    # Grab cli parameters
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-u', '--username', required=True)
    parser.add_argument('-p', '--passwd', required=True)
    parser.add_argument('-h', '--hostname', required=True)
    args = parser.parse_args(argv)

    # Cerberus Spot Functions Instance
    cerberus_init = Spot(args.username, args.passwd, args.hostname)

    try:
        cerberus_init.spot_login() # Log into Spot
        cerberus_init.spot_poweroff() # Poweroff Spot
    except Exception as exc:  # pylint: disable=broad-except
        logger = bosdyn.client.util.get_logger()
        logger.error("[!] Spot threw an exception: %r", exc)
        sys.exit(1)

if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)
