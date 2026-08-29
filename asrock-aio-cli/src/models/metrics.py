"""
System metrics data transfer object.

This module defines the SystemMetrics DTO which represents the actual system
information that will be displayed on the AIO LCD screen.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Limits:
    """
    Represents the maximum values for system metrics that can be displayed on 
    the AIO LCD screen.

    Attributes:
        max_pump_rpm: Maximum pump speed in revolutions per minute
        max_cpu_frequency_mhz: Maximum CPU frequency in MHz
        max_cpu_temperature_celsius: Maximum CPU temperature in Celsius
    """
    max_pump_rpm: int
    max_cpu_frequency_mhz: int
    max_cpu_temperature_celsius: float = 100.0

    def __post_init__(self):
        if self.max_pump_rpm <= 0:
            raise ValueError("Pump RPM must be greater than 0")
        if self.max_cpu_frequency_mhz <= 0:
            raise ValueError("CPU frequency must be greater than 0")
        if self.max_cpu_temperature_celsius <= 0:
            raise ValueError("CPU temperature must be greater than 0")


@dataclass(frozen=True)
class SystemMetrics:
    """
    Represents real-world system information that is to be encoded into USB 
    protocol packets.

    Attributes:
        cpu_temperature_celsius: CPU temperature in Celsius
        cpu_frequency_mhz: CPU frequency in MHz
        pump_rpm: Pump speed in revolutions per minute
    """

    pump_rpm: int
    cpu_frequency_mhz: int
    cpu_temperature_celsius: float
    limits: Limits

    def __post_init__(self):
        """Validate metric ranges."""
        if not (0 <= self.cpu_temperature_celsius
                <= self.limits.max_cpu_temperature_celsius):
            raise ValueError(
                f"CPU temperature must be 0-{
                    self.limits.max_cpu_temperature_celsius}°C, got {
                    self.cpu_temperature_celsius}"
            )

        if not (0 <= self.cpu_frequency_mhz
                <= self.limits.max_cpu_frequency_mhz):
            raise ValueError(
                f"CPU frequency must be 0-{
                    self.limits.max_cpu_frequency_mhz} MHz, got {
                    self.cpu_frequency_mhz}"
            )

        if not 0 <= self.pump_rpm <= self.limits.max_pump_rpm:
            raise ValueError(
                f"Pump RPM must be 0-{self.limits.max_pump_rpm}, got {
                    self.pump_rpm}"
            )

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"CPU: {self.cpu_temperature_celsius:.1f}°C @ {
                self.cpu_frequency_mhz} MHz | "
            f"Pump: {self.pump_rpm} RPM"
        )
