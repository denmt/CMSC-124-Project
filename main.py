import tkinter as tk
import lexical_analyzer
from tkinter import filedialog, messagebox


def main():
    # Open file dialog to select a file.

    filepath = filedialog.askopenfilename()

    if filepath:
        with open(filepath, 'r') as file:
            content = file.read()

            # Save file content in a list.
            program = content.split('\n')

            # Remove white space.
            program = [line.strip() for line in program]

            lexical_analyzer.lexical_analyzer(program)
                 
        


main()