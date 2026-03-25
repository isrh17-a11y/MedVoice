from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from dotenv import load_dotenv

import report_parser
import ai_simplifier
import murf_tts

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "MedVoice is running"})


@app.route("/voices", methods=["GET"])
def voices():
    return jsonify({"voices": murf_tts.get_voices()})


@app.route("/process-report", methods=["POST"])
def process_report():
    try:
        language = request.form.get("language", "english")
        voice_id = request.form.get("voice_id", "en-US-natalie")

        if "file" in request.files:
            pdf_file = request.files["file"]
            tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
            try:
                pdf_file.save(tmp.name)
                extracted_text = report_parser.extract_text_from_pdf(tmp.name)
            finally:
                os.unlink(tmp.name)

        elif "text" in request.form:
            extracted_text = report_parser.extract_text_from_string(request.form["text"])

        else:
            return jsonify({"success": False, "error": "Please upload a PDF or paste text"}), 400

        report_dict = ai_simplifier.simplify_report(extracted_text, language)
        tts_text = murf_tts.build_tts_text(report_dict)
        audio_base64 = murf_tts.generate_audio(tts_text, voice_id)

        return jsonify({
            "success": True,
            "report": report_dict,
            "audio_base64": audio_base64,
            "audio_available": audio_base64 is not None,
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/ask-followup", methods=["POST"])
def ask_followup():
    try:
        body = request.get_json()
        question = body["question"]
        context = body["context"]

        answer_text = ai_simplifier.ask_followup(question, context)
        audio = murf_tts.generate_audio(answer_text)

        return jsonify({
            "answer": answer_text,
            "audio_base64": audio,
            "audio_available": audio is not None,
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(debug=True, port=port)
