#!/usr/bin/env python3
# See LICENSE file for licensing details.

"""Charm the application."""

import logging

import ops
from charms.operator_libs_linux.v0 import grub, sysctl

from profiles import Profile

logger = logging.getLogger(__name__)


class OsConfigWorkshopCharm(ops.CharmBase):
    """Charm the application."""

    def __init__(self, *args):
        super().__init__(*args)
        self.grub = grub.Config(self.app.name)
        self.sysctl = sysctl.Config(self.app.name)

        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.remove, self._on_remove)

    def _on_start(self, event: ops.StartEvent):
        """Handle start event."""
        self.unit.status = ops.ActiveStatus()

    def _on_config_changed(self, event: ops.ConfigChangedEvent):
        """Handle config changed event."""
        profile = self.config["profile"]

        configured = self._config(profile=profile)

        if not configured:
            self.unit.status = ops.BlockedStatus()
            return

        self.unit.status = ops.ActiveStatus()

    def _on_remove(self, event: ops.RemoveEvent):
        """Handle start event."""
        self.grub.remove()
        self.sysctl.remove()

    def _config(self, profile: str) -> bool:
        """Add sysctl config."""
        configured = True
        if profile == "production":
            try:
                self.grub.update(config=Profile.PRODUCTION.value.grub)
            except (grub.ApplyError, grub.ValidationError) as e:
                logger.error(f"Error setting GRUB profile values: {e.message}")
                configured = False

            try:
                self.sysctl.configure(config=Profile.PRODUCTION.value.sysctl)
            except sysctl.Error as e:
                logger.error(f"Error setting sysctl profile values: {e.message}")
                configured = False

        elif profile == "testing":
            try:
                self.grub.update(config=Profile.TESTING.value.grub)
            except (grub.ApplyError, grub.ValidationError) as e:
                logger.error(f"Error setting GRUB profile values: {e.message}")
                configured = False

            try:
                self.sysctl.configure(config=Profile.TESTING.value.sysctl)
            except sysctl.Error as e:
                logger.error(f"Error setting sysctl profile values: {e.message}")
                configured = False

        return configured


if __name__ == "__main__":  # pragma: nocover
    ops.main(OsConfigWorkshopCharm)  # type: ignore
