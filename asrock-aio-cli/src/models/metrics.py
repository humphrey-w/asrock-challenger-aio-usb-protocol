"""
System metrics data transfer object.

This module defines the SystemMetrics DTO which represents the actual system
information that will be displayed on the AIO LCD screen.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SystemMetrics:
    """
    Data Transfer Object (DTO) for system metrics.

    This immutable dataclass represents real-world system information that is
    to be encoded into USB protocol packets. Using a DTO separates the business
    logic from the protocol layer.

    Attributes:
        cpu_temperature_celsius: CPU temperature in Celsius
        cpu_frequency_mhz: CPU frequency in MHz
        pump_rpm: Pump speed in revolutions per minute

    The frozen=True parameter makes instances immutable and hashable, which is
    useful for caching and comparison.
    """

    cpu_temperature_celsius: float
    cpu_frequency_mhz: int
    pump_rpm: int

    def __post_init__(self):
        """Validate metric ranges."""
        if not (0 <= self.cpu_temperature_celsius <= 100):
            raise ValueError(
                f"CPU temperature must be 0-100°C, got {
                    self.cpu_temperature_celsius}"
            )

        if not (0 <= self.cpu_frequency_mhz <= 5000):
            raise ValueError(
                f"CPU frequency must be 0-5000 MHz, got {
                    self.cpu_frequency_mhz}"
            )

        if not (0 <= self.pump_rpm <= 3300):
            raise ValueError(f"Pump RPM must be 0-3300, got {self.pump_rpm}")

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"CPU: {self.cpu_temperature_celsius:.1f}°C @ {
                self.cpu_frequency_mhz} MHz | "
            f"Pump: {self.pump_rpm} RPM"
        )
