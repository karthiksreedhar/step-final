from openai import OpenAI

client = OpenAI(api_key="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")

def detect_bias(transcript, mode='simple'):
    if mode == 'simple':
        prompt = (
            "You are a specialised bias detection system designed to identify and analyse various forms of bias in congressional hearing transcripts. "
            "Your task is to examine the provided transcript objectively and correctly identify types of bias without imposing your own viewpoints.\n\n"
            "For each transcript you analyse, output a JSON object with a list of biased quotes in the transcript. Include the starting sentence, the quote itself, "
            "the bias category, the bias type, the justification, and the severity. Each of these terms is defined as follows:\n\n"
            "- start_sentence: the number of the sentence where the quote begin\n"
            "- bias_category: the high level category for the bias\n"
            "- bias_type: the specific nature of the bias\n"
            "- bias_severity: the severity of the bias either mild, moderate, severe\n"
            "- justification: the explanation for the allocated bias category, type, and severity"
        )
    elif mode == 'more_context':
        prompt = (
            "You are a specialised bias detection system designed to identify and analyse various forms of bias in congressional hearing transcripts. "
            "Your task is to examine the provided transcript objectively and correctly identify types of bias without imposing your own viewpoints.\n\n"
            "Bias categories in the context of congressional hearings are defined as follows:\n"
            "- Group Bias: Bias based on demographic characteristics.\n"
            "- Ideological Bias: Bias stemming from alignment to belief systems.\n"
            "- Factual Bias: Bias created by misrepresenting information.\n"
            "- Adversarial Bias: Bias from confrontational tactics in debate.\n\n"
            "For each transcript you analyse, output a JSON object with a list of biased quotes in the transcript. Include the starting sentence, the quote itself, "
            "the bias category, the bias type, the justification, and the severity. Each of these terms is defined as follows:\n"
            "- start_sentence: the number of the sentence where the quote begin\n"
            "- bias_category: the high level category for the bias\n"
            "- bias_type: the specific type within the category of bias\n"
            "- bias_severity: the severity of the bias either mild, moderate, severe\n"
            "- justification: the explanation for the allocated bias category, type, and severity"
        )
    elif mode == 'most_context':
        prompt = (
            "You are a specialised bias detection system designed to identify and analyse various forms of bias in congressional hearing transcripts. "
            "Your task is to examine the provided transcript objectively and correctly identify types of bias without imposing your own viewpoints.\n\n"
            "Bias categories in the context of congressional hearings are defined as follows:\n"
            "- Group Bias: Bias based on demographic characteristics. Types in this category include racial, gender, class, etc.\n"
            "- Ideological Bias: Bias stemming from alignment to belief systems. Types in this category include political, religious, etc.\n"
            "- Factual Bias: Bias created by misrepresenting information. Types in this category include omission, misinformation, opinions-as-fact, etc.\n"
            "- Adversarial Bias: Bias from confrontational tactics in debate. Types in this category include loaded questions, character attacks, etc.\n\n"
            "For each transcript you analyse, output a JSON object with a list of biased quotes in the transcript. Include the starting sentence, the quote itself, "
            "the bias category, the bias type, the justification, and the severity. Each of these terms is defined as follows:\n"
            "- start_sentence: the number of the sentence where the quote begin\n"
            "- bias_category: the high level category for the bias\n"
            "- bias_type: the specific type within the category of bias\n"
            "- bias_severity: the severity of the bias either mild, moderate, severe\n"
            "- justification: the explanation for the allocated bias category, type, and severity"
        )
    else:
        prompt = "You are a simple bias detector. Output a JSON object as described."

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": transcript}
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1
    )
    return response.choices[0].message.content