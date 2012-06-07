#
# $Id, routegrammar.py 14 2012-06-07 02:46:19Z nickw $
#
# NAME,         routegrammar.py
#
# AUTHOR,       Nick Whalen <nickw@mindstorm-networks.net>
# COPYRIGHT,    2012 by Nick Whalen
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
#
#

import sys
import parsenode
import cidrize

# -------- NODE_SPEC --------

class NODE_SPEC_Error(Exception):
    pass

class NODE_SPEC(parsenode.ParseNode):
    """
    Defines the 'NODE_SPEC' segment of the iproute2 routing grammar.
    """
    # Defined by iproute2's grammar
    types = ('unicast', 'local', 'broadcast', 'multicast', 'throw', 'unreachable', 'prohibit', 'blackhole', 'nat')
    options = ('tos','table','proto','scope','metric')

    # NODE_SPEC variables/options
    TYPE = None
    PREFIX = None
    tos = None
    table = None
    proto = None
    scope = None
    metric = None

    def __init__(self, tokens):
        """
        Constructor.  Just calls the parent constructor (where all the interesting stuff lives).

        :param tokens:

        """
        super(NODE_SPEC,self).__init__(tokens)
    #---


    def parse(self, tokens):
        """
        Parses the NODE_SPEC part of a route (as defined by iproute2)

        :param tokens:
        :return, Array of tokens that were not used by the parser.

        """

        # Type is optional
        if tokens[0] in self.types:
            self.TYPE = tokens[0]
            self._addRawSegment(self.TYPE)      # Make sure we have the string segment stored
            tokens.remove(tokens[0])

        # PREFIX validation
        error_txt = self.validatePrefix(tokens[0])
        if not error_txt:
            self.PREFIX = tokens[0]
            self._addRawSegment(self.PREFIX)     # Make sure we have the string segment stored
            tokens.remove(tokens[0])
        else:
            raise NODE_SPEC_Error("Prefix (%s) did not pass validation, %s" %(tokens[0], error_txt))

        # Option parsing
        new_token_list = list(tokens)
        matched_option = False
        for token in tokens:
            # If we matched a token, it had a parameter we need to ignore
            if matched_option:
                matched_option = False
                continue

            # If the token is matched, store it
            if token in self.options:
                self[token] = tokens[tokens.index(token)+1]
                self._addRawSegment(token)
                self._addRawSegment(self[token])
                new_token_list.pop(new_token_list.index(token)+1)   # remove option parameter
                new_token_list.remove(token)                # remove the option from the list
                matched_option = True

        # Clean up raw_data
        self.raw_data = self.raw_data.strip()

        return new_token_list
    #---


    def validatePrefix(self, prefix):
        """
        Validates an Internet network or ip address (/32).

        :param prefix, The network in CIDR notation.
        :return, Text of error from cidrize on error, otherwise None.

        """
        try:
            cidrize.cidrize(prefix)
        except cidrize.CidrizeError:
            return sys.exc_value
        else:
            return None
    #---
#---


# -------- NH --------

class NH(parsenode.ParseNode):
    """
    Defines the 'NH' segment of the iproute2 routing grammar.
    """
    options = ('via', 'dev', 'weight')
    flags = ('onlink', 'pervasive')

    # NH variables/options
    NHFLAGS = None
    via = None
    dev = None
    weight = None


    def __init__(self, tokens):
        """
        """
        super(NH,self).__init__(tokens)
    #---

    def parse(self, tokens):
        """
        Parses the NH part of a route (as defined by iproute2)

        :param tokens:
        :return, Array of tokens that were not used by the parser.

        """
        # NHFLAGS is optional
        if tokens[0] in self.flags:
            self.NHFLAGS = tokens[0]
            self._addRawSegment(self.NHFLAGS)      # Make sure we have the string segment stored
            tokens.remove(tokens[0])

        # Option parsing
        new_token_list = list(tokens)
        matched_option = False
        for token in tokens:
            # If we matched a token, it had a parameter we need to ignore
            if matched_option:
                matched_option = False
                continue

            # If the token is matched, store it
            if token in self.options:
                self[token] = tokens[tokens.index(token)+1]
                self._addRawSegment(token)
                self._addRawSegment(self[token])
                new_token_list.pop(new_token_list.index(token)+1)   # remove option parameter
                new_token_list.remove(token)                # remove the option from the list
                matched_option = True

        # Clean up raw_data
        self.raw_data = self.raw_data.strip()

        return new_token_list
    #---
#----


# -------- OPTIONS --------

class OPTIONS(parsenode.ParseNode):
    """
    Defines the 'OPTIONS' segment of the iproute2 routing grammar.
    """
    options = ('mtu', 'advmss','rtt','rttvar','reordering','window','cwnd','initcwnd','ssthresh','realms','src',
               'rto_min','hoplimit','initrwnd')

    # OPTIONS variables/options
    mtu = None
    advmss = None
    rtt = None
    rttvar = None
    reordering = None
    window = None
    cwnd = None
    initcwnd = None
    ssthresh = None
    realms = None
    src = None
    rto_min = None
    hoplimit = None
    initrwnd = None


    def __init__(self, tokens):
        """
        """
        super(OPTIONS,self).__init__(tokens)
        #---

    def parse(self, tokens):
        """
        Parses the OPTIONS part of a route (as defined by iproute2)

        :param tokens:
        :return, Array of tokens that were not used by the parser.

        """
        # Option parsing
        new_token_list = list(tokens)
        matched_option = False
        for token in tokens:
            # If we matched a token, it had a parameter we need to ignore
            if matched_option:
                matched_option = False
                continue

            # If the token is matched, store it
            if token in self.options:
                self[token] = tokens[tokens.index(token)+1]
                self._addRawSegment(token)
                self._addRawSegment(self[token])
                new_token_list.pop(new_token_list.index(token)+1)   # remove option parameter
                new_token_list.remove(token)                # remove the option from the list
                matched_option = True

        # Clean up raw_data
        self.raw_data = self.raw_data.strip()

        return new_token_list
    #---
#----


# -------- INFO_SPEC --------

class INFO_SPEC_Error(Exception):
    pass

class INFO_SPEC(parsenode.ParseNode):
    """
    Defines the 'INFO_SPEC' segment of the iproute2 routing grammar.
    """
    #TODO: This is reference to NH according to the grammar, and there can be multiples.  Fix it to support this.
    nexthop = None


    def __init__(self, tokens):
        super(INFO_SPEC,self).__init__(tokens, [NH, OPTIONS])
    #---

    def parse(self, tokens):
        return tokens
    #---
#---


# -------- ROUTE --------

class ROUTE(parsenode.ParseNode):
    """
    Defines the 'ROUTE' segment of the the iproute2 routing grammar.
    """
    actions = ('add', 'del', 'change', 'append', 'replace', 'monitor')
    action = None

    def __init__(self, tokens):
        super(ROUTE,self).__init__(tokens, [NODE_SPEC, INFO_SPEC])
    #---


    def parse(self, tokens):
        """
        Parses the ROUTE part of an iproute2 routing entry.

        :param tokens:
        :return, Array of tokens that were not used by the parser.

        """
        if tokens[0] in self.actions:
            self.action = tokens[0]
            self._addRawSegment(self.action)     # Make sure we have the string segment stored
            tokens.remove(tokens[0])

        return tokens
    #---
#---