import re
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

    # ATS-related constants
    ACTION_VERBS = [
        "developed", "implemented", "designed", "optimized", "built", "created", 
        "analyzed", "managed", "led", "coordinated", "executed", "delivered",
        "improved", "enhanced", "increased", "reduced", "streamlined", "automated",
        "integrated", "deployed", "tested", "debugged", "collaborated", "communicated"
    ]

    CORE_SECTIONS = ["education", "skills", "experience", "projects"]
    OPTIONAL_SECTIONS = ["certifications", "certificates", "awards", "publications", "interests"]

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

    # ============================================================
    # ATS SCORE CALCULATION METHODS
    # ============================================================

    def _calculate_keyword_match_score(self, resume_text, job_role):
        """Calculate keyword match score (40 points max)"""
        resume_lower = resume_text.lower()
        required_skills = self.get_required_skills(job_role)
        
        matching_skills = []
        for skill in required_skills:
            if skill.lower() in resume_lower:
                matching_skills.append(skill)
        
        if len(required_skills) > 0:
            score = (len(matching_skills) / len(required_skills)) * 40
        else:
            score = 0
        
        return min(round(score, 1), 40), matching_skills

    def _calculate_section_score(self, resume_text):
        """Calculate section presence score (20 points max)"""
        resume_lower = resume_text.lower()
        
        score = 0
        sections_found = []
        
        # Check core sections (5 points each)
        for section in self.CORE_SECTIONS:
            if section in resume_lower:
                score += 5
                sections_found.append(section)
        
        # Check optional sections (2.5 points each, up to 10 points)
        optional_count = 0
        for section in self.OPTIONAL_SECTIONS:
            if section in resume_lower:
                optional_count += 1
        
        score += min(optional_count * 2.5, 10)
        
        return min(round(score, 1), 20), sections_found

    def _calculate_action_verbs_score(self, resume_text):
        """Calculate action verbs score (10 points max)"""
        resume_lower = resume_text.lower()
        
        found_verbs = []
        for verb in self.ACTION_VERBS:
            # Use word boundary matching
            if re.search(r'\b' + verb + r'\b', resume_lower):
                found_verbs.append(verb)
        
        # Give 2 points per unique action verb found, max 10
        score = min(len(found_verbs) * 2, 10)
        
        return round(score, 1), found_verbs

    def _calculate_quantification_score(self, resume_text):
        """Calculate quantification score (10 points max) - prefers numbers"""
        # Check for percentages, numbers, and metrics
        patterns = [
            r'\d+%',           # Percentages like 50%
            r'\d+\s*(years?|yrs?)',  # Years of experience
            r'\$\d+',          # Dollar amounts
            r'\d+\s*(users?|customers?|clients?)',  # User counts
            r'\d+\s*(projects?|tasks?|features?)',    # Project counts
            r'\d+\s*(team members?|employees?)',     # Team sizes
            r'\d+',            # Any standalone number
        ]
        
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, resume_text, re.IGNORECASE)
            matches.extend(found)
        
        # Give points based on unique quantification instances
        unique_matches = len(set(matches))
        
        if unique_matches >= 5:
            return 10.0, matches[:10]
        elif unique_matches >= 3:
            return 7.5, matches[:7]
        elif unique_matches >= 1:
            return 5.0, matches[:5]
        else:
            return 0.0, []

    def _calculate_formatting_score(self, resume_text):
        """Calculate formatting simplicity score (20 points max)"""
        score = 20
        issues = []
        
        # Word count check
        word_count = len(resume_text.split())
        
        if word_count < 300:
            score -= 10
            issues.append("Resume too short (under 300 words)")
        elif word_count < 500:
            score -= 5
            issues.append("Resume could be more detailed")
        
        if word_count > 1500:
            score -= 10
            issues.append("Resume too long (over 1500 words)")
        elif word_count > 1000:
            score -= 5
            issues.append("Consider keeping resume under 2 pages")
        
        # Special characters check
        special_chars = ['@', '#', '$', '%', '^', '&', '*', '!', '~', '`']
        special_count = sum(1 for char in special_chars if char in resume_text)
        
        if special_count > 5:
            score -= 5
            issues.append("Too many special characters")
        
        # Check for excessive symbols or formatting issues
        if resume_text.count('|') > 10 or resume_text.count('•') > 20:
            score -= 3
            issues.append("Excessive bullet points or symbols")
        
        return max(round(score, 1), 0), issues

    def calculate_ats_score(self, resume_text, job_role):
        """
        Calculate comprehensive ATS score for the resume.
        
        Returns:
            dict with:
                - score: int (0-100)
                - breakdown: dict with individual component scores
                - suggestions: list of improvement suggestions
        """
        # Calculate individual components
        keyword_score, matched_skills = self._calculate_keyword_match_score(resume_text, job_role)
        section_score, sections_found = self._calculate_section_score(resume_text)
        action_verbs_score, verbs_found = self._calculate_action_verbs_score(resume_text)
        quantification_score, quantifications = self._calculate_quantification_score(resume_text)
        formatting_score, formatting_issues = self._calculate_formatting_score(resume_text)
        
        # Calculate total score
        total_score = int(keyword_score + section_score + action_verbs_score + 
                         quantification_score + formatting_score)
        
        # Generate suggestions
        suggestions = []
        
        # Keyword suggestions
        if keyword_score < 30:
            required_skills = self.get_required_skills(job_role)
            missing_tech = [s for s in required_skills if s.lower() not in resume_text.lower()]
            if missing_tech:
                missing_str = ", ".join(missing_tech[:5])
                suggestions.append(f"Add missing technical skills like {missing_str}.")
        
        # Section suggestions
        if section_score < 15:
            missing_sections = [s for s in self.CORE_SECTIONS if s not in [sec.lower() for sec in sections_found]]
            if missing_sections:
                suggestions.append(f"Add a dedicated {missing_sections[0].title()} section.")
        
        # Action verbs suggestions
        if action_verbs_score < 7:
            suggestions.append("Use more strong action verbs like Developed, Implemented, Built, Optimized.")
        
        # Quantification suggestions
        if quantification_score < 7:
            suggestions.append("Include measurable achievements with numbers, percentages, or metrics.")
        
        # Formatting suggestions
        if formatting_issues:
            for issue in formatting_issues[:2]:  # Limit to 2 formatting suggestions
                suggestions.append(issue.capitalize() + ".")
        
        # Build breakdown
        breakdown = {
            "keyword_match": {
                "score": keyword_score,
                "max": 40,
                "matched_skills": matched_skills
            },
            "sections": {
                "score": section_score,
                "max": 20,
                "found": sections_found
            },
            "action_verbs": {
                "score": action_verbs_score,
                "max": 10,
                "found": verbs_found[:5]  # Show top 5
            },
            "quantification": {
                "score": quantification_score,
                "max": 10,
                "examples": quantifications[:3]  # Show top 3 examples
            },
            "formatting": {
                "score": formatting_score,
                "max": 20,
                "issues": formatting_issues
            }
        }
        
        return {
            "score": total_score,
            "breakdown": breakdown,
            "suggestions": suggestions
        }

    def analyze(self, uploaded_file, job_role):
        text = self.extract_text(uploaded_file)

        matching, missing = self.match_skills(text, job_role)
        suggestions = self.generate_suggestions()
        score = self.calculate_match_score()
        
        # Calculate ATS score
        ats_result = self.calculate_ats_score(text, job_role)

        return {
            "resume_text": text,
            "job_role": job_role,
            "matching_skills": matching,
            "missing_skills": missing,
            "suggestions": suggestions,
            "match_score": score,
            "ats_score": ats_result["score"],
            "ats_breakdown": ats_result["breakdown"],
            "ats_suggestions": ats_result["suggestions"]
        }
