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

# Director Class
class Director:
    def __init__(self):
        self.script = ""
        self.builders = {
            'section': SectionBuilder(),
            'text': TextBuilder(),
            'text_input': TextInputBuilder()
        }
        self.setup_document()

    def setup_document(self):
        header = (
            "\\documentclass[12pt]{article}\n"
            "\\usepackage[a4paper, total={4in, 6in}, margin=0.5in]{geometry}\n"
            "\\usepackage{forloop}\n"
            "\\newcounter{ct}\n"
            "\\newcommand{\\lines}[2]{% #1: number of lines, #2: spacing between lines\n"
            "  \\forloop{ct}{1}{\\value{ct} < #1}{\\noindent\\rule{\\linewidth}{0.4pt}\\\\[#2]}\n"
            "}\n"
            "\\begin{document}\n"
        )
        self.script += header

    def add_section(self, title):
        self.script += self.builders['section'].build_part(content=title)

    def add_text(self, text):
        self.script += self.builders['text'].build_part(content=text)

    def draw_lines(self, number_of_lines, spacing=0.29, openup='0.8cm'):
        self.script += self.builders['text_input'].build_part(number_of_lines=number_of_lines+1, spacing=spacing, openup=openup)

    def finalize_document(self):
        self.script += "\\end{document}\n"

    def write_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.script)

if __name__ == '__main__':
    # Initializing director
    director = Director()

    # Building the document
    director.add_section("Computer Text Section 1")
    director.add_text("This section contains the first part of regular computer text.")

    director.add_section("Handwriting Section 1")
    director.draw_lines(15)

    director.add_section("Computer Text Section 2")
    director.add_text("This section contains the second part of regular computer text.")

    director.add_section("Handwriting Section 2")
    director.draw_lines(20)

    # Finalizing document
    director.finalize_document()

    # Saving the document to a .tex file
    director.write_to_file('output.tex')
