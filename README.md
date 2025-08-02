
# 📄 Resume Parser using Python, spaCy & PDFPlumber

This project extracts useful information from resumes in PDF format using **Python**, **spaCy**, and **pdfplumber**. The goal is to automate resume parsing by pulling key details like:

- 👤 Name  
- 📧 Email  
- 📱 Phone number  
- 🎓 Degree & Institution  
- 🛠️ Skills  
- 🧠 Project Experience  

---

## 🚀 How It Works

### 🧠 NLP Model
- Uses **spaCy's `en_core_web_sm`** model for named entity recognition (NER).
- **PhraseMatcher** is used to detect predefined technical skills.

### 📄 PDF Parsing
- Utilizes `pdfplumber` to extract plain text from any resume PDF.

### 🧪 Regular Expressions
- Used to extract:
  - Email addresses
  - Phone numbers
  - Educational qualifications
  - Project experience

---

## 🧾 Sample Output

Here’s an example of the JSON output:

```json
{
  "Name": "Melvin S",
  "Email": "melvinsolomon200@gmail.com",
  "Phone": "9841441490",
  "Degree": "B.E. in Computer Science and Engineering",
  "Institution": "Saveetha Engineering College, Chennai, Tamil Nadu",
  "Skills": ["Python", "HTML", "CSS", "JavaScript"],
  "Experience": [
    {
      "Description": "Product Recommendation System",
      "Year": "2024"
    }
  ]
}
```

---

## 📁 File Structure

```bash
resume-parser/
├── Resume.pdf                # The input resume file
├── NLP.py                    # Main script for parsing
├── parsed_resume.json        # Output JSON with extracted data
└── README.md                 # Project documentation
```

---

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/resume-parser.git
cd resume-parser
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install pdfplumber spacy
python -m spacy download en_core_web_sm
```

---

## 🧠 How to Run

Make sure your resume file is named `Resume.pdf` and placed in the same directory.

```bash
python NLP.py
```

After execution, the script will generate `parsed_resume.json` containing the structured data.

---

## 🛠 Technologies Used

- [spaCy](https://spacy.io/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [re (regex)](https://docs.python.org/3/library/re.html)
- Python 3.x

---

## 📌 Code Explanation

- **`extract_name()`**: Uses regex and line context to find the candidate’s name near the email or phone.
- **`extract_project_section()`**: Extracts text under "Project" heading up to the next major section.
- **`PhraseMatcher`**: Matches known skills in the resume text.
- **Education Extraction**: Uses keyword matching to extract degree and institution names.
- **Experience Parsing**: Grabs the first project title and year from the project section.

---

## 🧠 Limitations & Future Work

- Only extracts **one** project (can be extended for multiple).
- Doesn’t extract work experience unless it's listed under the “Projects” section.
- Can be expanded with LinkedIn, certificates, and more.

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
