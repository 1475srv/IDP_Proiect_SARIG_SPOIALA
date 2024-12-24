import tkinter as tk
from tkinter import ttk, messagebox
import json

# Functie pentru actualizarea veniturilor, cheltuielilor si bugetului ramas
def actualizare_buget():
    venit_total = sum(venituri)
    cheltuieli_total = sum(cheltuieli)
    buget_ramas = venit_total - cheltuieli_total

    eticheta_venit.config(text=f"Venit total: {venit_total:.2f} RON")
    eticheta_cheltuieli.config(text=f"Cheltuieli totale: {cheltuieli_total:.2f} RON")
    eticheta_buget.config(text=f"Buget ramas: {buget_ramas:.2f} RON")

    # Verificare buget depășit
    if buget_ramas < 0:
        messagebox.showwarning("Buget Depășit", "Atenție! Aveți bugetul depășit.")

# Functie pentru adaugarea unei tranzactii
def adauga_tranzactie():
    categorie = categorie_var.get()
    try:
        suma = float(camp_suma.get())
        descriere = camp_descriere.get()

        if suma < 0:
            # Propunere pentru mutarea automata
            if categorie == "Venit":
                raspuns = messagebox.askyesno("Suma negativa", "Ai introdus o sumă negativă. O doresti introdusă la cheltuieli (cu valoare pozitivă)?")
                if raspuns:
                    categorie = "Cheltuiala"
                    suma = abs(suma)
                else:
                    messagebox.showerror("Eroare", "Nu se pot introduce sume negative!")
                    return
            elif categorie == "Cheltuiala":
                raspuns = messagebox.askyesno("Suma negativa", "Ai introdus o sumă negativă. O doresti introdusă la venituri (cu valoare pozitivă)?")
                if raspuns:
                    categorie = "Venit"
                    suma = abs(suma)
                else:
                    messagebox.showerror("Eroare", "Nu se pot introduce sume negative!")
                    return

        if categorie == "Venit":
            venituri.append(suma)
        else:
            cheltuieli.append(suma)

        # Adaugam in tabel
        tabel_tranzactii.insert('', 'end', values=(categorie, f"{suma:.2f} RON", descriere))

        # Resetam campurile
        camp_suma.delete(0, tk.END)
        camp_descriere.delete(0, tk.END)

        # Actualizam bugetul
        actualizare_buget()
    except ValueError:
        messagebox.showerror("Eroare", "Introduceti o suma valida!")

# Functie pentru salvarea datelor intr-un fisier JSON
def salveaza_date():
    date = {
        "tranzactii": [],
        "venituri": venituri,
        "cheltuieli": cheltuieli
    }

    # Preluam datele din tabel
    for id_rand in tabel_tranzactii.get_children():
        rand = tabel_tranzactii.item(id_rand)['values']
        date["tranzactii"].append({"Categorie": rand[0], "Suma": rand[1], "Descriere": rand[2]})

    try:
        with open("buget.json", "w") as fisier:
            json.dump(date, fisier, indent=4)
        messagebox.showinfo("Salvare reusita", "Datele au fost salvate in fisierul 'buget.json'.")
    except Exception as e:
        messagebox.showerror("Eroare", f"Nu s-a putut salva fisierul: {e}")

# Functie pentru incarcarea datelor dintr-un fisier JSON
def incarca_date():
    global venituri, cheltuieli
    try:
        with open("buget.json", "r") as fisier:
            date = json.load(fisier)

        # Resetam datele existente
        venituri = date.get("venituri", [])
        cheltuieli = date.get("cheltuieli", [])

        # Actualizam tabelul
        tabel_tranzactii.delete(*tabel_tranzactii.get_children())
        for tranzactie in date.get("tranzactii", []):
            tabel_tranzactii.insert('', 'end', values=(tranzactie["Categorie"], tranzactie["Suma"], tranzactie["Descriere"]))

        # Actualizam bugetul
        actualizare_buget()
        messagebox.showinfo("Incarcare reusita", "Datele au fost incarcate din fisierul 'buget.json'.")
    except FileNotFoundError:
        messagebox.showwarning("Fisier inexistent", "Fisierul 'buget.json' nu a fost gasit.")
    except Exception as e:
        messagebox.showerror("Eroare", f"Nu s-a putut incarca fisierul: {e}")

# Functie pentru stergerea unei tranzactii
def sterge_tranzactie():
    element_selectat = tabel_tranzactii.selection()
    if not element_selectat:
        messagebox.showerror("Eroare", "Selectati o tranzactie pentru a o sterge.")
        return

    # Confirmare inainte de stergere
    confirmare = messagebox.askyesno("Confirmare", "Sigur doriti sa stergeti tranzactia selectata?")
    if confirmare:
        for element in element_selectat:
            valori = tabel_tranzactii.item(element)['values']
            # Actualizam listele de venituri sau cheltuieli
            if valori[0] == "Venit":
                venituri.remove(float(valori[1].split(" ")[0]))
            else:
                cheltuieli.remove(float(valori[1].split(" ")[0]))

            # Stergem din tabel
            tabel_tranzactii.delete(element)
        actualizare_buget()

# Functie pentru editarea unei tranzactii
def editeaza_tranzactie():
    element_selectat = tabel_tranzactii.selection()
    if not element_selectat:
        messagebox.showerror("Eroare", "Selectati o tranzactie pentru a o edita.")
        return

    element = element_selectat[0]
    valori = tabel_tranzactii.item(element)['values']

    # Preluam detaliile tranzactiei selectate
    categorie_var.set(valori[0])  # Setam categoria
    camp_suma.delete(0, tk.END)
    camp_suma.insert(0, valori[1].split(" ")[0])  # Valoarea fara "RON"
    camp_descriere.delete(0, tk.END)
    camp_descriere.insert(0, valori[2])  # Descrierea

    # Stergem tranzactia curenta din liste pentru actualizare
    if valori[0] == "Venit":
        venituri.remove(float(valori[1].split(" ")[0]))
    else:
        cheltuieli.remove(float(valori[1].split(" ")[0]))

    # Stergem tranzactia din tabel temporar
    tabel_tranzactii.delete(element)
    actualizare_buget()

# Date globale
venituri = []
cheltuieli = []

# Creare fereastra principala
fereastra = tk.Tk()
fereastra.title("Calculator Buget Personal")
fereastra.geometry("1100x700")  # Dimensiune initiala
fereastra.configure(bg="#f0f0f0")

# Stiluri
stil = ttk.Style()
stil.configure("Treeview.Heading", font=("Arial", 12, "bold"))
stil.configure("Treeview", font=("Arial", 12), rowheight=30)
stil.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
stil.configure("TButton", font=("Arial", 12, "bold"))

# Configurare redimensionare automata
fereastra.grid_columnconfigure(0, weight=1)
fereastra.grid_rowconfigure(1, weight=1)

# Layout pentru formular
cadru_formular = tk.Frame(fereastra, bg="#f0f0f0")
cadru_formular.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

# Categorie (Venit/Cheltuiala)
tk.Label(cadru_formular, text="Categorie:", font=("Arial", 14), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
categorie_var = tk.StringVar(value="Venit")
radio_venit = tk.Radiobutton(cadru_formular, text="Venit", variable=categorie_var, value="Venit", font=("Arial", 12), bg="#f0f0f0")
radio_venit.grid(row=0, column=1, padx=10, pady=5, sticky="w")
radio_cheltuiala = tk.Radiobutton(cadru_formular, text="Cheltuiala", variable=categorie_var, value="Cheltuiala", font=("Arial", 12), bg="#f0f0f0")
radio_cheltuiala.grid(row=0, column=2, padx=10, pady=5, sticky="w")

# Suma
tk.Label(cadru_formular, text="Suma (RON):", font=("Arial", 14), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="e")
camp_suma = tk.Entry(cadru_formular, font=("Arial", 12), width=20)
camp_suma.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Descriere
tk.Label(cadru_formular, text="Descriere:", font=("Arial", 14), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="e")
camp_descriere = tk.Entry(cadru_formular, font=("Arial", 12), width=40)
camp_descriere.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Butoane
cadru_butoane = tk.Frame(fereastra, bg="#f0f0f0")
cadru_butoane.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

buton_adauga = tk.Button(cadru_butoane, text="Adauga tranzactie", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command=adauga_tranzactie)
buton_adauga.grid(row=0, column=0, padx=20, pady=10)

buton_salveaza = tk.Button(cadru_butoane, text="Salveaza date", font=("Arial", 14, "bold"), bg="#2196F3", fg="white", command=salveaza_date)
buton_salveaza.grid(row=0, column=1, padx=20, pady=10)

buton_incarca = tk.Button(cadru_butoane, text="Incarca date", font=("Arial", 14, "bold"), bg="#FFC107", fg="black", command=incarca_date)
buton_incarca.grid(row=0, column=2, padx=20, pady=10)

buton_iesire = tk.Button(cadru_butoane, text="Iesire", font=("Arial", 14, "bold"), bg="#D32F2F", fg="white", command=fereastra.quit)
buton_iesire.grid(row=0, column=3, padx=20, pady=10)

buton_sterge = tk.Button(cadru_butoane, text="Sterge tranzactie", font=("Arial", 14, "bold"), bg="#D32F2F", fg="white", command=sterge_tranzactie)
buton_sterge.grid(row=1, column=0, padx=20, pady=10)

buton_editeaza = tk.Button(cadru_butoane, text="Editeaza tranzactie", font=("Arial", 14, "bold"), bg="#FFC107", fg="black", command=editeaza_tranzactie)
buton_editeaza.grid(row=1, column=1, padx=20, pady=10)

# Tabel pentru tranzactii
cadru_tabel = tk.Frame(fereastra, bg="#f0f0f0")
cadru_tabel.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

tabel_tranzactii = ttk.Treeview(cadru_tabel, columns=("Categorie", "Suma", "Descriere"), show="headings")
tabel_tranzactii.heading("Categorie", text="Categorie")
tabel_tranzactii.heading("Suma", text="Suma (RON)")
tabel_tranzactii.heading("Descriere", text="Descriere")
tabel_tranzactii.column("Categorie", width=150, anchor="center")
tabel_tranzactii.column("Suma", width=150, anchor="center")
tabel_tranzactii.column("Descriere", width=400, anchor="w")
tabel_tranzactii.pack(side="left", fill="both", expand=True)

# Scrollbar pentru tabel
scrollbar = ttk.Scrollbar(cadru_tabel, orient="vertical", command=tabel_tranzactii.yview)
tabel_tranzactii.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Afisare venituri, cheltuieli si buget
cadru_rezumat = tk.Frame(fereastra, bg="#f0f0f0")
cadru_rezumat.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

eticheta_venit = tk.Label(cadru_rezumat, text="Venit total: 0.00 RON", font=("Arial", 16), bg="#f0f0f0", fg="#4CAF50")
eticheta_venit.grid(row=0, column=0, padx=30, pady=10)

eticheta_cheltuieli = tk.Label(cadru_rezumat, text="Cheltuieli totale: 0.00 RON", font=("Arial", 16), bg="#f0f0f0", fg="#D32F2F")
eticheta_cheltuieli.grid(row=0, column=1, padx=30, pady=10)

eticheta_buget = tk.Label(cadru_rezumat, text="Buget ramas: 0.00 RON", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
eticheta_buget.grid(row=0, column=2, padx=30, pady=10)

# Start aplicatie
fereastra.mainloop()
