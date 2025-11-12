# Backend Overview

The backend handles user data processing, loan management, and agentic AI interactions.

## Components
- **Database Schema**: Defines structure for users, loans, EMIs, and goals.
- **API Layer**: Provides endpoints for data retrieval and AI recommendations.
- **Agent Engine**: Communicates with predictive and optimization modules.

## Week 3 Progress

### Backend Functionality Implemented
- Flask-based backend running successfully at `http://127.0.0.1:5000/`
- Added endpoints:
  - `/get_summary` → Returns income, expenses, EMIs, and disposable income.
  - `/optimize` → Provides optimized loan repayment recommendation.

### Sample Outputs
**GET /get_summary**
```json
{
  "Disposable Income": 23900,
  "Monthly Income": 65000,
  "Total EMI": 16100,
  "Total Expenses": 25000
}
**GET /optimize**
{
  "Estimated Interest Saved": 1640.0,
  "Recommended Loan for Prepayment": "Home"
}

