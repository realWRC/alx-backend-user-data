#!/usr/bin/env python3
"""
Obfuscation functions for user data
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates user data in a logfile"""
    pattern = r'(' + '|'.join(fields) + r')=([^' + separator + r']*)'
    return re.sub(pattern, r'\1=' + redaction, message)
