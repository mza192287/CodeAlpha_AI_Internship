import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator


LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh-CN",
    "Hindi": "hi",
    "Turkish": "tr",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Italian": "it",
    "Portuguese": "pt",
}


class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Language Translation Tool")
        self.root.geometry("900x650")
        self.root.minsize(760, 560)

        self.source_lang = tk.StringVar(value="English")
        self.target_lang = tk.StringVar(value="Urdu")

        self.build_ui()

    def build_ui(self):
        title = ttk.Label(
            self.root,
            text="AI Language Translation Tool",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=(22, 5))

        subtitle = ttk.Label(
            self.root,
            text="Translate text between multiple languages using Google Translate.",
            font=("Segoe UI", 10)
        )
        subtitle.pack(pady=(0, 18))

        controls = ttk.Frame(self.root)
        controls.pack(fill="x", padx=35)

        ttk.Label(controls, text="Source Language:").grid(row=0, column=0, padx=8, pady=8)
        source_box = ttk.Combobox(
            controls, textvariable=self.source_lang,
            values=list(LANGUAGES.keys()), state="readonly", width=20
        )
        source_box.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(controls, text="Target Language:").grid(row=0, column=2, padx=8, pady=8)
        target_box = ttk.Combobox(
            controls, textvariable=self.target_lang,
            values=list(LANGUAGES.keys()), state="readonly", width=20
        )
        target_box.grid(row=0, column=3, padx=8, pady=8)

        ttk.Button(controls, text="Swap", command=self.swap_languages).grid(
            row=0, column=4, padx=12
        )

        ttk.Label(
            self.root, text="Enter Text",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=38, pady=(15, 5))

        self.input_box = tk.Text(
            self.root, height=9, wrap="word",
            font=("Segoe UI", 12), padx=10, pady=10
        )
        self.input_box.pack(fill="both", expand=True, padx=35)

        actions = ttk.Frame(self.root)
        actions.pack(pady=15)

        ttk.Button(actions, text="Translate", command=self.translate).pack(
            side="left", padx=8, ipadx=15
        )
        ttk.Button(actions, text="Clear", command=self.clear).pack(
            side="left", padx=8, ipadx=15
        )

        ttk.Label(
            self.root, text="Translated Result",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=38, pady=(3, 5))

        self.output_box = tk.Text(
            self.root, height=9, wrap="word",
            font=("Segoe UI", 12), padx=10, pady=10
        )
        self.output_box.pack(fill="both", expand=True, padx=35, pady=(0, 25))

    def swap_languages(self):
        source = self.source_lang.get()
        target = self.target_lang.get()
        self.source_lang.set(target)
        self.target_lang.set(source)

    def translate(self):
        text = self.input_box.get("1.0", "end").strip()

        if not text:
            messagebox.showwarning("Missing Text", "Please enter text to translate.")
            return

        source = LANGUAGES[self.source_lang.get()]
        target = LANGUAGES[self.target_lang.get()]

        try:
            translator = GoogleTranslator(source=source, target=target)
            result = translator.translate(text)

            self.output_box.delete("1.0", "end")
            self.output_box.insert("1.0", result)

        except Exception as error:
            messagebox.showerror(
                "Translation Error",
                f"Unable to translate the text.\n\nDetails: {error}"
            )

    def clear(self):
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
