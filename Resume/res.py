from flask import Flask, render_template, request, send_file
import boto3

app = Flask(__name__)

# AWS S3 configuration
S3_BUCKET_NAME = 'mohana-1'
S3_ACCESS_KEY = 'AKIA6GBMCTWCJUVCQOGT'
S3_SECRET_KEY = '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'
S3_REGION = 'eu-north-1'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Extracting user data from the form
    name = request.form['name']
    email = request.form['email']
    education = request.form['education']
    experience = request.form['experience']

    # Generate resume text
    resume_text = f"Name: {name}\nEmail: {email}\nEducation: {education}\nExperience: {experience}"

    # Save resume to a text file
    filename = 'resume.txt'
    with open(filename, 'w') as file:
        file.write(resume_text)

    # Upload file to S3
    s3_client = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY, region_name=S3_REGION)
    s3_client.upload_file(filename, S3_BUCKET_NAME, filename)

    return render_template('success.html')

@app.route('/download')
def download():
    # Download file from S3
    filename = 'resume.txt'
    s3_client = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY, region_name=S3_REGION)
    s3_client.download_file(S3_BUCKET_NAME, filename, filename)

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
