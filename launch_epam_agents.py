#!/usr/bin/env python3
"""
EPAM Business Intelligence System Launcher
Simple GUI launcher for the EPAM agent system
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import webbrowser
import os
import sys
import threading

class EPAMLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("EPAM Business Intelligence System")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Get the directory where this script is located
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#667eea', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="🏢 EPAM Business Intelligence",
                              font=('Arial', 16, 'bold'),
                              bg='#667eea', fg='white')
        title_label.pack(pady=20)

        # Main content
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)

        # Description
        desc_label = tk.Label(main_frame,
                             text="Multi-agent system for company analysis and opportunity discovery",
                             font=('Arial', 10),
                             wraplength=450)
        desc_label.pack(pady=(0, 20))

        # Buttons frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        # Launch Web UI button
        web_button = tk.Button(buttons_frame,
                              text="🌐 Launch Web Interface",
                              font=('Arial', 12, 'bold'),
                              bg='#667eea', fg='white',
                              width=25, height=2,
                              command=self.launch_web_ui)
        web_button.pack(pady=5)

        # Direct analysis button
        analysis_button = tk.Button(buttons_frame,
                                   text="🤖 Run Direct Analysis",
                                   font=('Arial', 12, 'bold'),
                                   bg='#28a745', fg='white',
                                   width=25, height=2,
                                   command=self.launch_direct_analysis)
        analysis_button.pack(pady=5)

        # Status frame
        status_frame = tk.Frame(main_frame)
        status_frame.pack(pady=20, fill='x')

        tk.Label(status_frame, text="Status:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.status_text = tk.Text(status_frame, height=6, width=60,
                                  font=('Courier', 9), bg='#f8f9fa')
        self.status_text.pack(fill='x')

        # Buttons at bottom
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(side='bottom', fill='x', pady=10)

        help_button = tk.Button(bottom_frame, text="❓ Help",
                               command=self.show_help)
        help_button.pack(side='left')

        exit_button = tk.Button(bottom_frame, text="❌ Exit",
                               command=self.root.quit)
        exit_button.pack(side='right')

        self.log_status("EPAM Business Intelligence System Ready")
        self.log_status("Choose an option above to get started")

    def log_status(self, message):
        """Add a message to the status log"""
        self.status_text.insert(tk.END, f"• {message}\n")
        self.status_text.see(tk.END)
        self.root.update()

    def launch_web_ui(self):
        """Launch the Flask web interface"""
        try:
            self.log_status("Starting Flask web server...")

            # Change to the script directory
            os.chdir(self.script_dir)

            # Start Flask app in a separate thread
            def run_flask():
                try:
                    subprocess.run([sys.executable, "epam_ui_app.py"],
                                 cwd=self.script_dir, check=True)
                except subprocess.CalledProcessError as e:
                    self.log_status(f"Error starting web server: {e}")
                except FileNotFoundError:
                    self.log_status("Error: epam_ui_app.py not found!")

            threading.Thread(target=run_flask, daemon=True).start()

            self.log_status("Web server starting...")
            self.log_status("Opening browser to http://localhost:8080")

            # Wait a moment then open browser
            self.root.after(3000, lambda: webbrowser.open("http://localhost:8080"))

        except Exception as e:
            self.log_status(f"Error launching web UI: {e}")
            messagebox.showerror("Error", f"Failed to launch web interface:\n{e}")

    def launch_direct_analysis(self):
        """Launch direct analysis via master agent chain"""
        company = tk.simpledialog.askstring("Company Analysis",
                                           "Enter company ticker symbol (e.g., NVDA, AAPL):")
        if company:
            try:
                self.log_status(f"Starting analysis for {company.upper()}...")

                # Change to script directory
                os.chdir(self.script_dir)

                def run_analysis():
                    try:
                        # Run the master agent chain
                        result = subprocess.run([sys.executable, "master_agent_chain.py", company.upper()],
                                              cwd=self.script_dir,
                                              capture_output=True, text=True, timeout=300)

                        if result.returncode == 0:
                            self.log_status(f"✅ Analysis complete for {company.upper()}")
                            self.log_status("Check output folder for Word report")
                        else:
                            self.log_status(f"❌ Analysis failed: {result.stderr}")

                    except subprocess.TimeoutExpired:
                        self.log_status("⏰ Analysis timed out (5 minutes)")
                    except Exception as e:
                        self.log_status(f"❌ Error during analysis: {e}")

                threading.Thread(target=run_analysis, daemon=True).start()

            except Exception as e:
                self.log_status(f"Error starting analysis: {e}")
                messagebox.showerror("Error", f"Failed to start analysis:\n{e}")

    def show_help(self):
        """Show help information"""
        help_text = """
EPAM Business Intelligence System Help

🌐 Launch Web Interface:
   • Starts the Flask web server on port 8080
   • Provides a professional web UI for company analysis
   • Includes optional API key configuration
   • Generates downloadable Word reports

🤖 Run Direct Analysis:
   • Runs analysis directly via command line
   • Prompts for company ticker symbol
   • Uses mock data (no API keys required)
   • Generates Word report in output folder

System Requirements:
   • Python 3.8+
   • All dependencies from requirements.txt
   • Internet connection for SEC data

For detailed documentation, see README.md
        """
        messagebox.showinfo("Help", help_text)

def main():
    # Import tkinter.simpledialog here to avoid issues if tkinter isn't available
    import tkinter.simpledialog
    tk.simpledialog = tkinter.simpledialog

    root = tk.Tk()
    app = EPAMLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()