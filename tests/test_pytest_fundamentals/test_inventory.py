"""
    Unit tests validating the inventory domain entities via pytest assertions.
"""

from python_advanced_lab.testing_lab.inventory import Server

def test_older_version_is_lower():    
    old = Server("etl-01", "Ubuntu", "18.04", ["postgresql", "ssh"])    
    new = Server("web-02", "Ubuntu", "24.04", ["nginx", "ssh", "cron"])    

    assert old < new


def test_equal_if_they_have_the_same_name():
    a = Server("web001", "Ubuntu", "22.04", ["nginx", "ssh", "cron"])
    b = Server("web001", "Debian", "12.5", ["ssh"])

    assert a == b

def test_length_is_the_number_of_services():
    a = Server("web001", "Ubuntu", "22.04", ["nginx", "ssh", "cron"])
    assert len(a) == 3

def test_min_returns_the_most_outdated_one():
    a = Server("web001", "Ubuntu", "22.04", ["nginx", "ssh", "cron"])
    b = Server("db001", "Ubuntu", "18.04", ["postgresql", "ssh"])
    d = Server("app001", "Ubuntu", "9.10", ["python"])
    assert min([a, b , d]) is d