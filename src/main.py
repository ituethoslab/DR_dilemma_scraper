import os
from scraper import (
    scraper_init,
    navigator,
    button_clicker,
    clicker_scroller,
    html_writer,
    cookie_handler,
)
from processor import html_opener, div_finder, dilemma_finder
from formatter_writer import (
    clean_text,
    save_to_csv,
    save_to_txt,
    save_to_json,
    prepare_json_data,
)

BUTTONS_TO_PUSH: list[str] = [
    "2023",
    "2022",
    "2021",
    "2020",
    "2019",
    "2018",
    # "TIDLIGERE", doesn't work and not worth it to try IMO
    "2024",
]  # ordered based on scrape logic, adjust accordingly
URL: str = "https://www.dr.dk/lyd/p4/sara-og-monopolet-podcast-1090358387000"
HTMLS_FOLDER: str = "/home/luisito/Development/dilemma_scraper/html_dumps/"
DATA_FOLDER: str = "/home/luisito/Development/dilemma_scraper/output_data/"
FILE_FORMAT: str = "csv"


def scrape_htmls(url: str, button: str, output_folder: str) -> None:
    """
    This function structures the logic of the scrape
    """
    driver = scraper_init()

    try:
        navigator(driver, url)
        cookie_handler(driver)
        button_clicker(driver, button)
        clicker_scroller(driver)
        html_writer(driver, output_folder, button)

    finally:
        driver.quit()


def process_html(filepath: str) -> list[str]:
    """
    Function to process the raw html dumps into lists containing the dilemmas
    """

    html_content = html_opener(filepath)
    description_divs = div_finder(html_content)
    dilemma_list = dilemma_finder(description_divs)

    return dilemma_list


def save_dilemmas(
    dilemma_list: list[str], file_format: str, data_directory: str, filename: str
) -> None:
    """
    Function to save processed dilemmas into the desired file format
    """

    cleaned_data = clean_text(dilemma_list)

    file_path = os.path.join(data_directory, filename)

    if file_format == "csv":
        save_to_csv(cleaned_data, file_path)
    elif file_format == "txt":
        save_to_txt(cleaned_data, file_path)
    elif file_format == "json":
        json_data = prepare_json_data(cleaned_data)
        save_to_json(json_data, file_path)
    else:
        print("Not a valid file format, choose between csv, txt, or json")


if __name__ == "__main__":
    # scraping each tab and dumping htmls
    for button in BUTTONS_TO_PUSH:
        scrape_htmls(URL, button, HTMLS_FOLDER)

    # processing and saving processed data
    for filename in os.listdir(HTMLS_FOLDER):
        full_file_path = os.path.join(HTMLS_FOLDER, filename)
        print(f"Processing {full_file_path}")
        dilemma_list = process_html(full_file_path)
        save_dilemmas(
            dilemma_list, FILE_FORMAT, DATA_FOLDER, f"dilemmas_{filename}.{FILE_FORMAT}"
        )
