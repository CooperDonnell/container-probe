from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, END, LEFT, X

from .cli import Style, render_text
from .detectors import inspect_file


class ContainerProbeGui(ttk.Window):
    def __init__(self) -> None:
        super().__init__(title="Container Probe", themename="flatly")
        self.geometry("980x680")
        self.minsize(760, 520)

        self.selected_path = ttk.StringVar()
        self.status = ttk.StringVar(value="Choose a file to analyze.")

        self.build_ui()

    def build_ui(self) -> None:
        toolbar = ttk.Frame(self, padding=12)
        toolbar.pack(fill=X)

        path_entry = ttk.Entry(toolbar, textvariable=self.selected_path)
        path_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 8))

        ttk.Button(toolbar, text="Choose File", command=self.choose_file).pack(side=LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Analyze", bootstyle="primary", command=self.analyze_file).pack(side=LEFT)

        self.output = ttk.Text(self, wrap="word", font=("Menlo", 12), padx=12, pady=12)
        self.output.pack(fill=BOTH, expand=True, padx=12, pady=(0, 8))

        status_bar = ttk.Label(self, textvariable=self.status, padding=(12, 6), anchor="w")
        status_bar.pack(fill=X)

    def choose_file(self) -> None:
        filename = filedialog.askopenfilename(title="Choose a file to analyze")
        if filename:
            self.selected_path.set(filename)
            self.status.set("Ready to analyze.")

    def analyze_file(self) -> None:
        path_text = self.selected_path.get().strip()
        if not path_text:
            messagebox.showerror("No File Selected", "Choose a file before analyzing.")
            return

        path = Path(path_text)
        if not path.exists():
            messagebox.showerror("File Not Found", f"Could not find:\n{path}")
            return

        self.status.set("Analyzing...")
        self.update_idletasks()

        try:
            report = inspect_file(path).to_dict()
            text = render_text(report, Style(False))
        except Exception as exc:
            messagebox.showerror("Analysis Failed", str(exc))
            self.status.set("Analysis failed.")
            return

        self.output.delete("1.0", END)
        self.output.insert("1.0", text)
        self.status.set(f"Analyzed {path.name}.")


def main() -> int:
    app = ContainerProbeGui()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
