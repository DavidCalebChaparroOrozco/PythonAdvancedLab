"""
    Unit tests for container emulation protocols.
"""

from python_advanced_lab.data_model.collections import ServerCluster


def test_cluster_container_operations() -> None:
    cluster = ServerCluster(cluster_name="staging", nodes=["web-01", "db-01", "api-01"])

    # Test __bool__ and __len__
    assert bool(cluster) is True
    assert len(cluster) == 3

    # Test __contains__ protocols
    assert "db-01" in cluster
    assert "WEB-01" in cluster
    assert "redis-01" not in cluster

    # Test __getitem__ indexing and slicing
    assert cluster[0] == "web-01"
    assert cluster[1:] == ["db-01", "api-01"]

    # Test implicit loop iteration provided by __getitem__
    nodes_list = [node for node in cluster]
    assert nodes_list == ["web-01", "db-01", "api-01"]


def test_empty_cluster_behavior() -> None:
    empty_cluster = ServerCluster(cluster_name="empty", nodes=[])
    assert bool(empty_cluster) is False
