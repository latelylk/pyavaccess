from pyavaccess import HDMIMatrixSerial

# Serial port to use for testing
SERIAL_URL = "/dev/ttyUSB0"


def test_create():
    """
    Test creating a HDMIMatrixSerial object
    """
    matrix = HDMIMatrixSerial(SERIAL_URL, "4KMX42-H2A")
    assert matrix is not None


def test_attributes():
    """
    Test the attributes of a HDMIMatrixSerial object
    """
    matrix = HDMIMatrixSerial(SERIAL_URL, "4KMX42-H2A")
    assert matrix.inputs == 4
    assert matrix.outputs == 2
    assert matrix.audioOutputs == [
        "hdmiaudioout1",
        "hdmiaudioout2",
        "audioout1",
        "spdifaudioout2",
    ]
    assert matrix.prmEDIDCount == 11
    assert matrix.maxDelay == 30
    assert matrix.irModeCount == 2
    assert matrix.commandCount == 24


def test_communication():
    """
    Test communicating with the device
    """
    matrix = HDMIMatrixSerial(SERIAL_URL, "4KMX42-H2A")
    output = matrix.getVer()
    assert output == "VER 1.0.2"
