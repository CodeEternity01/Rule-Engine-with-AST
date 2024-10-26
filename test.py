import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def create_rule_test(rule_string):
    """Test the creation of a new rule."""
    print("Initiating test for rule creation...")
    endpoint = f"{BASE_URL}/create_rule"
    payload = {"rule_string": rule_string}
    response = requests.post(endpoint, json=payload)
    print(f"Response: {response.json()}")
    return response.json().get('id')

def combine_rules_test(rule_id_1, rule_id_2):
    """Test the combination of two rules."""
    print("\nInitiating test for combining rules...")
    endpoint = f"{BASE_URL}/combine_rules"
    payload = {"rule_ids": [rule_id_1, rule_id_2]}
    response = requests.post(endpoint, json=payload)
    print(f"Response: {response.json()}")
    return response.json().get('id')

def evaluate_rule_test(rule_id, input_data):
    """Test the evaluation of a specific rule."""
    print("\nInitiating test for rule evaluation...")
    endpoint = f"{BASE_URL}/evaluate_rule"
    payload = {"rule_id": rule_id, "data": input_data}
    response = requests.post(endpoint, json=payload)
    print(f"Response: {response.json()}")

def modify_rule_test(rule_id, updated_rule_string):
    """Test the modification of an existing rule."""
    print("\nInitiating test for modifying a rule...")
    endpoint = f"{BASE_URL}/modify_rule"
    payload = {"rule_id": rule_id, "new_rule_string": updated_rule_string}
    response = requests.post(endpoint, json=payload)
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    # Test case for creating the first rule
    rule_str_1 = "(age > 30 AND department = 'Sales')"
    rule_id_1 = create_rule_test(rule_str_1)

    # Test case for creating the second rule
    rule_str_2 = "(salary > 50000 OR experience > 5)"
    rule_id_2 = create_rule_test(rule_str_2)

    # Test case for combining the two rules
    combined_rule_id = combine_rules_test(rule_id_1, rule_id_2)

    # Test case for evaluating the combined rule
    evaluation_data = {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 6
    }
    evaluate_rule_test(combined_rule_id, evaluation_data)

    # Test case for modifying the first rule
    new_rule_str = "age > 40 AND department = 'HR'"
    modify_rule_test(rule_id_1, new_rule_str)
