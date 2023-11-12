# Set default logging handler to avoid "No handler found" warnings.
import logging

from .hdmi_matrix import HDMIMatrixSerial

logging.getLogger(__name__).addHandler(logging.NullHandler())
