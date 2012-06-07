#
# $Id: routingtable.py 9 2012-06-05 04:56:36Z nickw $
#
# NAME:         routingtable.py
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
#   Defines a routing table.
#

from lib import nixcommon

# Exceptions
class RoutingTableError(Exception):
    pass
class InvalidRouteError(RoutingTableError):
    pass


# RoutingTable
class RoutingTable(object):
    """
    Defines a routing table.
    """
    name = None
    description = None
    routes = []

    def __init__(self, name, description = None, routes = []):
        """
        Constructor

        """
        self.name = name

        if description: self.description = description
        if routes: self.routes = routes
    #---


    def __str__(self):
        """
        Converts table to iproute2 string.
        """
    #---


    def _iproute_table(self, arguments):
        """
        Wrapper for calls to 'ip route'.

        """
        return nixcommon.runProcess("ip route %s table %s" %(arguments,self.name))
    #---


    def addRoute(self, route):
        """
        Adds a route to the routing table.  This route will not be applied to the system until meth:apply() is called.
        :param route: Instance of class:Route.

        """
        if type(route) != route.Route:
            raise InvalidRouteError("Route is not a 'Route' object.")

        self.routes.append(route)
    #---


    def removeRoute(self, route):
        """
        Removes a route from the routing table.  This change will not be applied to the system until meth:apply() is
        called.

        """
    #---


    def apply(self):
        """
        Applies the routing table definition to the system.

        """
    #---


    def remove(self):
        """
        Removes the routing table from the system.

        """
    #---


    def parse(self):
        """
        Parses the live routing table referred to by self.name and stores the data in this class.

        """

        table_info = self._iproute_table('list')

        if table_info['return_code']:
            raise RoutingTableError("Unexpected parse error: %s" %table_info['stderr'])


        # network
    #---

#---