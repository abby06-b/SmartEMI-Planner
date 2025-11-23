document.getElementById("summaryBtn").addEventListener("click", async () => {
    const res = await fetch("http://127.0.0.1:5000/get_summary");
    const data = await res.json();
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
});

document.getElementById("optimizeBtn").addEventListener("click", async () => {
    const res = await fetch("http://127.0.0.1:5000/optimize");
    const data = await res.json();
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
});
document.getElementById('setGoal').addEventListener('click', () => {
  const goal = document.getElementById('goalName').value;
  const amount = document.getElementById('goalAmount').value;
  if (goal && amount) {
    document.getElementById('goalStatus').innerText =
      `Goal "${goal}" set successfully! Target: ₹${amount}`;
  } else {
    alert('Please fill both fields.');
  }
});
// 👉 NEW (WEEK 5): AI Reasoning / AI Insights
document.getElementById("aiBtn").addEventListener("click", async () => {
    const res = await fetch("http://127.0.0.1:5000/ai_reasoning");
    const data = await res.json();
    document.getElementById("aiOutput").textContent =
        JSON.stringify(data, null, 2);
});
async function loadChart() {
    const res = await fetch("http://127.0.0.1:5000/get_summary");
    const data = await res.json();

    const ctx = document.getElementById('summaryChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Income', 'Expenses', 'EMI'],
            datasets: [{
                label: 'Monthly Financial Overview',
                data: [
                    data["Monthly Income"],
                    data["Total Expenses"],
                    data["Total EMI"]
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

loadChart();


