import tkinter as tk
from tkinter import scrolledtext
import lexical_analyzer
from tkinter import filedialog, messagebox

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
    
    return lexical_analyzer.lexical_analyzer(program)
                 
        
def execute():
    
    code = text_editor.get(1.0, tk.END).strip()

    if not code:
        messagebox.showwarning("Warning!s", "No code to tokenize!")
        return

    try:
        tokens = tokenize(code)
        token_output.delete(1.0, tk.END)
        for token in tokens:
            token_output.insert(tk.END, f"{token}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to tokenize code: {e}")


root = tk.Tk()
root.title("LOLCODE")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

left_column = tk.Frame(frame, width=400, padx=10, pady=10)
left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

file_button = tk.Button(left_column, text="Load File", command=loadfile)
file_button.pack(pady=5)

text_editor_label = tk.Label(left_column, text="Code Editor:")
text_editor_label.pack()
text_editor = scrolledtext.ScrolledText(left_column, wrap=tk.WORD, height=25)
text_editor.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

right_column = tk.Frame(frame, width=400, padx=10, pady=10)
right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

run_button = tk.Button(right_column, text="Execute", command=execute)
run_button.pack(pady=5)

token_output_label = tk.Label(right_column, text="Tokens:")
token_output_label.pack()
token_output = scrolledtext.ScrolledText(right_column, wrap=tk.WORD, height=25, bg="#f5f5f5")
token_output.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

root.mainloop()