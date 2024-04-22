from pyavaccess import HDMIMatrixSerial
import pytest

# Port used in tests (requires live device)
# Can be a url path "/dev/XYZ" or device name "COMx"
SERIAL_URL = "/dev/ttyUSB0"


def test_create():
    """
    Test creating an HDMIMatrixSerial object
    """
    matrix = HDMIMatrixSerial(SERIAL_URL, "4KMX42-H2A")
    assert matrix is not None


def test_communication():
    """
    Test communicating with the device
    """
    matrix = HDMIMatrixSerial(SERIAL_URL, "4KMX42-H2A")
    output = matrix.getVer()
    assert output == "VER 1.0.2"


def test_sendEmptyString():
    """
    Test communicating with the device
    """
    matrix = HDMIMatrixSerial(SERIAL_URL, AV_DEVICE)

    # getVer has a stable output to use for verifying communication
    with pytest.raises(Exception):
        matrix._SendData("")


# For manual use instead of pytest
if __name__ == "__main__":
    test_create()
    test_communication()
    test_sendEmptyString()
