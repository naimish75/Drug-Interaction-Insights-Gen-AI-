import os
import xml.etree.ElementTree as ET
import json
from datetime import datetime

def parse_drug_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {'hl7': 'urn:hl7-org:v3'}

        drug_info = {}

        # Extract drug name
        drug_name = root.find(".//hl7:name", ns)
        if drug_name is not None:
            drug_info["name"] = drug_name.text.strip()

        # Extract manufacturer
        manufacturer = root.find(".//hl7:representedOrganization/hl7:name", ns)
        if manufacturer is not None:
            drug_info["manufacturer"] = manufacturer.text.strip()

        # Extract brand name and medicine name
        manufactured_product = root.find(".//hl7:manufacturedProduct", ns)
        if manufactured_product is not None:
            brand_name = manufactured_product.find(".//hl7:name", ns)
            if brand_name is not None:
                drug_info["medicine_name"] = brand_name.text.strip()
            # Medicine name is the same as brand name in this case
            # drug_info["medicine_name"] = drug_info.get("brand_name", "N/A")
        
        # Extract active ingredients
        active_ingredients = []
        for ingredient in root.findall(".//hl7:ingredient", ns):
            substance = ingredient.find(".//hl7:name", ns)
            quantity = ingredient.find(".//hl7:quantity/hl7:numerator", ns)
            if substance is not None:
                active_ingredients.append({
                    "name": substance.text.strip(),
                    "quantity": {
                        "value": quantity.get("value") if quantity is not None else "N/A",
                        "unit": quantity.get("unit") if quantity is not None else "N/A"
                    }
                })
        drug_info["active_ingredients"] = active_ingredients

        # Extract sections and their content
        sections = {}
        for section in root.findall(".//hl7:section", ns):
            code = section.find("hl7:code", ns)
            text = section.find("hl7:text", ns)

            if code is not None and text is not None:
                display_name = code.get("displayName", "Unknown Section")
                paragraphs = [p.text.strip() for p in text.findall("hl7:paragraph", ns) if p.text]
                sections[display_name] = paragraphs if paragraphs else "No content available"

        drug_info["sections"] = sections
        return drug_info

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None


def process_xml_folder(folder_path, output_json_path):
    all_drug_data = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xml"):
            file_path = os.path.join(folder_path, file_name)
            parsed_data = parse_drug_xml(file_path)

            if parsed_data:
                all_drug_data.append({
                    "file_name": file_name,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "drug": parsed_data,
                    "metadata": {
                        "extraction_status": "complete",
                        "source": "FDA SPL Resources"
                    }
                })
            else:
                print(f"No data extracted from the XML file: {file_name}")

    # Save all extracted data to a single JSON file
    with open(output_json_path, "w") as json_file:
        json.dump(all_drug_data, json_file, indent=4)
    print(f"All drug information saved to {output_json_path}")

# Example usage
input_folder = "File_path"
output_folder = "File_apth"
process_xml_folder(input_folder, output_folder)
