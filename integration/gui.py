
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import scraper, etl, visualize
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Final Web Scrape → ETL → Visualization System")
        self.geometry("1200x750")

        frame = ttk.Frame(self)
        frame.pack(fill="x")

        ttk.Label(frame, text="Demo Website URL:").pack(side="left")
        self.url_entry = tk.Entry(frame, width=60)
        self.url_entry.pack(side="left", padx=5)
        self.url_entry.insert(0, "https://books.toscrape.com/")

        ttk.Button(frame, text="Scrape Website", command=self.run_scraper).pack(side="left", padx=5)
        ttk.Button(frame, text="Run ETL", command=self.run_etl).pack(side="left", padx=5)
        ttk.Button(frame, text="Show Graphs", command=self.show_graphs).pack(side="left", padx=5)

        self.log = tk.Text(self, height=10)
        self.log.pack(fill="x")

        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True)

        self.json_file = "../outputs/scraped.json"
        self.scraped_csv = "../outputs/scraped_raw.csv"
        self.processed_scrape_csv = "../outputs/processed_from_scrape.csv"
        self.processed_user_csv = "../outputs/processed_user.csv"

    def logmsg(self, msg):
        self.log.insert("end", msg + "\n")
        self.log.see("end")

    def run_scraper(self):
        def task():
            url = self.url_entry.get()
            try:
                scraper.scrape_demo_site(url, self.json_file)
                scraper.json_to_csv(self.json_file, self.scraped_csv)
                self.logmsg("Scraping Done → JSON + Raw CSV generated")
            except Exception as e:
                self.logmsg(f"Scraper Error: {e}")

        threading.Thread(target=task).start()

    def run_etl(self):
        def task():
            try:
                df = etl.load_csv(self.scraped_csv)
                df = etl.transform(df)
                etl.save_processed(df, self.processed_scrape_csv)
                self.logmsg("ETL Completed → processed_from_scrape.csv created")
            except Exception as e:
                self.logmsg(f"ETL Error: {e}")

        threading.Thread(target=task).start()

    def show_graphs(self):
        for w in self.plot_frame.winfo_children():
            w.destroy()

        df = pd.read_csv(self.processed_scrape_csv)

        fig, axs = plt.subplots(1, 3, figsize=(13, 4))

        visualize.plot_category(df, axs[0])
        visualize.plot_price_dist(df, axs[1])
        visualize.plot_popularity(df, axs[2])

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

app = App()
app.mainloop()
