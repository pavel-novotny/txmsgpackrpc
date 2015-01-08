from twisted.internet import protocol

from txmsgpackrpc.protocol import Msgpack
from txmsgpackrpc.handler  import SimpleConnectionHandler


class MsgpackServerFactory(protocol.Factory):
    protocol = Msgpack

    def __init__(self):
        self.connections = set()

    def buildProtocol(self, addr):
        p = self.protocol(self, sendErrors=True)
        return p

    def addConnection(self, connection):
        self.connections.add(connection)

    def delConnection(self, connection):
        self.connections.remove(connection)


class MsgpackClientFactory(protocol.ReconnectingClientFactory):
    maxDelay = 12
    protocol = Msgpack

    def __init__(self, handler=SimpleConnectionHandler, connectTimeout=None, waitTimeout=None, handlerConfig={}):
        self.connectTimeout = connectTimeout
        self.waitTimeout = waitTimeout
        self.handler = handler(self, **handlerConfig)

    def buildProtocol(self, addr):
        self.resetDelay()
        p = self.protocol(self, timeout=self.waitTimeout)
        return p

    def clientConnectionFailed(self, connector, reason):
        # print "clientConnectionFailed"
        connector.timeout = self.connectTimeout
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


    def clientConnectionLost(self, connector, reason):
        # print "clientConnectionLost"
        connector.timeout = self.connectTimeout
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def addConnection(self, connection):
        self.handler.addConnection(connection)

    def delConnection(self, connection):
        self.handler.delConnection(connection)


__all__ = ['MsgpackServerFactory', 'MsgpackClientFactory']
