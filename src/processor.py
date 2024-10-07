from bs4 import BeautifulSoup
from bs4.element import Tag


def html_opener(filepath: str) -> str:
    """
    Opens local htmls
    """

    with open(filepath, "r", encoding="utf-8") as file:
        html_content = file.read()

    return html_content


def div_finder(html_content: str) -> list[Tag]:
    """
    Finds the description of each episode
    """

    soup = BeautifulSoup(html_content, "html.parser")
    description_divs = soup.find_all(
        "div", class_=lambda x: x and x.startswith("Description_description_")
    )
    return description_divs


def dilemma_finder(divs: list[Tag]) -> list[str]:
    """
    Searches for dilemmas in the divs and extracts them
    """

    dilemma_list = []

    for element in divs:
        paragraphs = element.find_all("p")

        capture = False

        for paragraph in paragraphs:
            text = paragraph.get_text()
            if "Dilemmaliste" in text:
                capture = True
                continue
            if capture:
                dilemma_list.append(text)

    else:
        print("Description div not found.")

    print("Number of dilemmas " + str(len(dilemma_list)))
    return dilemma_list
