# Congressional Hearing Summarization & Bias Detection Tool

This web application enables users to analyze congressional hearing transcripts for bias and generate structured summaries. Users can upload a PDF, paste transcript text, or (in the future) provide a URL to a hearing transcript. The system leverages advanced language models to identify and categorize bias, provide justifications, and collect user feedback to improve future analyses.

## Features

- **Transcript Input:** Upload a PDF, paste raw text, or (coming soon) provide a URL to a transcript.
- **Summary Generation:** Produces structured, readable summaries of hearings, including title, committee, date, key points, and policy connections.
- **Bias Detection:** Select a portion of the transcript and choose a detection mode (Simple, More Context, Most Context) to analyze for bias.
- **Bias Analysis Output:** For each biased quote, the system displays the quote, bias category, bias type, severity (mild, moderate, severe), and a justification.
- **User Feedback:** Users can rate the bias analysis, provide their own assessment of bias type and severity, and leave comments to help improve the system.

## Demo

A video demonstration of both the summarization and bias detection tools is available here:  
[https://youtu.be/UOyKZhBNzzg](https://youtu.be/UOyKZhBNzzg)

## Further Reading

This tool and its methodology are described in greater detail in the accompanying paper, **Democratizing Government Discourse.pdf**, which is included in this repository. The paper outlines the design decisions, bias detection framework, and technical approach behind the system.

## Installation

1. **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd step-final
    ```

2. **(Recommended) Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install all requirements:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set your OpenAI API key:**
    - You must provide your own OpenAI API key.  
      Edit `summarize.py` and `bias.py` to include your OpenAI API key, or set it as an environment variable if preferred.

5. **Run the application:**
    ```bash
    python app.py
    ```
    or
    ```bash
    flask run
    ```

6. **Open your browser and go to:**  
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## User Feedback Data

All user feedback submitted through the bias analysis tool is saved in a CSV file named `results.csv` in the project directory. You can review this file to see ratings, comments, and user assessments of bias for each analyzed quote.

## Notes

- The application currently supports PDF uploads and pasted text for transcript input.
- **URL-based transcript extraction is still under development.** Many congressional hearing sites use anti-bot protections, so we are working on a robust solution for extracting text directly from URLs.

---
