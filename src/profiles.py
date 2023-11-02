#!/usr/bin/env python3

"""Profile setting for OS configs."""

TESTING_PROFILE = {
    "vm.swappiness": "1",
    "net.ipv4.tcp_max_syn_backlog": "2048",
}
PRODUCTION_PROFILE = {
    "vm.swappiness": "0",
    "net.ipv4.tcp_max_syn_backlog": "4096",
}
