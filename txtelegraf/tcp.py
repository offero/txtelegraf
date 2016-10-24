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

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue, Deferred, succeed
from twisted.protocols.basic import LineOnlyReceiver
from twisted.protocols import policies
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import Factory

logger = logging.getLogger(__name__)

DEFAULT_HOST="127.0.0.1"
DEFAULT_TCP_PORT=8094

class TelegrafTCPClient(object):

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_TCP_PORT):
        self.host = host
        self.port = port
        self.factory = TelegrafTCPFactory()
        self.proto = None

    @inlineCallbacks
    def getConnection(self):
        if self.proto and self.proto.connected:
            returnValue(self.proto)

        endpoint = TCP4ClientEndpoint(reactor, self.host, self.port)
        self.proto = yield endpoint.connect(self.factory)
        # connector = proto.transport.connector
        returnValue(self.proto)

    @inlineCallbacks
    def sendMeasurement(self, measurement):
        proto = yield self.getConnection()
        returnValue(proto.sendMeasurement(measurement))

    def close(self):
        logger.debug('<TelegrafTCPClient.close>')
        return self.proto.close()

class TelegrafTCPProtocol(LineOnlyReceiver, policies.TimeoutMixin, object):
    delimiter = b'\n'

    def __init__(self):
        self.closed_d = None

    def close(self):
        """Returns a deferred that fires when the connection is closed."""
        if self.connected == 0:
            return succeed(0)

        self.transport.loseConnection()
        return self.closed_d

    def connectionMade(self):
        logger.debug('<TelegrafProtocol.connectionMade> %s', self)
        self.closed_d = Deferred()
        self.connected = 1
        LineOnlyReceiver.connectionMade(self)

    def connectionLost(self, reason):
        self.connected = 0
        self.closed_d.callback(0)
        logger.debug('<TelegrafProtocol.connectionLost> %s %s', reason, self)
        LineOnlyReceiver.connectionLost(self)

    def sendMeasurement(self, measurement):
        logger.debug('Sending %s', str(measurement))
        return self.sendLine(str(measurement))

    def lineReceived(self, line):
        logger.debug("<TelegrafProtocol.lineReceived> %s", line)

    def logPrefix(self):
        return self.__class__.__name__

class TelegrafTCPFactory(Factory):
    protocol = TelegrafTCPProtocol
    # def startFactory(self):
    # def stopFactory(self):
