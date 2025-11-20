import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv

DB_FILE = 'nilai_siswa.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi REAL NOT NULL,
            fisika REAL NOT NULL,
            inggris REAL NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


    def insert_nilai(nama, bio, fis, ing, prediksi):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
            VALUES (?, ?, ?, ?, ?)
        ''', (nama, bio, fis, ing, prediksi))
        conn.commit()
        conn.close()


        def fetch_all():
            conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute('SELECT id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa ORDER BY id DESC')
        rows = cur.fetchall()
        conn.close()    
        return rows
    
    def predict_fakultas(biologi, fisika, inggris):
        if biologi > fisika and biologi > inggris:
            return 'Kedokteran'
        elif fisika > biologi and fisika > inggris:
            return 'Teknik'
        elif inggris > biologi and inggris > fisika:
            return 'Bahasa'
        else:
            # tie -> priority 
            max_val = max(biologi, fisika, inggris)
            if biologi == max_val:
                return 'Kedokteran'
            elif fisika == max_val:
                return 'Teknik'
            else:
                return 'Bahasa'
            
class NilaiApp:
    def __init__(self, root):
        self.root = root
        root.title('Input Nilai Siswa - SQLite')
        root.geometry('900x520')
        root.minisize(800, 480)

        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('TLabel', font=('segoe UI', 10))
        style.configure('TButton', font=('segoe UI', 10), padding=6)
        style.configure('Header.TLabel', font=('segoe UI', 12, 'bold'))
        style.configure('Treeview.Heading', font=('segoe UI', 10, 'bold'))
        style.configure('Treeview', font=('segoe UI', 10))

        frm_left = ttk.LabelFrame(root, text='From Input', padding=(12,12))
        frm_left.grid(row=0, column=0, sticky='nws', padx=12, pady=12)

        frm_right = ttk.LabelFrame(root, text='Data Tersimpan', padding=(8,8))
        frm_right.grid(row=0, column=1, sticky='nsew', padx=12, pady=12)

        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        ttk.Label(frm_left, text='Nama Siswa:', style='Header.TLabel').grid(row=0, column=0, sticky='w')
        self.entry_nama = ttk.Entry(frm_left, width=34)
        self.entry_nama.grid(row=1, column=0, pady=6, sticky='w')
        
        lbl_nilai = ttk.Label(frm_left, text='Nilai (0-100):', style='Header.TLabel')
        lbl_nilai.grid(row=2, column=0, sticky='w', pady=(8, 0))

        inner = ttk.Frame(frm_left)
        inner.grid(row=3, column=0, sticky='w')
        ttk.Label(inner, text='Biologi').grid(row=0, column=0, padx=(0,6))
        self.entry_bio = ttk.Entry(inner, width=8)
        self.entry_bio.grid(row=0, column=1, padx=(0,12))

        ttk.Label(inner, text='Fisika').grid(row=0, column=2, padx=(0,6))
        self.entry_fis = ttk.Entry(inner, width=8)
        self.entry_fis.grid(row=0, column=3, padx=(0,12))

        ttk.Label(inner, text='Inggris').grid(row=0, column=4, padx=(0,6))
        self.entry_ing = ttk.Entry(inner, width=8)
        self.entry_ing.grid(row=0, column=5)

        # self.lbl_info = ttk.Label(frm_left, text='Isi semua kolom, lalu tekan Submit.', foreground='#333')
        # self.lbl_info.grid(row=4, column=0, pady=(8,0), sticky='w')

