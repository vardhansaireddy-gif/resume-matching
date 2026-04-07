import streamlit as st
import re
import math
import json
import time
from collections import Counter
import random

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RecruitIQ · AI Resume Screener",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
  --bg: #0a0a0f;
  --surface: #12121a;
  --surface2: #1a1a28;
  --border: #2a2a3f;
  --accent: #7c6bff;
  --accent2: #ff6b9d;
  --accent3: #00d4aa;
  --accent4: #ffb347;
  --text: #e8e8f0;
  --text-muted: #8888aa;
  --success: #00d4aa;
  --danger: #ff4d6d;
  --warning: #ffb347;
}

html, body, .stApp {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Space Grotesk', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── HERO ── */
.hero {
  background: linear-gradient(135deg, #0a0a0f 0%, #12102a 40%, #0a1a1f 100%);
  padding: 60px 80px 40px;
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid var(--border);
}
.hero::before {
  content: '';
  position: absolute;
  top: -100px; right: -100px;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(124,107,255,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.hero::after {
  content: '';
  position: absolute;
  bottom: -100px; left: 200px;
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(0,212,170,0.08) 0%, transparent 70%);
  pointer-events: none;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(124,107,255,0.15);
  border: 1px solid rgba(124,107,255,0.3);
  border-radius: 100px;
  padding: 6px 16px;
  font-size: 12px;
  color: var(--accent);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 24px;
}
.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: clamp(2.2rem, 4vw, 3.8rem);
  font-weight: 800;
  line-height: 1.1;
  margin: 0 0 16px;
  background: linear-gradient(135deg, #ffffff 0%, #a89bff 50%, #00d4aa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub {
  font-size: 1.1rem;
  color: var(--text-muted);
  max-width: 600px;
  line-height: 1.6;
}

/* ── AGENT PIPELINE ── */
.pipeline-container {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 32px;
  margin: 0 80px 40px;
}
.pipeline-title {
  font-family: 'Syne', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 24px;
}
.agents-grid {
  display: flex;
  gap: 0;
  align-items: center;
  flex-wrap: wrap;
}
.agent-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 16px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  transition: all 0.3s;
  position: relative;
}
.agent-chip.active {
  border-color: var(--accent);
  color: var(--accent);
  background: rgba(124,107,255,0.1);
  box-shadow: 0 0 20px rgba(124,107,255,0.2);
}
.agent-chip.done {
  border-color: var(--success);
  color: var(--success);
  background: rgba(0,212,170,0.08);
}
.agent-arrow {
  color: var(--border);
  font-size: 18px;
  padding: 0 6px;
  flex-shrink: 0;
}

/* ── MAIN LAYOUT ── */
.main-content {
  padding: 0 80px 80px;
}

/* ── UPLOAD CARDS ── */
.upload-section {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 32px;
  transition: border-color 0.3s;
  height: 100%;
}
.upload-section:hover { border-color: var(--accent); }
.upload-label {
  font-family: 'Syne', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.upload-hint {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

/* ── STREAMLIT OVERRIDES ── */
.stTextArea textarea {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 13px !important;
  resize: vertical !important;
}
.stTextArea textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(124,107,255,0.15) !important;
}
.stButton > button {
  background: linear-gradient(135deg, var(--accent), #9b8bff) !important;
  color: white !important;
  border: none !important;
  border-radius: 12px !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
  padding: 16px 48px !important;
  cursor: pointer !important;
  transition: all 0.3s !important;
  width: 100% !important;
  letter-spacing: 0.5px !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 12px 40px rgba(124,107,255,0.4) !important;
}
label[data-testid="stWidgetLabel"] {
  color: var(--text-muted) !important;
  font-size: 13px !important;
}

/* ── VERDICT CARD ── */
.verdict-card {
  border-radius: 24px;
  padding: 48px;
  text-align: center;
  position: relative;
  overflow: hidden;
  margin-bottom: 32px;
}
.verdict-card.hired {
  background: linear-gradient(135deg, rgba(0,212,170,0.15), rgba(0,212,170,0.05));
  border: 2px solid rgba(0,212,170,0.4);
}
.verdict-card.rejected {
  background: linear-gradient(135deg, rgba(255,77,109,0.15), rgba(255,77,109,0.05));
  border: 2px solid rgba(255,77,109,0.3);
}
.verdict-card.borderline {
  background: linear-gradient(135deg, rgba(255,179,71,0.15), rgba(255,179,71,0.05));
  border: 2px solid rgba(255,179,71,0.3);
}
.verdict-emoji { font-size: 5rem; margin-bottom: 16px; display: block; }
.verdict-title {
  font-family: 'Syne', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 8px;
}
.verdict-sub { font-size: 1.1rem; color: var(--text-muted); }
.score-ring {
  display: inline-block;
  margin: 24px auto;
}

/* ── METRIC CARDS ── */
.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}
.metric-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
}
.metric-value {
  font-family: 'Syne', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 4px;
}
.metric-label {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* ── AGENT RESULT CARDS ── */
.agent-result {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 16px;
  transition: border-color 0.3s;
}
.agent-result:hover { border-color: var(--accent); }
.agent-result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.agent-name {
  font-family: 'Syne', sans-serif;
  font-weight: 700;
  font-size: 1.05rem;
  display: flex;
  align-items: center;
  gap: 10px;
}
.agent-score-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  padding: 4px 14px;
  border-radius: 100px;
}
.score-high { background: rgba(0,212,170,0.15); color: var(--success); }
.score-med { background: rgba(255,179,71,0.15); color: var(--warning); }
.score-low { background: rgba(255,77,109,0.15); color: var(--danger); }

/* ── SKILL TAGS ── */
.skill-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.skill-tag {
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
}
.skill-match { background: rgba(0,212,170,0.15); color: var(--success); border: 1px solid rgba(0,212,170,0.3); }
.skill-miss { background: rgba(255,77,109,0.1); color: var(--danger); border: 1px solid rgba(255,77,109,0.2); }
.skill-partial { background: rgba(255,179,71,0.1); color: var(--warning); border: 1px solid rgba(255,179,71,0.2); }

/* ── PROGRESS BAR ── */
.prog-bar-container { margin-bottom: 12px; }
.prog-bar-label { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
.prog-bar-track { background: var(--surface2); border-radius: 100px; height: 8px; overflow: hidden; }
.prog-bar-fill { height: 100%; border-radius: 100px; transition: width 1s ease; }

/* ── SUGGESTION CARDS ── */
.suggestion-card {
  background: var(--surface2);
  border-left: 3px solid var(--accent);
  border-radius: 0 12px 12px 0;
  padding: 16px 20px;
  margin-bottom: 12px;
  font-size: 14px;
  line-height: 1.6;
}
.suggestion-card.critical { border-color: var(--danger); }
.suggestion-card.medium { border-color: var(--warning); }
.suggestion-card.low { border-color: var(--accent3); }
.suggestion-priority {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-bottom: 6px;
}

/* ── SECTION HEADERS ── */
.section-header {
  font-family: 'Syne', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  margin: 40px 0 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}

/* ── DIVIDER ── */
.custom-divider {
  border: none;
  height: 1px;
  background: var(--border);
  margin: 40px 0;
}

/* ── KEYWORD DENSITY ── */
.kw-cloud { display: flex; flex-wrap: wrap; gap: 8px; }
.kw-chip {
  padding: 6px 14px;
  border-radius: 100px;
  font-size: 12px;
  font-family: 'JetBrains Mono', monospace;
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text-muted);
}
.kw-chip.high { color: var(--success); border-color: rgba(0,212,170,0.3); }
.kw-chip.med { color: var(--warning); border-color: rgba(255,179,71,0.3); }

.stProgress > div > div { background: var(--accent) !important; }

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NLP UTILITIES (TF-IDF based)
# ─────────────────────────────────────────────

STOPWORDS = set([
    'a','an','the','and','or','but','in','on','at','to','for','of','with',
    'by','from','is','was','are','were','be','been','being','have','has',
    'had','do','does','did','will','would','could','should','may','might',
    'this','that','these','those','i','we','you','he','she','they','it',
    'as','if','so','not','no','nor','yet','both','either','neither','each',
    'few','more','most','other','some','such','than','then','too','very',
    'just','because','while','although','though','since','until','unless',
    'between','through','during','before','after','above','below','up','down',
    'out','off','over','under','again','further','once','here','there','when',
    'where','why','how','all','any','both','each','more','much','s','t','can',
    'also','into','about','which','who','whom','whose','what','when','their',
    'its','our','my','your','his','her','us','them','me','him','her','we','am'
])

TECH_SKILLS = [
    'python','java','javascript','typescript','react','angular','vue','node',
    'django','flask','fastapi','spring','sql','mysql','postgresql','mongodb',
    'redis','docker','kubernetes','aws','azure','gcp','git','linux','ci/cd',
    'machine learning','deep learning','nlp','tensorflow','pytorch','scikit',
    'pandas','numpy','spark','hadoop','kafka','elasticsearch','rest','api',
    'microservices','devops','agile','scrum','html','css','c++','c#','go',
    'rust','scala','r','matlab','tableau','powerbi','excel','jira','jenkins',
    'terraform','ansible','nginx','graphql','oauth','jwt','blockchain',
    'data science','neural network','computer vision','reinforcement learning',
    'llm','gpt','bert','transformers','opencv','xgboost','selenium','airflow',
    'dbt','snowflake','databricks','mlflow','huggingface','langchain'
]

SOFT_SKILLS = [
    'leadership','communication','teamwork','problem solving','analytical',
    'creative','innovative','collaborative','adaptable','detail oriented',
    'critical thinking','time management','project management','mentoring',
    'strategic','organized','proactive','results driven','self motivated',
    'interpersonal','presentation','negotiation','conflict resolution'
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s/#+]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text):
    tokens = clean_text(text).split()
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]

def get_ngrams(tokens, n=2):
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def compute_tfidf(doc_tokens, all_docs_tokens):
    tf = Counter(doc_tokens)
    total = len(doc_tokens) or 1
    tf = {k: v/total for k, v in tf.items()}
    idf = {}
    N = len(all_docs_tokens)
    all_terms = set(t for doc in all_docs_tokens for t in doc)
    for term in all_terms:
        df = sum(1 for doc in all_docs_tokens if term in doc)
        idf[term] = math.log((N + 1) / (df + 1)) + 1
    tfidf = {term: tf.get(term, 0) * idf.get(term, 1) for term in all_terms}
    return tfidf

def cosine_similarity(v1, v2):
    common = set(v1.keys()) & set(v2.keys())
    dot = sum(v1[k] * v2[k] for k in common)
    mag1 = math.sqrt(sum(x**2 for x in v1.values()))
    mag2 = math.sqrt(sum(x**2 for x in v2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)

def extract_skills(text, skill_list):
    text_lower = text.lower()
    found = []
    for skill in skill_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return found

def extract_experience_years(text):
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
        r'(\d+)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)',
        r'experience\s*(?:of\s*)?(\d+)\+?\s*years?',
    ]
    years = []
    for p in patterns:
        matches = re.findall(p, text.lower())
        years.extend([int(m) for m in matches])
    return max(years) if years else 0

def extract_education(text):
    text_lower = text.lower()
    degrees = {
        'phd': ['phd', 'ph.d', 'doctorate', 'doctoral'],
        'masters': ['master', 'msc', 'm.s.', 'mba', 'mtech', 'm.tech', 'me ', 'ms '],
        'bachelors': ['bachelor', 'bsc', 'b.s.', 'btech', 'b.tech', 'be ', 'bs ','b.e'],
        'diploma': ['diploma', 'associate'],
    }
    found = []
    for degree, keywords in degrees.items():
        for kw in keywords:
            if kw in text_lower:
                found.append(degree)
                break
    return found

def extract_certifications(text):
    certs = ['aws certified','gcp certified','azure certified','pmp','cissp',
             'ceh','comptia','google analytics','scrum master','six sigma',
             'data science certificate','machine learning certificate',
             'tensorflow certificate','pytorch','coursera','udemy','linkedin learning']
    text_lower = text.lower()
    return [c for c in certs if c in text_lower]

def extract_keywords_tfidf(text, top_n=20):
    tokens = tokenize(text)
    bigrams = get_ngrams(tokens, 2)
    all_tokens = tokens + bigrams
    tf = Counter(all_tokens)
    total = len(all_tokens) or 1
    tfidf_scores = {k: (v/total) * (1 + math.log(1 + v)) for k, v in tf.items()}
    sorted_kw = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
    return [k for k, v in sorted_kw[:top_n]]

# ─────────────────────────────────────────────
# THE 10 AGENTS
# ─────────────────────────────────────────────

class Agent:
    def __init__(self, name, icon, description):
        self.name = name
        self.icon = icon
        self.description = description

    def analyze(self, resume, jd):
        raise NotImplementedError

# Agent 1: TF-IDF Semantic Similarity Agent
class SemanticSimilarityAgent(Agent):
    def analyze(self, resume, jd):
        r_tokens = tokenize(resume)
        j_tokens = tokenize(jd)
        r_bi = get_ngrams(r_tokens, 2)
        j_bi = get_ngrams(j_tokens, 2)
        r_all = r_tokens + r_bi
        j_all = j_tokens + j_bi
        tfidf_r, tfidf_j = compute_tfidf(r_all, [r_all, j_all]), compute_tfidf(j_all, [r_all, j_all])
        score = cosine_similarity(tfidf_r, tfidf_j)
        pct = round(score * 100, 1)
        interpretation = (
            "Excellent semantic match" if pct >= 70 else
            "Good contextual alignment" if pct >= 50 else
            "Moderate overlap" if pct >= 30 else
            "Low semantic similarity"
        )
        return {
            "score": pct,
            "max": 100,
            "label": "TF-IDF Cosine Similarity",
            "interpretation": interpretation,
            "details": f"TF-IDF vectorization on unigrams + bigrams yielded {pct}% cosine similarity.",
            "keywords_resume": extract_keywords_tfidf(resume, 10),
            "keywords_jd": extract_keywords_tfidf(jd, 10),
        }

# Agent 2: Technical Skills Matcher
class TechSkillsAgent(Agent):
    def analyze(self, resume, jd):
        resume_skills = set(extract_skills(resume, TECH_SKILLS))
        jd_skills = set(extract_skills(jd, TECH_SKILLS))
        matched = resume_skills & jd_skills
        missing = jd_skills - resume_skills
        extra = resume_skills - jd_skills
        pct = round((len(matched) / len(jd_skills) * 100) if jd_skills else 50, 1)
        return {
            "score": pct,
            "max": 100,
            "label": "Technical Skill Coverage",
            "matched": sorted(matched),
            "missing": sorted(missing),
            "extra": sorted(extra),
            "jd_total": len(jd_skills),
            "resume_total": len(resume_skills),
            "details": f"Matched {len(matched)}/{len(jd_skills)} required technical skills.",
        }

# Agent 3: Soft Skills Agent
class SoftSkillsAgent(Agent):
    def analyze(self, resume, jd):
        resume_soft = set(extract_skills(resume, SOFT_SKILLS))
        jd_soft = set(extract_skills(jd, SOFT_SKILLS))
        matched = resume_soft & jd_soft
        missing = jd_soft - resume_soft
        pct = round((len(matched) / len(jd_soft) * 100) if jd_soft else 60, 1)
        return {
            "score": pct,
            "max": 100,
            "label": "Soft Skills Alignment",
            "matched": sorted(matched),
            "missing": sorted(missing),
            "resume_total": len(resume_soft),
            "details": f"Matched {len(matched)}/{len(jd_soft)} required soft skills.",
        }

# Agent 4: Experience Evaluator
class ExperienceAgent(Agent):
    def analyze(self, resume, jd):
        resume_exp = extract_experience_years(resume)
        jd_exp = extract_experience_years(jd)
        if jd_exp == 0:
            score = 75.0
            gap = 0
            note = "No explicit experience requirement found in JD."
        elif resume_exp >= jd_exp:
            score = min(100.0, 70 + (resume_exp - jd_exp) * 5)
            gap = resume_exp - jd_exp
            note = f"You exceed the requirement by {gap} year(s)." if gap > 0 else "You meet the experience requirement exactly."
        else:
            gap = jd_exp - resume_exp
            score = max(10.0, 70 - gap * 15)
            note = f"You are {gap} year(s) short of the {jd_exp}-year requirement."
        return {
            "score": round(score, 1),
            "max": 100,
            "label": "Experience Match",
            "resume_years": resume_exp,
            "jd_years": jd_exp,
            "gap": gap if jd_exp > 0 else 0,
            "note": note,
            "details": note,
        }

# Agent 5: Education Checker
class EducationAgent(Agent):
    def analyze(self, resume, jd):
        degree_rank = {'phd': 4, 'masters': 3, 'bachelors': 2, 'diploma': 1}
        resume_edu = extract_education(resume)
        jd_edu = extract_education(jd)
        resume_rank = max([degree_rank.get(d, 0) for d in resume_edu], default=0)
        jd_rank = max([degree_rank.get(d, 0) for d in jd_edu], default=0)
        if jd_rank == 0:
            score = 80.0
            note = "No specific education requirement in JD."
        elif resume_rank >= jd_rank:
            score = 90.0 if resume_rank > jd_rank else 80.0
            note = f"Education meets or exceeds requirement."
        else:
            diff = jd_rank - resume_rank
            score = max(30.0, 80 - diff * 20)
            note = f"Education level may be below requirement."
        return {
            "score": round(score, 1),
            "max": 100,
            "label": "Education Compatibility",
            "resume_edu": resume_edu or ["Not detected"],
            "jd_edu": jd_edu or ["Not specified"],
            "note": note,
            "details": note,
        }

# Agent 6: Keyword Density Analyzer
class KeywordDensityAgent(Agent):
    def analyze(self, resume, jd):
        jd_keywords = extract_keywords_tfidf(jd, 25)
        resume_text_lower = resume.lower()
        found, missing = [], []
        for kw in jd_keywords:
            if kw in resume_text_lower:
                found.append(kw)
            else:
                missing.append(kw)
        pct = round(len(found) / len(jd_keywords) * 100, 1) if jd_keywords else 50
        return {
            "score": pct,
            "max": 100,
            "label": "JD Keyword Coverage",
            "found": found,
            "missing": missing[:8],
            "total_jd_keywords": len(jd_keywords),
            "details": f"Resume covers {len(found)}/{len(jd_keywords)} high-value JD keywords.",
        }

# Agent 7: Certification Checker
class CertificationAgent(Agent):
    def analyze(self, resume, jd):
        resume_certs = extract_certifications(resume)
        jd_certs = extract_certifications(jd)
        matched = set(resume_certs) & set(jd_certs)
        if not jd_certs:
            score = 70.0
            note = "No certifications required in JD. Yours are a bonus."
        else:
            score = round(min(100, 50 + len(matched) / len(jd_certs) * 50), 1)
            note = f"Matched {len(matched)}/{len(jd_certs)} required certifications."
        return {
            "score": score,
            "max": 100,
            "label": "Certification Match",
            "resume_certs": resume_certs or ["None detected"],
            "jd_certs": jd_certs or ["None required"],
            "matched": list(matched),
            "note": note,
            "details": note,
        }

# Agent 8: Resume Quality / ATS Agent
class ATSQualityAgent(Agent):
    def analyze(self, resume, jd):
        issues = []
        boosts = []
        # Length check
        words = len(resume.split())
        if words < 150:
            issues.append("Resume is too short (< 150 words). Add more detail.")
        elif words > 800:
            issues.append("Resume might be too lengthy (> 800 words). Consider trimming.")
        else:
            boosts.append(f"Good resume length ({words} words).")
        # Contact info
        has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume))
        has_phone = bool(re.search(r'(\+?\d[\d\s\-\.]{8,}\d)', resume))
        if has_email: boosts.append("Email address detected.")
        else: issues.append("No email address found.")
        if has_phone: boosts.append("Phone number detected.")
        else: issues.append("No phone number found.")
        # Sections
        sections = ['experience','education','skills','projects','summary','objective','achievements']
        found_sections = [s for s in sections if s in resume.lower()]
        if len(found_sections) >= 4:
            boosts.append(f"Well-structured with {len(found_sections)} sections.")
        else:
            issues.append(f"Only {len(found_sections)} standard sections found. Add more.")
        # Bullet points / action verbs
        action_verbs = ['developed','built','designed','led','managed','created','implemented',
                        'improved','achieved','delivered','analyzed','optimized','collaborated',
                        'architected','deployed','automated','increased','reduced','launched']
        found_verbs = [v for v in action_verbs if v in resume.lower()]
        if len(found_verbs) >= 4:
            boosts.append(f"Good use of action verbs ({len(found_verbs)} found).")
        else:
            issues.append("Use more action verbs (developed, led, built, etc.).")
        score = max(20, 100 - len(issues) * 12 + len(boosts) * 5)
        score = min(95, score)
        return {
            "score": round(score, 1),
            "max": 100,
            "label": "ATS & Resume Quality",
            "issues": issues,
            "boosts": boosts,
            "word_count": words,
            "details": f"{len(boosts)} strengths, {len(issues)} issues found.",
        }

# Agent 9: Role Title Alignment Agent
class RoleAlignmentAgent(Agent):
    def analyze(self, resume, jd):
        role_families = {
            'data_science': ['data scientist','machine learning','ml engineer','ai engineer','data analyst','nlp'],
            'software': ['software engineer','developer','programmer','backend','frontend','fullstack','sde'],
            'devops': ['devops','sre','cloud engineer','infrastructure','platform engineer','devsecops'],
            'product': ['product manager','pm','product owner','scrum master','business analyst'],
            'design': ['ui designer','ux designer','product designer','graphic designer'],
            'management': ['engineering manager','tech lead','cto','vp engineering','director'],
            'data_engineering': ['data engineer','etl','pipeline','spark','hadoop','kafka'],
            'security': ['security engineer','cybersecurity','penetration tester','soc analyst'],
        }
        def detect_family(text):
            text_lower = text.lower()
            scores = {}
            for family, keywords in role_families.items():
                count = sum(1 for kw in keywords if kw in text_lower)
                if count > 0:
                    scores[family] = count
            return scores
        resume_families = detect_family(resume)
        jd_families = detect_family(jd)
        overlap = set(resume_families.keys()) & set(jd_families.keys())
        if not jd_families:
            score = 65.0
            note = "Could not detect specific role family in JD."
        elif overlap:
            score = 85.0 if len(overlap) >= 2 else 75.0
            note = f"Role alignment: {', '.join(overlap)}."
        else:
            score = 30.0
            note = "Career trajectory may not align with target role."
        return {
            "score": round(score, 1),
            "max": 100,
            "label": "Role Title Alignment",
            "resume_roles": list(resume_families.keys()),
            "jd_roles": list(jd_families.keys()),
            "overlap": list(overlap),
            "note": note,
            "details": note,
        }

# Agent 10: Final Recommendation Engine
class RecommendationAgent(Agent):
    def analyze(self, resume, jd):
        # This agent synthesizes inputs; called separately
        return {}

    def synthesize(self, all_results):
        weights = {
            'semantic': 0.20,
            'tech_skills': 0.22,
            'soft_skills': 0.08,
            'experience': 0.15,
            'education': 0.08,
            'keywords': 0.10,
            'certification': 0.05,
            'ats': 0.07,
            'role': 0.05,
        }
        keys = list(weights.keys())
        agent_keys = ['semantic','tech_skills','soft_skills','experience','education',
                      'keywords','certification','ats','role']
        total_score = 0
        for i, key in enumerate(agent_keys):
            if i < len(all_results):
                s = all_results[i].get('score', 50)
                total_score += s * weights[key]

        suggestions = []
        tech_res = all_results[1]
        if tech_res.get('missing'):
            for skill in list(tech_res['missing'])[:3]:
                suggestions.append({"priority": "critical", "text": f"Add '{skill}' to your skillset or highlight any adjacent experience.", "agent": "Tech Skills Agent"})
        kw_res = all_results[5]
        if kw_res.get('missing'):
            for kw in list(kw_res['missing'])[:3]:
                suggestions.append({"priority": "medium", "text": f"Include keyword '{kw}' naturally in your resume to improve ATS scoring.", "agent": "Keyword Agent"})
        exp_res = all_results[3]
        if exp_res.get('gap', 0) > 0 and all_results[3].get('jd_years', 0) > 0 and all_results[3].get('resume_years', 0) < all_results[3].get('jd_years', 0):
            suggestions.append({"priority": "critical", "text": f"You're {exp_res['gap']} year(s) short. Highlight impactful project contributions and freelance/personal projects to bridge the gap.", "agent": "Experience Agent"})
        ats_res = all_results[7]
        for issue in ats_res.get('issues', []):
            suggestions.append({"priority": "medium", "text": issue, "agent": "ATS Agent"})
        soft_res = all_results[2]
        if soft_res.get('missing'):
            for sk in list(soft_res['missing'])[:2]:
                suggestions.append({"priority": "low", "text": f"Soft skill '{sk}' is mentioned in JD — add evidence in your cover letter or summary.", "agent": "Soft Skills Agent"})
        cert_res = all_results[6]
        if cert_res.get('jd_certs') and cert_res['jd_certs'] != ["None required"]:
            unmatched = set(cert_res.get('jd_certs', [])) - set(cert_res.get('matched', []))
            for c in list(unmatched)[:2]:
                suggestions.append({"priority": "low", "text": f"Consider obtaining '{c}' certification to strengthen your profile.", "agent": "Certification Agent"})
        sem_res = all_results[0]
        if sem_res.get('score', 0) < 40:
            suggestions.append({"priority": "critical", "text": "Low semantic similarity. Rewrite your resume summary to mirror the language and context of the JD.", "agent": "Semantic Agent"})
        return {
            "overall_score": round(total_score, 1),
            "suggestions": suggestions,
        }

# ─────────────────────────────────────────────
# INSTANTIATE AGENTS
# ─────────────────────────────────────────────
AGENTS = [
    SemanticSimilarityAgent("Semantic Similarity", "🔮", "TF-IDF cosine similarity between resume & JD"),
    TechSkillsAgent("Tech Skills Matcher", "⚙️", "Extracts and matches technical skills"),
    SoftSkillsAgent("Soft Skills Analyst", "🤝", "Evaluates interpersonal skill alignment"),
    ExperienceAgent("Experience Evaluator", "📅", "Compares years of experience"),
    EducationAgent("Education Checker", "🎓", "Validates degree and academic fit"),
    KeywordDensityAgent("Keyword Density", "🔑", "TF-IDF keyword extraction & coverage"),
    CertificationAgent("Certification Analyst", "🏅", "Matches certifications to requirements"),
    ATSQualityAgent("ATS Quality Guard", "🛡️", "Evaluates resume ATS-readiness"),
    RoleAlignmentAgent("Role Alignment", "🎯", "Checks career trajectory fit"),
    RecommendationAgent("Recommendation Engine", "🧠", "Synthesizes all agent outputs"),
]

# ─────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">⚡ 10-Agent NLP Pipeline · TF-IDF Powered</div>
  <div class="hero-title">RecruitIQ<br>AI Resume Screener</div>
  <div class="hero-sub">
    Upload your resume and the job description. Our multi-agent NLP system will analyze 
    compatibility across 9 dimensions and tell you exactly where you stand.
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AGENT PIPELINE VIZ
# ─────────────────────────────────────────────
chips_html = ""
for i, agent in enumerate(AGENTS):
    chips_html += f'<div class="agent-chip" id="chip-{i}">{agent.icon} {agent.name}</div>'
    if i < len(AGENTS) - 1:
        chips_html += '<div class="agent-arrow">→</div>'

st.markdown(f"""
<div class="pipeline-container">
  <div class="pipeline-title">Agent Pipeline</div>
  <div class="agents-grid">{chips_html}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────
st.markdown('<div class="main-content">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("""
    <div class="upload-section">
      <div class="upload-label">📄 Resume</div>
      <div class="upload-hint">Paste your complete resume text below</div>
    </div>
    """, unsafe_allow_html=True)
    resume_text = st.text_area(
        "Resume Text",
        height=320,
        placeholder="Paste your resume here...\n\nInclude: Work Experience, Education, Skills, Projects, Certifications...",
        label_visibility="collapsed",
        key="resume_input"
    )

with col2:
    st.markdown("""
    <div class="upload-section">
      <div class="upload-label">💼 Job Description</div>
      <div class="upload-hint">Paste the complete job description below</div>
    </div>
    """, unsafe_allow_html=True)
    jd_text = st.text_area(
        "Job Description",
        height=320,
        placeholder="Paste the job description here...\n\nInclude: Role, Requirements, Responsibilities, Qualifications...",
        label_visibility="collapsed",
        key="jd_input"
    )

st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze_btn = st.button("🚀 Analyze with 10 Agents", use_container_width=True)

# ─────────────────────────────────────────────
# ANALYSIS ENGINE
# ─────────────────────────────────────────────
if analyze_btn:
    if not resume_text.strip() or not jd_text.strip():
        st.error("⚠️ Please paste both your resume and the job description to proceed.")
    else:
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        progress_placeholder = st.empty()
        status_placeholder = st.empty()

        agent_results = []
        agent_labels = [
            "Semantic Similarity Agent analyzing text vectors...",
            "Tech Skills Agent scanning skill stack...",
            "Soft Skills Agent evaluating interpersonal fit...",
            "Experience Evaluator calculating tenure gap...",
            "Education Checker validating academic credentials...",
            "Keyword Density Agent computing TF-IDF coverage...",
            "Certification Analyst scanning credentials...",
            "ATS Quality Guard auditing resume structure...",
            "Role Alignment Agent mapping career trajectory...",
            "Recommendation Engine synthesizing insights...",
        ]

        prog_bar = progress_placeholder.progress(0)
        for i, (agent, label) in enumerate(zip(AGENTS[:-1], agent_labels[:-1])):
            status_placeholder.markdown(f"<p style='color:var(--text-muted);font-size:14px;text-align:center;'>🔄 {label}</p>", unsafe_allow_html=True)
            result = agent.analyze(resume_text, jd_text)
            agent_results.append(result)
            time.sleep(0.2)
            prog_bar.progress((i + 1) / 10)

        status_placeholder.markdown(f"<p style='color:var(--text-muted);font-size:14px;text-align:center;'>🧠 {agent_labels[-1]}</p>", unsafe_allow_html=True)
        rec_agent = AGENTS[-1]
        final = rec_agent.synthesize(agent_results)
        prog_bar.progress(1.0)
        time.sleep(0.3)
        progress_placeholder.empty()
        status_placeholder.empty()

        overall = final['overall_score']
        suggestions = final['suggestions']

        # ─── VERDICT ────────────────────────────────
        if overall >= 70:
            verdict_class = "hired"
            verdict_emoji = "🎯"
            verdict_title = "Strong Candidate!"
            verdict_sub = "Your profile aligns well with this role. You have a strong chance of moving forward."
            verdict_color = "var(--success)"
        elif overall >= 50:
            verdict_class = "borderline"
            verdict_emoji = "⚡"
            verdict_title = "Borderline Match"
            verdict_sub = "You're competitive but gaps exist. Address the suggestions below to significantly improve your odds."
            verdict_color = "var(--warning)"
        else:
            verdict_class = "rejected"
            verdict_emoji = "🔧"
            verdict_title = "Needs Improvement"
            verdict_sub = "Significant gaps found. Use the AI suggestions below to re-align your resume before applying."
            verdict_color = "var(--danger)"

        st.markdown(f"""
        <div class="verdict-card {verdict_class}">
          <span class="verdict-emoji">{verdict_emoji}</span>
          <div class="verdict-title" style="color:{verdict_color}">{verdict_title}</div>
          <div class="verdict-sub">{verdict_sub}</div>
          <div style="font-family:'Syne',sans-serif;font-size:4rem;font-weight:800;color:{verdict_color};margin-top:24px;">{overall}%</div>
          <div style="font-size:13px;color:var(--text-muted);letter-spacing:1px;text-transform:uppercase;">Overall Match Score</div>
        </div>
        """, unsafe_allow_html=True)

        # ─── METRIC GRID ────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        tech_score = agent_results[1].get('score', 0)
        sem_score = agent_results[0].get('score', 0)
        exp_years = agent_results[3].get('resume_years', 0)
        skill_count = len(agent_results[1].get('matched', []))

        with m1:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="color:var(--accent)">{tech_score}%</div>
              <div class="metric-label">Tech Skills</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="color:var(--accent2)">{sem_score}%</div>
              <div class="metric-label">Semantic Fit</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="color:var(--accent3)">{exp_years}yr</div>
              <div class="metric-label">Experience</div>
            </div>""", unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="color:var(--accent4)">{skill_count}</div>
              <div class="metric-label">Skills Matched</div>
            </div>""", unsafe_allow_html=True)

        # ─── AGENT DETAILS ─────────────────────────
        st.markdown('<div class="section-header">🤖 Agent Analysis Breakdown</div>', unsafe_allow_html=True)

        agent_display_config = [
            {"icon": "🔮", "color": "#7c6bff"},
            {"icon": "⚙️", "color": "#00d4aa"},
            {"icon": "🤝", "color": "#ff6b9d"},
            {"icon": "📅", "color": "#ffb347"},
            {"icon": "🎓", "color": "#64b5f6"},
            {"icon": "🔑", "color": "#ce93d8"},
            {"icon": "🏅", "color": "#80cbc4"},
            {"icon": "🛡️", "color": "#ef9a9a"},
            {"icon": "🎯", "color": "#a5d6a7"},
        ]

        col_left, col_right = st.columns(2, gap="large")
        for idx, (res, agent, cfg) in enumerate(zip(agent_results, AGENTS[:-1], agent_display_config)):
            score = res.get('score', 0)
            label = res.get('label', agent.name)
            detail = res.get('details', '')
            score_class = "score-high" if score >= 70 else "score-med" if score >= 45 else "score-low"
            bar_color = "#00d4aa" if score >= 70 else "#ffb347" if score >= 45 else "#ff4d6d"

            html = f"""
            <div class="agent-result">
              <div class="agent-result-header">
                <div class="agent-name">{cfg['icon']} {label}</div>
                <span class="agent-score-badge {score_class}">{score}%</span>
              </div>
              <div class="prog-bar-container">
                <div class="prog-bar-track">
                  <div class="prog-bar-fill" style="width:{score}%;background:{bar_color};"></div>
                </div>
              </div>
              <div style="font-size:13px;color:var(--text-muted);margin-top:8px;">{detail}</div>
            """

            # Extra details per agent
            if 'matched' in res and idx == 1:  # Tech skills
                if res.get('matched'):
                    html += '<div class="skill-tags">'
                    for sk in res['matched'][:6]:
                        html += f'<span class="skill-tag skill-match">✓ {sk}</span>'
                    html += '</div>'
                if res.get('missing'):
                    html += '<div class="skill-tags" style="margin-top:6px;">'
                    for sk in res['missing'][:4]:
                        html += f'<span class="skill-tag skill-miss">✗ {sk}</span>'
                    html += '</div>'

            if idx == 5 and res.get('found'):  # Keywords
                html += '<div class="skill-tags" style="margin-top:8px;">'
                for kw in res['found'][:6]:
                    html += f'<span class="skill-tag skill-match">✓ {kw}</span>'
                for kw in res.get('missing', [])[:3]:
                    html += f'<span class="skill-tag skill-miss">✗ {kw}</span>'
                html += '</div>'

            html += '</div>'

            if idx % 2 == 0:
                with col_left:
                    st.markdown(html, unsafe_allow_html=True)
            else:
                with col_right:
                    st.markdown(html, unsafe_allow_html=True)

        # ─── SUGGESTIONS ───────────────────────────
        if suggestions:
            st.markdown('<div class="section-header">💡 AI-Powered Improvement Suggestions</div>', unsafe_allow_html=True)

            priority_order = {"critical": 0, "medium": 1, "low": 2}
            sorted_suggestions = sorted(suggestions, key=lambda x: priority_order.get(x['priority'], 3))

            for i, sug in enumerate(sorted_suggestions[:12]):
                p = sug['priority']
                color = {"critical": "var(--danger)", "medium": "var(--warning)", "low": "var(--accent3)"}.get(p, "var(--accent)")
                label = {"critical": "🔴 Critical", "medium": "🟡 Medium Priority", "low": "🟢 Nice to Have"}.get(p, p)
                st.markdown(f"""
                <div class="suggestion-card {p}">
                  <div class="suggestion-priority" style="color:{color}">{label} · {sug.get('agent','')}</div>
                  {sug['text']}
                </div>
                """, unsafe_allow_html=True)

        # ─── KEYWORD ANALYSIS ──────────────────────
        st.markdown('<div class="section-header">📊 Keyword Intelligence</div>', unsafe_allow_html=True)
        kw_col1, kw_col2 = st.columns(2, gap="large")

        with kw_col1:
            st.markdown("""
            <div class="agent-result">
              <div class="agent-name" style="margin-bottom:12px;">🏷️ Top JD Keywords</div>
            """, unsafe_allow_html=True)
            jd_kws = extract_keywords_tfidf(jd_text, 15)
            st.markdown('<div class="kw-cloud">', unsafe_allow_html=True)
            for i, kw in enumerate(jd_kws):
                cls = "high" if i < 5 else "med" if i < 10 else ""
                st.markdown(f'<span class="kw-chip {cls}">{kw}</span>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        with kw_col2:
            st.markdown("""
            <div class="agent-result">
              <div class="agent-name" style="margin-bottom:12px;">📋 Top Resume Keywords</div>
            """, unsafe_allow_html=True)
            res_kws = extract_keywords_tfidf(resume_text, 15)
            st.markdown('<div class="kw-cloud">', unsafe_allow_html=True)
            for i, kw in enumerate(res_kws):
                cls = "high" if i < 5 else "med" if i < 10 else ""
                st.markdown(f'<span class="kw-chip {cls}">{kw}</span>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        # ─── FINAL SUMMARY TABLE ───────────────────
        st.markdown('<div class="section-header">📋 Agent Score Summary</div>', unsafe_allow_html=True)
        summary_html = """
        <div class="agent-result">
        <table style="width:100%;border-collapse:collapse;font-size:14px;">
          <thead>
            <tr style="border-bottom:1px solid var(--border);">
              <th style="text-align:left;padding:10px;color:var(--text-muted);">Agent</th>
              <th style="text-align:center;padding:10px;color:var(--text-muted);">Score</th>
              <th style="text-align:left;padding:10px;color:var(--text-muted);">Status</th>
            </tr>
          </thead>
          <tbody>
        """
        for res, agent, cfg in zip(agent_results, AGENTS[:-1], agent_display_config):
            s = res.get('score', 0)
            status = "✅ Pass" if s >= 70 else "⚠️ Needs Work" if s >= 45 else "❌ Gap"
            color = "var(--success)" if s >= 70 else "var(--warning)" if s >= 45 else "var(--danger)"
            summary_html += f"""
            <tr style="border-bottom:1px solid var(--border);">
              <td style="padding:10px;">{cfg['icon']} {agent.name}</td>
              <td style="text-align:center;padding:10px;font-family:'JetBrains Mono',monospace;font-weight:700;color:{color};">{s}%</td>
              <td style="padding:10px;color:{color};">{status}</td>
            </tr>"""
        summary_html += f"""
          </tbody>
        </table>
        <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;">
          <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem;">🏆 Overall Match Score</span>
          <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.5rem;color:{verdict_color};">{overall}%</span>
        </div>
        </div>
        """
        st.markdown(summary_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
