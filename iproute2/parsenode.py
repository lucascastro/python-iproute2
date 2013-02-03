#
# $Id: parsenode.py 14 2012-06-07 02:46:19Z nickw $
#
# NAME:         parsenode.py
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
#   Defines ParseNode, which acts as the base for grammar-based parsers.  This isn't an ideal class, but it works for
# many things.  It spun out of my need to parse iproute2 grammars, so bear that in mind.
#

from lib import orderedset

class ParseNode(object):
    raw_data = ''       # The node's raw, text data
    next_data = None    # Data which will be passed to the child nodes of this node
    child_classes = orderedset.OrderedSet() # Ordered list of the parser nodes 'under' this node (child_classes)
    children = {}

    def __init__(self, tokens, child_class_list = list()):
        """
        Constructor.  Calls meth:parse to parse the incoming tokens and then adds any child nodes.
        :param tokens: List of text tokens to parse
        :param child_class_list: List of child classes to parse token lists

        """
        # The token list can potentially be empty (not all grammar options are used)
        if tokens:
            self.next_data = self.parse(tokens)    # Call the child class' parser
        if child_class_list:
            self.addChildren(child_class_list, self.next_data)
    #---


    def __str__(self):
        return self.raw_data
    #---


    # Dictionary type getter/setters

    def __getitem__(self, item):
        """
        Getter for dictionary style operation.  Supports class variables and referencing child classes by their class
        names.
        :param item: String

        """
        try:
            return self.__dict__[item]
        # If the item doesn't exist, see if it matches a child's name
        except KeyError:
            if item in self.children:
                return self.children[item]
            else:
                raise
    #---


    def __setitem__(self, key, value):
        """
        Setter for dictionary style operation.  Supports class variables and referencing child classes by their class
        names.
        :param key: String
        :param value: String

        """
        try:
            self.__dict__[key] = value
        except KeyError:
            if key in self.children:
                self.children[key] = value
            else:
                raise
    #---


    def __delitem__(self, key):
        """
        Deletion operator for dictionary style operation.  Supports class variables and referencing child classes by
        their class names.
        :param key: String

        """
        try:
            del self.__dict__[key]
        except KeyError:
            if key in self.children:
                del self.children[key]
            else:
                raise
    #---


    # Simply adds a segment to self.raw_data with the proper spacing
    def _addRawSegment(self, segment): self.raw_data += "%s " %segment


    def addChildren(self, nodes, node_data):
        """
        Adds children to the child_classes ordered set.

        :param nodes: List of instances of class:ParseNode

        """
        data = node_data
        for node in nodes:
            # Instantiate the grammar node
            new_node = node(data)
            # Save the new, instantiated node in a dict by it's class name
            self.children[new_node.__class__.__name__] = new_node
            # Save unused data to be used by next node
            data = new_node.next_data
    #---
#---


