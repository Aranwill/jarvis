#!/usr/bin/env python3
"""RED stub para MALAK-RDD-VALIDATION-RECEIPT/v1.

La implementación deliberadamente no existe todavía. Este archivo mantiene el
RED causal y machine-readable hasta que los requisitos congelados tengan tests.
"""

from __future__ import annotations

import json
import sys


def main() -> int:
    print(json.dumps({
        "validator": "MALAK-RDD-RECEIPT-VALIDATOR/v1",
        "validator_result": "FAIL",
        "code": "NOT_IMPLEMENTED",
        "message": "RDD Stage 2 receipt helper is deliberately not implemented in RED",
        "authority_effect": "none",
    }, ensure_ascii=False, sort_keys=True))
    return 1


if __name__ == "__main__":
    sys.exit(main())
