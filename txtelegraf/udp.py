# coding: utf-8
# Copyright 2016 Chris Kirkos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import (absolute_import, unicode_literals)

import logging
import socket

from twisted.internet.defer import succeed

logger = logging.getLogger(__name__)

DEFAULT_HOST="127.0.0.1"
DEFAULT_UDP_PORT=8092

class TelegrafUDPClient(object):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_UDP_PORT, blocking=False):
        self.host = host
        self.port = port
        self.blocking = blocking
        self.s = None

    def getConnection(self):
        if self.s is None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.setblocking(self.blocking)
        return self.s

    def sendMeasurement(self, measurement):
        self.getConnection().sendto(str(measurement), (self.host, self.port))
        return succeed(1)

    def close(self):
        if self.s is not None:
            self.s.close()
            self.s = None
        return succeed(1)
