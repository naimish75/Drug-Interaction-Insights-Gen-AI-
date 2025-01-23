import streamlit as st
import pandas as pd
import json
from transformers import pipeline
from unidecode import unidecode

# Load JSON data
@st.cache_data
def load_interaction_data():
    try:
        with open("File_path", "r") as f:  # Adjusted path to match the uploaded file structure
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error("JSON file not found. Please ensure 'Drug_Info.Json' exists.")
        return []

# Summarizer model
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

# Find a drug by medicine name
def find_drug_by_name(name, interaction_data):
    normalized_name = unidecode(name.strip().lower())  # Normalize input drug name
    for drug_entry in interaction_data:
        drug = drug_entry.get("drug", {})  # Access the nested 'drug' key safely
        if unidecode(drug.get("medicine_name", "").strip().lower()) == normalized_name:
            return drug
    return None

# Analyze interactions
def analyze_interactions(existing_meds, new_med, interaction_data):
    interactions = []
    new_med_lower = new_med.lower()  # Normalize case for matching

    # Find the new medication in the dataset
    new_drug = find_drug_by_name(new_med, interaction_data)
    if not new_drug:
        st.write(f"New medication '{new_med}' not found in data.")
        return interactions

    # Iterate through existing medications to find interactions
    for med in existing_meds:
        med_lower = med.lower()  # Normalize case for matching
        if med_lower == new_med_lower:
            continue  # Skip self-matching

        existing_drug = find_drug_by_name(med, interaction_data)
        if not existing_drug:
            st.write(f"Existing medication '{med}' not found in data.")
            continue

        for ingredient in existing_drug.get("active_ingredients", []):
            for new_ingredient in new_drug.get("active_ingredients", []):
                # st.write(f"Comparing {ingredient['name']} with {new_ingredient['name']}")
                if ingredient["name"].lower() == new_ingredient["name"].lower():
                    interactions.append({
                        "Existing Medicine": med,
                        "New Medicine": new_med,
                        "Ingredient": ingredient["name"],
                        "Interaction": f"Potential overlap of {ingredient['name']}.",
                        "Severity": "Moderate"  # Set dynamically if needed
                    })
    return interactions

# Summarize interactions
def summarize_interactions(interactions, summarizer):
    summaries = []
    for interaction in interactions:
        interaction_text = (f"Interaction between {interaction['Existing Medicine']} and {interaction['New Medicine']}: "
                            f"{interaction['Interaction']} Severity: {interaction['Severity']}.")
        summary = summarizer(interaction_text, max_length=50, min_length=10, do_sample=False)
        summaries.append({
            "Drugs": f"{interaction['Existing Medicine']} + {interaction['New Medicine']}",
            "Summary": summary[0]['summary_text']
        })
    return summaries

# Style severity with color
def severity_badge(severity):
    if severity == "High":
        return '<span style="color:red; font-weight:bold;">High</span>'
    elif severity == "Moderate":
        return '<span style="color:orange; font-weight:bold;">Moderate</span>'
    elif severity == "Low":
        return '<span style="color:green; font-weight:bold;">Low</span>'
    return severity

# Main app
def main():
    st.title("Enhanced Drug Interaction Checker")
    st.write("Input your current medications and a new medication to check for potential interactions.")

    # Load data
    interaction_data = load_interaction_data()
    summarizer = load_summarizer()

    # User input
    existing_meds = st.text_area("Enter your current medications (one per line):").splitlines()
    new_med = st.text_input("Enter the new medication you want to check:")

    if st.button("Check Interactions"):
        if existing_meds and new_med:
            interactions = analyze_interactions(existing_meds, new_med, interaction_data)

            if interactions:
                # Display interaction table
                st.write("### Potential Drug Interactions")
                df = pd.DataFrame(interactions)
                st.dataframe(df)

                # Display summarized insights with styling
                st.write("### Summarized Insights")
                summaries = summarize_interactions(interactions, summarizer)
                for summary in summaries:
                    st.markdown(f"**{summary['Drugs']}**")
                    st.write(summary["Summary"])
            else:
                st.success("No significant interactions detected. It seems safe to proceed.")
        else:
            st.error("Please enter both existing medications and the new medication.")

if __name__ == "__main__":
    main()
