import re
import json
import csv


def clean_text(data: list[str]) -> list[str]:
    """
    Removes the numbering from the start of each string in the list.
    """
    cleaned_data = []
    for item in data:
        # Use regex to remove the leading number and any following punctuation or space
        cleaned_item = re.sub(r"^\d+\.\s*", "", item)
        cleaned_data.append(cleaned_item)

    return cleaned_data


def save_to_csv(data: list[str], file_name: str):
    """
    Saves a list of strings to a CSV file, one item per row.
    """
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow([row])


def save_to_txt(data: list[str], file_name: str):
    """
    Saves a list of strings to a TXT file, one item per line.
    """
    with open(file_name, "w", encoding="utf-8") as txtfile:
        for row in data:
            txtfile.write(f"{row}\n")


def save_to_json(data: list[dict[str, str]], file_name: str):
    """
    Saves a list of dictionaries (text and optional metadata) to a JSON file.
    JSON is preffered for vector database
    """
    with open(file_name, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)


def prepare_json_data(data: list[str]) -> list[dict[str, str]]:
    """
    Prepares the text data as a list of dictionaries for JSON export.
    """
    json_data = []
    for idx, text in enumerate(data, start=1):
        json_data.append(
            {
                "id": str(idx),
                "text": text,
                "metadata": {
                    "category": "General",  # You can replace or extend this metadata
                    "source": "ScrapedData",
                },
            }
        )
    return json_data
