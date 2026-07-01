results = []


# =========================
# 📌 LOG FUNCTION
# =========================
def log(level, message, recommendation=None):
    entry = {
        "level": level,
        "message": message,
        "recommendation": recommendation
    }

    results.append(entry)

    # CLI output
    print(f"[{level}] {message}")

    if recommendation:
        print(f"  ↳ Recommendation: {recommendation}")


# =========================
# 🧠 SCORING ENGINE
# =========================
def calculate_score():
    score = 100

    weights = {
        "PASS": 2,
        "INFO": 1,
        "LOW": -1,
        "MEDIUM": -3,
        "HIGH": -5,
        "ERROR": -2
    }

    for r in results:
        level = r["level"]
        score += weights.get(level, 0)

    # Clamp score
    if score > 100:
        score = 100
    if score < 0:
        score = 0

    return score


# =========================
# 📊 SUMMARY
# =========================
def summary():
    counts = {
        "PASS": 0,
        "INFO": 0,
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "ERROR": 0
    }

    for r in results:
        counts[r["level"]] += 1

    print("\n=== SUMMARY ===")
    for k, v in counts.items():
        print(f"{k}: {v}")

    score = calculate_score()

    print(f"\n🔥 Hardening Score: {score}/100")

    if score >= 90:
        print("Grade: A (Secure)")
    elif score >= 75:
        print("Grade: B (Good)")
    elif score >= 50:
        print("Grade: C (Needs Improvement)")
    else:
        print("Grade: D (High Risk)")


# =========================
# 📤 EXPORT JSON
# =========================
def export_json(filename):
    import json

    data = {
        "score": calculate_score(),
        "results": results
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n[INFO] JSON report saved to {filename}")


# =========================
# 📥 GET RESULTS (FOR UI)
# =========================
def get_results():
    return results