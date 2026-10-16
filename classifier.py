"""Transparent keyword scoring for common legal document types."""

import re


RULES = {
    "Non-disclosure agreement": [
        ("non-disclosure agreement", 5), ("confidential information", 4),
        ("nondisclosure", 4), ("non-disclosure", 4), ("proprietary information", 3),
        ("receiving party", 3), ("disclosing party", 3), ("trade secret", 3),
        ("not disclose", 2), ("confidentiality", 2),
    ],
    "Court filing": [
        ("plaintiff", 3), ("defendant", 3), ("petitioner", 3), ("respondent", 3),
        ("court of", 3), ("case number", 3), ("docket number", 3), ("motion to", 3),
        ("in the matter of", 3), ("hereby files", 2), ("memorandum of law", 3),
        ("wherefore", 2), ("jurisdiction", 1),
    ],
    "Affidavit or sworn statement": [
        ("affidavit", 5), ("deponent", 4), ("sworn statement", 4),
        ("under oath", 4), ("solemnly affirm", 4), ("notary public", 3),
        ("being duly sworn", 4), ("oath or affirmation", 3),
    ],
    "Legal notice": [
        ("notice to", 3), ("cease and desist", 5), ("demand letter", 5),
        ("notice of termination", 4), ("notice of default", 4), ("you are hereby notified", 4),
        ("cure the breach", 3), ("within days of receipt", 2), ("legal action", 2),
        ("without further notice", 2),
    ],
    "Employment document": [
        ("employment agreement", 5), ("employment contract", 5), ("job title", 3),
        ("employee", 2), ("employer", 2), ("salary", 2), ("compensation", 2),
        ("probationary period", 3), ("termination of employment", 3),
        ("non-compete", 3), ("severance", 2),
    ],
    "Lease or rental agreement": [
        ("lease agreement", 5), ("rental agreement", 5), ("landlord", 3),
        ("tenant", 3), ("monthly rent", 3), ("security deposit", 3),
        ("premises", 2), ("lease term", 3), ("vacate the premises", 3),
        ("rent due", 2),
    ],
    "Privacy policy": [
        ("privacy policy", 5), ("personal data", 3), ("personal information", 3),
        ("data controller", 4), ("data processor", 4), ("cookies", 2),
        ("data protection", 3), ("collect and use", 2), ("third parties", 1),
        ("retention period", 2),
    ],
    "General contract or agreement": [
        ("agreement", 2), ("contract", 2), ("parties agree", 3),
        ("terms and conditions", 2), ("effective date", 2), ("in consideration of", 2),
        ("breach of this agreement", 3), ("governing law", 2), ("indemnify", 2),
        ("shall", 1), ("hereby agrees", 2),
    ],
}


def _contains(text: str, phrase: str) -> bool:
    pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def classify_document(text: str) -> dict:
    """Rank document types by matched keyword weights; this is not ML confidence."""
    normalized = " ".join(text.split())
    ranked = []
    for category, rules in RULES.items():
        matches = [(phrase, weight) for phrase, weight in rules if _contains(normalized, phrase)]
        ranked.append({
            "category": category,
            "score": sum(weight for _, weight in matches),
            "matches": [phrase for phrase, _ in matches],
        })

    ranked.sort(key=lambda row: (-row["score"], row["category"]))
    top = ranked[0]
    next_score = ranked[1]["score"]
    if top["score"] == 0:
        strength = "No clear match"
        category = "Unclassified"
    elif top["score"] >= 7 and top["score"] - next_score >= 3:
        strength = "Several strong clues"
        category = top["category"]
    elif top["score"] >= 4:
        strength = "Some clues"
        category = top["category"]
    else:
        strength = "Limited clues"
        category = top["category"]

    return {
        "category": category,
        "strength": strength,
        "matches": top["matches"],
        "alternatives": [row for row in ranked[1:4] if row["score"] > 0],
        "ranked": ranked,
    }
