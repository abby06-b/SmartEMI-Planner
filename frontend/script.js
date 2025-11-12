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
