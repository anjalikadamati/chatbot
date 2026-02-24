from typing import Dict, List, Tuple

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None


class ResumeAnalyzer:

    SKILL_DICTIONARY = {
        "python developer": ["python", "django", "flask", "sql", "git", "rest api", "fastapi", "pandas", "numpy"],
        "data analyst": ["python", "pandas", "numpy", "sql", "excel", "power bi", "tableau", "statistics", "visualization"],
        "frontend developer": ["html", "css", "javascript", "react", "vue", "angular", "git", "responsive design", "bootstrap"],
        "backend developer": ["python", "java", "node.js", "express", "django", "flask", "sql", "mongodb", "rest api", "graphql"],
        "full stack developer": ["html", "css", "javascript", "react", "node.js", "python", "sql", "mongodb", "git", "rest api"],
        "data scientist": ["python", "pandas", "numpy", "machine learning", "tensorflow", "pytorch", "sql", "statistics", "data visualization"],
        "devops engineer": ["docker", "kubernetes", "jenkins", "aws", "azure", "linux", "terraform", "git", "ci/cd"],
        "software engineer": ["python", "java", "c++", "git", "sql", "data structures", "algorithms", "object-oriented programming"],
        "machine learning engineer": ["python", "tensorflow", "pytorch", "machine learning", "deep learning", "sql", "pandas", "numpy", "scikit-learn"],
        "android developer": ["java", "kotlin", "android", "xml", "json", "rest api", "git", "firebase"],
        "ios developer": ["swift", "objective-c", "ios", "xcode", "cocoa", "rest api", "git", "core data"],
        "ui/ux designer": ["figma", "sketch", "adobe xd", "photoshop", "illustrator", "wireframing", "prototyping", "user research"],
        "cloud engineer": ["aws", "azure", "gcp", "docker", "kubernetes", "linux", "networking", "security"],
        "qa engineer": ["selenium", "test cases", "automation", "manual testing", "jira", "python", "api testing", "jenkins"],
        "business analyst": ["sql", "excel", "powerpoint", "data analysis", "requirement gathering", "tableau", "communication"],
    }

    SUGGESTION_TEMPLATES = {
        "python": "Consider adding Python projects or mentioning Python in your skills section.",
        "django": "Add projects involving Django web framework to strengthen your profile.",
        "flask": "Include Flask-based projects or API development experience.",
        "sql": "Mention experience with SQL databases and query writing.",
        "java": "Highlight Java programming experience and any related projects.",
        "javascript": "Add JavaScript proficiency and frontend development experience.",
        "react": "Include React.js projects or frontend development work.",
        "html": "Mention HTML5 and semantic markup experience.",
        "css": "Add CSS styling experience including responsive design.",
        "git": "Include Git version control knowledge in your technical skills.",
        "docker": "Add containerization experience with Docker.",
        "aws": "Mention AWS cloud platform experience.",
        "machine learning": "Include machine learning projects or experience.",
        "pandas": "Add data analysis projects using Pandas.",
        "excel": "Highlight Excel proficiency including advanced formulas.",
    }

    def __init__(self):
        self.resume_text = ""
        self.job_role = ""
        self.matching_skills = []
        self.missing_skills = []
        self.suggestions = []

    def extract_text_from_pdf(self, uploaded_file):
        if pypdf is None:
            raise ImportError("Install pypdf using: pip install pypdf")

        reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text

    def extract_text_from_docx(self, uploaded_file):
        if docx is None:
            raise ImportError("Install python-docx using: pip install python-docx")

        document = docx.Document(uploaded_file)
        text = ""
        for para in document.paragraphs:
            text += para.text + "\n"
        return text

    def extract_text(self, uploaded_file):
        name = uploaded_file.name.lower()

        if name.endswith(".pdf"):
            return self.extract_text_from_pdf(uploaded_file)

        if name.endswith(".docx"):
            return self.extract_text_from_docx(uploaded_file)

        raise ValueError("Upload only PDF or DOCX files.")

    def get_required_skills(self, job_role):
        role = job_role.lower().strip()

        if role in self.SKILL_DICTIONARY:
            return self.SKILL_DICTIONARY[role]

        for key in self.SKILL_DICTIONARY:
            if role in key or key in role:
                return self.SKILL_DICTIONARY[key]

        return self.SKILL_DICTIONARY["software engineer"]

    def match_skills(self, resume_text, job_role):
        self.resume_text = resume_text
        self.job_role = job_role

        resume_lower = resume_text.lower()
        required = self.get_required_skills(job_role)

        matching = []
        missing = []

        for skill in required:
            if skill.lower() in resume_lower:
                matching.append(skill.title())
            else:
                missing.append(skill.title())

        self.matching_skills = matching
        self.missing_skills = missing

        return matching, missing

    def generate_suggestions(self):
        suggestions = []

        for skill in self.missing_skills:
            key = skill.lower()
            if key in self.SUGGESTION_TEMPLATES:
                suggestions.append(self.SUGGESTION_TEMPLATES[key])

        if self.missing_skills:
            count = len(self.missing_skills)

            if count >= 5:
                suggestions.append("Consider taking online courses or certifications to improve your profile.")

            if count >= 3:
                suggestions.append("Work on projects to show practical experience.")
                suggestions.append("Add measurable achievements with numbers and results.")

            suggestions.append("Use strong action verbs like Developed, Built, Implemented, Led, Optimized.")

        if len(self.matching_skills) >= 5:
            suggestions.append("Your resume aligns well with the selected role. Good work!")

        self.suggestions = suggestions
        return suggestions

    def calculate_match_score(self):
        total = len(self.matching_skills) + len(self.missing_skills)
        if total == 0:
            return 0.0

        score = (len(self.matching_skills) / total) * 100
        return round(score, 1)

    def analyze(self, uploaded_file, job_role):
        text = self.extract_text(uploaded_file)

        matching, missing = self.match_skills(text, job_role)
        suggestions = self.generate_suggestions()
        score = self.calculate_match_score()

        return {
            "resume_text": text,
            "job_role": job_role,
            "matching_skills": matching,
            "missing_skills": missing,
            "suggestions": suggestions,
            "match_score": score
        }