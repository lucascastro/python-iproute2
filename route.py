#
# $Id: route.py 9 2012-06-05 04:56:36Z nickw $
#
# NAME:         route.py
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
#   Defines a route and methods to work with it. Currently only works on Linux; Windows functionality is
#   planned.
#

from lib import nixcommon

# Exceptions
class RouteError(Exception):
    pass


TYPE = ('unicast', 'local', 'broadcast', 'multicast', 'throw', 'unreachable', 'prohibit', 'blackhole', 'nat')
SCOPE = ('host', 'link', 'global', "%d")

# Route
class Route(object):
    """
    Defines a network route and provides methods to work with it.
    """
    network = None
    nexthop = None
    source = None
    device = None
    description = None
    options = []


    def __init__(self, route = None):
        """
        Constructor

        """
        if route:
            self.route = route

    #---


    def __str__(self):
        """
        Converts route to iproute2 string.
        """
    #---


    def _iproute(self, arguments):
        """
        Wrapper for calls to 'ip route'.

        """
        return nixcommon.runProcess("ip route %s" %arguments)
    #---


    def validate(self):
        """
        Validates a route based on it's network definition.

        """
    #---


    def apply(self):
        """
        Applies the route to the appropriate table.

        """
        if not self.route:
            raise RouteError('Invalid routing entry (blank).')

        self.validate()
        route_cfg = "add %s" %self.network

        if self.device: route_cfg += "device %s" %self.device
        if self.nexthop: route_cfg += "via %s" %self.nexthop

        self._iproute(route_cfg)
    #---

    def parse(self):
        """
        Parses a routing string from iproute2.

        """
    #---
#---
