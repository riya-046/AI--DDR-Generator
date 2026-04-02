import streamlit as st
import fitz
import re

st.title("AI DDR Report Generator")

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def format_ddr(thermal_text):
    temps = re.findall(r"\d+\.?\d*", thermal_text)
    temps = [float(t) for t in temps if float(t) < 100]

    if temps:
        max_temp = max(temps)
        min_temp = min(temps)
        diff = max_temp - min_temp
    else:
        max_temp = min_temp = diff = 0

    report = f"""
DETAILED DIAGNOSTIC REPORT (DDR)

Temperature Range: {min_temp}°C to {max_temp}°C
Variation: {diff}°C

Observation:
Temperature variation suggests possible moisture or insulation issues.

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