import streamlit as st
import pandas as pd
import numpy as np
import random
import altair as alt

# --- 1. APP CONFIG & THEMING ---
st.set_page_config(
    page_title="Caprae AI-Score Lead Prioritizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    body { font-family: 'Inter', sans-serif; }
    .st-emotion-cache-p5mknv { padding: 2rem 2rem 10rem 2rem;}
    .stButton>button {border-radius:0.5rem; padding:0.5rem 1rem;font-weight:600;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA AND SCORING LOGIC ---
def calculate_cais(row):
    pain_score, readiness_score = 0, 0
    if 'manual' in row['Keywords'] or 'spreadsheet' in row['Keywords']:
        pain_score += 15
    if 'old CMS' in row['Tech Stack'] or 'legacy ERP' in row['Tech Stack']:
        pain_score += 10
    if 'basic website' in row['Tech Stack'] and row['Estimated Traffic'] < 5000:
        pain_score += 15
    if row['Estimated Traffic'] > 100000:
        readiness_score += 35
    elif row['Estimated Traffic'] > 10000:
        readiness_score += 25
    if 'Salesforce' in row['Tech Stack'] or 'Hubspot' in row['Tech Stack']:
        readiness_score += 15
    elif 'Google Analytics' in row['Tech Stack']:
        readiness_score += 5
    pain_score = min(pain_score, 50)
    readiness_score = min(readiness_score, 50)
    cais = int(pain_score + readiness_score)
    return cais, pain_score, readiness_score

def get_insights(cais, pain_score, readiness_score):
    if cais >= 75:
        summary = "HIGH FIT: Major scale + clear operational pain. Target fast AI integration for ROI."
    elif cais >= 50:
        summary = f"MEDIUM FIT: Some transformation headroom. Focus on pain point ({pain_score}/50)."
    else:
        summary = "LOW FIT: Minimal visible opportunity. Reassess in future."
    return cais, None, summary, pain_score, readiness_score

def load_mock_data():
    np.random.seed(42)
    random.seed(42)
    prefixes = ['Stream', 'Summit', 'Quick', 'Pioneer', 'BlueRidge', 'Global', 'Apex', 'Nova', 'Eco', 'Data',
                'Prime', 'Zenith', 'Verde', 'Iron', 'Digital']
    suffixes = ['Tech', 'Analytics', 'Solutions', 'Holdings', 'Consulting', 'Labs', 'Makers', 'Services',
                'Systems', 'Group', 'Ventures', 'Corp', 'Logistics', 'Retail', 'Software']
    techs = [
        'old CMS, custom billing, Google Analytics','legacy ERP, no CRM, basic website',
        'modern stack, Salesforce, custom BI','Excel-based, old CMS, minimal tech',
        'basic website, local tools','Salesforce, modern stack, Tableau',
        'modern stack, custom billing, HubSpot','Shopify, Google Analytics',
        'SharePoint, SAP, no modern BI','Custom Python backend, AWS, Redis',
        'MERN stack, no dedicated marketing automation','G Suite only, no formal project management tool'
    ]
    ranges = [(100,5000),(10000,90000),(100000,500000)]
    keywords = [
        'manual reporting, high growth','spreadsheet accounting, complex logistics',
        'digital transformation, AI-ready','outdated processes, high volume',
        'local service, simple','AI, market leader, scale',
        'custom needs, fast scaling','B2C, digital marketing',
        'complex data, manual reporting','B2B sales focused',
        'high compliance needs','global supply chain'
    ]
    rows = []
    for i in range(150):
        company = random.choice(prefixes)+' '+random.choice(suffixes)
        website = company.lower().replace(' ','').replace('g','x')+random.choice(['.com','.net','.io'])
        tech_stack = random.choice(techs)
        traffic = random.randint(*random.choice(ranges))
        keyword_subset = random.sample(keywords, k=random.randint(2,4))
        keywords_str = ', '.join(keyword_subset)
        first = random.choice(['John', 'Jane', 'Alex', 'Sarah', 'Mike', 'Emily', 'Chris', 'Pat', 'Jamie'])
        last = random.choice(list('ABCDEFGHIJKL'))
        email = f"{first.lower()}_{last.lower()}@{website.split('.')[0]}.com"
        company_size = random.choice(['10-50','51-200','201-500','500+'])
        funding = random.choice(['Seed','Series A','Series B','Growth','Bootstrapped'])
        rows.append({
            'Company':company,'Website':website,'Tech Stack':tech_stack,'Estimated Traffic':traffic,
            'Keywords':keywords_str,'Contact Name':f"{first} {last}.",'Email':email,
            'Company Size': company_size, 'Funding Stage': funding
        })
    df = pd.DataFrame(rows)
    scores = df.apply(lambda row:get_insights(*calculate_cais(row)),axis=1,result_type='expand')
    scores.columns=['CAIS','CAIS_HTML','AI-Actionable Insight','Pain Point Score','Readiness Score']
    df = pd.concat([df,scores.drop(columns=['CAIS_HTML'])],axis=1)
    df = df.sort_values('CAIS',ascending=False).reset_index(drop=True)
    return df

df_leads = load_mock_data()

# --- 3. CONTROLS & FILTERS ---
st.title("Caprae AI-Score Lead Prioritizer 🚀")
st.markdown("### Pinpoint high-value targets for post-acquisition AI-driven transformation.")

col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    min_cais = st.slider('Minimum CAIS Score',0,100,75,5,help="Show highest AI transformation fits.")

with col2:
    keyword_filter = st.multiselect('Filter by Keywords',
        options=list(set([kw for tpl in df_leads['Keywords'].str.split(',') for kw in tpl])),
        default=[]
    )

with col3:
    size_filter = st.multiselect('Company Size',
        options=df_leads['Company Size'].unique().tolist(),
        default=[]
    )

with col4:
    funding_filter = st.multiselect('Funding Stage',
        options=df_leads['Funding Stage'].unique().tolist(),
        default=[]
    )

df_filtered = df_leads[df_leads['CAIS']>=min_cais]
if keyword_filter:
    df_filtered = df_filtered[df_filtered['Keywords'].apply(lambda x:any(kw in x for kw in keyword_filter))]
if size_filter:
    df_filtered = df_filtered[df_filtered['Company Size'].isin(size_filter)]
if funding_filter:
    df_filtered = df_filtered[df_filtered['Funding Stage'].isin(funding_filter)]

st.markdown(f"**Showing {len(df_filtered)} / {len(df_leads)} Qualified Leads**")
st.divider()

# --- 4. EXPORT BUTTONS ---
col_exp1, col_exp2 = st.columns(2)
with col_exp1:
    st.subheader("Export Leads")
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("Download as CSV",csv,"caprae_filtered_leads.csv","text/csv")
with col_exp2:
    json_export = df_filtered.to_json(orient='records')
    st.download_button("Download as JSON",json_export,"caprae_filtered_leads.json","application/json")

# --- 5. MAIN TABLE and DETAILED INSIGHT ---
def display_table(df):
    display_df = df[['CAIS','Company','Website','AI-Actionable Insight','Estimated Traffic',
                     'Tech Stack','Contact Name','Email','Company Size','Funding Stage']].copy()
    display_df = display_df.rename(columns={'AI-Actionable Insight':'AI Insight','Estimated Traffic':'Traffic (Est.)','Contact Name':'Contact'})
    st.dataframe(display_df,hide_index=True,use_container_width=True)

if len(df_filtered)>0:
    display_table(df_filtered)
    st.markdown("---")
    st.subheader("Lead Scoring Breakdown")
    company_options = df_filtered['Company'].tolist()
    selected_company = st.selectbox('Select a company for in-depth analysis:',company_options)
    selected_lead = df_filtered[df_filtered['Company']==selected_company].iloc[0]
    cols_ins = st.columns([1,1,1,2])
    with cols_ins[0]:
        st.metric("Pain Point (0-50)",selected_lead['Pain Point Score'],"Why it needs change")
    with cols_ins[1]:
        st.metric("Readiness (0-50)",selected_lead['Readiness Score'],"Capacity to adopt AI")
    with cols_ins[2]:
        st.metric("Total Score",selected_lead['CAIS'],"Transformation fit")
    with cols_ins[3]:
        st.info(f"**Strategy**\n\n{selected_lead['AI-Actionable Insight']}\n\n**Key Data:** {selected_lead['Website']} | {selected_lead['Email']}")

    # --- 6. DATA VISUALIZATIONS ---
    # CAIS distribution histogram
    hist_chart = alt.Chart(df_filtered).mark_bar().encode(
        alt.X('CAIS:Q', bin=alt.Bin(maxbins=20), title='Caprae AI-Score'),
        y='count()',
        tooltip=['CAIS']
    ).properties(width=350,height=250)
    st.altair_chart(hist_chart,use_container_width=True)

    # Pie chart: Funding stage
    pie_funding = df_filtered['Funding Stage'].value_counts().reset_index()
    pie_funding.columns=['Funding Stage','Count']
    pie_chart = alt.Chart(pie_funding).mark_arc().encode(
        theta=alt.Theta(field="Count",type="quantitative"),
        color=alt.Color(field="Funding Stage",type="nominal"),
        tooltip=['Funding Stage','Count']
    ).properties(width=250,height=250)
    st.altair_chart(pie_chart,use_container_width=True)

    # Bar chart: Company Size counts
    size_counts = df_filtered['Company Size'].value_counts().reset_index()
    size_counts.columns=['Company Size','Count']
    size_chart = alt.Chart(size_counts).mark_bar().encode(
        x=alt.X('Company Size',type='nominal'),
        y=alt.Y('Count',type='quantitative'),
        color=alt.Color('Company Size',type='nominal'),
        tooltip=['Company Size','Count']
    ).properties(width=350,height=250)
    st.altair_chart(size_chart,use_container_width=True)

else:
    st.warning("No leads match current filters. Try relaxing your criteria.")

# --- 7. BUSINESS UNDERSTANDING (Sidebar) ---
st.sidebar.title("Submission Documentation")
st.sidebar.markdown("---")
st.sidebar.header("Challenge Rationale")
st.sidebar.markdown("""
**CAIS Lead Prioritizer** shifts lead gen from raw collection to actionable prioritization.
Top scoring leads reveal greatest likely ROI for post-acquisition AI-driven transformation, directly aligning with Caprae’s value-creation strategy.
""")
st.sidebar.header("Caprae Capital's Mission")
st.sidebar.markdown("""
Caprae Capital’s mission is to transcend traditional financial engineering, acting as a strategic, long-term partner in growing businesses after acquisition. The firm guides companies through a seven-year journey, using practical AI solutions and operational initiatives to unlock sustained value and turn good companies into great ones.
""")
st.sidebar.header("Caprae’s Impact on ETA/PE")
st.sidebar.markdown("""
Caprae is fundamentally changing the ETA and PE space by treating M&A as a long-term value-building service, not just a transaction. It institutionalizes transformation through AI readiness, scalable SaaS, and a repeatable operational playbook—making post-acquisition growth both systematic and accessible.
""")
st.sidebar.markdown("---")
st.sidebar.markdown("*(Made by Kasi)*")
