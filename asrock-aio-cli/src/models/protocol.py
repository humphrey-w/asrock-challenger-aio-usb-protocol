"""
USB protocol definitions for ASRock Challenger AIO.

This module defines the protocol data structures and enumerations based on the
documented USB HID protocol. It uses dataclasses for immutable, type-safe data.
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import List


class MetricsType(IntEnum):
    """
    Represents the type of system information in a USB packet.

    This corresponds to byte index 1 in the protocol specification.
    """

    CPU_TEMPERATURE = 0x00
    RESERVED_1 = 0x01
    RESERVED_2 = 0x02
    CPU_FREQUENCY = 0x03
    PUMP_RPM = 0x04


class DisplayMode(IntEnum):
    """
    Display modes determined by the last hex digit of byte 6 in final packet.

    PATTERN reference:
    - Digit ends in 2, 6, 9 → MODE_1
    - Digit ends in 3, 5, 7 → MODE_2
    - Digit ends in 0, 4, 8 → MODE_3
    """

    MODE_1 = 0x02  # Pump RPM (centered) + CPU Temp (corner)
    MODE_2 = 0x03  # CPU Frequency (centered) + CPU Temp (corner)
    MODE_3 = 0x04  # CPU Temperature (centered)


@dataclass(frozen=True)
class USBPacket:
    """
    Represents a single 64-byte USB HID packet for the AIO LCD.

    Attributes:
        report_id: Fixed value 0x07 for this device
        metrics_type: Type of system information (MetricsType enum)
        encoded_value: Bytes 2-5 containing encoded data (varies by type)
        mode: Display mode (only meaningful in final packet)
        bar_indicator: Bar graph level 0x00-0x14 (only in final packet)

    The frozen=True parameter makes instances immutable, which is important for
    passing around protocol data without accidental modifications.
    """

    report_id: int = 0x07
    metrics_type: MetricsType = MetricsType.CPU_TEMPERATURE
    encoded_value: bytes = b"\x00\x00\x00\x00"
    mode: DisplayMode = DisplayMode.MODE_3
    bar_indicator: int = 0x00

    def __post_init__(self):
        """Validate packet structure."""
        if self.report_id != 0x07:
            raise ValueError(f"Report ID must be 0x07, got {self.report_id:#x}")

        if not isinstance(self.metrics_type, MetricsType):
            raise ValueError(f"Invalid metrics type: {self.metrics_type}")

        if len(self.encoded_value) != 4:
            raise ValueError(
                f"Encoded value must be 4 bytes, got {len(self.encoded_value)}"
            )

        if not (0x00 <= self.bar_indicator <= 0x14):
            raise ValueError(
                f"Bar indicator must be 0x00-0x14, got {self.bar_indicator:#x}"
            )

    def to_bytes(self) -> bytes:
        """
        Convert packet to 64-byte format suitable for USB transmission.

        Returns:
            bytes: 64-byte USB packet with proper padding
        """
        # Build the packet: [report_id, metrics_type, encoded_value..., mode, bar, padding]
        packet = bytearray(64)
        packet[0] = self.report_id
        packet[1] = int(self.metrics_type)
        packet[2:6] = self.encoded_value
        packet[6] = int(self.mode)
        packet[7] = self.bar_indicator
        # Remaining bytes default to 0x00

        return bytes(packet)


@dataclass(frozen=True)
class LCDPacketSequence:
    """
    Represents a complete 3-packet sequence for LCD update.

    The protocol requires exactly 3 packets in sequence:
    1. CPU Temperature packet (metrics_type=0x00)
    2. CPU Frequency packet (metrics_type=0x03)
    3. Pump RPM packet (metrics_type=0x04) - determines display mode and bars

    This is a Composite pattern implementation that encapsulates the protocol
    requirement of sending multiple packets as a unit.
    """

    temperature_packet: USBPacket
    frequency_packet: USBPacket
    pump_packet: USBPacket

    def __post_init__(self):
        """Validate sequence structure."""
        if self.temperature_packet.metrics_type != MetricsType.CPU_TEMPERATURE:
            raise ValueError("First packet must be CPU_TEMPERATURE type")

        if self.frequency_packet.metrics_type != MetricsType.CPU_FREQUENCY:
            raise ValueError("Second packet must be CPU_FREQUENCY type")

        if self.pump_packet.metrics_type != MetricsType.PUMP_RPM:
            raise ValueError("Third packet must be PUMP_RPM type")

    def to_bytes_sequence(self) -> List[bytes]:
        """
        Convert sequence to list of 64-byte packets.

        Returns:
            List[bytes]: Three 64-byte packets in correct order
        """
        return [
            self.temperature_packet.to_bytes(),
            self.frequency_packet.to_bytes(),
            self.pump_packet.to_bytes(),
        ]
