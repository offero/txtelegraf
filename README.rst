TxTelegraf
==========

Description
-----------

A TCP/UDP Telegraf/InfluxDB client for Twisted using the Influx Line
Format.

Tested with Telegraf 1.0.1 and Twisted 15.1.0 on Python 2.7.10.

Please let me know success/failures testing with other versions of
Telegraf/Influx, Twisted, and Python.

How To
------

Add the following to your Telegraf config.

::

    # Generic TCP listener
    [[inputs.tcp_listener]]
    service_address = ":8094"
    allowed_pending_messages = 10000
    max_tcp_connections = 250
    data_format = "influx"

    # Generic UDP listener
    [[inputs.udp_listener]]
    service_address = ":8092"
    allowed_pending_messages = 10000
    data_format = "influx"

    # This output is good for testing. Point it at Influx DB otherwise!
    [[outputs.file]]
    files = ["stdout", "metrics.out"]
    data_format = "influx"

Run telegraf

::

    telegraf -config telegraf.conf

Clone the repo and run the example

::

    git clone https://github.com/offero/txtelegraf.git
    cd txtelegraf
    pip install .
    python examples/client.py
