import os
import uuid
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from gemini_service import GeminiService
from pdf_service import PDFService

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "material-purple-key")
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024

ai_service = None
store = {}

def get_ai_service() -> GeminiService:
    """Lazy loader for the Gemini Service."""
    global ai_service
    if ai_service is None:
        ai_service = GeminiService()
    return ai_service

@app.route("/", methods=["GET"])
def index():
    """Initial dashboard rendering."""
    return render_template("index.html")

@app.route("/form", methods=["GET"])
def get_form():
    """Returns the input editor form partial for HTMX replacement."""
    return render_template("partials/input_form.html")

@app.route("/generate", methods=["POST"])
def generate():
    """Generates study notes and returns dynamic tabs via HTMX."""
    notes = request.form.get("notes", "").strip()
    if len(notes) < 30:
        return (
            '<div class="alert-error">Content too short. Paste at least 30 characters.</div>',
            400
        )

    try:
        service = get_ai_service()
        payload = service.process_study_notes(notes)
        
        kit_id = str(uuid.uuid4())[:8]
        store[kit_id] = payload
        
        if len(store) > 100:
            oldest_key = next(iter(store))
            store.pop(oldest_key, None)

        return render_template("partials/study_kit.html", data=payload, kit_id=kit_id)
    except Exception as exc:
        return (
            f'<div class="alert-error">Synthesis failed: {str(exc)}</div>',
            500
        )

@app.route("/export/pdf/<kit_id>", methods=["GET"])
def export_pdf(kit_id):
    """Exports structured data to a downloadable formatted PDF."""
    scope = request.args.get("scope", "full")
    kit_data = store.get(kit_id)

    if not kit_data:
        return "Study Kit expired or not found. Please regenerate.", 404

    pdf_buffer = PDFService.generate_pdf(kit_data, scope=scope)
    safe_title = "".join(c for c in kit_data.get("title", "Study_Notes") if c.isalnum() or c in (" ", "_")).rstrip()
    filename = f"{safe_title.replace(' ', '_')}_{scope.upper()}.pdf"

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)