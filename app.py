import streamlit as st
import plotly.express as px
import base64

# Load EcoCampus logo for HTML rendering
with open("assets/ecocampus_app_icon.png", "rb") as image_file:
    logo_base64 = base64.b64encode(image_file.read()).decode()

from calculator import calculate_footprint
from ai_advisor import generate_recommendations
from firebase import save_record, get_history

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="EcoCampus",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "results" not in st.session_state:
    st.session_state["results"] = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #f7fbf7 0%,
        #ffffff 55%,
        #f2f8f3 100%
    );
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1250px;
}

/* MAIN CONTENT TEXT */

.main {
    color: #1f2937 !important;
}

.main p {
    color: #4b5563 !important;
}

.main h1,
.main h2,
.main h3,
.main h4 {
    color: #173d27 !important;
}

.main [data-testid="stMarkdownContainer"] {
    color: #1f2937 !important;
}

.main [data-testid="stMarkdownContainer"] p {
    color: #4b5563 !important;
}

.main [data-testid="stCaptionContainer"] {
    color: #66736a !important;
}

.main label {
    color: #374151 !important;
}
}


/* SIDEBAR */
/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #10251a !important;
}

section[data-testid="stSidebar"] > div {
    background-color: #10251a !important;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #b8c8bd !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
}

section[data-testid="stSidebar"] .stRadio label {
    padding: 0.35rem 0;
}


/* HERO */

.hero {
    padding: 2.8rem 3rem;
    border-radius: 24px;
    background: linear-gradient(
        135deg,
        #173d27 0%,
        #27663f 55%,
        #3f8056 100%
    );
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 15px 40px rgba(25, 70, 40, 0.15);
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    margin-bottom: 0.4rem;
}

.hero-subtitle {
    font-size: 1.15rem;
    opacity: 0.9;
}

.hero-description {
    font-size: 1rem;
    max-width: 720px;
    margin-top: 1.2rem;
    opacity: 0.85;
    line-height: 1.6;
}


/* SECTION */

.section-title {
    font-size: 1.8rem;
    font-weight: 750;
    margin-bottom: 0.25rem;
}

.section-description {
    color: #66736a;
    margin-bottom: 1.5rem;
}


/* FEATURE CARDS */

.feature-card {
    background: white;
    border: 1px solid #e3ebe5;
    border-radius: 18px;
    padding: 1.5rem;
    min-height: 175px;
    box-shadow: 0 5px 20px rgba(20, 50, 30, 0.05);
}

.feature-icon {
    font-size: 2rem;
    margin-bottom: 0.6rem;
}

.feature-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #173d27;
    margin-bottom: 0.4rem;
}

.feature-text {
    color: #68756c;
    font-size: 0.92rem;
    line-height: 1.5;
}


/* TOTAL CARD */

.total-card {
    background: linear-gradient(
        135deg,
        #e6f5e9,
        #f6fbf7
    );
    border: 1px solid #cde4d2;
    border-radius: 20px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.5rem;
}

.total-label {
    color: #52705b;
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.total-value {
    font-size: 2.5rem;
    font-weight: 800;
    color: #173d27;
    margin-top: 0.25rem;
}


/* EMISSION CARDS */

.emission-card {
    background: white;
    border-radius: 16px;
    border: 1px solid #e5ebe6;
    padding: 1rem;
    text-align: center;
    min-height: 115px;
    box-shadow: 0 4px 15px rgba(20, 50, 30, 0.04);
}

.emission-icon {
    font-size: 1.5rem;
}

.emission-name {
    font-size: 0.8rem;
    color: #6b776f;
    margin-top: 0.25rem;
}

.emission-value {
    font-size: 1.25rem;
    font-weight: 750;
    color: #183d27;
    margin-top: 0.2rem;
}


/* INFO BOX */

.info-box {
    background: #eef7f0;
    border-left: 4px solid #3d8055;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #36513e;
    margin: 1rem 0;
}


/* BUTTONS */

.stButton > button {
    border-radius: 10px;
    font-weight: 650;
    padding: 0.6rem 1rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.image(
    "assets/ecocampus_app_icon.png",
    width=85
)

st.sidebar.markdown(
    """
    <div style="
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 0.3rem;
        margin-bottom: 0.2rem;
        color: white;
    ">
        EcoCampus
    </div>

    <div style="
        font-size: 0.85rem;
        opacity: 0.75;
        margin-bottom: 1.5rem;
        color: white;
    ">
        Measure. Reduce. Sustain.
    </div>
    """,
    unsafe_allow_html=True
)



st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "📊 Calculate",
        "🤖 AI Advisor",
        "📉 Simulator",
        "📚 Methodology"
    ]
)

st.sidebar.divider()

st.sidebar.caption("Campus Carbon Management")
st.sidebar.caption("Prototype • 2026")


# ============================================================
# CHART
# ============================================================

def show_emission_chart(results):

    chart_data = {
        "Category": [
            "Electricity",
            "Petrol",
            "Diesel",
            "Composted Waste",
            "Landfill Waste"
        ],
        "Emissions": [
            results["electricity"],
            results["petrol"],
            results["diesel"],
            results["composted_waste"],
            results["landfill_waste"]
        ]
    }

    # EcoCampus color palette
    eco_colors = [
        "#7CC957",   # Fresh Green
        "#27663F",   # Nature Green
        "#0B4F3A",   # Deep Green
        "#8B5E3C",   # Earth Brown
        "#B7DDB9"    # Soft Green
    ]

    fig = px.pie(
        chart_data,
        names="Category",
        values="Emissions",
        hole=0.62,
        color_discrete_sequence=eco_colors
    )

    fig.update_traces(
        textinfo="percent",
        textfont_size=13,
        hovertemplate=(
            "<b>%{label}</b><br>"
            "%{value:,.2f} kg CO₂e<br>"
            "%{percent}<extra></extra>"
        ),
        marker=dict(
            line=dict(
                color="white",
                width=3
            )
        )
    )

    # Total in the center of the donut
    fig.add_annotation(
        x=0.5,
        y=0.5,
        text=(
            f"<b>{results['total']:,.0f}</b>"
            "<br><span style='font-size:12px'>kg CO₂e</span>"
        ),
        showarrow=False,
        font=dict(
            size=20,
            color="#173D27"
        )
    )

    fig.update_layout(
        title=dict(
    text="Emission Sources",
    font=dict(
        size=22,
        color="#173D27"
    ),
    x=0.02,
    xanchor="left"
),

        margin=dict(
            t=70,
            b=50,
            l=20,
            r=20
        ),

        height=520,

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.05,
            xanchor="center",
            x=0.5,
            font=dict(
                size=12,
                color="#52635A"
            )
        ),

        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_color="#173D27"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
def get_logo_base64():
    with open("assets/ecocampus_app_icon.png", "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    logo_base64 = get_logo_base64()

    st.html(f"""
        <div class="hero">

            <div style="
                display: flex;
                align-items: center;
                gap: 1.5rem;
            ">

                <img
                    src="data:image/png;base64,{logo_base64}"
                    style="
                        width: 100px;
                        height: 100px;
                        object-fit: contain;
                        border-radius: 16px;
                    "
                >

                <div>

                    <div class="hero-title">
                        EcoCampus
                    </div>

                    <div class="hero-subtitle">
                        Measure. Reduce. Sustain.
                    </div>

                </div>

            </div>

            <div class="hero-description">
                A campus carbon management platform that transforms
                everyday activity data into actionable sustainability
                insights.
            </div>

        </div>
    """)

    st.html("""
        <div style="
            font-size: 1.8rem;
            font-weight: 750;
            color: #173d27;
            margin-top: 1.5rem;
            margin-bottom: 0.3rem;
        ">
            Campus Sustainability Dashboard
        </div>

        <div style="
            font-size: 1rem;
            color: #66736a;
            margin-bottom: 1.5rem;
        ">
            Understand your campus footprint and discover where
            the biggest opportunities for reduction lie.
        </div>
    """)

    results = st.session_state["results"]

    if results is None:

        st.html("""
            <div class="info-box">
                <b>Your sustainability journey starts here.</b><br>
                Enter your campus electricity, transportation and
                waste data to calculate your estimated carbon footprint.
            </div>
        """)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.html("""
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">Measure</div>
                    <div class="feature-text">
                        Calculate your campus carbon footprint using
                        activity data and emission factors.
                    </div>
                </div>
            """)

        with col2:
            st.html("""
                <div class="feature-card">
                    <div class="feature-icon">🤖</div>
                    <div class="feature-title">Understand</div>
                    <div class="feature-text">
                        Use AI to identify major emission sources and
                        generate practical sustainability recommendations.
                    </div>
                </div>
            """)

        with col3:
            st.html("""
                <div class="feature-card">
                    <div class="feature-icon">📉</div>
                    <div class="feature-title">Reduce</div>
                    <div class="feature-text">
                        Explore reduction scenarios and understand
                        how sustainability actions can affect emissions.
                    </div>
                </div>
            """)

    else:

        st.html(f"""
            <div class="total-card">
                <div class="total-label">
                    Total Estimated Carbon Footprint
                </div>
                <div class="total-value">
                    {results['total']:,.2f}
                    <span style="font-size:1.1rem;">kg CO₂e</span>
                </div>
            </div>
        """)

        st.markdown("### Emission Breakdown")

        col1, col2, col3, col4, col5 = st.columns(5)

        cards = [
            ("⚡", "Electricity", results["electricity"]),
            ("⛽", "Petrol", results["petrol"]),
            ("🛢️", "Diesel", results["diesel"]),
            ("♻️", "Composted", results["composted_waste"]),
            ("🗑️", "Landfill", results["landfill_waste"])
        ]

        for column, (icon, name, value) in zip(
            [col1, col2, col3, col4, col5],
            cards
        ):

            with column:

                st.html(f"""
                    <div class="emission-card">
                        <div class="emission-icon">{icon}</div>
                        <div class="emission-name">{name}</div>
                        <div class="emission-value">
                            {value:,.0f} kg
                        </div>
                    </div>
                """)

        show_emission_chart(results)


# ============================================================
# CALCULATE
# ============================================================

elif page == "📊 Calculate":

    st.markdown("## 📊 Calculate Footprint")

    st.caption(
        "Enter your campus activity data for the selected month."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### ⚡ Energy")

        electricity = st.number_input(
            "Monthly electricity consumption (kWh)",
            min_value=0.0,
            value=0.0,
            step=100.0
        )

        st.markdown("### 🚗 Transportation")

        petrol = st.number_input(
            "Petrol consumption (litres)",
            min_value=0.0,
            value=0.0,
            step=10.0
        )

        diesel = st.number_input(
            "Diesel consumption (litres)",
            min_value=0.0,
            value=0.0,
            step=10.0
        )

    with col2:

        st.markdown("### ♻️ Waste")

        composted_waste = st.number_input(
            "Organic waste composted (kg)",
            min_value=0.0,
            value=0.0,
            step=10.0
        )

        landfill_waste = st.number_input(
            "Organic waste sent to landfill (kg)",
            min_value=0.0,
            value=0.0,
            step=10.0
        )

        st.html("""
            <div class="info-box">
                <b>Tip:</b> Use monthly campus-level activity data
                for the most useful estimate.
            </div>
        """)

    st.write("")

    if st.button(
        "🌍 Calculate Carbon Footprint",
        type="primary",
        use_container_width=True
    ):

        results = calculate_footprint(
            electricity,
            petrol,
            diesel,
            composted_waste,
            landfill_waste
        )

        st.session_state["results"] = results

        inputs = {
            "electricity_kwh": electricity,
            "petrol_litres": petrol,
            "diesel_litres": diesel,
            "composted_waste_kg": composted_waste,
            "landfill_waste_kg": landfill_waste
        }

        save_record(results, inputs)

        st.success("Footprint calculated successfully! 🌱")

        st.html(f"""
            <div class="total-card">
                <div class="total-label">
                    Estimated Monthly Footprint
                </div>
                <div class="total-value">
                    {results['total']:,.2f}
                    <span style="font-size:1.1rem;">kg CO₂e</span>
                </div>
            </div>
        """)

        show_emission_chart(results)

# ============================================================
# AI ADVISOR
# ============================================================

elif page == "🤖 AI Advisor":

    st.markdown(
        '<div class="section-title">🤖 AI Sustainability Advisor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Turn your carbon data into practical sustainability actions.'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state["results"] is None:

        st.info(
            "Calculate your campus footprint first to unlock "
            "sustainability recommendations."
        )

    else:

        results = st.session_state["results"]

        st.html(
    f"""
    <div class="total-card">

        <div class="total-label">
            Current Footprint
        </div>

        <div class="total-value">
            {results['total']:,.2f}
            <span style="font-size: 1.1rem;">
                kg CO₂e
            </span>
        </div>

    </div>
    """
)

        st.markdown(
            """
            <div class="info-box">
                <b>🌱 How it works</b><br>
                EcoCampus analyzes your emission profile,
                identifies the largest emission sources,
                and generates practical sustainability actions.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "✨ Analyze My Campus",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "🌱 Analyzing your campus footprint..."
            ):

                recommendations = generate_recommendations(results)

            st.session_state["recommendations"] = recommendations

        if "recommendations" in st.session_state:

            st.divider()

            st.markdown(
                '<div class="section-title">'
                '🌿 Sustainability Analysis'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                st.session_state["recommendations"]
            )


# ============================================================
# SIMULATOR
# ============================================================

elif page == "📉 Simulator":

    st.markdown("## 📉 What-if Simulator")

    st.caption(
        "Explore how sustainability improvements could change "
        "your campus footprint."
    )

    if st.session_state["results"] is None:

        st.info(
            "Calculate your current footprint first to use the simulator."
        )

    else:

        results = st.session_state["results"]

        electricity_reduction = st.slider(
            "⚡ Electricity reduction",
            0,
            100,
            0
        )

        transport_reduction = st.slider(
            "🚗 Transport reduction",
            0,
            100,
            0
        )

        waste_reduction = st.slider(
            "♻️ Waste reduction",
            0,
            100,
            0
        )

        electricity_saving = (
            results["electricity"]
            * electricity_reduction
            / 100
        )

        transport_saving = (
            (results["petrol"] + results["diesel"])
            * transport_reduction
            / 100
        )

        waste_saving = (
            (
                results["composted_waste"]
                + results["landfill_waste"]
            )
            * waste_reduction
            / 100
        )

        total_reduction = (
            electricity_saving
            + transport_saving
            + waste_saving
        )

        projected = results["total"] - total_reduction

        col1, col2 = st.columns(2)

        with col1:

            st.html(f"""
                <div class="total-card">
                    <div class="total-label">
                        Projected Footprint
                    </div>
                    <div class="total-value">
                        {projected:,.2f}
                        <span style="font-size:1rem;">kg CO₂e</span>
                    </div>
                </div>
            """)

        with col2:

            st.html(f"""
                <div class="total-card">
                    <div class="total-label">
                        Potential Reduction
                    </div>
                    <div class="total-value">
                        {total_reduction:,.2f}
                        <span style="font-size:1rem;">kg CO₂e</span>
                    </div>
                </div>
            """)


# ============================================================
# METHODOLOGY
# ============================================================

elif page == "📚 Methodology":

    st.markdown("## 📚 Methodology")

    st.caption(
        "How EcoCampus calculates estimated campus emissions."
    )

    st.html("""
        <div class="info-box">
            <b>Core equation</b><br><br>
            Emissions = Activity Data × Emission Factor
        </div>
    """)

    st.write(
        "Each emission source is calculated separately and the "
        "results are aggregated to estimate the campus footprint."
    )

    st.divider()

    st.subheader("Emission Factors")

    methodology_data = {
        "Category": [
            "Electricity",
            "Petrol",
            "Diesel",
            "Composted organic waste",
            "Landfilled organic waste"
        ],
        "Unit": [
            "kWh",
            "litres",
            "litres",
            "kg",
            "kg"
        ],
        "Factor (kg CO₂e/unit)": [
            "0.827",
            "2.27",
            "2.64",
            "0.32",
            "1.29"
        ]
    }

    st.table(methodology_data)

    st.divider()

    st.subheader("About the Calculation")

    st.write(
        "The prototype uses India-relevant emission factors from "
        "government and methodological references. Actual factors "
        "may vary depending on geography, reporting period and "
        "methodology."
    )

    st.info(
        "The carbon calculation is deterministic. AI is used for "
        "interpretation and recommendations rather than for "
        "inventing emission factors."
    )