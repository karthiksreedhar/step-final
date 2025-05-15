from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from summarize import extract_text_from_pdf, extract_text_from_url, summarize_text, clarify_question

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    link = request.form.get('link')
    text = request.form.get('text')
    file = request.files.get('pdf')

    transcript = None
    if link:
        transcript = extract_text_from_url(link)
    elif file and file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        transcript = extract_text_from_pdf(filepath)
    elif text:
        transcript = text

    if not transcript:
        return "Please provide a valid transcript source.", 400

    summary = summarize_text(transcript)
    return render_template('summary.html', summary=summary)

@app.route('/clarify', methods=['POST'])
def clarify():
    summary = request.form.get('summary')
    question = request.form.get('question')
    answer = clarify_question(summary, question)
    return render_template('summary.html', summary=summary, answer=answer)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
