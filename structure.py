"""
structure.py – Tkinter GUI to visualise a folder tree.
Run: python structure.py
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os


class FolderStructureGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Folder Structure Viewer")
        self.root.geometry("900x650")

        # ── State ──────────────────────────────────────
        self.folder_path = tk.StringVar()
        self.include_hidden = tk.BooleanVar(value=False)
        self.show_paths = tk.BooleanVar(value=False)
        self.include_files = tk.BooleanVar(value=True)
        self.max_depth = tk.IntVar(value=6)

        self.ignore_list = {
            "venv", ".venv", "node_modules", "__pycache__",
            ".git", ".idea", ".vscode", "dist", "build",
            ".next", "out", "staticfiles", "coverage",
        }

        self._build_ui()

    # ── UI ─────────────────────────────────────────────

    def _build_ui(self):
        # Top – folder picker
        top = tk.Frame(self.root, bg="#1e1e2e", pady=8, padx=12)
        top.pack(fill="x")

        tk.Label(top, text="📁 Folder:", bg="#1e1e2e", fg="#cdd6f4",
                 font=("Consolas", 11)).grid(row=0, column=0, sticky="w")
        tk.Entry(top, textvariable=self.folder_path, width=55,
                 bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4",
                 font=("Consolas", 10), relief="flat").grid(row=0, column=1, padx=8, ipady=4)
        tk.Button(top, text="Browse", command=self._browse,
                  bg="#89b4fa", fg="#1e1e2e", font=("Consolas", 10, "bold"),
                  relief="flat", padx=10).grid(row=0, column=2)

        # Options bar
        opts = tk.Frame(self.root, bg="#181825", pady=6, padx=12)
        opts.pack(fill="x")

        for text, var, col in [
            ("Hidden files", self.include_hidden, 0),
            ("Full paths", self.show_paths, 1),
            ("Include files", self.include_files, 2),
        ]:
            tk.Checkbutton(opts, text=text, variable=var,
                           bg="#181825", fg="#cdd6f4", selectcolor="#313244",
                           activebackground="#181825", activeforeground="#cdd6f4",
                           font=("Consolas", 10)).grid(row=0, column=col, sticky="w", padx=10)

        tk.Label(opts, text="Max depth:", bg="#181825", fg="#6c7086",
                 font=("Consolas", 9)).grid(row=0, column=3, padx=(20, 4))
        tk.Spinbox(opts, from_=1, to=20, textvariable=self.max_depth, width=4,
                   bg="#313244", fg="#cdd6f4", font=("Consolas", 10)).grid(row=0, column=4)

        tk.Label(opts, text=f"Auto-skip: {', '.join(sorted(self.ignore_list)[:6])}...",
                 bg="#181825", fg="#45475a", font=("Consolas", 8)).grid(
            row=1, column=0, columnspan=5, sticky="w", padx=10, pady=(2, 0))

        # Action buttons
        btns = tk.Frame(self.root, bg="#1e1e2e", pady=8, padx=12)
        btns.pack(fill="x")

        for text, cmd, bg in [
            ("⚡ Generate", self._generate, "#89b4fa"),
            ("💾 Save .txt", self._save, "#a6e3a1"),
            ("🗑 Clear", self._clear, "#f38ba8"),
        ]:
            tk.Button(btns, text=text, command=cmd,
                      bg=bg, fg="#1e1e2e", font=("Consolas", 10, "bold"),
                      relief="flat", padx=16, pady=4).pack(side="left", padx=6)

        # Output
        out_frame = tk.Frame(self.root, bg="#1e1e2e", padx=10, pady=4)
        out_frame.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        self.output = scrolledtext.ScrolledText(
            out_frame, wrap="none",
            font=("Consolas", 10),
            bg="#11111b", fg="#cdd6f4",
            insertbackground="#cdd6f4",
            selectbackground="#313244",
            relief="flat",
        )
        self.output.pack(fill="both", expand=True)

        # Status
        self.status = tk.Label(self.root, text="Ready", bd=1,
                               relief=tk.SUNKEN, anchor=tk.W,
                               bg="#181825", fg="#6c7086",
                               font=("Consolas", 9))
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    # ── Actions ────────────────────────────────────────

    def _browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def _generate(self):
        folder = self.folder_path.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Select a valid folder first.")
            return
        self.output.delete(1.0, tk.END)
        self.status.config(text="Generating…")
        self.root.update()
        tree = self._walk(folder, 0)
        self.output.insert(1.0, tree)
        count = tree.count("\n")
        self.status.config(text=f"Done · {count} lines · {os.path.basename(folder)}/")

    def _walk(self, path: str, depth: int) -> str:
        if depth > self.max_depth.get():
            return ""

        base = os.path.basename(path)
        if depth > 0 and base in self.ignore_list:
            return ""

        indent = "    " * depth
        result = f"{indent}{base}/\n"

        try:
            items = sorted(os.listdir(path),
                           key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
            for item in items:
                full = os.path.join(path, item)

                if not self.include_hidden.get() and item.startswith("."):
                    continue

                if os.path.isdir(full):
                    if item in self.ignore_list:
                        result += f"{indent}    ├── {item}/ [skipped]\n"
                    else:
                        result += self._walk(full, depth + 1)
                elif self.include_files.get():
                    name = full if self.show_paths.get() else item
                    result += f"{indent}    ├── {name}\n"

        except PermissionError:
            result += f"{indent}    └── [permission denied]\n"
        except Exception as e:
            result += f"{indent}    └── [error: {e}]\n"

        return result

    def _save(self):
        content = self.output.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Nothing to save.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("All", "*.*")],
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.status.config(text=f"Saved → {path}")
            except Exception as e:
                messagebox.showerror("Save failed", str(e))

    def _clear(self):
        self.output.delete(1.0, tk.END)
        self.status.config(text="Ready")


if __name__ == "__main__":
    root = tk.Tk()
    app = FolderStructureGUI(root)
    root.mainloop()
