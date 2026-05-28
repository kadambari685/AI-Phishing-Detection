def analyze_email_content(email_text: str):

    email_text = email_text.lower()

    threat_score = 0
    reasons = []

    suspicious_words = [
        "password",
        "verify",
        "urgent",
        "login",
        "bank",
        "account",
        "click here",
        "wire transfer",
        "reset password"
    ]

    for word in suspicious_words:
        if word in email_text:
            threat_score += 10
            reasons.append(f"Detected keyword: {word}")

    if threat_score >= 70:
        threat_level = "HIGH"
        action = "BLOCK_DOMAIN"

    elif threat_score >= 40:
        threat_level = "MEDIUM"
        action = "QUARANTINE"

    else:
        threat_level = "LOW"
        action = "MARK_SAFE"

    return {
        "threat_score": threat_score,
        "threat_level": threat_level,
        "action": action,
        "reasons": reasons
    }