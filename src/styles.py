"""
MARKETIX Global Styles & Animated UI Components
Inject once per page for consistent branding and animations.
"""

GLOBAL_CSS = """
<style>
/* ═══════════════════════════════════════════
   FONTS & BASE
═══════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ═══════════════════════════════════════════
   ANIMATED GRADIENT HEADER BANNER
═══════════════════════════════════════════ */
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(99, 179, 237, 0.4); }
    50%       { box-shadow: 0 0 0 12px rgba(99, 179, 237, 0); }
}
@keyframes countUp {
    from { opacity: 0; transform: scale(0.8); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes shimmer {
    0%   { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}
@keyframes borderPulse {
    0%, 100% { border-color: rgba(59, 130, 246, 0.3); }
    50%       { border-color: rgba(59, 130, 246, 0.9); }
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
@keyframes floatUp {
    0%   { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes dotBounce {
    0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
    40%            { transform: scale(1.2); opacity: 1; }
}

/* ═══════════════════════════════════════════
   MAIN HEADER WITH ANIMATED GRADIENT
═══════════════════════════════════════════ */
.main-hero {
    background: linear-gradient(-45deg, #0F172A, #1E3A8A, #0D9488, #1E40AF);
    background-size: 400% 400%;
    animation: gradientShift 8s ease infinite;
    color: white;
    padding: 2.5rem 2.5rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.main-hero::before {
    content: "";
    position: absolute;
    top: -50%;
    right: -20%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
    border-radius: 50%;
}
.main-hero::after {
    content: "";
    position: absolute;
    bottom: -40%;
    left: -10%;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(13,148,136,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: -1px;
    margin: 0 0 0.3rem;
    animation: fadeSlideDown 0.6s ease both;
}
.hero-subtitle {
    font-size: 1.1rem;
    font-weight: 400;
    color: #93C5FD;
    margin: 0 0 1rem;
    animation: fadeSlideDown 0.7s ease both;
}
.hero-desc {
    font-size: 0.9rem;
    color: #CBD5E1;
    max-width: 800px;
    line-height: 1.6;
    animation: fadeSlideDown 0.8s ease both;
}
.hero-badges {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-top: 1.2rem;
    animation: fadeSlideUp 1s ease both;
}
.hero-badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #E2E8F0;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    backdrop-filter: blur(10px);
}

/* ═══════════════════════════════════════════
   ANIMATED KPI METRIC CARDS
═══════════════════════════════════════════ */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.2rem 1.2rem;
    text-align: center;
    border: 1px solid #EFF6FF;
    box-shadow: 0 4px 20px rgba(30,58,138,0.07);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    animation: floatUp 0.6s ease both;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 32px rgba(30,58,138,0.14);
}
.kpi-card:nth-child(1)::before { background: linear-gradient(90deg, #3B82F6, #1D4ED8); }
.kpi-card:nth-child(2)::before { background: linear-gradient(90deg, #0D9488, #0F766E); }
.kpi-card:nth-child(3)::before { background: linear-gradient(90deg, #8B5CF6, #6D28D9); }
.kpi-card:nth-child(4)::before { background: linear-gradient(90deg, #F59E0B, #D97706); }
.kpi-card:nth-child(5)::before { background: linear-gradient(90deg, #10B981, #059669); }
.kpi-card:nth-child(6)::before { background: linear-gradient(90deg, #EC4899, #BE185D); }
.kpi-icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
.kpi-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1;
    animation: countUp 0.5s ease both;
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B;
    margin-top: 0.3rem;
}
.kpi-delta {
    font-size: 0.7rem;
    color: #10B981;
    margin-top: 0.3rem;
    font-weight: 600;
}

/* Stagger animation delay for cards */
.kpi-card:nth-child(1) { animation-delay: 0.05s; }
.kpi-card:nth-child(2) { animation-delay: 0.10s; }
.kpi-card:nth-child(3) { animation-delay: 0.15s; }
.kpi-card:nth-child(4) { animation-delay: 0.20s; }
.kpi-card:nth-child(5) { animation-delay: 0.25s; }
.kpi-card:nth-child(6) { animation-delay: 0.30s; }

/* ═══════════════════════════════════════════
   PAGE SECTION HEADERS
═══════════════════════════════════════════ */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 1.5rem 0 0.8rem;
    animation: fadeSlideUp 0.5s ease both;
}
.section-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}
.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0;
}
.section-subtitle {
    font-size: 0.8rem;
    color: #64748B;
    margin: 0.1rem 0 0;
}

/* ═══════════════════════════════════════════
   STATUS BADGES (Sidebar)
═══════════════════════════════════════════ */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.9rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
}
.status-pill .dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    animation: pulseGlow 2s infinite;
}
.pill-success { background: #DCFCE7; color: #15803D; }
.pill-success .dot { background: #22C55E; }
.pill-warning { background: #FEF3C7; color: #92400E; }
.pill-warning .dot { background: #F59E0B; }
.pill-danger  { background: #FEE2E2; color: #991B1B; }
.pill-danger  .dot { background: #EF4444; }

/* ═══════════════════════════════════════════
   INSIGHT / RECOMMENDATION CARDS
═══════════════════════════════════════════ */
.insight-card {
    background: white;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    border-left: 4px solid #3B82F6;
    box-shadow: 0 2px 16px rgba(30,58,138,0.07);
    margin-bottom: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    animation: floatUp 0.5s ease both;
}
.insight-card:hover {
    transform: translateX(4px);
    box-shadow: 0 6px 24px rgba(30,58,138,0.12);
}
.insight-card.priority-high  { border-left-color: #EF4444; }
.insight-card.priority-medium { border-left-color: #F59E0B; }
.insight-card.priority-low   { border-left-color: #10B981; }

.insight-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.9rem;
}
.insight-title {
    font-size: 1rem;
    font-weight: 700;
    color: #0F172A;
}
.priority-badge {
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.priority-badge.high   { background: #FEE2E2; color: #991B1B; }
.priority-badge.medium { background: #FEF3C7; color: #92400E; }
.priority-badge.low    { background: #DCFCE7; color: #15803D; }

.insight-row {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    line-height: 1.5;
}
.insight-label {
    font-weight: 700;
    color: #475569;
    white-space: nowrap;
    min-width: 90px;
}
.insight-text { color: #334155; }

/* ═══════════════════════════════════════════
   PERSONA CARDS (Segmentation)
═══════════════════════════════════════════ */
.persona-card {
    background: linear-gradient(135deg, #fff 0%, #F8FAFC 100%);
    border-radius: 16px;
    padding: 1.4rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: floatUp 0.6s ease both;
    height: 100%;
}
.persona-card:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 16px 40px rgba(30,58,138,0.15);
}
.persona-emoji { font-size: 2.4rem; margin-bottom: 0.5rem; }
.persona-name  { font-size: 1rem; font-weight: 800; color: #0F172A; margin-bottom: 0.8rem; }
.persona-stat  { font-size: 0.8rem; color: #64748B; margin-bottom: 0.3rem; }
.persona-stat strong { color: #1E3A8A; }
.persona-strategy {
    background: #EFF6FF;
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    font-size: 0.75rem;
    color: #1E40AF;
    margin-top: 0.8rem;
    text-align: left;
    line-height: 1.4;
}

/* ═══════════════════════════════════════════
   PREDICTION RESULT CARD
═══════════════════════════════════════════ */
.pred-card {
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    animation: floatUp 0.5s ease both;
    position: relative;
    overflow: hidden;
}
.pred-card.positive {
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
    border: 2px solid #34D399;
}
.pred-card.negative {
    background: linear-gradient(135deg, #FEF2F2, #FEE2E2);
    border: 2px solid #F87171;
}
.pred-verdict { font-size: 1.5rem; font-weight: 800; margin: 0.5rem 0; }
.pred-pct { font-size: 3.5rem; font-weight: 900; line-height: 1; }
.pred-label { font-size: 0.85rem; color: #64748B; margin-top: 0.4rem; }

/* ═══════════════════════════════════════════
   PROGRESS BARS
═══════════════════════════════════════════ */
.animated-bar-wrap { margin: 0.5rem 0; }
.animated-bar-label {
    display: flex; justify-content: space-between;
    font-size: 0.8rem; color: #475569; margin-bottom: 0.25rem;
}
.animated-bar-bg {
    background: #E2E8F0;
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
}
.animated-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
    animation: growBar 1.2s ease both;
}
@keyframes growBar {
    from { width: 0 !important; }
}

/* ═══════════════════════════════════════════
   MODULE NAVIGATION CARDS (Home Page)
═══════════════════════════════════════════ */
.module-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}
.module-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.3rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    transition: all 0.25s ease;
    cursor: default;
    animation: floatUp 0.5s ease both;
}
.module-card:hover {
    border-color: #93C5FD;
    box-shadow: 0 8px 28px rgba(30,58,138,0.12);
    transform: translateY(-3px);
}
.module-num {
    font-size: 0.7rem;
    font-weight: 700;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.module-emoji { font-size: 1.6rem; margin: 0.3rem 0; }
.module-title { font-size: 0.9rem; font-weight: 700; color: #0F172A; }
.module-desc  { font-size: 0.75rem; color: #64748B; margin-top: 0.3rem; line-height: 1.4; }

/* Stagger cards */
.module-card:nth-child(1) { animation-delay: 0.05s; }
.module-card:nth-child(2) { animation-delay: 0.10s; }
.module-card:nth-child(3) { animation-delay: 0.15s; }
.module-card:nth-child(4) { animation-delay: 0.20s; }
.module-card:nth-child(5) { animation-delay: 0.25s; }
.module-card:nth-child(6) { animation-delay: 0.30s; }
.module-card:nth-child(7) { animation-delay: 0.35s; }
.module-card:nth-child(8) { animation-delay: 0.40s; }

/* ═══════════════════════════════════════════
   HEALTH STATUS ROWS (Sidebar & Dashboards)
═══════════════════════════════════════════ */
.health-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 0.9rem;
    border-radius: 10px;
    background: #FFFFFF;
    margin-bottom: 0.6rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.health-row:hover {
    transform: translateX(2px);
    box-shadow: 0 3px 8px rgba(0,0,0,0.06);
}
.health-dot {
    width: 9px; height: 9px;
    border-radius: 50%;
    flex-shrink: 0;
}
.health-dot.green  { background: #10B981; animation: pulseGlow 2s infinite; }
.health-dot.yellow { background: #F59E0B; animation: pulseGlow 2.5s infinite; }
.health-dot.red    { background: #EF4444; }
.health-info { flex: 1; }
.health-label { font-size: 0.8rem; font-weight: 700; color: #1E293B; }
.health-desc  { font-size: 0.72rem; color: #64748B; margin-top: 0.1rem; }
.health-value { font-size: 0.75rem; font-weight: 700; color: #1E3A8A; white-space: nowrap; }

/* ═══════════════════════════════════════════
   TABLE STYLING
═══════════════════════════════════════════ */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05) !important;
    animation: fadeSlideUp 0.5s ease both;
}

/* ═══════════════════════════════════════════
   CRISP MODERN LIGHT SIDEBAR
═══════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background-color: #F8FAFC !important;
    border-right: 1px solid #E2E8F0 !important;
}
section[data-testid="stSidebar"] > div:first-child {
    background-color: #F8FAFC !important;
    padding-top: 1.2rem;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stCaption p {
    color: #334155 !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #0F172A !important;
    font-weight: 800 !important;
}
section[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid #E2E8F0 !important;
    margin: 1rem 0 !important;
}

/* Streamlit Sidebar Navigation Links */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    padding-top: 0.5rem !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li a {
    color: #334155 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    padding: 0.45rem 0.75rem !important;
    transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li a:hover {
    background-color: #EDF2F7 !important;
    color: #1E3A8A !important;
    transform: translateX(3px) !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li a[aria-current="page"] {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important;
    color: #1E40AF !important;
    font-weight: 700 !important;
    border-left: 3px solid #3B82F6 !important;
    box-shadow: 0 1px 3px rgba(59, 130, 246, 0.12) !important;
}

/* ═══════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════ */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(30,58,138,0.2) !important;
}
div[data-testid="stMetric"] {
    animation: floatUp 0.6s ease both;
}

/* ═══════════════════════════════════════════
   LOADING SPINNER
═══════════════════════════════════════════ */
.mktx-spinner {
    display: flex; align-items: center; gap: 0.6rem;
    padding: 1rem; color: #64748B; font-size: 0.85rem; font-weight: 500;
}
.mktx-spinner-ring {
    width: 20px; height: 20px;
    border: 2px solid #E2E8F0;
    border-top-color: #3B82F6;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
}

/* ═══════════════════════════════════════════
   DIVIDER
═══════════════════════════════════════════ */
.mktx-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #CBD5E1, transparent);
    margin: 1.5rem 0;
    border: none;
}

/* ═══════════════════════════════════════════
   GENERAL STREAMLIT TWEAKS
═══════════════════════════════════════════ */
.block-container { padding-top: 1.5rem !important; }
header[data-testid="stHeader"] { background: transparent !important; }
</style>
"""


def _clean(html: str) -> str:
    """Flattens HTML into an unindented string to prevent Markdown from interpreting indentation as code blocks."""
    return " ".join(line.strip() for line in html.strip().splitlines() if line.strip())


def inject_styles():
    """Injects the full MARKETIX CSS into the Streamlit page."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def kpi_card(icon: str, value: str, label: str, delta: str = "") -> str:
    delta_html = f'<div class="kpi-delta">▲ {delta}</div>' if delta else ""
    return _clean(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>""")


def kpi_grid(*cards: str) -> str:
    return _clean(f'<div class="kpi-grid">{"".join(cards)}</div>')


def section_header(icon_html: str, title: str, subtitle: str = "", color: str = "#3B82F6") -> str:
    icon_bg = color + "20"
    return _clean(f"""
    <div class="section-header">
        <div class="section-icon" style="background:{icon_bg};">{icon_html}</div>
        <div>
            <div class="section-title">{title}</div>
            {"" if not subtitle else f'<div class="section-subtitle">{subtitle}</div>'}
        </div>
    </div>""")


def hero_banner(title: str, subtitle: str, description: str, badges: list[str]) -> str:
    badge_html = "".join(f'<span class="hero-badge">{b}</span>' for b in badges)
    return _clean(f"""
    <div class="main-hero">
        <div class="hero-title">{title}</div>
        <div class="hero-subtitle">{subtitle}</div>
        <div class="hero-desc">{description}</div>
        <div class="hero-badges">{badge_html}</div>
    </div>""")


def status_pill(label: str, kind: str = "success") -> str:
    return _clean(f"""
    <div class="status-pill pill-{kind}">
        <span class="dot"></span>
        {label}
    </div>""")


def health_row(dot_color: str, label: str, desc: str, value: str = "") -> str:
    return _clean(f"""
    <div class="health-row">
        <div class="health-dot {dot_color}"></div>
        <div class="health-info">
            <div class="health-label">{label}</div>
            <div class="health-desc">{desc}</div>
        </div>
        {"" if not value else f'<div class="health-value">{value}</div>'}
    </div>""")


def module_card(num: str, emoji: str, title: str, desc: str) -> str:
    return _clean(f"""
    <div class="module-card">
        <div class="module-num">Module {num}</div>
        <div class="module-emoji">{emoji}</div>
        <div class="module-title">{title}</div>
        <div class="module-desc">{desc}</div>
    </div>""")


def insight_card(title: str, finding: str, evidence: str, recommendation: str, impact: str, priority: str) -> str:
    prio_cls = priority.lower()
    return _clean(f"""
    <div class="insight-card priority-{prio_cls}">
        <div class="insight-header">
            <div class="insight-title">🎯 {title}</div>
            <span class="priority-badge {prio_cls}">{priority}</span>
        </div>
        <div class="insight-row">
            <span class="insight-label">🔍 Finding:</span>
            <span class="insight-text">{finding}</span>
        </div>
        <div class="insight-row">
            <span class="insight-label">📊 Evidence:</span>
            <span class="insight-text">{evidence}</span>
        </div>
        <div class="insight-row">
            <span class="insight-label">🎯 Action:</span>
            <span class="insight-text">{recommendation}</span>
        </div>
        <div class="insight-row">
            <span class="insight-label">🚀 Impact:</span>
            <span class="insight-text">{impact}</span>
        </div>
    </div>""")


def persona_card(emoji: str, name: str, size: int, income: float, spend: float, response_rate: float, strategy: str, delay: float = 0) -> str:
    return _clean(f"""
    <div class="persona-card" style="animation-delay:{delay}s">
        <div class="persona-emoji">{emoji}</div>
        <div class="persona-name">{name}</div>
        <div class="persona-stat">👥 <strong>{size:,}</strong> customers</div>
        <div class="persona-stat">💰 Avg Income: <strong>${income:,.0f}</strong></div>
        <div class="persona-stat">🛒 Avg Spend: <strong>${spend:,.0f}</strong></div>
        <div class="persona-stat">📈 Response Rate: <strong>{response_rate:.1f}%</strong></div>
        <div class="persona-strategy">💡 {strategy}</div>
    </div>""")


def animated_progress(label: str, pct: float, color: str = "#3B82F6") -> str:
    return _clean(f"""
    <div class="animated-bar-wrap">
        <div class="animated-bar-label">
            <span>{label}</span>
            <strong>{pct:.1f}%</strong>
        </div>
        <div class="animated-bar-bg">
            <div class="animated-bar-fill" style="width:{pct}%;background:{color};"></div>
        </div>
    </div>""")


def divider() -> str:
    return '<div class="mktx-divider"></div>'
