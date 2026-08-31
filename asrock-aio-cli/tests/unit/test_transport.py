"""Unit tests for the transport classes."""
import pytest
from transports import (
    HIDTransport,
    MockTransport,
    DeviceNotFoundError
)
from models import DisplayMode


def test_mock_transport_connection():
    """Test mock transport connection state."""
    transport = MockTransport()
    assert not transport.is_connected()

    transport.connect()
    assert transport.is_connected()

    transport.disconnect()
    assert not transport.is_connected()


@pytest.mark.parametrize("packet_index", [0, 1, 2],
                         ids=["temp", "freq", "pump"])
def test_mock_transport_records_packets(packets, packet_index):
    """Test that mock transport records sent packets."""
    transport = MockTransport()
    transport.connect()

    packet = packets[packet_index]
    transport.send_packet(packet)

    assert len(transport.sent_packets) == 1
    assert transport.sent_packets[0] == packet


def test_mock_transport_sends_sequence(packets):
    """Test sending multiple packets in sequence."""
    transport = MockTransport()
    transport.connect()
    transport.send_sequence(packets)
    assert len(transport.sent_packets) == 3


@pytest.mark.parametrize("packet_index", [0, 1, 2],
                         ids=["temp", "freq", "pump"])
def test_mock_transport_fails_if_not_connected(packets, packet_index):
    """Test error when sending without connection."""
    transport = MockTransport()
    packet = packets[packet_index]

    with pytest.raises(RuntimeError):
        transport.send_packet(packet)


def test_context_manager():
    """Test transport as context manager."""
    with MockTransport() as transport:
        assert transport.is_connected()
    assert not transport.is_connected()


def test_hid_transport_connection():
    """Test HID transport connection."""
    transport = HIDTransport()
    try:
        transport.connect()
        assert transport.is_connected()
    except DeviceNotFoundError as e:
        pytest.skip(f"{e}")
    finally:
        transport.close()


@pytest.mark.parametrize("packet_index", [0, 1, 2],
                         ids=["temp", "freq", "pump"])
def test_hid_transport_send_packet(packets, packet_index):
    """Test sending a packet with HID transport."""
    transport = HIDTransport()
    try:
        transport.connect()
        packet = packets[packet_index]
        transport.send_packet(packet.to_bytes())
    except DeviceNotFoundError as e:
        pytest.skip(f"{e}")
    finally:
        transport.close()


@pytest.mark.parametrize("packets", [DisplayMode.MODE_1, DisplayMode.MODE_2,
                                     DisplayMode.MODE_3],
                         ids=["pump", "freq", "temp"], indirect=True)
def test_hid_transport_send_sequence(packets):
    """Test sending a sequence of packets with HID transport."""
    transport = HIDTransport()
    try:
        transport.connect()
        transport.send_sequence([packet.to_bytes() for packet in packets])
    except DeviceNotFoundError as e:
        pytest.skip(f"{e}")
    finally:
        transport.close()


def test_hid_transport_disconnect():
    """Test HID transport disconnection."""
    transport = HIDTransport()
    try:
        transport.connect()
        assert transport.is_connected()
        transport.disconnect()
        assert not transport.is_connected()
    except DeviceNotFoundError as e:
        pytest.skip(f"{e}")
    finally:
        transport.close()
