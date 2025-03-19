import os
import errno
from typing import List


class MarkdownGenerator:
    """
    MarkdownGenerator class: generates the MarkdownGenerator file content.
    """

    def __init__(self) -> None:
        self.content = ""

    def add_header(self, text: str) -> "MarkdownGenerator":
        """
        Adds a header block to the content

        Parameters
        ----------
        text: str
            The headers's text

        Returns
        -------
            MarkdownGenerator
        """
        string = "".join(["#"]) + f" {text}"
        self.content += self.create_block(string, 2)
        return self

    def add_text(self, text: str) -> "MarkdownGenerator":
        """
        Adds a text block to the content

        Parameters
        ----------
        text: str
            The text to add

        Returns
        -------
            MarkdownGenerator
        """

        self.content += self.create_block(text, 2)
        return self

    def add_linebreak(self) -> "MarkdownGenerator":
        """
        Adds a line break block to the content

        Returns
        -------
            MarkdownGenerator
        """

        self.content += self.create_block("", 1)
        return self

    @classmethod
    def create_block(cls, text: str = "", lbcount: int = 1) -> str:
        """
        Appends linebreaks to the given text

        Parameters
        ----------
        text: str
            The input text
        lbcount: int
            The number of linebreaks that will be appended
        Returns
        -------
            MarkdownGenerator
        """
        return text + "".join(["\n"] * lbcount)

    def add_table(self, rows: List[List[str]]) -> "MarkdownGenerator":
        """
        Adds a table to the content

        Parameters
        ----------
        rows: List[List[str]]
            List of table rows. First one being the header row.
        Returns
        -------
            MarkdownGenerator
        """

        for i, items in enumerate(list(rows)):
            self.content += "| " + "| ".join(items) + "\n"
            if i == 0:
                for item in items:
                    self.content += "| "
                    self.content += "".join(["-"] * len(item))
                self.content += "\n"
        self.content += "\n"
        return self

    def save(self, filename: str) -> None:
        """
        Saves the file

        Parameters
        ----------
        filename: str
            The path of the destination file
        Returns
        -------
            MarkdownGenerator
        """
        if not os.path.exists(filename):
            try:
                os.makedirs(os.path.dirname(filename), exist_ok=True)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        file = open(filename, "w")
        file.write(self.content)
        file.close()
