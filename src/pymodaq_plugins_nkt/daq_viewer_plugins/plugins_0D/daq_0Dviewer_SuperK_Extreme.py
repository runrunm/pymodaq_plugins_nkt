import numpy as np
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, DataToExport
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.parameter import Parameter

import pylablib as pll
from pymodaq_plugins_nkt.hardware.nkt_wrapper import Extreme


class DAQ_0DViewer_SuperK_Extreme(DAQ_Viewer_base):
    """ Instrument plugin class for a OD viewer.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Viewer module through inheritance via
    DAQ_Viewer_base. It makes a bridge between the DAQ_Viewer module and the Python wrapper of a particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of instruments that should be compatible with this instrument plugin.
        * With which instrument it has actually been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    # TODO add your particular attributes here if any

    """
    _laser_port = None

    ports = pll.list_backend_resources("serial")

    params = comon_parameters+[
        {'title': 'COM Port:', 'name': 'com_port', 'type': 'list', 'limits': ports},
        {'title': 'Power:', 'name': 'power', 'type': 'float', 'value': 17.0},
    ]

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        # self.controller: Extreme() = None

        #TODO declare here attributes you want/need to init with a default value
        pass

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == "com_port":
            self.controller.close_connection()  # when writing your own plugin replace this line
            self.controller.open_connection(port=self.settings['com_port'])

        elif param.name() == "power":
            self.controller.set_power(value=int(10 * self.settings['power']))

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        self.ini_detector_init(old_controller=controller, new_controller= Extreme(port=self.settings['com_port']))

        # TODO for your custom plugin (optional) initialize viewers panel with the future type of data
        # self.dte_signal_temp.emit(DataToExport(name='myplugin',
        #                                        data=[DataFromPlugins(name='Mock1',
        #                                                             data=[np.array([0]), np.array([0])],
        #                                                             dim='Data0D',
        #                                                             labels=['Mock1', 'label2'])]))

        # print(self.controller.scan_devices(port))

        # print(self.controller.system_type())

        info = "Whatever info you want to log"
        initialized = True
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""
        if not self.controller:
            pass
        else:
            self.controller.close()

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """

        self.controller.set_emission(state=3)  # 3 for ON

    def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        # data_tot = self.controller.your_method_to_get_data_from_buffer()
        # self.dte_signal.emit(DataToExport(name='myplugin',
        #                                   data=[DataFromPlugins(name='Mock1', data=data_tot,
        #                                                         dim='Data0D', labels=['dat0', 'data1'])]))
        pass

    def stop(self):
        """Stop the current grab hardware wise if necessary"""

        self.controller.set_emission(state=0)  # 0 for OFF

if __name__ == '__main__':
    main(__file__)

