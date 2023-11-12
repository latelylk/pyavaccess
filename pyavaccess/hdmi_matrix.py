import logging

from .avaccess_serial import AVAccessSerial
from .config.matrix_devices import MatrixDevices

# Config
_LOGGER = logging.getLogger(__name__)


class HDMIMatrixSerial(AVAccessSerial):
    """
    General class for AV Access HDMI Matrix devices
    """

    def __init__(
        self,
        url: str,
        device: str,
    ) -> None:
        """
        Initialize the AVAccess device for connecting over serial
        """
        # Get the device config from the yaml file
        deviceConfig = self._getDeviceConfig(device)

        _LOGGER.debug("Creating HDMI Matrix %s...")
        super().__init__(url)
        self.model = device
        self.inputs = deviceConfig["inputCount"]
        self.outputs = deviceConfig["outputCount"]
        self.audioOutputs = deviceConfig["audioOutputs"]
        self.prmEDIDCount = deviceConfig["EDIDParamCount"]
        self.maxDelay = deviceConfig["maxDelayInMin"]
        self.irModeCount = deviceConfig["irModeCount"]
        self.commandCount = deviceConfig["commandCount"]

    def _getDeviceConfig(self, device: str) -> dict:
        """
        @param device: Device name
        @return: Configuration for the device
        """
        _LOGGER.debug("Matching %s to config...", device)

        # If the device is not in the config, raise an error
        if device not in MatrixDevices:
            raise ValueError("Device %s does not exist in the config!", device)

        # Only return the config for the device
        return MatrixDevices[device]

    """ Function Helper Methods """

    def isOutNumInBounds(self, outNum: int) -> bool:
        """
        Check if the output number is in bounds
        @param outNum: output number
        @return: True if in bounds, False if not
        """
        if outNum < 1 or outNum > self.outputs:
            _LOGGER.error("Output number %s is out of bounds!", outNum)
            return False
        return True

    def isInputNumInBounds(self, inNum: int) -> bool:
        """
        Check if the input number is in bounds
        @param inNum: input number
        @return: True if in bounds, False if not
        """
        if inNum < 1 or inNum > self.inputs:
            _LOGGER.error("Input number %s is out of bounds!", inNum)
            return False
        return True

    def isAudioOutStringOnDevice(self, outString: str) -> bool:
        """
        Check if the audio output string exists on the device
        @param outString: string of the audio output device
        @return: True if on device, False if not
        """
        if outString not in self.audioOutputs:
            _LOGGER.error(
                "Audio output string %s does not exist on the device!", outString
            )
            return False
        return True

    def isEDIDPrmNumInBounds(self, prmNum: int) -> bool:
        """
        Check if the EDID param number is in bounds
        @param prmNum: EDID param number
        @return: True if in bounds, False if not
        """
        if prmNum < 1 or prmNum > self.prmEDIDCount:
            _LOGGER.error("EDID param number %s is out of bounds!", prmNum)
            return False
        return True

    def isDelayInBounds(self, delay: int) -> bool:
        """
        Check if the delay is in bounds
        @param delay: delay in minutes
        @return: True if in bounds, False if not
        """
        if delay < 1 or delay > self.maxDelay:
            _LOGGER.error("Delay %s is out of bounds!", delay)
            return False
        return True

    def isIRInBounds(self, mode: int) -> bool:
        """
        Check if the IR mode is in bounds
        @param mode: IR mode
        @return: True if in bounds, False if not
        """
        if mode < 1 or mode > self.irModeCount:
            _LOGGER.error("IR mode %s is out of bounds!", mode)
            return False
        return True

    """ Output Formatting Methods """

    def mappingToKeyValue(self, mapping: str) -> dict:
        """
        Convert a mapping string to a key value pair
        @param mapping: mapping string (ex: "MP in1 out2")
        @return: key value pair
        """
        # Find the positions of "in" and "out" in the mapping string
        in_index = mapping.find("in")
        out_index = mapping.find("out")

        # Extract the input and output values based on the positions
        input_value = mapping[in_index + 2 : out_index].strip()
        output_value = mapping[out_index + 3 :].strip()

        return {output_value: input_value}

    def mapAllToKeyValue(self, mapping: str, count: int) -> dict:
        """
        Create a dictionary for all values
        @param mapping: mapping string (ex: "MP in1 all")
        @param count: number of outputs for the dict
        @return: dictionary mapping all outputs to an input
        """
        # Find the positions of "in" and "out" in the mapping string
        in_index = mapping.find("in")
        all_index = mapping.find("all")

        # Extract the input and output values based on the positions
        input_value = mapping[in_index + 2 : all_index].strip()

        outputKV = {}
        for i in range(1, count + 1):
            outputKV[str(i)] = input_value

        return outputKV

    """ System Methods """

    def factoryReset(self) -> str:
        """
        Reset the device to factory settings
        @return: Device output
        """
        cmdStr = "RESET"
        _LOGGER.debug("Resetting device to factory settings...")
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def reboot(self) -> str:
        """
        Reboot the device
        @return: Device output
        """
        cmdStr = "REBOOT"
        _LOGGER.debug("Rebooting device...")
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def getVer(self) -> str:
        """
        @return: Current firmware version
        """
        cmdStr = "GET VER"
        _LOGGER.debug("Getting firmware version...")
        deviceOutput = self._SendData(cmdStr, True)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def getIR_SC(self) -> str:
        """
        @return: Current IR system code
        """
        cmdStr = "GET IR_SC"
        _LOGGER.debug("Getting IR system code...")
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def getAPI(self) -> str:
        """
        Debug method for quickly getting all commands available over rs232
        @return: Device API list
        """
        cmdStr = "help"
        _LOGGER.debug("Getting available commands...")
        deviceOutput = self._SendData(cmdStr, lineCount=self.commandCount)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    """ Status Methods """

    def getMapping(self, outNum: int) -> str:
        """
        @param outNum: output number
        @return: Current input number mapped to the output
        """
        if not self.isOutNumInBounds(outNum):
            return

        cmdStr = "GET MP out{}".format(outNum)
        _LOGGER.debug("Getting mapping for output %s...", outNum)
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return self.mappingToKeyValue(deviceOutput)

    def getMappings(self) -> str:
        """
        @return: Current input mapping to all outputs
        """
        cmdStr = "GET MP all"
        _LOGGER.debug("Getting mappings for all outputs...")
        deviceOutput = self._SendData(cmdStr, lineCount=self.outputs)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def getAutoCECStatus(self, outNum: int) -> str:
        """
        @param outNum: output number
        @return: Current "CEC AUTO POWER ON/OFF Status" of the output
        """
        if not self.isOutNumInBounds(outNum):
            return

        cmdStr = "GET AUTOCEC_FN out{}".format(outNum)
        _LOGGER.debug("Getting Auto CEC status for output %s...", outNum)
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def getCECDelay(self, outNum: int) -> str:
        """
        @param outNum: output number
        @return: Current "CEC POWER Delay Time Status" of the output
        """
        if not self.isOutNumInBounds(outNum):
            return

        cmdStr = "GET AUTOCEC_D out{}".format(outNum)
        _LOGGER.debug("Getting CEC Delay for output %s...", outNum)
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def getInputEDIDStatus(self, inNum: int) -> str:
        """
        @param inNum: input number
        @return: Current EDID Status of the input
        """
        if not self.isInputNumInBounds(inNum):
            return

        cmdStr = "GET EDID in{}".format(inNum)
        _LOGGER.debug("Getting EDID status for output %s...", inNum)
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def getAllInputEDIDStatus(self) -> str:
        """
        Return the EDID of all inputs
        @return: EDID status of all inputs
        """
        cmdStr = "GET EDID all"
        _LOGGER.debug("Getting EDID status for all inputs...")
        deviceOutput = self._SendData(cmdStr, lineCount=self.inputs)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def getMuteStatus(self, outString: str) -> str:
        """
        @param outString: string of the audio output device
        @return: Mute status of the output
        """
        if not self.isAudioOutStringOnDevice(outString):
            return

        cmdStr = "GET MUTE {}".format(outString)
        _LOGGER.debug("Getting mute status for %s...", outString)
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def getAllMuteStatus(self) -> str:
        """
        @param outString: string of the audio output device or "all"
        @return: SMute status of all outputs
        """
        cmdStr = "GET MUTE all"
        _LOGGER.debug(
            "Getting mute status for all audio outputs...",
        )
        deviceOutput = self._SendData(cmdStr, lineCount=4)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    """ Control Methods """

    def mapOutput(self, outNum: int, inNum: int) -> dict:
        """
        Map an input to an output
        @param outNum: output number
        @param inNum: input number
        @return: Current mapping of the output
        """
        if not self.isOutNumInBounds(outNum) or not self.isInputNumInBounds(inNum):
            return

        cmdStr = "SET SW in{} out{}".format(inNum, outNum)
        _LOGGER.debug("Mapping input %s to output %s...", inNum, outNum)
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return self.mappingToKeyValue(deviceOutput)

    def mapAllOutputs(self, inNum: int) -> dict:
        """
        Map an inputs to all outputs
        @param inNum: input number
        @return: Current mapping to all outputs
        """
        if not self.isInputNumInBounds(inNum):
            return

        cmdStr = "SET SW in{} all".format(inNum)
        _LOGGER.debug("Mapping input %s to all outputs...", inNum)
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return self.mapAllToKeyValue(deviceOutput, self.outputs)

    def setCECPower(self, outNum: int, state: bool) -> str:
        """
        Set the CEC power state of the output
        @param outNum: output number
        @param state: True = On, False = Off
        @return: Current power state of the output
        """
        if not self.isOutNumInBounds(outNum):
            return

        # Get the text to use for the command based on state
        stateText = "on" if state else "off"

        cmdStr = "SET CEC_PWR out{} {}".format(outNum, stateText)
        _LOGGER.debug(
            "Setting CEC power state for output %s to %s...", outNum, stateText
        )
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def setAutoCEC(self, outNum: int, state: bool) -> str:
        """
        Set the CEC auto power state of the output
        @param outNum: output number
        @param state: True = On, False = Off
        @return: Current auto power state of the output
        """
        if not self.isOutNumInBounds(outNum):
            return

        # Get the text to use for the command based on state
        stateText = "on" if state else "off"

        cmdStr = "SET AUTOCEC_FN out{} {}".format(outNum, stateText)
        _LOGGER.debug(
            "Setting CEC auto power state for output %s to %s...", outNum, stateText
        )
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def setCECDelay(self, outNum: int, delay: int) -> str:
        """
        Set the CEC power delay time for the output
        @param outNum: output number
        @param delay: Delay in minutes
        @return: Current delay time of the output in minutes
        """
        if not self.isOutNumInBounds(outNum) or not self.isDelayInBounds(delay):
            return

        cmdStr = "SET AUTOCEC_D out{} {}".format(outNum, delay)
        _LOGGER.debug("Setting CEC delay for output %s to %s...", outNum, delay)
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def setInputEDIDStatus(self, inNum: int, prmNum: int) -> str:
        """
        Set the EDID of the input
        @param inNum: input number
        @param prmNum: EDID param number (see API)
        @return: Current EDID status of the input
        """
        if not self.isInputNumInBounds(inNum) or not self.isEDIDPrmNumInBounds(prmNum):
            return

        cmdStr = "SET EDID in{} {}".format(inNum, prmNum)
        _LOGGER.debug("Setting EDID for input %s to %s...", inNum, prmNum)
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def setIR_SC(self, mode: int) -> str:
        """
        Set the IR system code
        @param mode: IR system code (see API)
        @return: Current IR system code
        """
        if not self.isIRInBounds(mode):
            return

        cmdStr = "SET IR_SC mode{}".format(mode)
        _LOGGER.debug("Setting IR system code to mode %s...", mode)
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput

    def setMuteStatus(self, outString: str, state: bool) -> str:
        """
        Set the mute status of the output
        @param outString: string of the audio output device
        @param state: True = On, False = Off
        @return: Current mute status of the output
        """
        if not self.isAudioOutStringOnDevice(outString):
            return

        # Get the text to use for the command based on state
        stateText = "on" if state else "off"

        cmdStr = "SET MUTE {} {}".format(outString, stateText)
        _LOGGER.debug("Setting mute status for %s to %s...", outString, stateText)
        deviceOutput = self._SendData(cmdStr)
        _LOGGER.debug("Device output: %s", deviceOutput)
        return deviceOutput
