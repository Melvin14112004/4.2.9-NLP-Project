import pdfplumber
import re
import spacy
import json
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    "Python", "JavaScript", "HTML", "CSS", "TensorFlow", "PyTorch",
    "Scikit-learn", "OpenCV", "BERT", "Neural Networks",
    "Computer Vision", "NLP", "Django", "REST API", "MongoDB",
    "Git", "AWS", "Jupyter", "Postman", "CI/CD"
]

degree_keywords = [
    "B.Tech", "Bachelor", "Master", "M.Tech", "PhD", "Diploma"
]

pdf_path = "Resume.pdf"

text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

def extract_name(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for i, line in enumerate(lines):
        if "@" in line or re.search(r"\d{10}", line):
            candidates = lines[max(0, i - 3):i]
            for cand in candidates:
                if re.match(r"^[A-Z][A-Z\s]+$", cand):
                    return cand.title()
                if re.match(r"^[A-Z][a-z]+ [A-Z][a-z]+$", cand):
                    return cand
    return None

# Insert this just before # Basic Info

def extract_project_section(text):
    lines = text.split('\n')
    start, end = -1, len(lines)
    for i, line in enumerate(lines):
        if re.search(r"\bprojects?\b", line.strip().lower()):
            start = i
            break
    if start == -1:
        return ""
    for j in range(start + 1, len(lines)):
        if re.search(r"\b(education|skills|certificates|achievements|experience|summary)\b", lines[j].strip().lower()):
            end = j
            break
    return '\n'.join(lines[start + 1:end])


# Basic Info
email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
emails = re.findall(email_pattern, text)
email = emails[0] if emails else None

phone_pattern = r"\b\d{10}\b"
phones = re.findall(phone_pattern, text)
phone = phones[0] if phones else None

name = extract_name(text)
doc = nlp(text)

# Education Info
education_info = {}
edu_pattern = re.compile(r"(Education|Academic Background|Qualifications)(.*?)(Experience|Projects|Skills|$)", re.S | re.I)
match = edu_pattern.search(text)
degree = None
institution = None
if match:
    edu_text = match.group(2).strip()
    lines = edu_text.split('\n')
    for line in lines:
        for deg_kw in degree_keywords:
            if deg_kw.lower() in line.lower():
                degree = line.strip()
        if any(kw in line for kw in ["College", "University", "Institute", "Engineering", "Saveetha"]):
            institution = line.strip()
education_info['Degree'] = degree
education_info['Institution'] = institution

# Skills
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp(skill) for skill in SKILLS_DB]
matcher.add("SKILLS", [*patterns])
matches = matcher(doc)
skills = set()
for match_id, start, end in matches:
    skill = doc[start:end].text
    skills.add(skill)
skills = list(skills)

# Experience (project section)
project_section = extract_project_section(text)
lines = [line.strip() for line in project_section.split('\n') if line.strip()]
experience = []

project_title = None
year = None

for i, line in enumerate(lines):
    if not project_title:
        project_title = line
    elif not year and re.search(r"\b20\d{2}\b", line):
        year = re.search(r"\b20\d{2}\b", line).group()

if project_title:
    exp = {"Description": project_title}
    if year:
        exp["Year"] = year
    experience.append(exp)


# Final Output
parsed_data = {
    "Name": name,
    "Email": email,
    "Phone": phone,
    "Degree": education_info.get('Degree'),
    "Institution": education_info.get('Institution'),
    "Skills": skills,
    "Experience": experience
}

print(json.dumps(parsed_data, indent=4))
with open("parsed_resume.json", "w") as f_out:
    json.dump(parsed_data, f_out, indent=4)
