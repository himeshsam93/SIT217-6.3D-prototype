# app.py
from flask import Flask, render_template, request, redirect, url_for, session, send_file, make_response
import spacy
import csv
import io
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  

# Load spaCy model once
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    nlp = None
    print("Warning: spaCy model not loaded. App will use a simple fallback split.")

KEYWORDS = ["must", "shall", "should"]

def extract_requirements_from_text(text, filename="(uploaded)"):
    """
    Returns a list of dicts: {id, text, category, source}
    """
    reqs = []
    # sentence splitting: prefer spaCy if available
    if nlp:
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
    else:
        # fallback: naive split by punctuation
        import re
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    idx = 1
    for i, s in enumerate(sentences, start=1):
        low = s.lower()
        if any(k in low for k in KEYWORDS):
            # decide category: 'must' -> Functional, otherwise Non-Functional
            if "must" in low or "shall" in low:
                category = "Functional"
            else:
                category = "Non-Functional"
            # generate sequential IDs (FR1, FR2, ... or NFR1 etc will be assigned later)
            reqs.append({
                "temp_index": idx,
                "text": s,
                "category": category,
                "source": f"{filename} | sentence {i}"
            })
            idx += 1
    return reqs

def assign_ids(reqs):
    """ Turn temp list into IDs FR1, FR2... """
    fr_count = 1
    for r in reqs:
        r_id = f"FR{fr_count}"
        fr_count += 1
        r["id"] = r_id
    return reqs

@app.route("/", methods=["GET"])
def index():
    requirements = session.get("requirements", [])
    return render_template("index.html", requirements=requirements, enumerate=enumerate)


@app.route("/extract", methods=["POST"])
def extract():
    uploaded = request.files.get("file")
    if not uploaded:
        return redirect(url_for("index"))
    text = uploaded.read().decode("utf-8", errors="ignore")
    filename = uploaded.filename or "(uploaded)"
    reqs = extract_requirements_from_text(text, filename=filename)
    reqs = assign_ids(reqs)
    session["requirements"] = reqs
    return redirect(url_for("index"))

@app.route("/save", methods=["POST"])
def save():
    # expects form fields like id-0, text-0, category-0, source-0 for rows
    new_reqs = []
    count = int(request.form.get("row-count", 0))
    for i in range(count):
        rid = request.form.get(f"id-{i}")
        text = request.form.get(f"text-{i}")
        category = request.form.get(f"category-{i}")
        source = request.form.get(f"source-{i}")
        new_reqs.append({"id": rid, "text": text, "category": category, "source": source})
    session["requirements"] = new_reqs
    return redirect(url_for("index"))

@app.route("/export", methods=["GET"])
def export():
    reqs = session.get("requirements", [])
    # produce CSV in memory
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(["ID", "Requirement", "Category", "Source"])
    for r in reqs:
        writer.writerow([r.get("id"), r.get("text"), r.get("category"), r.get("source")])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=requirements.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route("/clear", methods=["POST"])
def clear():
    session.pop("requirements", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

