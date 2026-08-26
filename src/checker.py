import re


def check_output(show_output: str) -> dict:
    """
    Deterministic rule checker for Cisco-style
    troubleshooting evidence.

    The checker looks for common configuration
    and status problems before AI reasoning.
    """

    findings = []

    # -------------------------------------------------
    # 1. INTERFACE ADMINISTRATIVELY DOWN
    # -------------------------------------------------
    if re.search(
        r"administratively down",
        show_output,
        re.IGNORECASE
    ):
        findings.append({
            "type": "INTERFACE_DOWN",
            "severity": "HIGH",
            "message": "An interface is administratively down."
        })

    # -------------------------------------------------
    # 2. INTERFACE DOWN/DOWN
    # -------------------------------------------------
    if re.search(
        r"\bdown\s+down\b",
        show_output,
        re.IGNORECASE
    ):
        findings.append({
            "type": "INTERFACE_DOWN",
            "severity": "HIGH",
            "message": "An interface is down/down."
        })

    # -------------------------------------------------
    # 3. VLAN MISMATCH
    # -------------------------------------------------
    if re.search(
        r"VLAN.*mismatch|mismatch.*VLAN",
        show_output,
        re.IGNORECASE
    ):
        findings.append({
            "type": "VLAN_MISMATCH",
            "severity": "HIGH",
            "message": "Possible VLAN mismatch detected."
        })

    # -------------------------------------------------
    # 4. MISSING VLAN
    # -------------------------------------------------
    if re.search(
        r"VLAN.*not found|VLAN.*missing|VLAN.*does not exist",
        show_output,
        re.IGNORECASE
    ):
        findings.append({
            "type": "MISSING_VLAN",
            "severity": "HIGH",
            "message": "Possible missing VLAN detected."
        })

    # -------------------------------------------------
    # 5. MISSING ROUTE
    # -------------------------------------------------
    if re.search(
        r"missing route|no route|network not in routing table",
        show_output,
        re.IGNORECASE
    ):
        findings.append({
            "type": "MISSING_ROUTE",
            "severity": "HIGH",
            "message": "Possible missing route detected."
        })

    # -------------------------------------------------
    # 6. ACL DENY
    # -------------------------------------------------
    if re.search(
        r"access-list|ACL.*deny|deny.*ACL",
        show_output,
        re.IGNORECASE
    ):
        findings.append({
            "type": "ACL_DENY",
            "severity": "MEDIUM",
            "message": "Possible ACL-related blocking detected."
        })

    # -------------------------------------------------
    # 7. NAT / OVERLOAD
    # -------------------------------------------------
    if re.search(
        r"NAT|overload",
        show_output,
        re.IGNORECASE
    ):
        findings.append({
            "type": "NAT",
            "severity": "MEDIUM",
            "message": "Possible NAT-related configuration detected."
        })

    # -------------------------------------------------
    # 8. DUPLICATE IP
    # -------------------------------------------------
    if re.search(
        r"duplicate.*IP|IP.*duplicate|duplicate address",
        show_output,
        re.IGNORECASE
    ):
        findings.append({
            "type": "DUPLICATE_IP",
            "severity": "HIGH",
            "message": "Possible duplicate IP address detected."
        })

    # -------------------------------------------------
    # 9. WRONG SUBNET MASK
    # -------------------------------------------------
    if re.search(
        r"incorrect.*mask|wrong.*mask|invalid.*mask|mask.*mismatch",
        show_output,
        re.IGNORECASE
    ):
        findings.append({
            "type": "WRONG_MASK",
            "severity": "HIGH",
            "message": "Possible incorrect subnet mask detected."
        })

    # -------------------------------------------------
    # 10. GATEWAY MISMATCH
    # -------------------------------------------------
    if re.search(
        r"gateway.*mismatch|wrong.*gateway|incorrect.*gateway",
        show_output,
        re.IGNORECASE
    ):
        findings.append({
            "type": "GATEWAY_MISMATCH",
            "severity": "HIGH",
            "message": "Possible default gateway mismatch detected."
        })

    # -------------------------------------------------
    # FINAL RESULT
    # -------------------------------------------------

    if findings:
        return {
            "status": "ERRORS_DETECTED",
            "findings": findings
        }

    return {
        "status": "NO_DETERMINISTIC_ERRORS",
        "findings": []
    }