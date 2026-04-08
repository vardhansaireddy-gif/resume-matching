# 🧠 RecruitIQ — AI Resume Screener

> **A 10-Agent NLP Pipeline for intelligent resume-to-job description matching.**  
> Built with Python · Streamlit · TF-IDF · Cosine Similarity · Zero external AI API

---

## Overview

RecruitIQ is an AI-powered resume screening application that analyses a candidate's resume against a Job Description across **9 analytical dimensions**, producing a weighted composite match score and prioritised improvement suggestions. The entire pipeline is self-contained — no OpenAI, no external APIs, no GPU required.

```
Resume Text ──┐
              ├──► 10-Agent NLP Pipeline ──► Overall Score + Suggestions
JD Text ──────┘
```

---

## Features

- **10-Agent pipeline** — 9 specialised NLP agents + 1 synthesis engine
- **TF-IDF cosine similarity** for semantic text matching
- **Technical skills matching** across 60+ technologies
- **Soft skills analysis** across 23 interpersonal traits
- **Experience gap detection** via regex pattern extraction
- **Education level comparison** with degree rank hierarchy
- **Keyword density analysis** — simulates ATS keyword scanning
- **Certification matching** across 15+ credential types
- **ATS quality audit** — structure, length, action verbs, contact info
- **Role alignment detection** across 8 career domain families
- **AI-powered improvement suggestions** ranked Critical / Medium / Low
- **Dark-theme responsive UI** with real-time progress visualisation
- **Zero data transmission** — 100% local processing, privacy-first

---

## Quick Start

### Prerequisites

```bash
python >= 3.8
pip install streamlit
```

### Run the Application

```bash
# Clone or copy app11.py to your working directory
streamlit run app11.py
```

The application will open at `http://localhost:8501` in your default browser.

### Usage

1. **Paste your resume** into the left text area (plain text)
2. **Paste the job description** into the right text area
3. Click **"🚀 Analyze with 10 Agents"**
4. Review your scores, verdict, and improvement suggestions

---

## The 10-Agent Pipeline

| # | Agent | Icon | Weight | Description |
|---|-------|------|--------|-------------|
| 1 | Semantic Similarity | 🔮 | 20% | TF-IDF cosine similarity across unigrams + bigrams |
| 2 | Tech Skills Matcher | ⚙️ | 22% | Regex matching against 60+ technical skill patterns |
| 3 | Soft Skills Analyst | 🤝 | 8% | Interpersonal skill detection against 23 traits |
| 4 | Experience Evaluator | 📅 | 15% | Years-of-experience gap detection and scoring |
| 5 | Education Checker | 🎓 | 8% | Degree rank hierarchy matching (Diploma→Masters→PhD) |
| 6 | Keyword Density | 🔑 | 10% | JD top-25 keyword coverage check (ATS simulation) |
| 7 | Certification Analyst | 🏅 | 5% | 15+ certification type matching |
| 8 | ATS Quality Guard | 🛡️ | 7% | Resume structure, length, contact info, action verbs |
| 9 | Role Alignment | 🎯 | 5% | Career domain family matching across 8 role types |
| 10 | Recommendation Engine | 🧠 | — | Synthesises all 9 scores + generates suggestions |

**Total weight:** 100%

---

## Scoring & Verdict

| Overall Score | Verdict | Meaning |
|--------------|---------|---------|
| ≥ 70% | 🎯 Strong Candidate | Strong alignment — good chance of proceeding |
| 50–69% | ⚡ Borderline Match | Competitive but gaps exist — improvements recommended |
| < 50% | 🔧 Needs Improvement | Significant gaps — resume should be revised before applying |

---

## NLP Algorithms

### TF-IDF Vectorisation

```
TF(t, d) = count(t in d) / |d|
IDF(t)   = log((N + 1) / (df(t) + 1)) + 1   [Laplace smoothed]
TF-IDF   = TF × IDF
```

### Cosine Similarity

```
similarity = (R · J) / (|R| × |J|)
           = Σ(r_i × j_i) / (√Σr_i²  ×  √Σj_i²)
```

### Skill Extraction

```python
pattern = r'\b' + re.escape(skill) + r'\b'
# Word-boundary anchors prevent partial matches
# "rust" will NOT match "trust"
```

---

## Project Structure

```
app11.py                    ← Main application (single-file)
├── GLOBAL CSS              ← Custom dark-theme CSS injected via st.markdown()
├── NLP UTILITIES           ← clean_text(), tokenize(), compute_tfidf(), cosine_similarity()
├── TECH_SKILLS list        ← 60+ technical skill patterns
├── SOFT_SKILLS list        ← 23 soft skill patterns
├── Agent (base class)      ← Abstract analyze(resume, jd) → dict
├── SemanticSimilarityAgent ← Agent 1
├── TechSkillsAgent         ← Agent 2
├── SoftSkillsAgent         ← Agent 3
├── ExperienceAgent         ← Agent 4
├── EducationAgent          ← Agent 5
├── KeywordDensityAgent     ← Agent 6
├── CertificationAgent      ← Agent 7
├── ATSQualityAgent         ← Agent 8
├── RoleAlignmentAgent      ← Agent 9
├── RecommendationAgent     ← Agent 10 (synthesis)
├── AGENTS list             ← All 10 agents instantiated
├── HERO SECTION            ← UI header
├── AGENT PIPELINE VIZ      ← Chip row showing pipeline
├── INPUT SECTION           ← Text area widgets
└── ANALYSIS ENGINE         ← Orchestration loop + result rendering
```

---

## Agent Output Format

Every Agent 1–9 returns a dict with at minimum:

```python
{
    "score":   float,   # 0–100 normalised score
    "label":   str,     # Human-readable dimension name
    "details": str,     # One-sentence explanation
    # Agent-specific fields below...
}
```

Agent 10 (Recommendation Engine) returns:

```python
{
    "overall_score": float,      # Weighted composite score
    "suggestions":  list[dict],  # [{"priority": "critical"|"medium"|"low", "text": str, "agent": str}]
}
```

---

## Design System

The UI uses a CSS custom property design token system:

| Variable | Value | Usage |
|----------|-------|-------|
| `--bg` | `#0a0a0f` | Page background |
| `--surface` | `#12121a` | Card background |
| `--accent` | `#7c6bff` | Primary purple |
| `--accent2` | `#ff6b9d` | Pink highlight |
| `--accent3` | `#00d4aa` | Success / pass (teal) |
| `--accent4` | `#ffb347` | Warning (amber) |
| `--danger` | `#ff4d6d` | Fail / critical (red) |

**Typography:**
- `Space Grotesk` — body text
- `Syne` — headings and titles
- `JetBrains Mono` — scores, numbers, code

---

## Configuration & Defaults

### Edge Case Defaults

| Situation | Agent | Default Score |
|-----------|-------|--------------|
| No tech skills in JD | Agent 2 | 50% |
| No experience requirement in JD | Agent 4 | 75% |
| No education requirement in JD | Agent 5 | 80% |
| No certifications required | Agent 7 | 70% |
| No role family detected in JD | Agent 9 | 65% |

### Tuning the Weights

To change the scoring weights, edit the `weights` dict in `RecommendationAgent.synthesize()`:

```python
weights = {
    'semantic':       0.20,   # ← adjust these
    'tech_skills':    0.22,
    'soft_skills':    0.08,
    'experience':     0.15,
    'education':      0.08,
    'keywords':       0.10,
    'certification':  0.05,
    'ats':            0.07,
    'role':           0.05,   # must sum to 1.0
}
```

### Adding a New Skill

Add entries to `TECH_SKILLS` or `SOFT_SKILLS` lists at the top of the file:

```python
TECH_SKILLS = [
    ...
    'your_new_skill',   # ← add here (lowercase)
]
```

### Adding a New Agent

1. Subclass `Agent` and implement `analyze(self, resume, jd) → dict`
2. Append an instance to the `AGENTS` list
3. Add a weight key in `RecommendationAgent.synthesize()`
4. Add display config in `agent_display_config`

---

## Performance

| Operation | Complexity | Typical Runtime |
|-----------|-----------|-----------------|
| Text preprocessing | O(n) | < 1ms |
| TF-IDF computation | O(V) | < 5ms |
| Skill extraction (60 skills) | O(n × S) | < 10ms |
| All 9 agents combined | O(n × S + V) | < 50ms |
| Full UX (with progress delays) | — | ~2.5 seconds |

*n = word count, V = vocabulary size, S = skill list size*

---

## Known Limitations

- **Plain text only** — PDF/DOCX resume upload requires external text extraction
- **English only** — multilingual support not implemented
- **Explicit experience claims** — candidates who don't mention years receive 0
- **Keyword matching** — cannot infer synonyms (e.g., "React.js" ≠ "ReactJS" unless both are in the list)
- **Soft skills are buzzword-based** — cannot detect genuine demonstrated skills from context
- **Bag-of-words model** — word order and deep semantics are partially lost

---

## Security & Privacy

- ✅ No resume data is transmitted externally
- ✅ No persistent storage — all processing is in-memory
- ✅ No user authentication or tracking
- ✅ No analytics or telemetry
- ⚠️ In production, deploy behind HTTPS
- ⚠️ Consider adding input length limits to prevent memory exhaustion

---

## Roadmap

**Phase 1 (1–3 months)**
- [ ] PDF/DOCX upload support
- [ ] Bulk analysis & candidate ranking
- [ ] PDF export of analysis report
- [ ] Multi-language support

**Phase 2 (3–6 months)**
- [ ] SBERT/sentence-transformer embeddings (optional premium mode)
- [ ] Named Entity Recognition for title/company detection
- [ ] Saved analysis history
- [ ] Recruiter leaderboard mode

**Phase 3 (6–12 months)**
- [ ] ATS API integrations (Greenhouse, Lever, Workday)
- [ ] LLM-powered resume rewriting assistant
- [ ] Anonymisation / bias-blind screening mode
- [ ] Enterprise SSO & RBAC

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-agent`)
3. Add your agent class implementing the `Agent` base interface
4. Ensure the output dict includes at minimum `score`, `label`, `details`
5. Add a weight in `RecommendationAgent.synthesize()`
6. Open a pull request with a description of the new dimension being measured

---

## License

This project is provided for educational and internal use. See `LICENSE` for details.

---

## Acknowledgements

Built with Streamlit

Click to open web application [Streamlit](https://resume-matcher-ai-e8xa99qwbkrexmmybc5icr.streamlit.app/)
---

*RecruitIQ — Making resume screening transparent, fast, and actionable.*
