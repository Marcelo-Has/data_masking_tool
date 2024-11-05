import tkinter as tk
from tkinter import ttk, scrolledtext

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Masking Tool")

        # Add global variable for delimiter selection
        self.delimiter_var = tk.StringVar(value=",")

        # UI Setup for delimiter selection
        delimiter_label = tk.Label(self.root, text="Select CSV Delimiter:")
        delimiter_label.pack(pady=(10, 0))

        delimiter_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.delimiter_var,
            values=[",", ";", "|", "\t"],
            state="readonly"
        )
        delimiter_dropdown.pack(pady=(0, 10))
        delimiter_dropdown.set(",")  # Default delimiter

        # Instructions label
        instructions = tk.Label(
            self.root, text="Upload a CSV or Excel file to mask columns with fake data:"
        )
        instructions.pack(pady=10)

        # Upload button
        self.upload_button = tk.Button(self.root, text="Upload and Mask Data")
        self.upload_button.pack(pady=5)

        # Scrollable frame for column settings
        self.column_canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.column_canvas.yview)
        self.scrollable_frame = tk.Frame(self.column_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.column_canvas.configure(scrollregion=self.column_canvas.bbox("all")),
        )

        self.column_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.column_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.column_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Inner frame to hold column settings widgets
        self.column_inner_frame = tk.Frame(self.scrollable_frame)
        self.column_inner_frame.pack()

        # Generate button (initially disabled)
        self.generate_button = tk.Button(
            self.root, text="Generate Fake Data", state="disabled"
        )
        self.generate_button.pack(pady=5)

        # Checkbox to keep mapping consistent (default checked)
        self.keep_mapping_var = tk.BooleanVar(value=True)
        self.keep_mapping_checkbox = tk.Checkbutton(
            self.root, text="Keep Mapping Consistent", variable=self.keep_mapping_var
        )
        self.keep_mapping_checkbox.pack(pady=5)

        # Log display
        self.log_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.log_text.pack(pady=10)

        # Footer with hyperlink
        footer = tk.Label(self.root, text="Created by Marcelo Has", fg="blue", cursor="hand2")
        footer.pack(pady=10)
        footer.bind("<Button-1>", self.open_link)

    def open_link(self, event):
        import webbrowser
        webbrowser.open("https://www.linkedin.com/in/marcelohas/")
