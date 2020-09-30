import os
from datetime import datetime

from weasyprint import HTML


dir_path = os.path.dirname(os.path.realpath(__file__))


def big_html_to_pdf():
    """
    This way of conervting a html page to pdf is not possible because
    of to much processing time.
    """
    start = datetime.now()
    html_path = f"{dir_path}/html/big_table.html"
    pdf_path = f"{dir_path}/build/big_table.pdf"
    HTML(html_path).write_pdf(pdf_path)
    print(datetime.now() - start)


def small_html_to_pdf():
    """
    With this small size the rendering is being handled without problems.
    It seems we have a problem with either the size of the pages or something
    else.
    """
    start = datetime.now()
    html_path = f"{dir_path}/html/small_table.html"
    pdf_path = f"{dir_path}/build/small_table.pdf"
    HTML(html_path).write_pdf(pdf_path)
    print(datetime.now() - start)


def paginated_templates_to_pdf():
    """
    This is the path we were searching for. Try to write templates with jinja.
    The only thing left to do is to find a way to know how to render tables
    spanning more than one page.
    """
    start = datetime.now()
    html_path = f"{dir_path}/html/small_table.html"
    pdf_path = f"{dir_path}/build/paginated_table.pdf"
    document = HTML(html_path).render()
    documents = [document] * 10000
    all_pages = [p for doc in documents for p in doc.pages]
    documents[0].copy(all_pages).write_pdf(pdf_path)
    print(datetime.now() - start)


class Hero:
    name: str
    power: str
    nemesis: str

    def __init__(self, name: str, power: str, nemesis: str):
        self.name = name
        self.power = power
        self.nemesis = nemesis


def read_file(filepath) -> str:
    with open(filepath) as open_file:
        return open_file.read()


def jinja2_template_to_pdf():
    """
    This is also not working. Because there is too much to render.
    Another solution would be to build templates like this in HTML (maybe even live).
    and use CSS DINA4 boundaries to determine which layout it should have.
    Then split each page into its own document and combine pages to render them.
    This would lead to a safer rendering size (splitted table but documents with only
    one page rendered). For this we actually have to find out how many rows fit in
    our table before its boundaries are reached. Maybe try to emulate the Vimcar
    PDF example and rebuilt it in HTML with those DINA4 Bounds.
    """
    start = datetime.now()
    from jinja2 import Environment, BaseLoader

    template_path = f"{dir_path}/templates/table.jinja2"
    rtemplate = Environment(loader=BaseLoader).from_string(read_file(template_path))
    rendered = rtemplate.render(
        heroes=[Hero(name="Foo", power="Bar", nemesis="Baz")] * 10000
    )
    pdf_path = f"{dir_path}/build/jinja2_table.pdf"
    HTML(string=rendered).write_pdf(pdf_path)
    print(datetime.now() - start)


def jinja2_multipage_to_pdf():
    """
    Determine max size of entries that fit in a page. Split data into chunks of this
    size. Iterate over chunks and render html to documents. Combine all pages.
    Render to pdf and measure the time it took.

    This works. for clearing up the multipage problem. Now we just have to stick pages
    together and everything works fine.

    """
    start = datetime.now()

    from jinja2 import Environment, BaseLoader

    template_path = f"{dir_path}/templates/table_body.jinja2"
    pdf_path = f"{dir_path}/build/jinja2_table.pdf"
    rtemplate = Environment(loader=BaseLoader).from_string(read_file(template_path))

    # make 10000 heroes
    heroes = [Hero(name="Foo", power="Bar", nemesis="Baz")] * 100000
    heroes_per_page = 33
    chunks = [heroes[x : x + heroes_per_page] for x in range(0, len(heroes), 100)]

    documents = []
    for chunk in chunks:
        rendered = rtemplate.render(heroes=chunk)
        document = HTML(string=rendered).render()
        documents.append(document)

    all_pages = [p for doc in documents for p in doc.pages]
    documents[0].copy(all_pages).write_pdf(pdf_path)

    print(datetime.now() - start)


if __name__ == "__main__":
    jinja2_multipage_to_pdf()
