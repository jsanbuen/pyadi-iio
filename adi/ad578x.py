# Copyright (C) 2023 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD


from decimal import Decimal

from adi.attribute import attribute
from adi.context_manager import context_manager
from adi.rx_tx import tx


class ad578x(tx, context_manager):
    """ AD578x DAC """

    _complex_data = False
    channel = []  # type: ignore
    _device_name = ""

    def __init__(self, uri="", device_name=""):
        """Constructor for AD578x class."""
        context_manager.__init__(self, uri, self._device_name)

        compatible_parts = [
            "ad5780",
            "ad5781",
            "ad5790",
            "ad5791",
            "ad5760",
        ]

        self._ctrl = None

        if not device_name:
            device_name = compatible_parts[0]
        else:
            if device_name not in compatible_parts:
                raise Exception(
                    f"Not a compatible device: {device_name}. Supported device names "
                    f"are: {','.join(compatible_parts)}"
                )

        # Select the device matching device_name as working device
        for device in self._ctx.devices:
            if device.name == device_name:
                self._ctrl = device
                self._txdac = device
                break

        if not self._ctrl:
            raise Exception("Error in selecting matching device")

        if not self._txdac:
            raise Exception("Error in selecting matching device")

        self.output_bits = []
        for ch in self._ctrl.channels:
            name = ch.id
            self.output_bits.append(ch.data_format.bits)
            self._tx_channel_names.append(name)
            self.channel.append(self._channel(self._ctrl, name))

        tx.__init__(self)

    @property
    def powerdown_mode(self):
        """Ad578x powerdown_mode config"""
        return self._get_iio_dev_attr_str("powerdown_mode")

    @powerdown_mode.setter
    def powerdown_mode(self, value):
        self._set_iio_dev_attr_str("powerdown_mode", value)

    @property
    def powerdown_mode_available(self):
        """AD578x powedown mode available"""
        return self._get_iio_dev_attr_str("powerdown_mode_available")

    @property
    def sampling_frequency(self):
        """AD578x sampling frequency config"""
        return self._get_iio_dev_attr_str("sampling_frequency")

    @sampling_frequency.setter
    def sampling_frequency(self, value):
        self._set_iio_dev_attr_str("sampling_frequency", value)

    @property
    def code_select(self):
        """AD578x code format config"""
        return self._get_iio_dev_attr_str("code_select")

    @code_select.setter
    def code_select(self, value):
        self._set_iio_dev_attr_str("code_select", value)

    @property
    def code_select_available(self):
        """AD578x code format available"""
        return self._get_iio_dev_attr_str("code_select_available")

    class _channel(attribute):
        """AD578x channel"""

        def __init__(self, ctrl, channel_name):
            self.name = channel_name
            self._ctrl = ctrl

        @property
        def raw(self):
            """AD578x channel raw value"""
            return self._get_iio_attr(self.name, "raw", True)

        @raw.setter
        def raw(self, value):
            self._set_iio_attr(self.name, "raw", True, str(int(value)))

        @property
        def offset(self):
            """AD578x channel offset"""
            return self._get_iio_attr(self.name, "offset", True)

        @offset.setter
        def offset(self, value):
            self._set_iio_attr(self.name, "offset", True, str(Decimal(value).real))

        @property
        def scale(self):
            """AD578x channel scale"""
            return self._get_iio_attr(self.name, "scale", True)

        @scale.setter
        def scale(self, value):
            self._set_iio_attr(self.name, "scale", True, str(Decimal(value).real))

        @property
        def powerdown(self):
            """AD578x powerdown config"""
            return self._get_iio_attr(self.name, "powerdown", True)

        @powerdown.setter
        def powerdown(self, value):
            self._set_iio_attr(self.name, "powerdown", True, value)
