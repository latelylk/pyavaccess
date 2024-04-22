import serial
import logging

_LOGGER = logging.getLogger(__name__)
SERIAL_TIMEOUT = 10


class AVAccessSerial:
    """
    General class for communicating with AV Access devices over RS232 serial
    """

    def __init__(self, url: str) -> None:
        """
        Initialize the AVAccess device for connecting over serial
        """
        self._port = serial.serial_for_url(url, do_not_open=True)
        self._port.baudrate = 115200
        self._port.bytesize = serial.EIGHTBITS
        self._port.parity = serial.PARITY_NONE
        self._port.stopbits = serial.STOPBITS_ONE
        self._port.timeout = SERIAL_TIMEOUT
        self._port.write_timeout = SERIAL_TIMEOUT
        self._port.open()

    def _SendData(
        self, cmdStr: str, useDeviceEOL: bool = False, lineCount: int = 1
    ) -> str:
        """
        Send a command to the device and receive its response
        @param cmdStr: Data to send
        @return: Response from the device
        """
        _LOGGER.debug("Checking cmdStr content before sending to device")
        # Make sure string exists
        if not cmdStr:
            raise ValueError("Cannot send empty line to device!")

        _LOGGER.debug("Clearing buffers...")
        self._port.reset_output_buffer()
        self._port.reset_input_buffer()

        # Process the cmd for sending
        _LOGGER.debug('Encoding "%s"...', cmdStr)
        cmdStr = cmdStr + "\r\n"
        encodedCmd = cmdStr.encode("ascii")

        _LOGGER.debug('Sending "%s"...', encodedCmd)
        self._port.write(encodedCmd)
        self._port.flush()

        _LOGGER.debug("Receiving...")
        result = bytearray()
        linesRead = 0
        while True:
            char = self._port.read(1)

            # Check for end of incoming serial
            if char is None:
                break

            # If we received back nothing, but not null (ex: "")
            if not char:
                # Usually only reached by invalid command
                raise serial.SerialTimeoutException(
                    "Connection timed out! Last received bytes {}".format(
                        [hex(c) for c in result]
                    )
                )

            result += char
            if len(result) > 0 and (
                # Most responses end with \r\n but some end with \n\r such as GET VER
                result.endswith(b"\n\r" if useDeviceEOL else b"\r\n")
            ):
                linesRead += 1

            if linesRead >= lineCount:
                break

        # Process the byte array for returning
        ret = bytes(result)
        _LOGGER.debug('Received "%s"', ret)

        # Return the response as an ascii string
        return ret.decode("ascii").strip()
