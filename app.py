from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import csv
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

@app.route('/process', methods=['POST'])
def process():
    link = request.form.get('link')
    text = request.form.get('text')
    file = request.files.get('pdf')
    action_type = request.form.get('action_type')

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

    if action_type == "summarize":
        summary = summarize_text(transcript) 
        return render_template('summary.html', summary=summary)
    elif action_type == "bias": 
        # print("Call to bias detection API with transcript:", transcript)
        return render_template('bias.html', transcript=transcript)
    else:
        return "Invalid action.", 400

@app.route('/bias', methods=['POST'])
def bias():
    selected_text = request.form.get('selected_text')
    if not selected_text:
        return jsonify({'error': 'No text selected.'}), 400
    # result = detect_bias(selected_text)
    # TODO: replace 
    # Example result:
    result = {
        "bias_severity": "High",
        "bias_type": "Political",
        "justification": "The statement strongly favors one party."
    }
    return jsonify(result)

@app.route('/bias_feedback', methods=['POST'])
def bias_feedback():
    
    selected_text = request.form.get('selected_text')
    # remove new line chars for saving to csv for further analysis
    if selected_text:
        selected_text = ' '.join(selected_text.splitlines())
        
    bias_severity = request.form.get('bias_severity')
    bias_type = request.form.get('bias_type')
    justification = request.form.get('justification')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    user_bias_severity = request.form.get('user_bias_severity')
    user_bias_type = request.form.get('user_bias_type')

    fieldnames = [
        'selected_text', 'bias_severity', 'bias_type', 'justification',
        'rating', 'comment', 'user_bias_severity', 'user_bias_type'
    ]
    row = {
        'selected_text': selected_text,
        'bias_severity': bias_severity,
        'bias_type': bias_type,
        'justification': justification,
        'rating': rating,
        'comment': comment,
        'user_bias_severity': user_bias_severity,
        'user_bias_type': user_bias_type
    }

    csv_path = 'results.csv'
    write_header = not os.path.isfile(csv_path) or os.path.getsize(csv_path) == 0
    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    return '', 204

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
