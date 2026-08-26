from src.checker import check_output


def test_interface_down():
    output = """
    GigabitEthernet0/0.10 is up, line protocol is up
    GigabitEthernet0/0.30 is administratively down,
    line protocol is down
    """

    result = check_output(output)

    assert result["status"] == "ERRORS_DETECTED"

    assert any(
        finding["type"] == "INTERFACE_DOWN"
        for finding in result["findings"]
    )


def test_vlan_mismatch():
    output = """
    VLAN mismatch detected on trunk interface
    """

    result = check_output(output)

    assert result["status"] == "ERRORS_DETECTED"

    assert any(
        finding["type"] == "VLAN_MISMATCH"
        for finding in result["findings"]
    )


def test_missing_route():
    output = """
    Network not in routing table
    """

    result = check_output(output)

    assert result["status"] == "ERRORS_DETECTED"

    assert any(
        finding["type"] == "MISSING_ROUTE"
        for finding in result["findings"]
    )


def test_clean_output():
    output = """
    GigabitEthernet0/0 is up
    Line protocol is up
    """

    result = check_output(output)

    assert result["status"] == "NO_DETERMINISTIC_ERRORS"
    assert result["findings"] == []