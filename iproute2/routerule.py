#
# $Id: routerule.py 9 2012-06-05 04:56:36Z nickw $
#
# NAME:         routerule.py
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
#   Class which allows the manipulation of a routing rule.
#

from lib import nixcommon

# Exceptions
class RouteRuleError(Exception):
    pass


# RouteRule
class RouteRule(object):
    """
    Defines a routing rule for Linux's iproute2.
    """

    def __init__(self):
        """
        Constructor

        """
    #---
#---