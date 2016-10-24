# TxTelegraf

## Description

A TCP/UDP Telegraf/InfluxDB client for Twisted.

Tested with Telegraf 1.0.1

## How To

Add the following to your Telegraf config.

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

Read the example in `examples/client.py`.
