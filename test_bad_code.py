# This file intentionally contains bad code to test CodeGuard's AI agents

import os
import json  # unused import

# Hardcoded API key (security agent should catch)
API_KEY = "MY_FAKE_HARDCODED_SECRET_KEY_12345"

def get_user(user_id):
    # SQL injection vulnerability (security agent should catch)
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

def divide(a, b):
    # No zero check (bug agent should catch)
    return a / b

def process(x, y, z, aa, bb):
    # Terrible variable names (quality agent should catch)
    cc = x + y
    dd = z * aa
    return cc + dd + bb

def calc_total(items):
    # Duplicated logic (quality agent should catch)
    total = 0
    for i in items:
        total = total + i
    return total

def compute_sum(items):
    # This is a duplicate of calc_total
    total = 0
    for i in items:
        total = total + i
    return total

def get_data(user):
    # No None check (bug agent should catch)
    return user.name.upper()