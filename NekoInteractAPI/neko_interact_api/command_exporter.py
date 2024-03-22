from enum import Enum

from mcdreforged.command.builder.nodes.arguments import Number, Integer, Float, Text, QuotableText, GreedyText, Boolean, Enumeration
from mcdreforged.command.builder.nodes.basic import Literal, AbstractNode


class NodeTypes(Enum):
    LITERAL = Literal
    NUMBER = Number
    INTEGER = Integer
    FLOAT = Float
    TEXT = Text
    QUOTABLE_TEXT = QuotableText
    GREEDY_TEXT = GreedyText
    BOOLEAN = Boolean
    ENUMERATION = Enumeration

class Node:
    def __init__(self, name: str, node: AbstractNode):
        self.name = name
        self.type = None
        self.children = []

        # get type
        try:
            self.type = NodeTypes(node.__class__)
        except ValueError:
            self.type = NodeTypes.TEXT

        # Literal children
        for literal, literal_children in node._children_literal.items():
            self.children.append(Node(literal, literal_children[0]))

        # Argument children
        for argument_child in node._children:
            self.children.append(
                Node(
                    argument_child._ArgumentNode__name,
                    argument_child
                )
            )

    @property
    def dict(self):
        return {
            'name': self.name,
            'type': self.type.name,
            'children': [i.dict for i in self.children]
        }
