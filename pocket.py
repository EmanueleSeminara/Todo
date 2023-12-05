# pocket.py
from models.movement import Movement
from os import system
from db import db, movements
import json
from math import ceil
from datetime import datetime
from decimal import Decimal
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from collections import Counter
import string
import json


class Pocket:
    def __init__(self, db_path):
        self.conn = db.connect_db(db_path)
        self.movements = movements.get_all_movements(self.conn)
        self.months_dict = {
                                1: 'Gennaio',
                                2: 'Febbraio',
                                3: 'Marzo',
                                4: 'Aprile',
                                5: 'Maggio',
                                6: 'Giugno',
                                7: 'Luglio',
                                8: 'Agosto',
                                9: 'Settembre',
                                10: 'Ottobre',
                                11: 'Novembre',
                                12: 'Dicembre'
                            }


        # Recuperare il JSON da un file e inserirlo nella variabile
        with open('config/word_category.json', 'r') as json_file:
            loaded_data = json.load(json_file)

        # Inserire il JSON nella variabile
        self.word_category = loaded_data

        # Nome del file JSON
        file_path = "config/config.json"

        # Leggi il file JSON
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        # Estrai la costante
        MOVEMENTS_RECORD_PAGE = data.get("MOVEMENTS_RECORD_PAGE")
        MOVEMENTS_MAX_EXPENSES = data.get("MOVEMENTS_MAX_EXPENSES")
        self.max_expenses = MOVEMENTS_MAX_EXPENSES
        self.record_page_number = MOVEMENTS_RECORD_PAGE

    def aggiungi_movement(self, nome, data_contabile, data_valuta, causale_abi, descrizione, category, amount, mv_type):
        data_valuta = datetime.strptime(data_valuta, "%d/%m/%Y")
        data_contabile = datetime.strptime(data_contabile, "%d/%m/%Y")
        flag_priority = False
        if(category == ""):
            for key, list in self.word_category.items():
                for val in list['keywords']:
                    if(val.upper() in descrizione.upper()):
                        category = key
                        flag_priority = True
                        break
                if(flag_priority):
                    break
        if(category == ""):
            category = "Altro"
        movement = Movement(nome, data_contabile, data_valuta, causale_abi, descrizione, category, amount, mv_type)
        movements.add_movement(self.conn, movement)
        self.movements = movements.get_all_movements(self.conn)
    def mostra_movement(self):
        #movements = get_all_movements(self.conn)
        if not self.movements:
            print(f"La lista delle attivita' e' vuota {self.movements}.")
            return

        print("{:<3} {:<30} {:<10} {:<10} {:<10} {:<15}".format("ID", "Nome", "Data", "Categoria", "Cifra", "Tipologia"))
        for movement in self.movements:
            print("{:<3} {:<30} {:<10} {:<10} {:<10} {:<15}".format(movement.id, movement.name[:30], movement.data_contabile, movement.category, movement.amount, movement.type))

    def remove_movement(self, id):
        movements.delete_movement(self.conn, id)
        self.movements = movements.get_all_movements(self.conn)

    def mostra_movements_page(self, page, num_for_page = 3):
        if not self.movements:
            print(f"La lista dei movimenti e' vuota {self.movements}.")
            return
        num_for_page = int(self.record_page_number)
        if(page > ceil(len(self.movements)/num_for_page)):
            print(f"Pagina richiesta non presente.")
            return
        j = int(page) * int(num_for_page)
        page = int(page - 1)
        i = page if page == 0 else page * num_for_page
        i = int(i)
        sorted_movements = sorted(self.movements, key=lambda x: x.data_valuta)

        amount_sum = sum(
            float(movement.amount.replace('.', '').replace(',', '.')) 
            if movement and movement.amount 
            else 0
            for movement in self.movements
        )


        mv_to_show = sorted_movements[i : j]
        
        print("{:<131}".format("-" * 131))
        print("| {:^3} | {:^30} | {:^17} | {:^17} | {:^15} | {:^12} | {:^15} |".format("ID", "Nome", "Data contabile", "Data valuta", "Categoria", "Cifra", "Tipologia"))
        print("{:<131}".format("-" * 131))
        for movement in mv_to_show:
            if movement.data_valuta:
                if isinstance(movement.data_valuta, datetime):
                    movement_data_valuta = f"{movement.data_valuta.strftime('%d')} {self.months_dict[int(movement.data_valuta.strftime('%m'))]} {movement.data_valuta.strftime('%y')}"
                    movement_data_contabile = f"{movement.data_valuta.strftime('%d')} {self.months_dict[int(movement.data_valuta.strftime('%m'))]} {movement.data_valuta.strftime('%y')}"
                else:
                    movement_data_valuta = movement.data_valuta
                    movement_data_contabile = movement.data_contabile
            else:
                movement_data_valuta = ""
                movement_data_contabile = ""

            print("| {:^3} | {:^30} | {:^17} | {:^17} | {:^15} | {:^12} | {:^15} |".format(movement.id, movement.name[:30], movement_data_contabile, movement_data_valuta, movement.category, movement.amount, movement.type))
        print("{:<131}".format("-" * 131))
        print("| {:<42}{:^43}{:>42} |".format(f"TOT: {len(self.movements)}", "Pagina " + str(page + 1) + " di " + str(ceil(len(self.movements)/num_for_page)), "SOMMA MOVIMENTI: {:.2f}".format(amount_sum)))
        print("{:<131}".format("-" * 131))

    def setRecordPage(self, movements_record_number):
        # Nome del file JSON
        file_path = "config/config.json"

        # Leggi il file JSON
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        # Modifica la costante
        data["MOVEMENTS_RECORD_PAGE"] = movements_record_number  # Modifica il valore secondo le tue esigenze
        self.record_page_number = movements_record_number
        # Scrivi il file JSON aggiornato
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=2)

        print("File JSON aggiornato con successo.")

    def get_categories(self):
        return self.categories

    def clean_all(self):
        movements.clean_movements(self.conn)
        movements.clean_movements_files(self.conn)
        self.movements = []
    
    def stats_movements(self, year, input_month):
        if not self.movements:
            print(f"La lista dei movimenti e' vuota {self.movements}.")
            return
        stats_movements = []
        month_stats = {}
        entrate_totali = Decimal(0.0)
        uscite_totali = Decimal(0.0)
        sorted_movements = sorted(self.movements, key=lambda x: x.data_valuta)

        for movement in self.movements:
            
            if(movement.data_valuta.year == year):
                if(int(input_month) != -1 ):
                    if(int(movement.data_valuta.month) == int(input_month)):
                        stats_movements.append(movement)
                else:
                    stats_movements.append(movement)
                
                month = int(movement.data_valuta.strftime("%m"))
                
                if month not in month_stats:
                    month_stats[month] = {'entrate': 0, 'uscite': 0}
                if(movement.amount[0] == "-"):
                    uscite_totali += Decimal(movement.amount[1:].replace('.', '').replace(',', '.'))
                    month_stats[month]['uscite'] += Decimal(movement.amount[1:].replace('.', '').replace(',', '.'))

                elif(movement.amount[0] == "+"):
                    entrate_totali += Decimal(movement.amount[1:].replace('.', '').replace(',', '.'))
                    month_stats[month]['entrate'] += Decimal(movement.amount[1:].replace('.', '').replace(',', '.'))
                
        
        for month, values in month_stats.items():
            for key, value in values.items():
                month_stats[month][key] = float(value)

        print(f"USCITE: {uscite_totali} - ENTRATE: {entrate_totali} - TOT: {entrate_totali - uscite_totali}\n\n")
        month_stats = dict(sorted(month_stats.items()))

        # Creazione dell'istogramma
        months = [self.months_dict[val] for val in month_stats.keys()]
        entrate = [stats['entrate'] for stats in month_stats.values()]
        uscite = [stats['uscite'] for stats in month_stats.values()]

        bar_width = 0.35  # Larghezza delle barre
        r1 = np.arange(len(months))
        r2 = [x + bar_width + 0.1 for x in r1]  # Aggiungi un offset di 0.1 per distanziare le barre

        fig, ax = plt.subplots()
        # [stats['entrate'] for stats in month_stats.values()]
        amount_sum_entrate = sum(stats['entrate'] for stats in month_stats.values())
        amount_sum_uscite = sum(stats['uscite'] for stats in month_stats.values())
        ax.bar(r1, entrate, width=bar_width, label=f'Entrate: {amount_sum_entrate:.2f}€')
        ax.bar(r2, uscite, width=bar_width, label=f'Uscite: {amount_sum_uscite:.2f}')

        plt.title(f"Entrate e Uscite {year}\nAggiornato a {self.months_dict[int(sorted_movements[-1].data_valuta.strftime('%m'))]}")
        plt.xticks([r + bar_width / 2 for r in range(len(months))], months)  # Posiziona le etichette dei mesi al centro
        plt.legend()

        # Calcola la media delle entrate e delle uscite
        media_entrate = np.mean(entrate)
        media_uscite = np.mean(uscite)

        # Aggiungi le linee orizzontali per la media delle entrate e delle uscite
        ax.axhline(y=media_entrate, color='green', linestyle='--', label=f'Media Entrate: {media_entrate:.2f}€')
        ax.axhline(y=media_uscite, color='red', linestyle='--', label=f'Media Uscite: {media_uscite:.2f}€')
        ax.axhline(y=float(self.max_expenses), color='yellow', linestyle='--', label=f'Soglia Uscite: {float(self.max_expenses):.2f}€')

        # Aggiungi le cifre in cima ad ogni barra con il simbolo dell'euro
        for i, value in enumerate(entrate):
            ax.text(r1[i], value, f'{value:.2f}€', ha='center', va='bottom')
        
        for i, value in enumerate(uscite):
            ax.text(r2[i], value, f'{value:.2f}€', ha='center', va='bottom')

        # Formatta automaticamente i valori dell'asse y con il simbolo dell'euro
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:.2f}€'))
        legend = ['Pippo']

        plt.legend()
        plt.get_current_fig_manager().set_window_title(f"Entrate uscite {self.months_dict[int(sorted_movements[-1].data_valuta.strftime('%m'))]} {year}")
        plt.show(block=False)


        # Calcola il totale per ogni categoria
        categories_expenses = {}
        categories_entries = {}
        for movement in stats_movements:
            category = movement.category
            if movement.amount[0] == '-':
                if category not in categories_expenses:
                    categories_expenses[category] = Decimal(0.0)
                categories_expenses[category] += Decimal(movement.amount[1:].replace('.', '').replace(',', '.'))
            
            elif movement.amount[0] == '+':
                if category not in categories_entries:
                    categories_entries[category] = Decimal(0.0)
                categories_entries[category] += Decimal(movement.amount[1:].replace('.', '').replace(',', '.'))

        # Ordina le categorie per il totale decrescente
        sorted_categories_expenses = sorted(categories_expenses.items(), key=lambda x: x[1], reverse=True)
        sorted_categories_entries = sorted(categories_entries.items(), key=lambda x: x[1], reverse=True)

        # Estrai le categorie e i totali ordinati per le uscite
        categories_expenses, totals_expenses = zip(*sorted_categories_expenses)

        # Crea il grafico a torta per le uscite senza nomi delle categorie
        plt.figure(figsize=(8, 8))
        plt.subplot(121)  # Creazione del subplot a sinistra

        def autopct_func_expenses(pct):
            return f'{pct:.1f}%' if pct > 2 else ''

        pie_chart_expenses = plt.pie(totals_expenses, autopct=autopct_func_expenses, startangle=140)

        # Aggiungi una legenda personalizzata per le uscite
        legend_labels_expenses = []
        i = 1

        for category, total in zip(categories_expenses, totals_expenses):
            legend_labels_expenses.append(f"{i}. {category}: {total:.2f}€")
            i += 1

        plt.legend(pie_chart_expenses[0], legend_labels_expenses, loc="upper right", bbox_to_anchor=(1.05, 0, 0.5, 1), fontsize='small')

        plt.title(f"Distribuzione delle uscite per categorie - {year}\nAggiornato a {self.months_dict[int(sorted_movements[-1].data_valuta.strftime('%m'))]}")

        # Estrai le categorie e i totali ordinati per le entrate
        categories_entries, totals_entries = zip(*sorted_categories_entries)

        # Crea il grafico a torta per le entrate senza nomi delle categorie
        plt.subplot(122)  # Creazione del subplot a destra

        def autopct_func_entries(pct):
            return f'{pct:.1f}%' if pct > 2 else ''

        pie_chart_entries = plt.pie(totals_entries, autopct=autopct_func_entries, startangle=140)

        # Aggiungi una legenda personalizzata per le entrate
        legend_labels_entries = []
        i = 1

        for category, total in zip(categories_entries, totals_entries):
            legend_labels_entries.append(f"{i}. {category}: {total:.2f}€")
            i += 1

        plt.legend(pie_chart_entries[0], legend_labels_entries, loc="lower center", bbox_to_anchor=(0.5, -0.2, 0, 0), fontsize='small')

        plt.title(f"Distribuzione delle entrate per categorie - {year}\nAggiornato a {self.months_dict[int(sorted_movements[-1].data_valuta.strftime('%m'))]}")
        plt.get_current_fig_manager().set_window_title(f"Suddivisione categorie {self.months_dict[int(sorted_movements[-1].data_valuta.strftime('%m'))]} {year}")
        plt.subplots_adjust(wspace=0.5)
        plt.show()