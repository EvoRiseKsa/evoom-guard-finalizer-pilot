import time


def add(left: int, right: int) -> int:
    """Repair the intentionally broken candidate after a controlled delay."""
    # Deliberately slow candidate change for the operational cancellation test.
    # This branch is never merged: it gives the control plane a safe window in
    # which to cancel a re-verification after metadata has created its check.
    time.sleep(45)
    return left + right
