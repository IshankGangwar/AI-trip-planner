import streamlit as st
from trip_backend import run_trip_planner
import re
import base64
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ------------------ Static Background ------------------
def set_static_background(image_path="images/bg1.jpg"):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ------------------ PDF Generator ------------------
def generate_pdf(itinerary_text, title="Trip Itinerary"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, title)
    c.setFont("Helvetica", 12)
    y = height - 80
    for line in itinerary_text.splitlines():
        if not line.strip():
            y -= 12
            continue
        for chunk in [line[i : i + 90] for i in range(0, len(line), 90)]:
            c.drawString(50, y, chunk)
            y -= 14
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 50
    c.save()
    buffer.seek(0)
    return buffer


# ------------------ Custom Styling ------------------
st.markdown(
    """
<style>
div[data-baseweb="form-control"] label {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #000 !important;
    margin-bottom: 12px !important;
    display: block !important;
}
.stTextInput input,
.stNumberInput input {
    font-size: 1.3rem !important;
    color: #fff !important;
}
h1 {
    font-size: 4.2rem !important;
    font-weight: 900 !important;
    color: #000 !important;
    margin-bottom: 1rem !important;
}
p {
    font-size: 1.5rem !important;
    color: #000 !important;
}
.stMarkdown, .st-expanderContent p, .st-expanderContent li,
.stMarkdown ul li, .stMarkdown ol li, .stMarkdown strong {
    font-size: 1.6rem !important;
    color: black !important;
    line-height: 2 !important;
}
.stSpinner > div > div {
    color: black !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
}
.stAlert-success {
    background-color: rgba(200, 255, 200, 0.9) !important;
    color: #111 !important;
    font-weight: bold !important;
    font-size: 1.5rem !important;
}
.stDownloadButton button {
    color: white !important;
    background-color: #2196F3 !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    padding: 0.5rem 1rem !important;
    margin-top: 0.5rem !important;
}
.stDownloadButton button:nth-child(2) {
    background-color: #9C27B0 !important;
    margin-top: 0.5rem !important;
}
.stDownloadButton button:hover {
    opacity: 0.9 !important;
    transform: scale(1.02) !important;
    transition: all 0.2s ease !important;
}
.stButton > button {
    background-color: #2196F3 !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    padding: 0.5rem 1rem !important;
    border-radius: 6px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    outline: none !important;
}
.stButton > button:hover {
    background-color: #1976D2 !important;
    transform: scale(1.02);
    outline: none !important;
    box-shadow: none !important;
}
#welcome-line {
    color: #a10303 !important;
}

</style>
""",
    unsafe_allow_html=True,
)

# ------------------ Page Config ------------------
st.set_page_config(page_title="AI Trip Planner", page_icon="👛", layout="wide")
set_static_background()

# ------------------ Header ------------------
st.markdown(
    """
<div style='text-align: center; margin-bottom: 2rem;'>
  <span style='font-size: 4rem; font-weight: 900; color: #732a32;'>AI Trip Planner</span>
  <span style='font-size: 1.5rem; color: #444;'> (Plan your dream trip using a local LLaMA-powered AI assistant!)</span>
</div>
""",
    unsafe_allow_html=True,
)

# ------------------ Layout ------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        """
    <h2 style='color:black; font-size: 2.5rem; margin-bottom: 1.5rem;'>Enter Your Trip Details</h2>
    """,
        unsafe_allow_html=True,
    )
    destination = st.text_input("🌍 Destination", placeholder="e.g., Tokyo")
    days = st.number_input("🔕 Number of Days", min_value=1, max_value=10)
    interests = st.text_input("🎯 Interests", placeholder="e.g., nature, culture, food")
    submitted = st.button("🗸️ Plan My Trip")

with col2:
    with st.container():
        if not submitted:
            st.markdown(
                """
                <div style='text-align: center; padding: 2rem;'>
                    <h2 style='color:#732a32; font-size: 2.2rem;'>✨ Welcome to AI Trip Planner</h2>
                   <p id="welcome-line" style="font-size: 1.3rem; color: #1fd7e0 !important; font-weight: 700;">Plan your perfect journey with just a few clicks.</p>
                    <img src='https://cdn-icons-png.flaticon.com/512/854/854894.png' width='120' style='margin-top:1rem;' />
                </div>
                """,
                unsafe_allow_html=True,
            )

        elif submitted:
            if not destination.strip() or not interests.strip():
                st.error("❌ Please fill in all fields before planning your trip.")
            elif not isinstance(days, int) or days < 1 or days > 10:
                st.error("❌ Number of days must be an integer between 1 and 10.")
            else:
                try:
                    with st.spinner("🧠 Crafting your perfect journey... hang tight!"):
                        final_result = run_trip_planner(
                            destination, int(days), interests
                        )

                    st.success("🎉 Your AI-Planned Trip Itinerary is Ready!")

                    st.markdown(
                        "<div style='margin-top:-10px; margin-bottom:20px;'></div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        """
                        <div style="text-align: center; font-size: 2.4rem; font-weight: 800; color: #000; margin-top: 1rem; margin-bottom: 2rem;">
                            ✈️ Final Optimized Itinerary
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    def extract_days(itinerary_text):
                        pattern = r"(Day\s*\d+:.*?)(?=(Day\s*\d+:|$))"
                        matches = re.findall(pattern, itinerary_text, re.DOTALL)
                        if matches:
                            return [m[0].strip() for m in matches]
                        else:
                            return [f"Day 1:\n{itinerary_text.strip()}"]

                    days_output = extract_days(final_result)

                    if days_output:
                        extra_sections_to_render = []

                        for day in days_output:
                            day_title = day.splitlines()[0]
                            day_body = day.splitlines()[1:]

                            main_lines = []
                            current_section = None
                            section_buffer = []

                            for line in day_body:
                                if line.strip().startswith(
                                    "**"
                                ) and line.strip().endswith("**"):
                                    if current_section:
                                        extra_sections_to_render.append(
                                            (current_section, section_buffer)
                                        )
                                    current_section = line.strip("*").strip()
                                    section_buffer = []
                                elif current_section:
                                    section_buffer.append(line)
                                else:
                                    main_lines.append(line)

                            if current_section:
                                extra_sections_to_render.append(
                                    (current_section, section_buffer)
                                )

                            # Render Day card
                            full_content = f"""
                            <div style="
                                background: rgba(255, 255, 255, 0.15);
                                backdrop-filter: blur(14px);
                                -webkit-backdrop-filter: blur(14px);
                                border-radius: 20px;
                                border: 1px solid rgba(255, 255, 255, 0.25);
                                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                                padding: 25px 30px;
                                margin-bottom: 30px;
                            ">
                            <h3 style="font-size: 2rem; font-weight: 700; color: #192ac2; margin-bottom: 1rem;">🗓️ {day_title}</h3>
                            """

                            for line in main_lines:
                                if line.strip().startswith("* Morning:"):
                                    full_content += f"<p><strong>🌅 Morning {line.split(':', 1)[1].strip()}</strong></p>"
                                elif line.strip().startswith("* Afternoon:"):
                                    full_content += f"<p><strong>🏙️ Afternoon {line.split(':', 1)[1].strip()}</strong></p>"
                                elif line.strip().startswith("* Lunch:"):
                                    full_content += f"<p><strong>🍽️ Lunch {line.split(':', 1)[1].strip()}</strong></p>"
                                elif line.strip().startswith("* Evening:"):
                                    full_content += f"<p><strong>🌆 Evening {line.split(':', 1)[1].strip()}</strong></p>"
                                elif line.strip():
                                    full_content += (
                                        f"<p><strong>{line.strip()}</strong></p>"
                                    )

                            full_content += "</div>"
                            st.markdown(full_content, unsafe_allow_html=True)

                        # ✅ Now render extra sections (AFTER all days)
                        for title, content_lines in extra_sections_to_render:
                            extra_card = f"""
                            <div style="
                                background: rgba(255, 255, 255, 0.15);
                                backdrop-filter: blur(14px);
                                -webkit-backdrop-filter: blur(14px);
                                border-radius: 20px;
                                border: 1px solid rgba(255, 255, 255, 0.25);
                                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                                padding: 25px 30px;
                                margin-bottom: 30px;
                            ">
                            <h3 style="font-size: 1.6rem; font-weight: 700; color: #192ac2; margin-bottom: 1rem;">{title}</h3>
                            """

                            for line in content_lines:
                                if line.strip():
                                    extra_card += (
                                        f"<p><strong>{line.strip()}</strong></p>"
                                    )

                            extra_card += "</div>"
                            st.markdown(extra_card, unsafe_allow_html=True)

                    else:
                        st.markdown(final_result)

                    st.balloons()

                    # ✅ Center the single PDF download button
                    st.markdown(
                        "<div style='text-align: center;'>", unsafe_allow_html=True
                    )
                    file_name_pdf = (
                        f"{destination.lower().replace(' ', '_')}_trip_plan.pdf"
                    )
                    pdf_data = generate_pdf(
                        final_result, title=f"{destination.title()} Trip Itinerary"
                    )
                    st.download_button(
                        label="📄 Download as PDF",
                        data=pdf_data,
                        file_name=file_name_pdf,
                        mime="application/pdf",
                        use_container_width=False,
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Oops! Something went wrong: {e}")
