# coding: utf-8
from __future__ import (absolute_import, unicode_literals)

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.protocols.basic import LineOnlyReceiver
from twisted.protocols import policies
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import Factory

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
        returnValue(self.proto)

    @inlineCallbacks
    def sendMeasurement(self, measurement):
        proto = yield self.getConnection()
        returnValue(proto.sendMeasurement(measurement))

    def close(self):
        return self.proto.transport.loseConnection()

class TelegrafTCPProtocol(LineOnlyReceiver, policies.TimeoutMixin, object):
    def connectionMade(self):
        print('<TelegrafProtocol.connectionMade>', self)
        self.connected = 1
        LineOnlyReceiver.connectionMade(self)

    def connectionLost(self, reason):
        self.connected = 0
        print('<TelegrafProtocol.connectionLost>', reason, self)
        LineOnlyReceiver.connectionLost(self)

    def sendMeasurement(self, measurement):
        print('Sending', str(measurement))
        return self.sendLine(str(measurement))

class TelegrafTCPFactory(Factory):
    protocol = TelegrafTCPProtocol
    # def startFactory(self):
    # def stopFactory(self):
