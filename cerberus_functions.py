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

import os
import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util

class Spot:
    """Spot Connectivity Functions"""

    def __init__(self, username, passwd, hostname):
        """init"""
        self.username = username
        self.passwd = passwd
        self.hostname = hostname

    def spot_login(self):
        """Spot Authentication"""

        global robot
        global lease_client

        print("Connecting to spot at " + self.hostname + " ...\n\n\n")

        # ======= LOGIN/AUTH/CONNECT =======
        # Set username/passwd as env vars
        os.environ["BOSDYN_CLIENT_USERNAME"] = self.username
        os.environ["BOSDYN_CLIENT_PASSWORD"] = self.passwd

        # Create SDK and assign hostname
        sdk = bosdyn.client.create_standard_sdk('Cerberus')
        robot = sdk.create_robot(self.hostname)
        # Connect and authenticate to spot using env vars
        bosdyn.client.util.authenticate(robot)
        robot.time_sync.wait_for_sync()
        assert not robot.is_estopped(), "Robot is estopped, use an external E-Stop client"
        lease_client = robot.ensure_client(bosdyn.client.lease.LeaseClient.default_service_name)

    def spot_poweroff(self):
        """Causes Spot to immediately collapse and power off"""

        operator_msg = "FUCK MAGA"

        # ======= TERMINATE SPOT =======
        with bosdyn.client.lease.LeaseKeepAlive(lease_client, must_acquire=True, return_at_exit=True):
            # Send a comment to the owners of the Spot device
            robot.operator_comment(operator_msg, timeout=10)
            # "cut_immediately" causes spot to just power off and potentially collapse lol
            robot.power_off(cut_immediately=True, timeout_sec=10)
            assert not robot.is_powered_on(), "Robot power off failed."
            print("Spot has been powered off")
