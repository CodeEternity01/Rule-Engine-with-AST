from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import json
import logging

app = Flask(__name__)
Base = declarative_base()

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

class Rule(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True)
    rule_content = Column(String, nullable=False)
    rule_ast = Column(Text, nullable=False)

# Set up the database engine and session
engine = create_engine('sqlite:///rules.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

class ASTNode:
    def __init__(self, node_type, node_value, left_branch=None, right_branch=None):
        self.node_type = node_type
        self.node_value = node_value
        self.left_branch = left_branch
        self.right_branch = right_branch

    def to_dict(self):
        return {
            'type': self.node_type,
            'value': self.node_value,
            'left': self.left_branch.to_dict() if self.left_branch else None,
            'right': self.right_branch.to_dict() if self.right_branch else None
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            node_type=data['type'],
            node_value=data['value'],
            left_branch=cls.from_dict(data['left']),
            right_branch=cls.from_dict(data['right'])
        )

def parse_rule(rule_content):
    tokens = rule_content.replace('(', ' ( ').replace(')', ' ) ').split()

    def parse_expr():
        stack = [[]]
        for token in tokens:
            if token == '(':
                stack.append([])
            elif token == ')':
                expr = stack.pop()
                stack[-1].append(expr)
            elif token in ['AND', 'OR']:
                stack[-1].append(token)
            else:
                stack[-1].append(token)
        
        def build_tree(expression):
            if isinstance(expression, list):
                if len(expression) == 1:
                    return build_tree(expression[0])
                elif 'OR' in expression:
                    idx = expression.index('OR')
                    return ASTNode('operator', 'OR', build_tree(expression[:idx]), build_tree(expression[idx+1:]))
                elif 'AND' in expression:
                    idx = expression.index('AND')
                    return ASTNode('operator', 'AND', build_tree(expression[:idx]), build_tree(expression[idx+1:]))
            return ASTNode('operand', ' '.join(expression))
        
        return build_tree(stack[0])
    
    return parse_expr()

def evaluate_ast_node(ast_node, input_data):
    if ast_node.node_type == 'operator':
        if ast_node.node_value == 'AND':
            return evaluate_ast_node(ast_node.left_branch, input_data) and evaluate_ast_node(ast_node.right_branch, input_data)
        elif ast_node.node_value == 'OR':
            return evaluate_ast_node(ast_node.left_branch, input_data) or evaluate_ast_node(ast_node.right_branch, input_data)
    elif ast_node.node_type == 'operand':
        left, operator, right = ast_node.node_value.split()
        left_value = input_data.get(left)
        right_value = int(right) if right.isdigit() else right.strip("'")
        if operator == '>':
            return left_value > right_value
        elif operator == '<':
            return left_value < right_value
        elif operator == '=':
            return left_value == right_value
    return False

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_content = request.json['rule_string']
    ast_node = parse_rule(rule_content)
    rule_entry = Rule(rule_content=rule_content, rule_ast=json.dumps(ast_node.to_dict()))
    db_session.add(rule_entry)
    db_session.commit()
    return jsonify({'id': rule_entry.id, 'ast': rule_entry.rule_ast})

@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    rule_ids = request.json['rule_ids']
    rules = db_session.query(Rule).filter(Rule.id.in_(rule_ids)).all()
    combined_ast = ASTNode('operator', 'AND', *[ASTNode.from_dict(json.loads(rule.rule_ast)) for rule in rules])
    combined_rule_content = " AND ".join([rule.rule_content for rule in rules])
    combined_rule = Rule(rule_content=combined_rule_content, rule_ast=json.dumps(combined_ast.to_dict()))
    db_session.add(combined_rule)
    db_session.commit()
    return jsonify({'id': combined_rule.id, 'combined_ast': json.dumps(combined_ast.to_dict())})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    rule_id = request.json['rule_id']
    rule = db_session.query(Rule).filter_by(id=rule_id).first()
    if not rule:
        return jsonify({'error': 'Rule not found'}), 404
    ast_node = ASTNode.from_dict(json.loads(rule.rule_ast))
    input_data = request.json['data']
    result = evaluate_ast_node(ast_node, input_data)
    return jsonify({'result': result})

@app.route('/modify_rule', methods=['POST'])
def modify_rule():
    try:
        rule_id = request.json['rule_id']
        updated_rule_string = request.json['new_rule_string']
        rule = db_session.query(Rule).filter_by(id=rule_id).first()
        if rule:
            rule.rule_content = updated_rule_string
            rule.rule_ast = json.dumps(parse_rule(updated_rule_string).to_dict())
            db_session.commit()
            return jsonify({'message': 'Rule updated successfully'})
        else:
            return jsonify({'message': 'Rule not found'}), 404
    except Exception as e:
        logging.error(f"Error modifying rule: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
