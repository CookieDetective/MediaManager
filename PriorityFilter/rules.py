

def match_rules(subject, body, keywords):
    text = (subject or "") + " " + (body or "")
    tags = []
    for word in keywords:
        if word.lower() in text.lower():
            tags.append(f"match:{word.lower()}")
    return tags