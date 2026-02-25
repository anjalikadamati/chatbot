import streamlit as st
from chatbot import ConversationManager
from resume_analyzer import ResumeAnalyzer


st.set_page_config(
    page_title="Placement Prep AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "analyzer" not in st.session_state:
    st.session_state.analyzer = ResumeAnalyzer()

if "chatbot" not in st.session_state:
    st.session_state.chatbot = ConversationManager()


st.markdown("""
<style>
.stApp {
    background-color: #343541;
}

[data-testid="stSidebar"] {
    background-color: #000000;
    padding-top: 20px;
}

[data-testid="stSidebar"] .stMarkdown h1 {
    color: #ffffff !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    padding: 10px 20px;
}

.nav-button {
    display: block;
    width: 100%;
    padding: 12px 20px;
    margin: 5px 0;
    background-color: transparent;
    border: none;
    border-radius: 10px;
    color: #a0a0a0;
    font-size: 16px;
    font-weight: 500;
    text-align: left;
    cursor: pointer;
    transition: all 0.3s ease;
}

.nav-button:hover {
    background-color: #2d2d35;
    color: #ffffff;
}

.nav-button.active {
    background-color: #5436da;
    color: #ffffff;
}

.feature-card {
    background: linear-gradient(145deg, #4a4a5a, #3d3d4d);
    border-radius: 15px;
    padding: 30px;
    margin: 15px 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(84, 54, 218, 0.5);
}

.feature-card h2 {
    color: #ffffff;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 15px;
}

.feature-card p {
    color: #b0b0b0;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
}

.stButton > button {
    background: linear-gradient(135deg, #5436da, #7857f5);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 30px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #6b46e0, #8b6cf5);
    transform: scale(1.02);
    box-shadow: 0 4px 15px rgba(84, 54, 218, 0.4);
}

.skill-tag {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
    margin: 4px;
}

.skill-tag.matching {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
}

.skill-tag.missing {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
}

.upload-box {
    background: linear-gradient(145deg, #3d3d4d, #444654);
    border: 2px dashed #6b7280;
    border-radius: 15px;
    padding: 40px;
    text-align: center;
    transition: all 0.3s ease;
}

.upload-box:hover {
    border-color: #5436da;
    background: linear-gradient(145deg, #444654, #4a4a5a);
}

.match-score {
    font-size: 48px;
    font-weight: 700;
    color: #5436da;
}

.stTextInput > div > div > input {
    background-color: #40414f;
    color: #ffffff;
    border: 1px solid #52525b;
    border-radius: 10px;
    padding: 12px 15px;
}

.stTextInput > div > div > input:focus {
    border-color: #5436da;
    box-shadow: 0 0 0 2px rgba(84, 54, 218, 0.2);
}

[data-testid="stChatMessage"] {
    background-color: #40414f;
    border-radius: 15px;
    padding: 15px;
    margin: 10px 0;
}

h1, h2, h3 {
    color: #ffffff !important;
}

.section-header {
    color: #ffffff;
    font-size: 22px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #5436da;
}

.suggestion-box {
    background: linear-gradient(145deg, #3d3d4d, #444654);
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
    border-left: 4px solid #5436da;
}
</style>
""", unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("# 🎯 Placement Prep AI")
        st.markdown("---")

        pages = {
            "dashboard": "📊 Dashboard",
            "chat": "🤖 Chat Assistant",
            "resume": "📄 Resume Analyzer"
        }

        for key, label in pages.items():
            if st.session_state.page == key:
                st.markdown(f'<button class="nav-button active">{label}</button>',
                            unsafe_allow_html=True)
            else:
                if st.button(label, key=f"nav_{key}"):
                    st.session_state.page = key
                    st.rerun()

        st.markdown("---")

        if st.session_state.page == "chat":
            st.markdown("### ⚙️ Chat Settings")

            chatbot = st.session_state.chatbot

            persona = st.selectbox(
                "Choose Persona",
                ["helpful", "teacher", "sassy"]
            )

            if st.button("Apply Persona"):
                chatbot.set_persona(persona)
                st.success(f"Persona set to {persona}")

            if st.button("Clear Chat"):
                chatbot.clear_history()
                st.rerun()


def render_dashboard():
    st.markdown("<h1 style='text-align:center;'>Welcome to Placement Prep AI</h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#a0a0a0;'>Your all-in-one placement preparation companion</p>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2>🤖 Chat Assistant</h2>
            <p>Get help with coding, interviews and technical concepts.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Chat Assistant"):
            st.session_state.page = "chat"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2>📄 Resume Analyzer</h2>
            <p>Match your resume with job roles and improve your profile.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Resume Analyzer"):
            st.session_state.page = "resume"
            st.rerun()


def render_chat():
    st.title("🤖 AI Chat Assistant")

    chatbot = st.session_state.chatbot

    for msg in chatbot.conversation_history:
        if msg["role"] == "system":
            continue
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chatbot.chat_completion(user_input)
                st.markdown(reply)

        st.rerun()


def render_resume():
    st.title("📄 Resume Analyzer")

    analyzer = st.session_state.analyzer
    col1, col2 = st.columns([1, 1.2])

    with col1:
        uploaded_file = st.file_uploader("Upload PDF or DOCX",
                                         type=["pdf", "docx"])
        job_role = st.text_input("Enter Job Role")

        quick_roles = [
            "Python Developer", "Data Analyst", "Frontend Developer",
            "Backend Developer", "Full Stack Developer",
            "Data Scientist", "DevOps Engineer", "Software Engineer"
        ]

        selected = st.selectbox("Select Target Job", [""] + quick_roles)

        if selected and not job_role:
            job_role = selected

        analyze_btn = st.button("Analyze Resume", use_container_width=True)

    results = None

    if analyze_btn:
        if not uploaded_file:
            st.error("Please upload a resume file.")
        elif not job_role:
            st.error("Please enter a job role.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    results = analyzer.analyze(uploaded_file, job_role)
                except Exception as e:
                    st.error(str(e))

    with col2:
        if results:
            # Skill Match Score Section
            score = results["match_score"]
            st.progress(score / 100)
            st.markdown(f"<p class='match-score'>{score}%</p>",
                        unsafe_allow_html=True)

            if results["matching_skills"]:
                st.markdown("<div class='section-header'>Matching Skills</div>",
                            unsafe_allow_html=True)
                for skill in results["matching_skills"]:
                    st.markdown(f"<span class='skill-tag matching'>{skill}</span>",
                                unsafe_allow_html=True)

            if results["missing_skills"]:
                st.markdown("<div class='section-header'>Missing Skills</div>",
                            unsafe_allow_html=True)
                for skill in results["missing_skills"]:
                    st.markdown(f"<span class='skill-tag missing'>{skill}</span>",
                                unsafe_allow_html=True)

            if results["suggestions"]:
                st.markdown("<div class='section-header'>Suggestions</div>",
                            unsafe_allow_html=True)
                for s in results["suggestions"]:
                    st.markdown(f"<div class='suggestion-box'>{s}</div>",
                                unsafe_allow_html=True)

            # ATS Score Section
            if "ats_score" in results:
                st.markdown("---")
                st.markdown("<div class='section-header'>📊 ATS Score</div>",
                            unsafe_allow_html=True)
                
                ats_score = results["ats_score"]
                ats_breakdown = results["ats_breakdown"]
                ats_suggestions = results.get("ats_suggestions", [])
                
                # Determine color based on score
                if ats_score >= 70:
                    score_color = "#10b981"  # Green
                elif ats_score >= 40:
                    score_color = "#f59e0b"  # Orange
                else:
                    score_color = "#ef4444"  # Red
                
                # ATS Score Display
                st.markdown(f"""
                <div style="text-align:center; padding: 20px; background: linear-gradient(145deg, #444654, #3d3d4d); 
                            border-radius: 15px; margin: 15px 0;">
                    <p style="font-size: 18px; color: #a0a0a0; margin-bottom: 10px;">ATS Score</p>
                    <p style="font-size: 56px; font-weight: 700; color: {score_color}; margin: 0;">
                        {ats_score}<span style="font-size: 24px; color: #6b7280;">/100</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Progress bar for ATS score
                st.progress(ats_score / 100)
                
                # Detailed Breakdown
                st.markdown("<div class='section-header'>📌 Detailed Breakdown:</div>",
                            unsafe_allow_html=True)
                
                breakdown_html = """
                <div style="background: linear-gradient(145deg, #444654, #3d3d4d); 
                            border-radius: 12px; padding: 20px; margin: 10px 0;">
                """
                
                # Keyword Match
                kw_score = ats_breakdown["keyword_match"]["score"]
                kw_max = ats_breakdown["keyword_match"]["max"]
                kw_pct = (kw_score / kw_max) * 100
                breakdown_html += f"""
                <div style="margin: 12px 0;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="color:#ffffff;">Keyword Match</span>
                        <span style="color:#a0a0a0;">{kw_score}/{kw_max}</span>
                    </div>
                    <div style="background:#2d2d35; border-radius:5px; height:8px;">
                        <div style="background: linear-gradient(90deg, #5436da, #7857f5); border-radius:5px; height:100%; width:{kw_pct}%"></div>
                    </div>
                </div>
                """
                
                # Sections
                sec_score = ats_breakdown["sections"]["score"]
                sec_max = ats_breakdown["sections"]["max"]
                sec_pct = (sec_score / sec_max) * 100
                breakdown_html += f"""
                <div style="margin: 12px 0;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="color:#ffffff;">Sections Present</span>
                        <span style="color:#a0a0a0;">{sec_score}/{sec_max}</span>
                    </div>
                    <div style="background:#2d2d35; border-radius:5px; height:8px;">
                        <div style="background: linear-gradient(90deg, #5436da, #7857f5); border-radius:5px; height:100%; width:{sec_pct}%"></div>
                    </div>
                </div>
                """
                
                # Action Verbs
                av_score = ats_breakdown["action_verbs"]["score"]
                av_max = ats_breakdown["action_verbs"]["max"]
                av_pct = (av_score / av_max) * 100
                breakdown_html += f"""
                <div style="margin: 12px 0;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="color:#ffffff;">Action Verbs</span>
                        <span style="color:#a0a0a0;">{av_score}/{av_max}</span>
                    </div>
                    <div style="background:#2d2d35; border-radius:5px; height:8px;">
                        <div style="background: linear-gradient(90deg, #5436da, #7857f5); border-radius:5px; height:100%; width:{av_pct}%"></div>
                    </div>
                </div>
                """
                
                # Quantification
                qn_score = ats_breakdown["quantification"]["score"]
                qn_max = ats_breakdown["quantification"]["max"]
                qn_pct = (qn_score / qn_max) * 100
                breakdown_html += f"""
                <div style="margin: 12px 0;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="color:#ffffff;">Quantification</span>
                        <span style="color:#a0a0a0;">{qn_score}/{qn_max}</span>
                    </div>
                    <div style="background:#2d2d35; border-radius:5px; height:8px;">
                        <div style="background: linear-gradient(90deg, #5436da, #7857f5); border-radius:5px; height:100%; width:{qn_pct}%"></div>
                    </div>
                </div>
                """
                
                # Formatting
                fmt_score = ats_breakdown["formatting"]["score"]
                fmt_max = ats_breakdown["formatting"]["max"]
                fmt_pct = (fmt_score / fmt_max) * 100
                breakdown_html += f"""
                <div style="margin: 12px 0;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="color:#ffffff;">Formatting</span>
                        <span style="color:#a0a0a0;">{fmt_score}/{fmt_max}</span>
                    </div>
                    <div style="background:#2d2d35; border-radius:5px; height:8px;">
                        <div style="background: linear-gradient(90deg, #5436da, #7857f5); border-radius:5px; height:100%; width:{fmt_pct}%"></div>
                    </div>
                </div>
                """
                
                breakdown_html += "</div>"
                st.markdown(breakdown_html, unsafe_allow_html=True)
                
                # Areas to Improve
                if ats_suggestions:
                    st.markdown("<div class='section-header'>⚠ Areas to Improve:</div>",
                                unsafe_allow_html=True)
                    
                    for suggestion in ats_suggestions:
                        st.markdown(f"""
                        <div class='suggestion-box' style="border-left-color: #f59e0b;">
                            {suggestion}
                        </div>
                        """, unsafe_allow_html=True)

        else:
            st.markdown(
                "<p style='color:#6b7280;'>Upload resume and enter job role to see results.</p>",
                unsafe_allow_html=True
            )


def main():
    render_sidebar()

    if st.session_state.page == "dashboard":
        render_dashboard()
    elif st.session_state.page == "chat":
        render_chat()
    elif st.session_state.page == "resume":
        render_resume()


if __name__ == "__main__":
    main()