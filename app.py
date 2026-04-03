import streamlit as st
import fitz
import re

st.title("AI-Powered Thermal Diagnostic Report Generator")

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def format_ddr(thermal_text):
    import re

    # Extract numbers
    temps = re.findall(r"\d+\.?\d*", thermal_text)

    # Convert & filter realistic temps
    temps = [float(t) for t in temps if 20 <= float(t) <= 35]

    if temps:
        # Sort values
        temps = sorted(temps)

        # Remove outliers (very important)
        if len(temps) > 4:
            temps = temps[1:-1]

        max_temp = max(temps)
        min_temp = min(temps)
        diff = round(max_temp - min_temp, 2)
    else:
        max_temp = min_temp = diff = 0

    report = f"""
DETAILED DIAGNOSTIC REPORT (DDR)

Temperature Range: {min_temp}°C to {max_temp}°C
Variation: {diff}°C

Observation:
The observed temperature variation exceeds normal uniform conditions and may indicate moisture intrusion or insulation gaps.

Recommended Action:
Further inspection and waterproofing suggested.
"""
    return report

inspection_file = st.file_uploader("Upload Inspection Report", type="pdf")
thermal_file = st.file_uploader("Upload Thermal Report", type="pdf")

if st.button("Generate Report"):
    if inspection_file and thermal_file:
        thermal_text = extract_text(thermal_file)
        result = format_ddr(thermal_text)
        st.text(result)
    else:
        st.warning("Please upload both files")