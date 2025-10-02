# Caprae AI-Score Lead Prioritizer

## What is this project about?

This project is a powerful, easy-to-use web application built with Streamlit that helps sales and strategy teams prioritize their sales leads using a smart AI-based scoring system called the **Caprae AI-Score (CAIS)**.

Most lead generation tools simply collect data — they compile lists of leads with basic info but don’t tell you who to focus on first. This tool goes beyond that by analyzing each lead’s operational challenges and their readiness to adopt AI-driven transformation. It ranks leads according to their potential for delivering real, post-acquisition business value through AI.

By doing so, it helps Caprae Capital and other business users identify the highest-value opportunities efficiently, so sales efforts and strategic outreach are smart, targeted, and impactful.

---

## How does it work?

1. **Data Simulation and Loading:** For demonstration, it generates synthetic company lead data, including company characteristics, tech stacks, estimated web traffic, keywords describing pains and growth areas, contact info, funding stage, and company size.

2. **Scoring Leads with CAIS:** Each lead is scored on two main components:

   - **Pain Point Score:** Measures operational inefficiencies, like old software or manual processes that indicate urgent transformation needs.
  
   - **Readiness Score:** Assesses company scale and technological adoption levels, showing their ability and willingness to invest in AI solutions.

These two scores combine for the overall CAIS, a number from 0 to 100 indicating how attractive the lead is for AI-driven growth initiatives.

3. **Filtering and Exploration:** Users can filter leads by CAIS threshold, keywords, company size, and funding stage to easily narrow down the most promising targets.

4. **Detailed Lead Insights:** Selecting a company displays a breakdown of why it scored a certain way, helping sales teams tailor their approach and pitch appropriately.

5. **Data Export & Integration:** Filtered leads can be exported as CSV or JSON files ready to be imported into CRMs or other sales tools.

6. **Visual Analytics:** Interactive charts — including histograms of CAIS scores, pie charts for funding stages, and bar charts for company size distribution — give users a clear, high-level understanding of the lead portfolio landscape.

---

## Why is this important?

Caprae Capital’s mission is to transform businesses post-acquisition by emphasizing operational and technological upgrades rather than traditional financial engineering. This app embodies that paradigm by focusing on **AI readiness and transformation potential** rather than just raw data.

It transforms lead generation from a passive data exercise into a strategic activity, ensuring that sales efforts are focused on companies most likely to benefit from Caprae’s value-driven approach. It reduces wasted effort, highlights actionable insights, and aligns perfectly with modern private equity’s shift towards technology-enabled growth.

---

## Getting started

### Prerequisites
- Python 3.8 or above
- Recommended: a virtual environment tool such as `venv` or `conda`

### Installation

1. Clone this repository:
    ```
    git clone <your-repo-url>
    cd <repo-folder>
    ```

2. Create and activate a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate   # on Windows: venv\Scripts\activate
    ```

3. Install required packages:
    ```
    pip install -r requirements.txt
    ```

4. Run the Streamlit app:
    ```
    streamlit run app.py
    ```

Open your web browser and go to `http://localhost:8501` to interact with the app.

---

## How to use the app

- Adjust the sliders and filters on top to set your minimum CAIS score, select relevant keywords, company sizes, or funding stages.
- View the filtered list of leads ranked by CAIS.
- Click on any company to see its detailed AI readiness and transformation potential.
- Download filtered results anytime for CRM or reporting integration.
- Use the interactive charts to understand portfolio distribution and prioritize outreach strategy.

---

## Acknowledgments

This tool was built specifically for Caprae Capital’s AI-readiness pre-screening challenge. It reflects a blend of data engineering, user experience design, and strategic business understanding — all aimed at accelerating AI transformation in acquired companies.

*Created by Kasi*

---

## License

This project is open source and available under the MIT License.

