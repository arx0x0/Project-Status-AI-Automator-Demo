**Project-Status-AI-Automator** project, incorporating elements from the HTML, images, and project information provided:

---

# Project-Status-AI-Automator

**Project-Status-AI-Automator** is a web-based tool designed to streamline and automate the creation of comprehensive project status reports. This application allows users to upload various project-related files (e.g., templates, transcripts, context PDFs) and generate status reports, tailored for different views (e.g., Project Manager, Software Developer, Sales, Executive). 

The tool offers a responsive, user-friendly interface using HTML, Tailwind CSS, and JavaScript, enabling quick uploads and custom report generation for effective project tracking and reporting.

## Features

1. **File Upload Interface**: 
   - Supports uploading JPEG templates, PDF transcripts, and additional context files.
   - Provides a drag-and-drop interface for easy file uploads.

2. **Automated Report Generation**:
   - Generates project status reports based on uploaded files.
   - Offers customized views for different roles (Project Manager, Software Developer, etc.).

3. **Dynamic Report Display**:
   - Allows switching between views without re-uploading files.
   - Displays generated reports directly within the interface for immediate review.

4. **Project Status Indicators**:
   - Provides visual indicators (On Track, Require Attention, Off Track) for key metrics like schedule, cost, risk, and quality.

5. **Development Tracking**:
   - Displays sprint progress, team velocity, and blocked tasks.
   - Logs current development status with critical items, required resources, and progress notes.

## Project Files and Structure (Example files are attached below)

### `index.html`
This is the main frontend file. It includes:
- **HTML** and **CSS (Tailwind)** to render the upload section, file information, and generated report.
- **JavaScript** functions for handling file uploads, drop zone events, report generation, and view switching.

### `README.md`
Provides a brief overview of the project and how to use it.

### `template_file.jpg`
A sample template for generating reports, illustrating layout design and sections for project scope, schedule, cost, risks, and quality.

### `app.py`
Backend code for processing file uploads, report generation, and serving the HTML front-end. Handles data processing and retrieval for role-specific views.

### `transcript_file.pdf`
A sample project meeting transcript file that details discussion points and next steps for project completion. Key information from this file is included in the report, such as:
   - **On-Schedule Payment Processing**.
   - **Resource Allocation for Security Fixes**.
   - **Infrastructure Scaling and Load Testing Requirements**.

## Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/arx0x0/Project-Status-AI-Automator-Demo.git
   cd Project-Status-AI-Automator
   ```

2. **Install Dependencies**:
   Ensure Python and any required libraries (like Flask, if using a Flask backend) are installed. Use `pip` to install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Start the app locally:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   Open your browser and navigate to `http://localhost:5000`. Use the interface to upload files and generate project reports.

5. **Generate Reports**:
   - Upload your template, transcript, and any context files.
   - Select a role-specific view to customize the report output for various stakeholders.

## Sample Usage Scenarios

- **Project Manager View**: See the overall status, scope, schedule, cost, risks, and quality indicators with visual cues for each aspect.
- **Developer View**: Focus on sprint deliverables, blocked tasks, and progress on key development items.
- **Executive View**: High-level insights on project progress, resource allocation, and any critical issues needing executive attention.

## Future Enhancements

- **Additional Roles**: Introduce more role-based views as per user feedback.
- **Detailed Error Handling**: Improve user feedback for missing files, file format issues, or upload errors.
- **Enhanced Analytics**: Provide more in-depth analytics and export options for project metrics.

---
#Template JPG
![fintech-automation-report-project-manager_1](https://github.com/user-attachments/assets/90710749-d859-40a5-88f2-358a1b085bad)

#Transcript PDF
[Project_Meeting_Transcript_Nov2024_Corrected.pdf](https://github.com/user-attachments/files/17535275/Project_Meeting_Transcript_Nov2024_Corrected.pdf)

#Context PDF (ex. Project Charter)
[Project_Charter_Construction_Project.pdf](https://github.com/user-attachments/files/17535277/Project_Charter_Construction_Project.pdf)

This README provides users with a clear understanding of the project’s purpose, usage, and setup, as well as how to contribute and any potential future enhancements. Let me know if you'd like any specific modifications!
