// --- Simple multi-user frontend using user_id from login ---

// user_id is stored by login.html after successful login
const USER_ID = localStorage.getItem('smartemi_user_id') || 1;

function jsonFetch(url, options = {}) {
    options.headers = options.headers || {};
    if (!options.headers['Content-Type']) {
        options.headers['Content-Type'] = 'application/json';
    }
    return fetch(url, options);
}

// ---------------- BUTTON API CALLS ----------------

// Get Financial Summary
document.getElementById("summaryBtn").addEventListener("click", async () => {
    const res = await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/summary`);
    const data = await res.json();
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
});

// Optimize EMI
document.getElementById("optimizeBtn").addEventListener("click", async () => {
    const res = await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/optimize`);
    const data = await res.json();
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
});

// AI Insights
document.getElementById("aiBtn").addEventListener("click", async () => {
    const res = await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/ai_reasoning`);
    const data = await res.json();
    document.getElementById("aiOutput").textContent = JSON.stringify(data, null, 2);
});

// ---------------- GOAL SETTING ----------------

document.getElementById('setGoal').addEventListener('click', async () => {
    const goal_name = document.getElementById('goalName').value;
    const target_amount = document.getElementById('goalAmount').value;

    await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/set_goal`, {
        method: "POST",
        body: JSON.stringify({
            goal_name,
            target_amount,
            target_month: "2025-12"
        })
    });

    document.getElementById('goalStatus').innerText =
        `Goal "${goal_name}" set successfully! Target: ₹${target_amount}`;
});

// ---------------- EDITABLE FINANCIAL DATA ----------------

async function loadEditable() {
    const res = await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/summary`);
    const data = await res.json();

    document.getElementById('incomeInput').value = data["Monthly Income"] || 0;

    const expDiv = document.getElementById('expensesList');
    expDiv.innerHTML = "";
    (data["Expenses"] || []).forEach(e => {
        const row = document.createElement('div');
        row.innerHTML = `
            <input data-exp-id="${e.id}" class="expInput" type="number" value="${e.amount}">
            <span>${e.category}</span>
            <button class="saveExp">Save</button>
        `;
        expDiv.appendChild(row);
    });

    const loanDiv = document.getElementById('loansList');
    loanDiv.innerHTML = "";
    (data["Loans"] || []).forEach(l => {
        const row = document.createElement('div');
        row.innerHTML = `
            <input data-loan-id="${l.id}" class="loanInput" type="number" value="${l.emi}">
            <span>${l.type} | ₹${l.principal} @ ${l.interest_rate}%</span>
            <button class="saveLoan">Save</button>
            <button class="delLoan" style="background:red;">Delete</button>
        `;
        loanDiv.appendChild(row);
    });
}

// Save Income
document.getElementById("saveIncome").addEventListener("click", async () => {
    const income = document.getElementById("incomeInput").value;

    await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/update_income`, {
        method: "POST",
        body: JSON.stringify({ income })
    });

    alert("Income saved!");
    loadChart();
});

// Save Expense
document.getElementById("expensesList").addEventListener("click", async (e) => {
    if (e.target.classList.contains("saveExp")) {
        const input = e.target.parentElement.querySelector(".expInput");
        const id = input.dataset.expId;
        const amount = input.value;

        await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/update_expense`, {
            method: "POST",
            body: JSON.stringify({ id, amount })
        });

        alert("Expense updated!");
        loadChart();
    }
});

// Save or Delete Loan
document.getElementById("loansList").addEventListener("click", async (e) => {
    const input = e.target.parentElement.querySelector(".loanInput");
    const id = input?.dataset.loanId;

    if (e.target.classList.contains("saveLoan")) {
        const emi = input.value;

        await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/update_loan`, {
            method:"POST",
            body: JSON.stringify({ id, emi })
        });

        alert("Loan updated!");
        loadChart();
    }

    if (e.target.classList.contains("delLoan")) {
        await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/delete_loan`, {
            method:"POST",
            body: JSON.stringify({ id })
        });

        alert("Loan deleted!");
        loadEditable();
        loadChart();
    }
});

// Add Expense
document.getElementById("addExpense").addEventListener("click", async () => {
    const category = prompt("Enter expense category:");
    const amount = prompt("Enter amount:");

    await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/add_expense`, {
        method:"POST",
        body: JSON.stringify({ category, amount })
    });

    loadEditable();
    loadChart();
});

// Add Loan
document.getElementById("addLoan").addEventListener("click", async () => {
    const loan_type = prompt("Loan type:");
    const principal = prompt("Principal amount:");
    const interest_rate = prompt("Interest rate (%):");
    const tenure_months = prompt("Tenure (months):");
    const emi = prompt("EMI:");

    await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/add_loan`, {
        method:"POST",
        body: JSON.stringify({ loan_type, principal, interest_rate, tenure_months, emi })
    });

    loadEditable();
    loadChart();
});

// ---------------- CHART ----------------

async function loadChart() {
    const res = await jsonFetch(`http://127.0.0.1:5000/user/${USER_ID}/summary`);
    const data = await res.json();

    const ctx = document.getElementById('summaryChart');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Income', 'Expenses', 'Total EMI'],
            datasets: [{
                label: 'Financial Overview',
                data: [
                    data["Monthly Income"] || 0,
                    data["Total Expenses"] || 0,
                    data["Total EMI"] || 0
                ],
                borderWidth: 1
            }]
        }
    });
}

// Load data on startup
loadEditable();
loadChart();
