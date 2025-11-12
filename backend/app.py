from flask import Flask, jsonify
from flask_cors import CORS   # ADD THIS LINE
import json
from emi_optimizer import optimize_repayment

app = Flask(__name__)
CORS(app)   # ADD THIS LINE — allows frontend to talk to backend

with open('financial_data.json', 'r') as f:
    data = json.load(f)

@app.route('/')
def home():
    return "SmartEMI Planner - Backend Running Successfully"

@app.route('/get_summary')
def get_summary():
    income = data['income']
    total_expenses = sum(data['expenses'].values())
    total_emi = sum(loan['emi'] for loan in data['loans'])
    disposable_income = income - total_expenses - total_emi
    return jsonify({
        "Monthly Income": income,
        "Total Expenses": total_expenses,
        "Total EMI": total_emi,
        "Disposable Income": disposable_income
    })

@app.route('/optimize')
def optimize():
    return jsonify(optimize_repayment(data))

if __name__ == '__main__':
    app.run(debug=True)
