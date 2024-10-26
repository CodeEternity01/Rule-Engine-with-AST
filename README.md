Rule Engine with AST
This application is a rule engine built on a three-tier architecture using Flask, SQLAlchemy, and SQLite. It supports the creation, combination, and evaluation of rules that leverage Abstract Syntax Trees (ASTs) for logical operations.

Getting Started
Installation
To set up the project, install the necessary dependencies:

bash
Copy code
pip install flask sqlalchemy
Running the Application
Start the Flask server:

bash
Copy code
python main.py
Application Components
Backend: main.py - Handles all core operations using Flask and SQLAlchemy.
Frontend: rlg.py - Provides a basic UI with Tkinter.
Automated Testing: test.py - An automated script for testing application functionality (uses the requests library).
Features
Create Rule: Adds a new rule and displays the ID in the UI (e.g., two rules created will have IDs 1 and 2).
Combine Rules: Allows merging multiple rules by specifying rule IDs in a comma-separated format, resulting in a "mega rule" with a new ID.
Evaluate Rule: Evaluates a specific rule by entering its ID and relevant data parameters in JSON format.
API Endpoints
1. Create Rule
URL: /create_rule

Method: POST

Request JSON:

json
Copy code
{
  "rule_string": "(age > 30 AND department = 'Sales') OR (salary > 50000)"
}
Response:

json
Copy code
{
  "id": 1,
  "ast": "..."
}
2. Combine Rules
URL: /combine_rules

Method: POST

Request JSON:

json
Copy code
{
  "rule_ids": [1, 2]
}
Response:

json
Copy code
{
  "id": 3,
  "combined_ast": "..."
}
3. Evaluate Rule
URL: /evaluate_rule

Method: POST

Request JSON:

json
Copy code
{
  "rule_id": 3,
  "data": {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 6
  }
}
Response:

json
Copy code
{
  "result": true
}
4. Modify Rule
URL: /modify_rule

Method: POST

Request JSON:

json
Copy code
{
  "rule_id": 1,
  "new_rule_string": "age > 40 AND department = 'HR'"
}
Response:

json
Copy code
{
  "message": "Rule updated successfully"
}
Testing the Rule Engine with Curl
You can test the application using the following curl commands:

Create a Rule:

bash
Copy code
curl -X POST http://127.0.0.1:5000/create_rule -H "Content-Type: application/json" -d '{"rule_string": "(age > 30 AND department = '\''Sales'\'') OR (salary > 50000)"}'
Create Another Rule:

bash
Copy code
curl -X POST http://127.0.0.1:5000/create_rule -H "Content-Type: application/json" -d '{"rule_string": "experience > 5 AND department = '\''Marketing'\''"}'
Combine Rules (replace IDs 1 and 2 as necessary):

bash
Copy code
curl -X POST http://127.0.0.1:5000/combine_rules -H "Content-Type: application/json" -d '{"rule_ids": [1, 2]}'
Evaluate Combined Rule (replace ID 3 as necessary):

bash
Copy code
curl -X POST http://127.0.0.1:5000/evaluate_rule -H "Content-Type: application/json" -d '{
  "rule_id": 3,
  "data": {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 6
  }
}'
Modify a Rule (replace ID 1 as necessary):

bash
Copy code
curl -X POST http://127.0.0.1:5000/modify_rule -H "Content-Type: application/json" -d '{
  "rule_id": 1,
  "new_rule_string": "age > 40 AND department = '\''HR'\''"
}'
Automated Testing with test.py
The test.py script automates testing of the rule engine's core functions. To run the test suite:

bash
Copy code
python test.py
test.py Script
Below is the script for automated testing:

python
Copy code
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_create_rule(rule_string):
    print("Creating rule...")
    url = f"{BASE_URL}/create_rule"
    data = {"rule_string": rule_string}
    response = requests.post(url, json=data)
    print("Create response:", response.json())
    return response.json()['id']

def test_combine_rules(rule_id_1, rule_id_2):
    print("\nCombining rules...")
    url = f"{BASE_URL}/combine_rules"
    data = {"rule_ids": [rule_id_1, rule_id_2]}
    response = requests.post(url, json=data)
    print("Combine response:", response.json())
    return response.json()['id']

def test_evaluate_rule(rule_id, data):
    print("\nEvaluating rule...")
    url = f"{BASE_URL}/evaluate_rule"
    data = {"rule_id": rule_id, "data": data}
    response = requests.post(url, json=data)
    print("Evaluate response:", response.json())

def test_modify_rule(rule_id, new_rule_string):
    print("\nModifying rule...")
    url = f"{BASE_URL}/modify_rule"
    data = {"rule_id": rule_id, "new_rule_string": new_rule_string}
    response = requests.post(url, json=data)
    print("Modify response:", response.json())

if __name__ == "__main__":
    # Test rule creation
    rule_1_id = test_create_rule("(age > 30 AND department = 'Sales')")
    rule_2_id = test_create_rule("(salary > 50000 OR experience > 5)")

    # Test rule combination
    combined_rule_id = test_combine_rules(rule_1_id, rule_2_id)

    # Test rule evaluation
    evaluation_data = {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 6
    }
    test_evaluate_rule(combined_rule_id, evaluation_data)

    # Test rule modification
    modified_rule_string = "age > 40 AND department = 'HR'"
    test_modify_rule(rule_1_id, modified_rule_string)
    
This README and script provide clear instructions and automated tests for verifying your rule engine's functionality. Use these instructions and script to ensure your application is working as intended.