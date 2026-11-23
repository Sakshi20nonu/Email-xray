
import re
from urllib.parse import urlparse


def analyze_email(subject, email_content):

    text = (subject + " " + email_content).lower()

    indicators = []
    score = 0

    # 1. Suspicious keywords
    suspicious_words = [
        "urgent action required",
        "verify your account",
        "account suspended",
        "click here",
        "password",
        "bank details",
        "free prize",
        "you have won",
        "limited time",
        "otp"
    ]

    for word in suspicious_words:
        if word in text:
            indicators.append(
                f"Suspicious keyword detected: {word}"
            )
            score += 10

    # 2. Check suspicious URLs
    urls = re.findall(
        r'https?://[^\s<>"\']+',
        email_content,
        re.IGNORECASE
    )

    for url in urls:
        try:
            parsed = urlparse(url)
            hostname = (parsed.hostname or "").lower()

            suspicious_url = False

            if not hostname:
                suspicious_url = True

            if hostname.startswith("xn--"):
                suspicious_url = True

            if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", hostname):
                suspicious_url = True

            if "@" in url:
                suspicious_url = True

            if suspicious_url:
                indicators.append(
                    f"Potentially suspicious URL: {url}"
                )
                score += 20

        except Exception:
            indicators.append("URL parsing issue detected")
            score += 10

    # 3. Check sensitive information requests
    sensitive_phrases = [
        "share your otp",
        "enter your password",
        "credit card number",
        "send your bank details"
    ]

    for phrase in sensitive_phrases:
        if phrase in text:
            indicators.append(
                f"Sensitive information request: {phrase}"
            )
            score += 20

    # 4. Calculate final score
    score = min(score, 100)

    if score >= 60:
        classification = "High Risk"

    elif score >= 30:
        classification = "Suspicious"

    else:
        classification = "Safe"

    if not indicators:
        indicators.append(
            "No suspicious indicators found by basic checks"
        )

    return {
        "risk_score": score,
        "classification": classification,
        "indicators": indicators,
        "detected_urls": urls
    }
