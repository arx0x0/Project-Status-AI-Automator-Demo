from flask import Flask, request, jsonify, render_template, send_from_directory, session
import os
import json
from PyPDF2 import PdfReader
import base64
import boto3
import uuid

app = Flask(__name__)

# Set a secret key for session management
# Generate one with: python -c "import secrets; print(secrets.token_hex(32))"
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "insert secret key here")

# AWS Bedrock setup
# Boto3 resolves credentials automatically from (in order):
#   1. Environment variables (AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY)
#   2. Shared credentials file (~/.aws/credentials)
#   3. IAM role attached to the instance/container
# Do not hardcode AWS access keys here.
BEDROCK_REGION = os.environ.get("AWS_REGION", "insert AWS region here")
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "insert model ID here")

bedrock = boto3.client(service_name="bedrock-runtime", region_name=BEDROCK_REGION)

# Global dictionary to store session data
session_data = {}

# Function to encode image to base64
def encode_image_to_base64(image):
    try:
        encoded_string = base64.b64encode(image.read()).decode('utf-8')
        return encoded_string
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

# Function to extract text from a single PDF file
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Function to process multiple context PDFs
def extract_text_from_context_pdfs(context_files):
    combined_context = ""
    for file in context_files:
        combined_context += extract_text_from_pdf(file) + "\n"
    return combined_context

# Function to generate HTML/CSS using Claude via AWS Bedrock
def generate_html_with_claude(transcript_text, context_text, encoded_image, view):
    prompt = [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": encoded_image
            }
        },
        {
            "type": "text",
            "text": f"""
You are to create an HTML/CSS project status report tailored for a {view} based on the provided template image and meeting transcript. Use the provided context to guide the formatting and information of the report.

### Instructions:
1. **Template Header Recognition**: First, analyze the provided template image to identify the headers or sections explicitly listed in the template.
   - You should identify all headers or section titles present in the template, such as “Sprint Progress,” “Blocked Tasks,” “Current Development Status,” etc.
   - Only include sections that are explicitly mentioned in the provided template image.

2. **Content Population Based on Headers**: After identifying the headers, extract relevant content from the transcript and context files, and populate the identified sections in the HTML/CSS.
   - Tailor the content to be most relevant to a {view}. For example, if the view is "Executive," focus on high-level summaries and key metrics.
   - Use only content from the transcript and context that is contextually related to the identified headers.
   - If the corresponding content in the given template is not explicitly mentioned, then use a placeholder value instead (i.e., "insert project completion %").
   - Always favour the information in the transcript over that of the context, as the information in the transcript will be more up to date. For any contradictions between the transcript and the context files, always refer to the transcript over any other context files.
   - Do not introduce new headers or sections that are not present in the template image, even if they are mentioned in the transcript.

3. **Consistency with Template Design**: Ensure that the generated HTML/CSS code strictly adheres to the design layout and styling of the provided template image.
   - This includes maintaining consistency in terms of font sizes, colors, section placements, indicators, and overall layout.
   - Make sure you do not use the same value as provided in the template for anything; all the headers, titles, content, etc., should either say "insert" or be tailored to the transcript or context instead.

4. **Output**: Return the complete HTML/CSS code that matches the design of the provided template, only return the HTML/CSS code not messages before or after.

Template Image: [Template Image File]
Transcript: {transcript_text}
Context: {context_text}
"""
        }
    ]

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1500,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        }),
    )

    # Extract and return the generated report content
    result = json.loads(response["body"].read())
    generated_html = result.get("content", [{}])[0].get("text", "No response generated")
    return generated_html

# Function to generate meeting minutes based on transcript-only input
def generate_meeting_minutes(transcript_text):
    # Placeholder function for generating meeting minutes and action items
    prompt = f"""
Analyze the provided meeting transcript and generate structured meeting minutes - make it organized by headers, subheaders, UX/UI friendly spacing, and Include the following sections: 
- Summary of Key Points Discussed
- Action Items and Responsibilities
- Decisions Made
- Issues Raised (if any)

Meeting Transcript: {transcript_text}
"""
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1500,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        }),
    )

    result = json.loads(response["body"].read())
    meeting_minutes = result.get("content", [{}])[0].get("text", "No response generated")
    return meeting_minutes

@app.route('/')
def home():
    return send_from_directory('', 'index.html')  # Serve index.html from the current directory

@app.route('/generate-report', methods=['POST', 'GET'])
def generate_report():
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id

    if request.method == 'POST':
        # Retrieve files from the POST request
        template_file = request.files.get('templateFile')
        transcript_file = request.files.get('transcriptFile')
        context_files = request.files.getlist('contextFiles')
        view = request.form.get('view', 'Project Manager')

        # Check the conditions
        if transcript_file and not template_file:
            # Only the transcript was uploaded
            transcript_text = extract_text_from_pdf(transcript_file)
            meeting_minutes = generate_meeting_minutes(transcript_text)
            # Store data in session_data
            session_data[session_id] = {
                'transcript_text': transcript_text,
                'context_text': '',
                'encoded_image': None,
                'available_views': ['Default'],
                'current_view': 'Default'
            }
            return jsonify({"report": meeting_minutes, "availableViews": ['Default']})

        elif transcript_file and template_file:
            # Transcript and template (with/without context) were uploaded
            transcript_text = extract_text_from_pdf(transcript_file)
            context_text = extract_text_from_context_pdfs(context_files) if context_files else ""
            encoded_image = encode_image_to_base64(template_file)

            if not encoded_image:
                return jsonify({"report": "Error: Could not encode the image."})

            # Store data in session_data
            session_data[session_id] = {
                'transcript_text': transcript_text,
                'context_text': context_text,
                'encoded_image': encoded_image,
                'available_views': ['Project Manager', 'Software Developer', 'Sales', 'Executive'],
                'current_view': view
            }

            # Call Claude to generate the HTML/CSS based on the template image, transcript, context, and view
            generated_report = generate_html_with_claude(transcript_text, context_text, encoded_image, view)
            return jsonify({"report": generated_report, "availableViews": session_data[session_id]['available_views']})

        else:
            return jsonify({"report": "Error: Please upload the required files (Transcript and optionally Template and Context)."}), 400

    elif request.method == 'GET':
        # Handle view change requests
        view = request.args.get('view', 'Project Manager')
        session_info = session_data.get(session_id)
        if session_info:
            transcript_text = session_info['transcript_text']
            context_text = session_info['context_text']
            encoded_image = session_info['encoded_image']

            if not encoded_image:
                # Handle the case where only transcript is available
                meeting_minutes = generate_meeting_minutes(transcript_text)
                return jsonify({"report": meeting_minutes})
            else:
                # Generate report for the new view
                generated_report = generate_html_with_claude(transcript_text, context_text, encoded_image, view)
                # Update current view in session_data
                session_info['current_view'] = view
                return jsonify({"report": generated_report})
        else:
            return jsonify({"report": "Session data not found. Please start a new report."}), 400

if __name__ == '__main__':
    app.run(debug=True)
