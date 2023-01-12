import tkinter as tk
from tkinter import ttk
import requests
import json
import sqlite3

api_key = "AIzaSyCRL_yuU8DbhCFgrjunyjbzp8ZTbe8i7yo"
cse_id = "e7df85514513c4d0b"

def setup_db():
    conn = sqlite3.connect('search_results.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS search_results (search_term text, link text, snippet text)''')
    conn.commit()
    return conn

def google_search(search_term, conn):
    c = conn.cursor()
    c.execute('''SELECT * FROM search_results WHERE search_term = ?''', (search_term,))
    result = c.fetchone()
    if result:
        print("Data found in database")
        return result
    else:
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": search_term,
            "cx": cse_id,
            "key": api_key
        }
        response = requests.get(search_url, params=params)
        search_results = json.loads(response.text)
        for item in search_results["items"]:
            c.execute("INSERT INTO search_results VALUES (?,?,?)", (search_term, item["link"], item["snippet"]))
            conn.commit()
        return search_results

def search_button_clicked():
    search_term = search_entry.get()
    conn = setup_db()
    search_results = google_search(search_term, conn)
    result_text.configure(state='normal')
    result_text.delete(1.0, tk.END)
    for item in search_results["items"]:
        result_text.insert(tk.END, f"Link: {item['link']}\n")
        result_text.insert(tk.END, f"Snippet: {item['snippet']}\n")
    result_text.configure(state='disabled')
    conn.close()

root = tk.Tk()
root.title("Google Search")

search_label = ttk.Label(root, text="Search Term:")
search_label.grid(row=0, column=0)

search_entry = ttk.Entry(root)
search_entry.grid(row=0, column=1)

search_button = ttk.Button(root, text="Search", command=search_button_clicked)
search_button.grid(row=0, column=2)

result_text = tk.Text(root)
result_text.grid(row=1, column=0, columnspan=3)
result_text.configure(state='disabled')

root.mainloop()
