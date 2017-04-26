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

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet.defer import succeed, Deferred

logger = logging.getLogger(__name__)

DEFAULT_HOST="127.0.0.1"
DEFAULT_UDP_PORT=8092

class TelegrafUDPProtocol(DatagramProtocol):

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_UDP_PORT):
        self.host = host
        self.port = port
        self.closed_d = None

    def startProtocol(self):
        logger.debug('<TelegrafUDPProtocol.startProtocol>')
        self.closed_d = Deferred()
        self.transport.connect(self.host, self.port)

    def stopProtocol(self):
        logger.debug('<TelegrafUDPProtocol.stopProtocol>')
        self.closed_d.callback(0)

    def write(self, s):
        logger.debug('<TelegrafUDPProtocol.write>')
        return self.transport.write(s + b"\n")  # returns bytes sent

    def close(self):
        self.transport.loseConnection()
        return self.closed_d


class TelegrafUDPClient(object):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_UDP_PORT):
        self.host = host
        self.port = port
        self.proto = None

    def getConnection(self):
        if self.proto is None:
            self.proto = DatagramProtocol()
            reactor.listenUDP(0, self.proto)

    def sendMeasurement(self, measurement):
        self.getConnection()
        self.proto.transport.write(str(measurement), (self.host, self.port))
        return succeed(1)

    def close(self):
        if self.proto is not None:
            self.proto.transport.loseConnection()
        return succeed(1)
