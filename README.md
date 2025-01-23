# Enhanced Drug Interaction Checker

## Overview
The **Enhanced Drug Interaction Checker** is a comprehensive AI-driven solution designed to analyze potential interactions between drugs. This project involves extracting drug data from DailyMed's publicly available resources, converting XML files to JSON, and leveraging this structured data to detect drug interactions using advanced models.

This repository contains scripts for:
- Extracting XML files from compressed archives.
- Converting XML files to JSON.
- Performing drug interaction analysis and generating summaries.

## Project Workflow

### 1. **Data Collection from DailyMed**
We utilized the publicly available **DailyMed SPL (Structured Product Labeling)** data as the primary source of drug information. The SPL data, provided in XML format, was downloaded and stored locally for processing.

### 2. **XML Extraction**
- **Script:** `XML_Extract.py`
- **Purpose:** Extract all XML files from compressed archives.
- **Key Functionality:**
  - The script scans the specified folder for `.zip` files.
  - It extracts only XML files and saves them into an `extracted_xmls` directory for further processing.

### 3. **XML to JSON Conversion**
- **Script:** `XMl-Json.py`
- **Purpose:** Convert the extracted XML files into a single JSON file for structured analysis.
- **Key Functionality:**
  - Parses XML files to extract key details such as drug names, manufacturers, active ingredients, and sections like warnings and dosage information.
  - Saves all processed data into a single JSON file for scalability and easy integration.

### 4. **Drug Interaction Analysis**
- **Script:** `Drug-Interaction.py`
- **Purpose:** Analyze potential drug interactions using the JSON file generated in the previous step.
- **Key Functionality:**
  - Allows users to input a list of current medications and a new drug.
  - Compares active ingredients across medications to identify overlaps or potential interactions.
  - Uses a summarization model (e.g., Facebook’s BART) to provide concise summaries of detected interactions.

## File Details

### 1. `XML_Extract.py`
- Extracts XML files from `.zip` archives located in the specified folder.
- Outputs: XML files stored in the `extracted_xmls` folder.

### 2. `XMl-Json.py`
- Converts extracted XML files into a single JSON file.
- Extracted information includes:
  - **Drug Name**
  - **Manufacturer**
  - **Active Ingredients** (name and quantity)
  - **Sections** like warnings, dosage instructions, and usage indications.
- Outputs: A consolidated JSON file.

### 3. `Drug-Interaction.py`
- Analyzes drug interactions using the processed JSON file.
- Key features:
  - Identifies overlapping active ingredients.
  - Summarizes interactions using AI-driven models.
  - Provides user-friendly insights and recommendations.

## Why JSON Instead of XML?
We’ve included the JSON file instead of the original XML data due to:
- **File Size Limitations**: The XML data files are significantly larger and less structured for direct use.
- **Efficiency**: JSON files allow faster access and integration into machine learning workflows.

## How to Use
1. **Run `XML_Extract.py`**: Extract XML files from the downloaded `.zip` archives.
2. **Run `XMl-Json.py`**: Convert the extracted XML files to JSON format.
3. **Run `Drug-Interaction.py`**: Use the JSON file to analyze potential drug interactions and generate insights.

## Data Source
- The drug information was sourced from **DailyMed**: [https://dailymed.nlm.nih.gov/](https://dailymed.nlm.nih.gov/)
- The SPL XML files were parsed and processed into JSON for this project.

## Collaboration
This project is a collaborative effort with **Eshaa Gogia**, and we’re proud to share this AI-driven tool for enhancing medication safety.

## Future Enhancements
- Adding support for real-time updates from DailyMed APIs.
- Expanding the scope to include more comprehensive drug interaction types.
- Integrating additional NLP models for more detailed insights.

---
We hope this project contributes to safer healthcare practices and better medication management. Feel free to explore the repository and reach out with any questions or suggestions!

