fetch("/data")
  .then(res => res.json())
  .then(data => {
    if (data.error) {
        document.getElementById("results").innerHTML = "No report.json found";
        return;
    }

    // Score
    document.getElementById("score").innerText = "Score: " + data.score;
    document.getElementById("barFill").style.width = data.score + "%";

    // Results
    let container = document.getElementById("results");

    data.results.forEach(r => {
        let div = document.createElement("div");
        div.className = "card";

        div.innerHTML = `
            <strong class="${r.level}">${r.level}</strong><br>
            ${r.message}<br>
            ${r.recommendation ? "<em>" + r.recommendation + "</em>" : ""}
        `;

        container.appendChild(div);
    });
  });