import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog, messagebox
import lexical_analyzer
from syntax_analyzer import SyntaxAnalyzer  # Import your custom syntax analyzer

def loadfile():
    # Open file dialog to select a file.
    filepath = filedialog.askopenfilename()

    if filepath:
        with open(filepath, 'r') as file:
            content = file.read()

        text_editor.delete(1.0, tk.END)
        text_editor.insert(1.0, content)

def tokenize(content):
    # Save file content in a list.
    program = content.split('\n')

    # Remove white space.
    program = [line.strip() for line in program]

    # Use lexical_analyzer to get the tokens
    return lexical_analyzer.lexical_analyzer(program)

def analyze_syntax(tokens):
    # Use your SyntaxAnalyzer to check the tokens
    analyzer = SyntaxAnalyzer(tokens)
    return analyzer.program_start()  # Start syntax analysis from the program level

def execute():
    code = text_editor.get(1.0, tk.END).strip()

    if not code:
        messagebox.showwarning("Warning", "No code to tokenize!")
        return

    try:
        # Get the tokens from lexical analyzer
        tokens = tokenize(code)
    
        # Clear previous outputs
        token_output.delete(1.0, tk.END)
        syntax_output.delete(1.0, tk.END)

        # Display the tokens and syntax analysis result
        token_output.insert(tk.END, "Tokens:\n")
        for token in tokens:
            token_output.insert(tk.END, f"{token}\n")

        # Perform syntax analysis on the tokens
        analysis_result = analyze_syntax(tokens)

        syntax_output.insert(tk.END, "Syntax Analysis Result:\n")
        syntax_output.insert(tk.END, analysis_result)
        
        # Print analysis result to the console
        print(analysis_result)
        
    except Exception as e:
        print("Error", f"Failed to tokenize or analyze code: {e}")

# Create the main Tkinter window
root = tk.Tk()
root.title("LOLCODE Tokenizer with Syntax Analyzer")

# Create a frame to hold both columns
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Left column - for the code editor and file loading
left_column = tk.Frame(frame, width=400, padx=10, pady=10)
left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Load File button
file_button = tk.Button(left_column, text="Load File", command=loadfile)
file_button.pack(pady=5)

# Code editor label
text_editor_label = tk.Label(left_column, text="Code Editor:")
text_editor_label.pack()

# Code editor (scrolled text box)
text_editor = scrolledtext.ScrolledText(left_column, wrap=tk.WORD, height=25)
text_editor.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

# Right column - for token output and executing the tokenization
right_column = tk.Frame(frame, width=400, padx=10, pady=10)
right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Execute button
run_button = tk.Button(right_column, text="Execute", command=execute)
run_button.pack(pady=5)

# Token output label
token_output_label = tk.Label(right_column, text="Tokens:")
token_output_label.pack()

# Token output area (scrolled text box)
token_output = scrolledtext.ScrolledText(right_column, wrap=tk.WORD, height=12, bg="#f5f5f5")
token_output.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

# Syntax output label
syntax_output_label = tk.Label(right_column, text="Syntax Analysis Result:")
syntax_output_label.pack()

# Syntax output area (scrolled text box)
syntax_output = scrolledtext.ScrolledText(right_column, wrap=tk.WORD, height=12, bg="#f5f5f5")
syntax_output.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

# Start the Tkinter main loop
root.mainloop()
