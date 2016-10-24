# coding: utf-8
# Copyright 2016 Chris Kirkos
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
from __future__ import (absolute_import, division, print_function, unicode_literals)

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from txtelegraf import TelegrafTCPClient, TelegrafUDPClient, Measurement
from twisted.internet.task import deferLater

import logging

def sendFailed(failure, measurement):
    print('<sendFailed>', failure, measurement)

@inlineCallbacks
def writeMeasurements(client):
    measurement_values = [
        ('Chris', 6.5, 10.0, 85, 'run1'),
        ('Chris', 6.8, 11.0, 90, 'run1'),
        ('Chris', 6.2, 12.0, 83, 'run1')
    ]
    for runner_name, speed, distance, heart_rate, run_id in measurement_values:
        measurement = Measurement("run_stats",
            tags={"runner_name": runner_name, "run_id": run_id},
            fields={"speed": speed, "distance": distance, "heart_rate": heart_rate}
        )

        yield deferLater(reactor, 1, client.sendMeasurement, measurement)\
              .addErrback(sendFailed, measurement)

    # yield deferLater(reactor, 1, lambda *args: None)

def main():
    client = TelegrafTCPClient()
    # client = TelegrafUDPClient()

    def closeClient(*args):
        return client.close()

    def stopReactor(*args):
        return reactor.stop()

    writeMeasurements(client)\
        .addCallbacks(closeClient, closeClient)\
        .addCallbacks(stopReactor, stopReactor)

    reactor.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
