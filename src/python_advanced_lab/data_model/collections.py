"""
    Module implementing custom container emulation and truthiness protocols.
"""

from typing import Any, Sequence, overload


class ServerCluster:
    """
        Emulates a secure, read-only Python sequence of server nodes.
    """

    def __init__(self, cluster_name: str, nodes: Sequence[str]) -> None:
        self.cluster_name: str = cluster_name
        self._nodes: list[str] = list(nodes)

    def __bool__(self) -> bool:
        """
            Evaluates truthiness based on whether the cluster contains active nodes.
        """
        return len(self._nodes) > 0

    def __contains__(self, node: Any) -> bool:
        """
            Implements the 'in' operator using a case-insensitive check.
        """
        if not isinstance(node, str):
            return False
        return node.strip().lower() in [n.lower() for n in self._nodes]

    @overload
    def __getitem__(self, index: int) -> str: ...

    @overload
    def __getitem__(self, index: slice) -> list[str]: ...

    def __getitem__(self, index: int | slice) -> str | list[str]:
        """
            Provides direct index lookup, slicing capabilities, and implicit loop iteration.
        """
        return self._nodes[index]

    def __len__(self) -> int:
        """
            Returns the total amount of hardware items currently registered.
        """
        return len(self._nodes)
