"""Unit tests for the controllers module."""
import pytest
from models import DisplayMode
from controllers import LCDController


def test_controller_initialization(hid_transport):
    """Test that the controller initializes correctly."""
    controller = LCDController(hid_transport)
    assert controller is not None
    assert hasattr(controller, '_LCDController__transport')
    assert hasattr(controller, '_LCDController__builder')


@pytest.mark.parametrize("mode", [DisplayMode.MODE_1, DisplayMode.MODE_2,
                                  DisplayMode.MODE_3],
                         ids=["pump", "freq", "temp"])
def test_controller_display(hid_transport, system_metrics, mode):
    """Test that the controller can display metrics without errors."""
    controller = LCDController(hid_transport)
    try:
        controller.display(system_metrics, mode)
        controller.close()  # Ensure the transport is closed after display
    except Exception as e:
        pytest.fail(f"Controller display raised an exception: {e}")


def test_controller_display_invalid_mode(hid_transport, system_metrics):
    """Test that the controller raises an error for an invalid display mode."""
    controller = LCDController(hid_transport)
    with pytest.raises(ValueError) as exception_info:
        controller.display(system_metrics, "INVALID_MODE")
    assert "Unsupported display mode" in str(exception_info.value)


def test_controller_close(hid_transport):
    """Test that the controller closes the transport without errors."""
    controller = LCDController(hid_transport)
    try:
        controller.close()
    except Exception as e:
        pytest.fail(f"Controller close raised an exception: {e}")


def test_controller_display_transport_error(hid_transport, system_metrics):
    """Test that the controller handles transport errors gracefully."""
    controller = LCDController(hid_transport)
    # Simulate a transport error by closing the transport before display
    hid_transport.close()
    with pytest.raises(Exception) as exception_info:
        controller.display(system_metrics, DisplayMode.MODE_1)
    assert "Not connected to device" in str(exception_info.value)


def test_controller_with_context_manager(hid_transport, system_metrics):
    """Test that the controller can be used as a context manager."""
    with LCDController(hid_transport) as controller:
        try:
            controller.display(system_metrics, DisplayMode.MODE_1)
        except Exception as e:
            pytest.fail(f"Controller display raised an exception: {e}")
    # After exiting the context, the transport should be closed
    assert not hid_transport.is_connected()
