#
# $Id: interface.py 6 2012-05-28 18:43:14Z nickw $
#
# NAME:         interface.py
#
# AUTHOR:       Nick Whalen <nickw@mindstorm-networks.net>
# COPYRIGHT:    2012 by Nick Whalen
# LICENSE:
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# DESCRIPTION:
#   Defines a network interface and methods to work with it.  Currently only works on Linux; Windows functionality is
#   planned.
#

from lib import nixcommon

IP_V4 = 4
IP_V6 = 6

INT_GBPS = 0x4
INT_MBPS = 0x3
INT_KBPS = 0x2
INT_BPS = 0x1


# Exceptions
class InterfaceError(Exception):
    pass
class ConfigError(InterfaceError):
    """Raised when there is a problem with the config dictionary."""
    pass
class RequiresEscalationError(InterfaceError):
    pass
class AddressError(InterfaceError):
    pass


# Interface Class
class Interface(object):
    """
    Defines a network interface.
    """
    name = None             # Interface name as per the OS
    display_name = None
    units = INT_MBPS
    bandwidth_in = 0
    bandwidth_out = 0
    addresses = {'v4':[], 'v6':[]}


    def __init__(self, name, config = None):
        """
        Constructor
        """
        self.setName(name)

        if config:
            self.importConfig(config)
    #---


    def _iplink(self, arguments):
        """
        Runs the 'ip' command with the provided arguments.
        :param arguments: Argument string to pass to the 'ip' command.
        :return: Dictionary from meth:nixcommon.runProcess
        """
        return nixcommon.runProcess("ip link %s" %arguments)
    #---


    def _ipaddress(self, arguments):
        """
        Just an alias to the 'ip address' command.
        :return: Dictionary from meth:nixcommon.runProcess
        """
        return nixcommon.runProcess("ip address %s" %arguments)
    #---


    def importConfig(self, config):
        """
        Imports configuration from a dictionary

        :param config: Dictionary of configuration parameters
        """
        for key in config:
            if hasattr(self, key):
                setattr(self, key, config[key])
            else:
                raise ConfigError("%s is not a valid configuration option!" %key)
    #---


    def setName(self, name):
        """
        Sets the name of the operating system interface this class refers to.

        :param name: [String] Operating system's name for the interface
        """
        # Checks to see if the interface name is valid
        ip_link = self._iplink("show \"%s\"" %name)

        
        if ip_link['return_value'] == 255:
            raise InterfaceError("Invalid interface name: %s" %name)
        elif ip_link['return_value']:
            print "return_value: %s" %ip_link['return_value']
            raise InterfaceError("Unexpected error: %s" %ip_link['stderr'])
        else:
            self.name = name
    #---


    def setBandwidth(self, bw_in = 0, bw_out = 0, units = INT_MBPS):
        """
        Sets the bandwidth of the interface (if values are provided), otherwise tries to determine interface speed
        from the operating system.  Setting bandwdith will NOT change the speed on the interface.  In the future it
        should set the rates in the traffic-management system.

        :param bw_in: Integer representing the inbound bandwidth capabilities.
        :param bw_out: Integer representing the outbound bandwidth capabilities.
        :param units: Units the bandwidth is represented in.
        """
    #---


    def getAddresses(self):
        """
        Fetches the interface's addresses (and caches them locally).

        :return: Dictionary of interface's v4 and v6 addresses.
        """
        v4 = []
        v6 = []
        ip_address = self._ipaddress("show dev \"%s\"" %self.name)
        int_ip_info = ip_address['stdout'].strip().splitlines()

        for info_line in int_ip_info:
            split_line = info_line.strip().split()

            # IPv4 address
            if split_line[0] == 'inet':
                v4.append(tuple(split_line[1].split('/')))
            # IPv6 address
            elif split_line[0] == 'inet6':
                v6.append(tuple(split_line[1].split('/')))

        self.addresses['v4'] = v4
        self.addresses['v6'] = v6

        return self.addresses
    #---


    def addAddress(self, address):
        """
        Adds an IP address to an interface.

        :param address: String containing IP address and subnet in CIDR notation.
        """
        ip_address = self._ipaddress("add \"%s\" dev \"%s\"" %(address, self.name))

        if ip_address['return_value'] == 254:
            raise AddressError("%s already exists on %s" %(address,self.name))
        elif ip_address['return_value']:
            raise InterfaceError("Unexpected error: %s" %ip_address['stderr'])

        self.getAddresses()     # Update the IP address cache
    #---


    def delAddress(self, address):
        """
        Removes an IP address from an interface.

        :param address: String containing IP address and subnet in CIDR notation.
        """
        ip_address = self._ipaddress("del \"%s\" dev \"%s\"" %(address, self.name))

        if ip_address['return_value'] == 254:
            raise AddressError("%s does not exist on %s" %(address,self.name))
        elif ip_address['return_value']:
            raise InterfaceError("Unexpected error: %s" %ip_address['stderr'])

        self.getAddresses()     # Update the IP address cache
    #---


    def up(self):
        """
        Brings the interface up.

        """
        iproute = self._iplink("set \"%s\" up" %self.name)
        
        if iproute['return_value'] == 2:
            raise RequiresEscalationError("Altering interface state requires escalated privileges.")
        elif iproute['return_value']:
            raise InterfaceError("Unexpected error: %s" %iproute['stderr'])
    #---


    def down(self):
        """
        Disables the interface.

        """
        iproute = self._iplink("set \"%s\" down" %self.name)
        
        if iproute['return_value'] == 2:
            raise RequiresEscalationError("Altering interface state requires escalated privileges.")
        elif iproute['return_value']:
            raise InterfaceError("Unexpected error: %s" %iproute['stderr'])
    #---


    def status(self, simple = False):
        """
        Fetches the status of the interface, according to iproute.

        :param simple: Return only the status, no additional information if ``True``.
        :return: Simple status string if param:simple is ``True``, otherwise, full iproute status string.
        """
        iproute = self._iplink("show \"%s\"" %self.name)
        
        if iproute['return_value']:
            raise InterfaceError("Unexpected error: %s" %iproute['stderr'])

        if simple:
            return iproute['stdout'].split('state')[1].split()[0]

        return iproute['stdout']
    #---