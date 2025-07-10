import os
import hashlib
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
from datetime import datetime
import webbrowser
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

class CyberGuardiansApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyber Guardians - Virus Behavior Simulation")
        self.root.geometry("850x630")
        self.root.configure(bg="#1e1e2f")
        self.root.resizable(False, False)

        self.log_entries = []
        self.known_signatures = self.load_fake_signatures()
        self.scan_path = os.getcwd()

        self.build_ui()
        self.show_intro_screen()

    def show_intro_screen(self):
        self.intro_frame = tk.Frame(self.root, bg="#121f2e")
        self.intro_frame.place(relwidth=1, relheight=1)

        title = tk.Label(
            self.intro_frame,
            text="🛡️ CYBER GUARDIANS",
            font=("Segoe UI", 36, "bold"),
            fg="#00bcd4",
            bg="#121f2e"
        )
        title.pack(expand=True)

        subtitle = tk.Label(
            self.intro_frame,
            text="Simulating Virus Behavior (Safe Mode)",
            font=("Segoe UI", 14),
            fg="white",
            bg="#121f2e"
        )
        subtitle.pack(pady=10)

        self.intro_progress_label = tk.Label(self.intro_frame, text="Loading: 0%", font=("Segoe UI", 12), fg="white", bg="#121f2e")
        self.intro_progress_label.pack(pady=(0, 5))

        self.intro_progress = ttk.Progressbar(self.intro_frame, orient='horizontal', length=400, mode='determinate')
        self.intro_progress.pack(pady=10)

        self.fade_in(self.intro_frame)
        self.simulate_intro_loading(0)

    def simulate_intro_loading(self, progress):
        if progress > 100:
            self.fade_out(self.intro_frame, self.intro_frame.destroy)
        else:
            self.intro_progress['value'] = progress
            self.intro_progress_label.config(text=f"Loading: {progress}%")
            self.root.after(30, lambda: self.simulate_intro_loading(progress + 2))

    def fade_in(self, widget, alpha=0.0, step=0.05):
        alpha += step
        if alpha > 1.0:
            alpha = 1.0
        try:
            self.root.attributes('-alpha', alpha)
        except:
            pass
        if alpha < 1.0:
            self.root.after(30, lambda: self.fade_in(widget, alpha, step))

    def fade_out(self, widget, callback=None, alpha=1.0, step=0.05):
        alpha -= step
        if alpha < 0:
            alpha = 0
        try:
            self.root.attributes('-alpha', alpha)
        except:
            pass
        if alpha > 0:
            self.root.after(30, lambda: self.fade_out(widget, callback, alpha, step))
        else:
            if callback:
                callback()
            try:
                self.root.attributes('-alpha', 1.0)
            except:
                pass

    def build_ui(self):
        tk.Label(
            self.root, text="🦠 Cyber Guardians - Virus Behavior Simulation", font=("Segoe UI", 18, "bold"),
            fg="#00e676", bg="#1e1e2f"
        ).pack(pady=15)

        path_frame = tk.Frame(self.root, bg="#1e1e2f")
        path_frame.pack(pady=5)
        tk.Label(path_frame, text="Scan Folder:", font=("Segoe UI", 10), fg="white", bg="#1e1e2f").pack(side=tk.LEFT, padx=5)
        self.path_display = tk.Entry(path_frame, width=50, font=("Segoe UI", 10))
        self.path_display.insert(0, self.scan_path)
        self.path_display.pack(side=tk.LEFT)
        tk.Button(path_frame, text="Browse", command=self.browse_folder, bg="#4FC3F7", fg="black").pack(side=tk.LEFT, padx=5)

        self.output_box = scrolledtext.ScrolledText(
            self.root, width=100, height=22, font=("Consolas", 10),
            bg="#2e2e3e", fg="#d0d0d0", insertbackground="white"
        )
        self.output_box.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#1e1e2f")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Simulate Virus Scan", command=self.simulate_scan, bg="#66BB6A", fg="white", width=25).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Export Log as PDF", command=self.export_pdf_log, bg="#FFB300", fg="black", width=18).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Clear Output", command=self.clear_output, bg="#E53935", fg="white", width=18).pack(side=tk.LEFT, padx=10)

        self.progress_label = tk.Label(self.root, text="Scan Progress: 0%", font=("Segoe UI", 10), fg="white", bg="#1e1e2f")
        self.progress_label.pack(pady=(5, 2))

        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=400, mode='determinate')
        self.progress.pack(pady=8)
        self.progress['value'] = 0

    def browse_folder(self):
        selected_path = filedialog.askdirectory()
        if selected_path:
            self.scan_path = selected_path
            self.path_display.delete(0, tk.END)
            self.path_display.insert(0, selected_path)

    def clear_output(self):
        self.output_box.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.progress_label.config(text="Scan Progress: 0%")

    def load_fake_signatures(self):
        return {
            "19a08cf1081ff329f91451d798a5d00c181ca81be6e8c0ae77ae75d63eb0b2c2"
        }

    def compute_file_hash(self, filepath):
        try:
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            print(f"Error reading file: {filepath}, {e}")
            return None

    def simulate_scan(self):
        self.log_entries = []
        threat_count = [0]  # Fix applied here
        extensions_of_interest = ['.docx', '.pdf', '.xls', '.txt']

        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, f"[🕵️‍♂️] Simulating scan in: {self.scan_path}\n\n")

        file_list = []
        for root_dir, _, files in os.walk(self.scan_path):
            for file in files:
                file_list.append(os.path.join(root_dir, file))

        total_files = len(file_list)
        if total_files == 0:
            self.output_box.insert(tk.END, "[INFO] No files found to scan.\n")
            return

        def scan_file(i):
            if i >= total_files:
                summary = f"\n[✅] Scan complete. {threat_count[0]} threat(s) detected.\n"
                self.output_box.insert(tk.END, summary)
                self.progress['value'] = 100
                self.progress_label.config(text="Scan Progress: 100%")
                return

            filepath = file_list[i]
            file_hash = self.compute_file_hash(filepath)
            file_ext = os.path.splitext(filepath)[1].lower()
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            file_name = os.path.basename(filepath)

            if not file_hash:
                self.output_box.insert(tk.END, f"[SKIP] Could not read: {filepath}\n")
                self.root.after(10, lambda: scan_file(i + 1))
                return

            if file_ext in extensions_of_interest:
                status = "Found sensitive file"
                self.output_box.insert(tk.END, f"[LOG] {file_name} - {status}\n")
                self.log_entries.append({"date": date_str, "time": time_str, "file": file_name, "status": status})

            if file_hash in self.known_signatures:
                status = "Threat detected!"
                self.output_box.insert(tk.END, f"[THREAT] {file_name} - {status}\n")
                self.log_entries.append({"date": date_str, "time": time_str, "file": file_name, "status": status})
                threat_count[0] += 1
            else:
                status = "File is safe"
                self.output_box.insert(tk.END, f"[OK] {file_name}\n")
                self.log_entries.append({"date": date_str, "time": time_str, "file": file_name, "status": status})

            progress_value = ((i + 1) / total_files) * 100
            progress_percent = int(progress_value)
            self.progress['value'] = progress_value
            self.progress_label.config(text=f"Scan Progress: {progress_percent}%")
            self.root.update_idletasks()

            self.root.after(10, lambda: scan_file(i + 1))

        scan_file(0)

    def export_pdf_log(self):
        if not self.log_entries:
            messagebox.showinfo("No Logs", "No scan logs available. Please run a scan first.")
            return

        pdf_filename = os.path.join(os.getcwd(), "cyber_guardians_log.pdf")

        doc = SimpleDocTemplate(pdf_filename, pagesize=LETTER)
        elements = []
        styles = getSampleStyleSheet()

        title = Paragraph("Cyber Guardians Scan Log", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        data = [["Date", "Time", "File", "Status"]]
        for log in self.log_entries:
            data.append([log['date'], log['time'], log['file'], log['status']])

        table = Table(data, colWidths=[90, 60, 250, 150])

        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#00bcd4")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
        ])

        for i, log in enumerate(self.log_entries, start=1):
            status = log['status'].lower()
            if "threat" in status or "sensitive" in status:
                bg_color = colors.HexColor("#f28b82")
            else:
                bg_color = colors.HexColor("#ccff90")
            style.add('BACKGROUND', (0, i), (-1, i), bg_color)

        table.setStyle(style)
        elements.append(table)

        try:
            doc.build(elements)
            messagebox.showinfo("PDF Exported", f"Log exported successfully as:\n{pdf_filename}")
            webbrowser.open(f'file://{pdf_filename}')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberGuardiansApp(root)
    root.mainloop()
