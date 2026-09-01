"""Pytest fixtures for testing the ASRock AIO CLI application."""
import pytest
from builders import PacketBuilder
from models import Limits, SystemMetrics, DisplayMode, MAX_BAR_INDICATOR
from transports import MockTransport, HIDTransport, DeviceNotFoundError


@pytest.fixture
def mock_transport():
    """Fixture that provides a MockTransport instance for testing."""
    transport = MockTransport()
    transport.connect()
    yield transport
    transport.disconnect()


@pytest.fixture
def hid_transport():
    """Fixture that provides a HIDTransport instance for testing."""
    transport = HIDTransport()
    try:
        transport.connect()
    except DeviceNotFoundError as e:
        pytest.skip(f"{e}")
    yield transport
    transport.disconnect()


@pytest.fixture
def packets(request, system_metrics):
    """Fixture that provides sample system metrics for testing."""
    mode = getattr(request, 'param', DisplayMode.MODE_3)
    builder = PacketBuilder()
    temp_packet = builder.with_cpu_temperature(
        system_metrics.cpu_temperature_celsius).build()
    freq_packet = builder.with_cpu_frequency(
        system_metrics.cpu_frequency_mhz).build()
    pump_packet = (
        builder.with_pump_rpm(system_metrics.pump_rpm)
        .with_mode(mode)
    )

    if mode == DisplayMode.MODE_1:
        pump_packet = pump_packet.with_bar_indicator(
            int((system_metrics.pump_rpm / system_metrics.limits.max_pump_rpm)
                * MAX_BAR_INDICATOR)
        ).build()
    elif mode == DisplayMode.MODE_2:
        pump_packet = pump_packet.with_bar_indicator(
            int((system_metrics.cpu_frequency_mhz /
                 system_metrics.limits.max_cpu_frequency_mhz) *
                MAX_BAR_INDICATOR)
        ).build()
    else:  # Default to MODE_3 if no specific mode is provided
        pump_packet = pump_packet.with_bar_indicator(
            round((system_metrics.cpu_temperature_celsius /
                   system_metrics.limits.max_cpu_temperature_celsius)
                  * MAX_BAR_INDICATOR)
        ).build()

    return temp_packet, freq_packet, pump_packet


@pytest.fixture(name="limits")
def display_limits():
    """Fixture that provides system limits for testing."""
    return Limits(max_pump_rpm=3200, max_cpu_frequency_mhz=4968,
                  max_cpu_temperature_celsius=100)


@pytest.fixture(name="system_metrics")
def metrics(limits):
    """Fixture that provides system metrics for testing."""
    return SystemMetrics(cpu_temperature_celsius=39.0,
                         cpu_frequency_mhz=3600,
                         pump_rpm=2967,
                         limits=limits)
