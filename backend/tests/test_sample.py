"""Test file with intentional failure to test failure reporting."""

def test_this_passes():
    """This test passes."""
    assert 1 + 1 == 2


def test_this_fails():
    """This test fails intentionally."""
    assert 1 + 1 == 3, "This test is designed to fail to demonstrate failure reporting"


def test_another_pass():
    """Another passing test."""
    assert "hello".upper() == "HELLO"
