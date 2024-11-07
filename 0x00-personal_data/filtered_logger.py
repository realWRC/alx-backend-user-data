#!/usr/bin/env python3
"""
Obfuscation functions for user data
"""

import re


def filter_datum(fields, redaction, message, separator):
    """Obfuscates user data in a logfile"""
    pattern = r'(' + '|'.join(fields) + r')=([^' + separator + r']*)'
    return re.sub(pattern, r'\1=' + redaction, message)
