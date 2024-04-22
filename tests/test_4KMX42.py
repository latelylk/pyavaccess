from pyavaccess import HDMIMatrixSerial
import pytest

# Port used in tests (requires live device)
# Can be a url path "/dev/XYZ" or device name "COMx"
SERIAL_URL = "/dev/ttyUSB0"
AV_DEVICE = "4KMX42-H2A"


def test_createDevice():
    """
    Test creating an HDMIMatrixSerial object
    """
    matrix = HDMIMatrixSerial(SERIAL_URL, AV_DEVICE)
    assert matrix is not None


def test_canCommmunicate():
    """
    Test communicating with the device
    """
    matrix = HDMIMatrixSerial(SERIAL_URL, AV_DEVICE)

    # getVer has a stable output to use for verifying communication
    output = matrix.getVer()
    
    assert output == matrix.apiVersion


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
    test_createDevice()
    test_canCommmunicate()
    test_sendEmptyString()
