from flask import Blueprint, render_template, request, send_file, jsonify
from docxtpl import DocxTemplate
import os
import uuid

resume_bp = Blueprint('resume', __name__, template_folder='templates')

@resume_bp.route('/resume', methods=['GET', 'POST'])
def resume_form():
    if request.method == 'POST':
        # Collect form data
        data = {
            'NAME': request.form['name'],
            'ADDRESS': request.form['address'],
            'PHONE': request.form['phone'],
            'EMAIL': request.form['email'],
            'PROFILE': request.form['profile'],
            'EXP_HEADING1': request.form['experience_1_title'],
            'EXP_DETAIL1': request.form['experience_1_desc'],
            'EXP_HEADING2': request.form['experience_2_title'],
            'EXP_DETAIL2': request.form['experience_2_desc'],
            'EDUCATION_DETAILS': request.form['education'],
            'SKILLS': request.form['skills'],
            'ACTIVITIES': request.form['activities'],
        }

        # Template selection
        template_choice = request.form.get('template_choice')
        template_path = os.path.join(os.path.dirname(__file__),'templates_docx', f'{template_choice}.docx')

        doc = DocxTemplate(template_path)
        doc.render(data)

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploads_dir = os.path.join(project_root, 'uploads')

        # Make sure uploads directory exists
        os.makedirs(uploads_dir, exist_ok=True)

        output_filename = f"{uuid.uuid4()}.docx"
        output_path = os.path.join(uploads_dir, output_filename)

        doc.save(output_path)  # Save works

        # ✅ Now send_file with full absolute path
        return send_file(output_path, as_attachment=True)

    return render_template('resume_form.html')