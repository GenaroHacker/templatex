# Implementing the Builder design pattern to generate a LaTeX document as specified

# Importing necessary Python libraries
from abc import ABC, abstractmethod

# Builder Abstract Base Class
class Builder(ABC):
    @abstractmethod
    def build_part(self, content, **kwargs):
        pass

# Concrete Builders
class SectionBuilder(Builder):
    def build_part(self, content, **kwargs):
        return f"\\section*{{{content}}}\n"

class TextBuilder(Builder):
    def build_part(self, content, **kwargs):
        return f"{content}\n"

class TextInputBuilder(Builder):
    def build_part(self, content, **kwargs):
        lines = kwargs.get('number_of_lines', 10)
        spacing = kwargs.get('spacing_mm', '8mm')
        return f"{{\\openup {kwargs.get('openup', '0.8cm')}\n\\lines{{{lines}}}{{{spacing}}} % {content}\n}}\n"

# Director Class
class Director:
    def __init__(self):
        self.script = ""
        self.setup_document()

    def setup_document(self):
        header = (
            "\\documentclass[12pt]{article}\n"
            "\\usepackage[a4paper, total={6in, 8in}]{geometry}\n"
            "\\usepackage{forloop}\n"
            "\\newcounter{ct}\n"
            "\\newcommand{\\lines}[2]{% #1: number of lines, #2: spacing between lines\n"
            "  \\forloop{ct}{1}{\\value{ct} < #1}{\\noindent\\rule{\\linewidth}{0.4pt}\\\\[#2]}\n"
            "}\n"
            "\\begin{document}\n"
        )
        self.script += header

    def add_section(self, builder, title):
        self.script += builder.build_part(title)

    def add_text(self, builder, text):
        self.script += builder.build_part(text)

    def draw_lines(self, builder, content, number_of_lines, spacing_mm='8mm', openup='0.8cm'):
        self.script += builder.build_part(content, number_of_lines=number_of_lines, spacing_mm=spacing_mm, openup=openup)

    def finalize_document(self):
        self.script += "\\end{document}\n"

# Initializing director and builders
director = Director()
section_builder = SectionBuilder()
text_builder = TextBuilder()
text_input_builder = TextInputBuilder()

# Building the document
director.add_section(section_builder, "Computer Text Section 1")
director.add_text(text_builder, "This section contains the first part of regular computer text.")

director.add_section(section_builder, "Handwriting Section 1")
director.draw_lines(text_input_builder, "15 lines with 8mm spacing", 15, '8mm')

director.add_section(section_builder, "Computer Text Section 2")
director.add_text(text_builder, "This section contains the second part of regular computer text.")

director.add_section(section_builder, "Handwriting Section 2")
director.draw_lines(text_input_builder, "20 lines with 8mm spacing", 20, '8mm')

# Finalizing document
director.finalize_document()

# Saving the document to a .tex file
with open('/mnt/data/output.tex', 'w') as file:
    file.write(director.script)

# Output the script for verification
director.script
