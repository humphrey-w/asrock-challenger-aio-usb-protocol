"""Integration tests for packet sequence generation and transport."""
import pytest
from models import LCDPacketSequence, DisplayMode


def test_packet_sequence_matches_protocol(packets):
    """Test that the generated packet sequence matches expected protocol
    structure."""
    sequence = LCDPacketSequence(*packets)
    packets = sequence.to_bytes_sequence()

    assert packets[0][1] == 0x00
    assert packets[1][1] == 0x03
    assert packets[2][1] == 0x04


def test_packet_sequence_with_mock_transport(mock_transport, packets):
    """Test sending a packet sequence using the MockTransport."""
    sequence = LCDPacketSequence(*packets)

    mock_transport.send_sequence(sequence.to_bytes_sequence())

    assert len(mock_transport.sent_packets) == 3
    assert mock_transport.sent_packets[0][1] == 0x00
    assert mock_transport.sent_packets[1][1] == 0x03
    assert mock_transport.sent_packets[2][1] == 0x04

    mock_transport.reset()

    assert len(mock_transport.sent_packets) == 0


@pytest.mark.parametrize("packets", [DisplayMode.MODE_1, DisplayMode.MODE_2,
                                     DisplayMode.MODE_3],
                         ids=["pump", "freq", "temp"], indirect=True)
def test_cpu_temp_packet_sequence_with_hid_transport(hid_transport, packets):
    """Test sending a packet sequence with CPU temp mode using the
    HIDTransport."""
    sequence = LCDPacketSequence(*packets)

    assert hid_transport.is_connected()

    hid_transport.send_sequence(sequence.to_bytes_sequence())
