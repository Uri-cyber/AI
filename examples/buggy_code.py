"""
Example buggy code for demonstration
This file contains intentional bugs for testing the AI assistant
"""

import sqlite3


# Bug 1: Hardcoded credentials (CRITICAL)
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"


# Bug 2: SQL Injection vulnerability (CRITICAL)
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()


# Bug 3: eval() usage (HIGH)
def calculate(expression):
    # Dangerous: can execute arbitrary code
    return eval(expression)


# Bug 4: Bare except clause (MEDIUM)
def risky_operation():
    try:
        result = 10 / 0
        return result
    except:  # Catches everything, including system exits
        pass


# Bug 5: String comparison with == (not applicable in Python, but...)
def compare_strings(str1, str2):
    # In Python this works, but shows the pattern
    if str1 == str2:
        return True
    return False


# Bug 6: Potential resource leak
def read_file(filename):
    file = open(filename, 'r')
    data = file.read()
    # File not closed - resource leak
    return data


# Bug 7: Mutable default argument
def append_to_list(item, my_list=[]):
    my_list.append(item)
    return my_list


# Bug 8: TODO marker
def process_data(data):
    # TODO: Add validation
    # FIXME: This doesn't handle edge cases
    return data.upper()


# Bug 9: Unused variable
def calculate_total(items):
    total = 0
    count = 0
    for item in items:
        total += item['price']
        count += 1  # Never used
    return total


# Bug 10: No input validation
def divide_numbers(a, b):
    return a / b  # No check for b == 0


if __name__ == "__main__":
    # This code has multiple security and quality issues
    print("This is buggy code for demonstration purposes")
    print(f"Password: {DATABASE_PASSWORD}")  # Exposing credentials
