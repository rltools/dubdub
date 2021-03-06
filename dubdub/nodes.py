import abc
from typing import Any, AnyStr

from inflection import underscore
from loguru import logger

from dubdub import dataclass
from dubdub.types import TokenType


@dataclass
class Node(abc.ABC):
    @property
    def cls_name(self) -> str:
        return underscore(type(self).__name__).lower()

    @property
    def vname(self) -> str:
        return f"visit_{self.cls_name}"

    @property
    def ltag(self) -> str:
        return f"leave_{self.cls_name}"

    def visit(self, visitor: "Visitor") -> None:
        visitor.visit(self)


class Visitor(abc.ABC):
    """
    The Visitor Interface declares a set of visiting methods that correspond to
    component classes. The signature of a visiting method allows the visitor to
    identify the exact class of the component that it's dealing with.
    """

    def visit(self, node: "Node"):
        """Allow the visitor run through multiple steps. Only"""

        return self.on_visit(node)

    def on_visit(self, node: Node):
        vname = node.vname
        visit_func = getattr(self, vname, None)

        is_function = visit_func is not None
        if not is_function:
            raise Exception(f"The function {vname} doesn't exist.")
        return_value = visit_func(node)
        return return_value


@dataclass
class Token(Node):
    token_type: TokenType
    lexeme: str
    literal: Any
    line: int

    def __str__(self) -> str:
        return f"Token(type={self.token_type}, lexeme={self.lexeme}, literal={self.literal})"


class PrintVisitor(Visitor):
    def on_visit(self, node: Node) -> None:
        logger.warning(f"Printing {node.vname}")
        super().on_visit(node)

    def visit_token(self, node: "Node") -> None:
        logger.debug("Visiting a token")


def main() -> None:
    nand_token = Token(token_type=TokenType.AND, lexeme="and", literal="and", line=1)
    print_visit = PrintVisitor()
    print_visit.visit(nand_token)


if __name__ == "__main__":
    main()
