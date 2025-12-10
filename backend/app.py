from flask import Flask, jsonify, request
from flask_cors import CORS

from emi_optimizer import optimize_repayment, ai_reasoning
from models import get_engine, get_session, User, Loan, Expense, Goal, Base

app = Flask(__name__)
CORS(app)

# ---------------- DB SETUP -----------------
engine = get_engine('sqlite:///finance.db')
session = get_session(engine)


# ------------- HELPER: SUMMARY -------------
def compute_summary(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return {}

    # income stored as an Expense with category 'income'
    income_row = session.query(Expense).filter_by(
        user_id=user_id, category='income'
    ).first()
    income = income_row.amount if income_row else 0.0

    expenses = session.query(Expense).filter(
        Expense.user_id == user_id,
        Expense.category != 'income'
    ).all()

    loans = session.query(Loan).filter_by(user_id=user_id).all()

    total_expenses = sum(e.amount for e in expenses)
    total_emi = sum(l.emi for l in loans)

    return {
        "Monthly Income": income,
        "Total Expenses": total_expenses,
        "Total EMI": total_emi,
        "Disposable Income": income - total_expenses - total_emi,
        "Loans": [
            {
                "id": l.id,
                "type": l.loan_type,
                "principal": l.principal,
                "interest_rate": l.interest_rate,
                "tenure_months": l.tenure_months,
                "emi": l.emi
            } for l in loans
        ],
        "Expenses": [
            {
                "id": e.id,
                "category": e.category,
                "amount": e.amount
            } for e in expenses
        ]
    }


# ------------- BASIC HOME -------------
@app.route("/")
def home():
    return "SmartEMI Planner Backend Running"


# ------------- AUTH: SIGNUP & LOGIN -------------

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name") or "User"
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    existing = session.query(User).filter_by(email=email).first()
    if existing:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(name=name, email=email)
    new_user.set_password(password)

    session.add(new_user)
    session.commit()

    return jsonify({
        "message": "Account created successfully",
        "user_id": new_user.id
    })


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = session.query(User).filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user_id": user.id
    })


# ------------- USER DATA ENDPOINTS -------------

@app.route("/user/<int:user_id>/summary", methods=["GET"])
def get_summary(user_id):
    return jsonify(compute_summary(user_id))


@app.route("/user/<int:user_id>/update_income", methods=["POST"])
def update_income(user_id):
    data = request.get_json()
    amount = float(data.get("income", 0))

    inc = session.query(Expense).filter_by(
        user_id=user_id, category='income'
    ).first()
    if inc:
        inc.amount = amount
    else:
        inc = Expense(user_id=user_id, category='income', amount=amount)
        session.add(inc)

    session.commit()
    return jsonify({"status": "success", "message": "Income updated"})


@app.route("/user/<int:user_id>/add_expense", methods=["POST"])
def add_expense(user_id):
    data = request.get_json()
    category = data.get("category")
    amount = float(data.get("amount", 0))

    exp = Expense(user_id=user_id, category=category, amount=amount)
    session.add(exp)
    session.commit()

    return jsonify({"status": "success", "message": "Expense added"})


@app.route("/user/<int:user_id>/update_expense", methods=["POST"])
def update_expense(user_id):
    data = request.get_json()
    exp_id = int(data.get("id"))
    amount = float(data.get("amount", 0))

    exp = session.query(Expense).filter_by(id=exp_id, user_id=user_id).first()
    if not exp:
        return jsonify({"status": "error", "message": "Expense not found"}), 404

    exp.amount = amount
    session.commit()
    return jsonify({"status": "success", "message": "Expense updated"})


@app.route("/user/<int:user_id>/add_loan", methods=["POST"])
def add_loan(user_id):
    data = request.get_json()

    loan = Loan(
        user_id=user_id,
        loan_type=data.get("loan_type"),
        principal=float(data.get("principal", 0)),
        interest_rate=float(data.get("interest_rate", 0)),
        tenure_months=int(data.get("tenure_months", 0)),
        emi=float(data.get("emi", 0)),
    )
    session.add(loan)
    session.commit()

    return jsonify({
        "status": "success",
        "message": "Loan added",
        "loan_id": loan.id
    })


@app.route("/user/<int:user_id>/update_loan", methods=["POST"])
def update_loan(user_id):
    data = request.get_json()
    loan_id = int(data.get("id"))

    loan = session.query(Loan).filter_by(id=loan_id, user_id=user_id).first()
    if not loan:
        return jsonify({"status": "error", "message": "Loan not found"}), 404

    loan.loan_type = data.get("loan_type", loan.loan_type)
    loan.principal = float(data.get("principal", loan.principal))
    loan.interest_rate = float(data.get("interest_rate", loan.interest_rate))
    loan.tenure_months = int(data.get("tenure_months", loan.tenure_months))
    loan.emi = float(data.get("emi", loan.emi))

    session.commit()
    return jsonify({"status": "success", "message": "Loan updated"})


@app.route("/user/<int:user_id>/delete_loan", methods=["POST"])
def delete_loan(user_id):
    data = request.get_json()
    loan_id = int(data.get("id"))

    loan = session.query(Loan).filter_by(id=loan_id, user_id=user_id).first()
    if not loan:
        return jsonify({"status": "error", "message": "Loan not found"}), 404

    session.delete(loan)
    session.commit()
    return jsonify({"status": "success", "message": "Loan deleted"})


@app.route("/user/<int:user_id>/set_goal", methods=["POST"])
def set_goal(user_id):
    data = request.get_json()

    existing = session.query(Goal).filter_by(user_id=user_id).first()
    if existing:
        existing.goal_name = data.get("goal_name", existing.goal_name)
        existing.target_amount = float(
            data.get("target_amount", existing.target_amount)
        )
        existing.target_month = data.get(
            "target_month", existing.target_month
        )
    else:
        new_goal = Goal(
            user_id=user_id,
            goal_name=data.get("goal_name"),
            target_amount=float(data.get("target_amount", 0)),
            target_month=data.get("target_month")
        )
        session.add(new_goal)

    session.commit()
    return jsonify({"status": "success", "message": "Goal set"})


# ------------- OPTIMIZER & AI ENDPOINTS -------------

@app.route("/user/<int:user_id>/optimize", methods=["GET"])
def optimize_user(user_id):
    summary = compute_summary(user_id)
    if not summary:
        return jsonify({"error": "User or data not found"}), 404

    data = {
        "income": summary["Monthly Income"],
        "expenses": {
            e["category"]: e["amount"] for e in summary["Expenses"]
        },
        "loans": [
            {
                "type": l["type"],
                "amount": l["principal"],
                "interest_rate": l["interest_rate"],
                "tenure_months": l["tenure_months"],
                "emi": l["emi"],
            } for l in summary["Loans"]
        ],
    }

    result = optimize_repayment(data)
    return jsonify(result)


@app.route("/user/<int:user_id>/ai_reasoning", methods=["GET"])
def ai_user(user_id):
    summary = compute_summary(user_id)
    if not summary:
        return jsonify({"error": "User or data not found"}), 404

    data = {
        "income": summary["Monthly Income"],
        "expenses": {
            e["category"]: e["amount"] for e in summary["Expenses"]
        },
        "loans": [
            {
                "type": l["type"],
                "amount": l["principal"],
                "interest_rate": l["interest_rate"],
                "tenure_months": l["tenure_months"],
                "emi": l["emi"],
            } for l in summary["Loans"]
        ],
    }

    return jsonify(ai_reasoning(data))


if __name__ == "__main__":
    app.run(debug=True)
