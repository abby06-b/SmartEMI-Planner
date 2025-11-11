import json

def optimize_repayment(data):
    loans = data['loans']
    extra_payment = 2000  # assume user pays extra
    best_option = None
    max_interest_saved = 0

    for loan in loans:
        remaining_months = loan['tenure_months']
        monthly_interest = loan['interest_rate'] / (12 * 100)
        saved = extra_payment * remaining_months * monthly_interest
        if saved > max_interest_saved:
            max_interest_saved = saved
            best_option = loan['type']

    return {
        "Recommended Loan for Prepayment": best_option,
        "Estimated Interest Saved": round(max_interest_saved, 2)
    }

if __name__ == "__main__":
    with open('financial_data.json', 'r') as f:
        data = json.load(f)
    print(optimize_repayment(data))
