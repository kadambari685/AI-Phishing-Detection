async function analyzeEmail() {

    const email = document.getElementById("emailInput").value;

    document.getElementById("result").textContent =
        "Analyzing email...";

    try {

        const response = await fetch(
            "http://127.0.0.1:8001/analyze",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email
                })
            }
        );

        const data = await response.json();

        document.getElementById("result").textContent =
            JSON.stringify(data, null, 2);

        const score = data.threat_score;

        const progressFill =
            document.getElementById("progressFill");

        const scoreValue =
            document.getElementById("scoreValue");

        const threatBadge =
            document.getElementById("threatBadge");

        const scoreSection =
            document.getElementById("scoreSection");

        scoreSection.style.display = "block";

        progressFill.style.width = score + "%";

        scoreValue.textContent =
            score + "%";

        threatBadge.className = "badge";

        if (data.threat_level === "LOW") {

            progressFill.style.background =
                "#22c55e";

            threatBadge.classList.add("low");

        }

        else if (data.threat_level === "MEDIUM") {

            progressFill.style.background =
                "#f59e0b";

            threatBadge.classList.add("medium");

        }

        else {

            progressFill.style.background =
                "#ef4444";

            threatBadge.classList.add("high");

        }

        threatBadge.textContent =
            data.threat_level;

    }

    catch (error) {

        document.getElementById("result").textContent =
            "Unable to connect to backend.";

        console.error(error);
    }
}