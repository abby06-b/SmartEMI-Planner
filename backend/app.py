from flask import Flask, jsonify
from flask_cors import CORS
import json
from emi_optimizer import optimize_repayment

app = Flask(__name__)
CORS(app)  # Allow frontend to talk to backend

# Load financial data
with open('financial_data.json', 'r') as f:
    data = json.load(f)

@app.route('/')
def home():
    return "✅ SmartEMI Planner - Backend Running Successfully"

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

# ✅ Added AI reasoning route properly *before* app.run()
@app.route('/ai_reasoning')
def ai_reasoning():
    try:
        # Using the same data file for now
        result = optimize_repayment(data)
        reasoning = {
            "AI Analysis": f"The system analyzed all loans and found that prepaying the {result['Recommended Loan for Prepayment']} saves the most interest ({result['Estimated Interest Saved']} INR).",
            "Optimization Result": result
        }
        return jsonify(reasoning)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
