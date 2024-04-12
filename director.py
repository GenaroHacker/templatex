# Importing necessary Python libraries
from abc import ABC, abstractmethod

# Builder Abstract Base Class
class Builder(ABC):
    @abstractmethod
    def build_part(self, **kwargs):
        pass

# Concrete Builders
class SectionBuilder(Builder):
    def build_part(self, **kwargs):
        content = kwargs['content']
        return f"\\section*{{{content}}}\n"

class TextBuilder(Builder):
    def build_part(self, **kwargs):
        content = kwargs['content']
        return f"{content}\n"

class TextInputBuilder(Builder):
    def build_part(self, **kwargs):
        lines = kwargs.get('number_of_lines', 10)
        spacing = kwargs.get('spacing', 3.0)
        spacing_mm = f"{spacing * 10}mm"
        return f"{{\\openup {kwargs.get('openup', '0.8cm')}\n\\lines{{{lines}}}{{{spacing_mm}}}\n}}\n"

class CheckboxBuilder(Builder):
    def build_part(self, **kwargs):
        items = kwargs.get('items', [])
        checkboxes = "\\begin{itemize}\n"
        for item in items:
            checkboxes += f"  \\item[$\\Box$] {item}\n"
        checkboxes += "\\end{itemize}\n"
        return checkboxes

# Director Class
class Director:
    def __init__(self):
        self.script = ""
        self.builders = {
            'section': SectionBuilder(),
            'text': TextBuilder(),
            'text_input': TextInputBuilder(),
            'checkbox': CheckboxBuilder()
        }
        self.setup_document()

    def setup_document(self):
        header = (
            "\\documentclass[12pt]{article}\n"
            "\\usepackage[a4paper, total={4in, 6in}, margin=0.5in]{geometry}\n"
            "\\usepackage{forloop}\n"
            "\\usepackage{amssymb}\n"  # Include the amssymb package for the checkbox symbol
            "\\newcounter{ct}\n"
            "\\newcommand{\\lines}[2]{% #1: number of lines, #2: spacing between lines\n"
            "  \\forloop{ct}{1}{\\value{ct} < #1}{\\noindent\\rule{\\linewidth}{0.4pt}\\\\[#2]}\n"
            "}\n"
            "\\pagestyle{empty}\n"  # Add this line to remove page numbers
            "\\begin{document}\n"
        )
        self.script += header

    def add_section(self, title):
        self.script += self.builders['section'].build_part(content=title)

    def add_text(self, text):
        self.script += self.builders['text'].build_part(content=text)

    def draw_lines(self, number_of_lines, spacing=0.29, openup='0.8cm'):
        self.script += self.builders['text_input'].build_part(number_of_lines=number_of_lines+1, spacing=spacing, openup=openup)

    def add_checkboxes(self, items):
        self.script += self.builders['checkbox'].build_part(items=items)

    def new_page(self):
        self.script += "\\newpage\n"  # Adds a new page in the document

    def finalize_document(self):
        self.script += "\\end{document}\n"

    def write_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.script)

if __name__ == '__main__':
    # Initializing director
    d = Director()

    # Building the document
    d.add_section("Computer Text Section 1")
    d.add_text("This section contains the first part of regular computer text.")

    d.add_section("Handwriting Section 1")
    d.draw_lines(15)

    d.add_section("Computer Text Section 2")
    d.add_text("This section contains the second part of regular computer text.")

    d.add_section("Handwriting Section 2")
    d.draw_lines(20)

    d.new_page()

    d.add_section("Checklist")
    d.add_checkboxes(["Option one", "Option two", "Option three"])

    # Finalizing document
    d.finalize_document()

    # Saving the document to a .tex file
    d.write_to_file('output.tex')
