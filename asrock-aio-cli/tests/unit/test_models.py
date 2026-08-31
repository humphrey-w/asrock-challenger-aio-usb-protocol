"""Unit tests for the models module."""
from models import SystemMetrics, MetricsType, DisplayMode, USBPacket


def test_system_metrics(system_metrics, limits):
    """Tests the SystemMetrics class."""
    assert system_metrics.cpu_temperature_celsius == 39.0
    assert system_metrics.cpu_frequency_mhz == 3600
    assert system_metrics.pump_rpm == 2967

    metrics_data_invalid_temp = {
        "cpu_temperature_celsius": 150.0,
        "cpu_frequency_mhz": system_metrics.cpu_frequency_mhz,
        "pump_rpm": system_metrics.pump_rpm
    }

    try:
        SystemMetrics(**metrics_data_invalid_temp, limits=limits)
        assert False, "Expected ValueError for invalid CPU temperature"
    except ValueError:
        pass

    metrics_data_invalid_freq = {
        "cpu_temperature_celsius": system_metrics.cpu_temperature_celsius,
        "cpu_frequency_mhz": 6000,
        "pump_rpm": system_metrics.pump_rpm
    }

    try:
        SystemMetrics(**metrics_data_invalid_freq, limits=limits)
        assert False, "Expected ValueError for invalid CPU frequency"
    except ValueError:
        pass

    metrics_data_invalid_rpm = {
        "cpu_temperature_celsius": system_metrics.cpu_temperature_celsius,
        "cpu_frequency_mhz": system_metrics.cpu_frequency_mhz,
        "pump_rpm": 4000
    }

    try:
        SystemMetrics(**metrics_data_invalid_rpm, limits=limits)
        assert False, "Expected ValueError for invalid pump RPM"
    except ValueError:
        pass


def test_usb_packet_to_bytes():
    """Tests the to_bytes method of the USBPacket class."""
    # Create a packet with specific values
    packet = USBPacket(
        report_id=0x07,
        metrics_type=MetricsType.PUMP_RPM,
        encoded_value=b'\x02\x09\x06\x07',
        reserved_byte_1=DisplayMode.MODE_3,
        reserved_byte_2=0x08
    )

    bytes_result = packet.to_bytes()

    # Should be exactly 64 bytes
    assert len(bytes_result) == 64

    # Check specific byte positions from README structure
    assert bytes_result[0] == 0x07  # Report ID
    assert bytes_result[1] == 0x04  # Metrics type (pump RPM)
    assert bytes_result[2:6] == b'\x02\x09\x06\x07'  # Encoded value
    assert bytes_result[6] == 0x04  # Mode (MODE_3 = 0x04)
    assert bytes_result[7] == 0x08  # Bar indicator

    # Check padding (remaining bytes should be 0x00)
    assert all(b == 0x00 for b in bytes_result[8:])
