#!/usr/bin/env python3

"""Profile setting for OS configs."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict


@dataclass
class ProfileConfig:
    """Definition of a profile."""

    sysctl: Dict[str, str]
    grub: Dict[str, str]


class Profile(Enum):
    """List of profiles."""

    TESTING = ProfileConfig(
        sysctl={
            "vm.swappiness": "1",
            "net.ipv4.tcp_max_syn_backlog": "2048",
        },
        grub={
            "GRUB_CMDLINE_LINUX_DEFAULT": "$GRUB_CMDLINE_LINUX_DEFAULT hugepagesz=500M",
        },
    )
    PRODUCTION = ProfileConfig(
        sysctl={
            "vm.swappiness": "0",
            "net.ipv4.tcp_max_syn_backlog": "4096",
        },
        grub={
            "GRUB_CMDLINE_LINUX_DEFAULT": "$GRUB_CMDLINE_LINUX_DEFAULT hugepagesz=1G",
        },
    )
