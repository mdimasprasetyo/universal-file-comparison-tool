import hashlib
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import difflib

class FileComparerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal File Comparison Tool")
        self.root.geometry("650x500")

        self.file1_path = ""
        self.file2_path = ""

        self.create_widgets()

    def create_widgets(self):
        # File 1 Selection
        f1_frame = ttk.LabelFrame(self.root, text=" File 1 ")
        f1_frame.pack(fill="x", padx=10, pady=5)
        
        self.f1_label = ttk.Label(f1_frame, text="No file selected", width=50, anchor="w")
        self.f1_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        ttk.Button(f1_frame, text="Browse...", command=self.select_file1).pack(side="right", padx=5, pady=5)

        # File 2 Selection
        f2_frame = ttk.LabelFrame(self.root, text=" File 2 ")
        f2_frame.pack(fill="x", padx=10, pady=5)

        self.f2_label = ttk.Label(f2_frame, text="No file selected", width=50, anchor="w")
        self.f2_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        ttk.Button(f2_frame, text="Browse...", command=self.select_file2).pack(side="right", padx=5, pady=5)

        # Action Button
        ttk.Button(self.root, text="Compare Files", command=self.compare_files).pack(pady=10)

        # Results Display
        res_frame = ttk.LabelFrame(self.root, text=" Analysis Output ")
        res_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_text = tk.Text(res_frame, wrap="word", height=15)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)

    def select_file1(self):
        self.file1_path = filedialog.askopenfilename()
        if self.file1_path:
            self.f1_label.config(text=os.path.basename(self.file1_path))

    def select_file2(self):
        self.file2_path = filedialog.askopenfilename()
        if self.file2_path:
            self.f2_label.config(text=os.path.basename(self.file2_path))

    def get_hash(self, filepath):
        """Calculates SHA-256 hash for byte-level accuracy."""
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def compare_files(self):
        if not self.file1_path or not self.file2_path:
            messagebox.showwarning("Warning", "Please select two files to compare.")
            return

        self.result_text.delete(1.0, tk.END)
        self.log(f"Comparing:\n1: {self.file1_path}\n2: {self.file2_path}\n" + "-"*50)

        # 1. Metadata Check
        size1 = os.path.getsize(self.file1_path)
        size2 = os.path.getsize(self.file2_path)
        self.log(f"File Size 1: {size1:,} bytes")
        self.log(f"File Size 2: {size2:,} bytes")

        # 2. SHA-256 Hash Check (Exact binary match)
        hash1 = self.get_hash(self.file1_path)
        hash2 = self.get_hash(self.file2_path)

        if hash1 == hash2:
            self.log("\n[VERDICT] Files are EXACT BINARY MATCHES (100% identical).")
            return
        else:
            self.log("\n[VERDICT] Files are DIFFERENT at the binary level.")

        # 3. Text/Document Diff (attempted text inspection)
        ext1 = os.path.splitext(self.file1_path)[1].lower()
        ext2 = os.path.splitext(self.file2_path)[1].lower()

        if ext1 in ['.txt', '.csv', '.json', '.py', '.md', '.html', '.xml'] and ext1 == ext2:
            self.log("\n--- Performing Text Line-by-Line Diff ---")
            self.compare_text_files()
        elif ext1 == '.cdr' or ext2 == '.cdr':
            self.log("\n[Note on .cdr files]: CorelDRAW files are binary vector archives. "
                     "Because binary hashes differ, rasterize them to PNG via Inkscape CLI "
                     "or UniConverter to compare visual pixel outputs.")

    def compare_text_files(self):
        try:
            with open(self.file1_path, 'r', encoding='utf-8', errors='ignore') as f1, \
                 open(self.file2_path, 'r', encoding='utf-8', errors='ignore') as f2:
                diff = list(difflib.unified_diff(
                    f1.readlines(),
                    f2.readlines(),
                    fromfile='File 1',
                    tofile='File 2',
                    lineterm=''
                ))
                if diff:
                    self.log("\nFirst few line differences:\n" + "\n".join(diff[:15]))
                else:
                    self.log("Text content is identical despite structural differences.")
        except Exception as e:
            self.log(f"Could not read text content: {e}")

    def log(self, text):
        self.result_text.insert(tk.END, text + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileComparerApp(root)
    root.mainloop()