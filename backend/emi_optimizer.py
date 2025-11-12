import json

def optimize_repayment(data):
    """
    Determines which loan should be prepaid first based on maximum interest savings.
    """
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


def ai_reasoning(data):
    """
    Provides intelligent financial advice based on disposable income and spending pattern.
    """
    income = data['income']
    expenses = sum(data['expenses'].values())
    total_emi = sum(loan['emi'] for loan in data['loans'])
    disposable = income - expenses - total_emi

    if disposable < 5000:
        advice = "Your disposable income is low. Try reducing non-essential expenses."
    elif disposable > 20000:
        advice = "You have healthy disposable income! Consider prepaying high-interest loans."
    else:
        advice = "Maintain current spending balance while saving for future EMIs."

    return {
        "AI Reasoning": advice,
        "Disposable Income": disposable,
        "Total EMI": total_emi,
        "Total Expenses": expenses
    }


if __name__ == "__main__":
    with open('financial_data.json', 'r') as f:
        data = json.load(f)
    
    print("Optimization Result:")
    print(optimize_repayment(data))
    
    print("\nAI Reasoning:")
    print(ai_reasoning(data))