# Ownership notice: Bodapati Bharat chandra
def explain(text):
    return list(set([w for w in text.lower().split() if len(w) > 4]))[:6]
