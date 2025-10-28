CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    income REAL,
    expenses REAL
);

CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    loan_type TEXT,
    principal REAL,
    interest_rate REAL,
    emi REAL,
    tenure_months INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    goal_description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
