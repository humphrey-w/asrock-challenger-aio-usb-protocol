"""Unit tests for the PacketBuilder class."""
import pytest
from models import DisplayMode, MAX_BAR_INDICATOR
from builders import PacketBuilder


def test_packet_builder_with_temperature(system_metrics):
    """Tests the with_temperature method of the PacketBuilder class."""
    builder = PacketBuilder()
    packet = builder.with_cpu_temperature(
        system_metrics.cpu_temperature_celsius
    ).build()

    assert packet.metrics_type == 0x00  # Metrics type (CPU_TEMPERATURE)
    assert packet.encoded_value == b'\x00\x03\x09\x00'  # 39°C


def test_packet_builder_with_frequency(system_metrics):
    """Tests the with_cpu_frequency method of the PacketBuilder class."""
    builder = PacketBuilder()
    packet = builder.with_cpu_frequency(
        system_metrics.cpu_frequency_mhz
    ).build()

    assert packet.metrics_type == 0x03  # Metrics type (CPU_FREQUENCY)
    assert packet.encoded_value == b'\x03\x06\x00\x00'  # 3600 MHz


@pytest.mark.parametrize("display_mode, bars", [
    (DisplayMode.MODE_1, 18),
    (DisplayMode.MODE_2, 14),
    (DisplayMode.MODE_3, 8)
])
def test_packet_builder_with_pump_rpm(system_metrics, limits, display_mode,
                                      bars):
    """Tests the with_pump_rpm method of the PacketBuilder class."""
    builder = PacketBuilder()
    packet = builder.with_pump_rpm(system_metrics.pump_rpm)

    if display_mode == DisplayMode.MODE_1:
        packet = packet.with_mode(display_mode) \
            .with_bar_indicator(
                int((system_metrics.pump_rpm / limits.max_pump_rpm) *
                    MAX_BAR_INDICATOR)
            ).build()
    elif display_mode == DisplayMode.MODE_2:
        packet = packet.with_mode(display_mode) \
            .with_bar_indicator(
                int((system_metrics.cpu_frequency_mhz /
                     limits.max_cpu_frequency_mhz) * MAX_BAR_INDICATOR)
            ).build()
    elif display_mode == DisplayMode.MODE_3:
        packet = packet.with_mode(display_mode) \
            .with_bar_indicator(
                round((system_metrics.cpu_temperature_celsius /
                       limits.max_cpu_temperature_celsius) * MAX_BAR_INDICATOR)
            ).build()

    assert packet.metrics_type == 0x04  # Metrics type (PUMP_RPM)
    assert packet.encoded_value == b'\x02\x09\x06\x07'  # 2967 RPM
    assert packet.reserved_byte_1 == display_mode
    assert packet.reserved_byte_2 == bars
