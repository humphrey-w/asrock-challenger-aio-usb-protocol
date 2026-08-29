"""Pytest fixtures for testing the ASRock AIO CLI application."""
import pytest
from builders import PacketBuilder
from models import Limits, SystemMetrics, DisplayMode
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
def packets(request):
    """Fixture that provides sample system metrics for testing."""
    builder = PacketBuilder()
    limits = Limits(max_pump_rpm=3200, max_cpu_frequency_mhz=4968)
    metrics_data = {
        "cpu_temperature_celsius": 39.0,
        "cpu_frequency_mhz": 3600,
        "pump_rpm": 2967
    }
    system_metrics = SystemMetrics(**metrics_data, limits=limits)
    temp_packet = builder.with_cpu_temperature(
        system_metrics.cpu_temperature_celsius).build()
    builder.reset()
    freq_packet = builder.with_cpu_frequency(
        system_metrics.cpu_frequency_mhz).build()
    builder.reset()
    pump_packet = (
        builder.with_pump_rpm(system_metrics.pump_rpm)
        .with_mode(
            request.param if hasattr(request, 'param') else DisplayMode.MODE_3)
        .with_bar_indicator(8)
        .build()
    )
    builder.reset()

    return temp_packet, freq_packet, pump_packet
