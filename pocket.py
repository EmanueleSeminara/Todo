# pocket.py
from movement import Movement
from os import system
from db import connect_db, add_movement, get_all_movements, delete_movement, get_all_categories, clean_movements, clean_movements_files
import json
from math import ceil
from datetime import datetime
from decimal import Decimal
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from collections import Counter
import string






class Pocket:
    def __init__(self, db_path):
        self.conn = connect_db(db_path)
        self.movements = get_all_movements(self.conn)
        self.categories = get_all_categories(self.conn)
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
        self.word_category = {
            'Stipendio': ['join business management', 'progesi'],
            'Paypal': ['paypal'],
            'Prelievi': ['prelievo bancomat'],
            'Spese Domestiche': ['amatilli', 'igino'],                                                              # Affitto/mutuo, bollette domestiche (luce, gas, acqua), spese condominiali.
            'Cibo e Generi Alimentari': ['mcdonald', 'esercente farina', 'eurospin', 'famila', 'casalandia', 'zangaloro', 'pedevilla', 'ma supermercati'],       # Spese legate agli acquisti di generi alimentari e pasti fuori casa.
            'Trasporti': ['anagnina', 'quintiliani', 'monti tiburtini', 'castro pretorio', 'cinecitta', 'tiburtina'],                                                                                        # Carburante, trasporto pubblico, manutenzione dell'auto.
            'Assicurazioni': [],                                                                                    # Premi assicurativi per auto, casa, salute, ecc.
            'Spese Mediche': [],                                                                                    # Ticket sanitari, farmaci, visite mediche.
            'Divertimento e Tempo Libero': [],                                                                      # Spese per attività ricreative, cinema, ristoranti, hobby.
            'Debiti e Prestiti': [],                                                                                # Rate di prestiti, pagamenti di carte di credito.
            'Risparmi e Investimenti': ['satispay', 'acomea', 'aiello giuseppina'],                                 # Trasferimenti verso conti di risparmio o investimenti.
            'Educazione': [],                                                                                       # Spese legate all\'istruzione, come tasse scolastiche, libri, corsi.
            'Abbigliamento e Accessori': ['portadiroma', 'decathlon'],                                                           # Acquisti di vestiti, scarpe e altri accessori.
            'Emergenze': [],                                                                                        # Fondi destinati a spese impreviste o emergenze.
            'Vizi': ['tabacchi', 'tabaccheria', 'goglia mario'],                                                    # Contributi a organizzazioni non profit o cause benefiche.
            'Acquisti Online': ['amazon.it', 'amzn mktp'],
        }
        # Nome del file JSON
        file_path = "config.json"

        # Leggi il file JSON
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        # Estrai la costante
        MOVEMENTS_RECORD_PAGE = data.get("MOVEMENTS_RECORD_PAGE")
        self.recordPageNumber = MOVEMENTS_RECORD_PAGE

        # Stampa la costante
        print("MOVEMENTS_RECORD_PAGE:", MOVEMENTS_RECORD_PAGE)

    def aggiungi_movement(self, nome, data_contabile, data_valuta, causale_abi, descrizione, category, amount, mv_type):
        #print(f"{data_contabile} - {amount}")
        data_valuta = datetime.strptime(data_valuta, "%d/%m/%Y")
        data_contabile = datetime.strptime(data_contabile, "%d/%m/%Y")
        if(category == ""):
            for key, list in self.word_category.items():
                for val in list:
                    if(val.upper() in descrizione.upper()):
                        category = key
        if(category == ""):
            category = "Altro"
        movement = Movement(nome, data_contabile, data_valuta, causale_abi, descrizione, category, amount, mv_type)
        #print(movement)
        add_movement(self.conn, movement)
        self.movements = get_all_movements(self.conn)

    def mostra_movement(self):
        #movements = get_all_movements(self.conn)
        if not self.movements:
            print(f"La lista delle attivita' e' vuota {self.movements}.")
            return

        print("{:<3} {:<30} {:<10} {:<10} {:<10} {:<15}".format("ID", "Nome", "Data", "Categoria", "Cifra", "Tipologia"))
        for movement in self.movements:
            print("{:<3} {:<30} {:<10} {:<10} {:<10} {:<15}".format(movement.id, movement.name[:30], movement.data_contabile, movement.category, movement.amount, movement.type))

    def remove_movement(self, id):
        delete_movement(self.conn, id)
        self.movements = get_all_movements(self.conn)

    def mostra_movements_page(self, page, num_for_page = 3):
        if not self.movements:
            print(f"La lista dei movimenti e' vuota {self.movements}.")
            return
        num_for_page = int(self.recordPageNumber)
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
            #print(type(movement.data_valuta))
            if movement.data_valuta:
                #print("PIPPO")
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
            #print("| {:^3} | {:^30} | {:^17} | {:^17} | {:^15} | {:^12} | {:^15} |".format(movement.id, movement.data_contabile, movement.data_contabile, "asd", "asd", "asd", "asd"))
        print("{:<131}".format("-" * 131))
        print("| {:<42}{:^43}{:>42} |".format(f"TOT: {len(self.movements)}", "Pagina " + str(page + 1) + " di " + str(ceil(len(self.movements)/num_for_page)), "SOMMA MOVIMENTI: {:.2f}".format(amount_sum)))
        print("{:<131}".format("-" * 131))

    def setRecordPage(self, movements_record_number):
        # Nome del file JSON
        file_path = "config.json"

        # Leggi il file JSON
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        # Modifica la costante
        data["MOVEMENTS_RECORD_PAGE"] = movements_record_number  # Modifica il valore secondo le tue esigenze
        self.recordPageNumber = movements_record_number
        # Scrivi il file JSON aggiornato
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=2)

        print("File JSON aggiornato con successo.")

    def get_categories(self):
        return self.categories

    def clean_all(self):
        clean_movements(self.conn)
        clean_movements_files(self.conn)
        self.movements = []
    
    def stats_movements(self, year):
        stats_movements = []
        month_stats = {}
        entrate_totali = Decimal(0.0)
        uscite_totali = Decimal(0.0)

        for movement in self.movements:
            
            if(movement.data_valuta.year == year):
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

        
        
        #print(len(self.movements))
        #print(len(stats_movements))
        print(f"USCITE: {uscite_totali} - ENTRATE: {entrate_totali} - TOT: {entrate_totali - uscite_totali}\n\n")
        month_stats = dict(sorted(month_stats.items()))
        print(month_stats)
        # for month, stats in month_stats.items():
        #     print(f"{month}: USCITE: {stats['uscite']} - ENTRATE: {stats['entrate']} - TOT: {stats['entrate'] - stats['uscite']}")

        # Creazione dell'istogramma
        months = [self.months_dict[val] for val in month_stats.keys()]
        entrate = [stats['entrate'] for stats in month_stats.values()]
        uscite = [stats['uscite'] for stats in month_stats.values()]

        bar_width = 0.35  # Larghezza delle barre
        r1 = np.arange(len(months))
        r2 = [x + bar_width + 0.1 for x in r1]  # Aggiungi un offset di 0.1 per distanziare le barre

        fig, ax = plt.subplots()
        ax.bar(r1, entrate, width=bar_width, label='Entrate')
        ax.bar(r2, uscite, width=bar_width, label='Uscite')

        plt.title(f"Entrate e Uscite {year}")
        plt.xticks([r + bar_width / 2 for r in range(len(months))], months)  # Posiziona le etichette dei mesi al centro
        plt.legend()

        # Calcola la media delle entrate e delle uscite
        media_entrate = np.mean(entrate)
        media_uscite = np.mean(uscite)

        # Aggiungi le linee orizzontali per la media delle entrate e delle uscite
        ax.axhline(y=media_entrate, color='green', linestyle='--', label=f'Media Entrate: {media_entrate:.2f}€')
        ax.axhline(y=media_uscite, color='red', linestyle='--', label=f'Media Uscite: {media_uscite:.2f}€')

        # Aggiungi le cifre in cima ad ogni barra con il simbolo dell'euro
        for i, value in enumerate(entrate):
            ax.text(r1[i], value, f'{value:.2f}€', ha='center', va='bottom')
        
        for i, value in enumerate(uscite):
            ax.text(r2[i], value, f'{value:.2f}€', ha='center', va='bottom')

        # Formatta automaticamente i valori dell'asse y con il simbolo dell'euro
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:.2f}€'))

        plt.legend()
        plt.show(block=False)


        # Calcola il totale per ogni categoria
        categories_total = {}
        for movement in stats_movements:
            category = movement.category
            if movement.amount[0] == '-':
                if category not in categories_total:
                    categories_total[category] = Decimal(0.0)
                categories_total[category] += Decimal(movement.amount[1:].replace('.', '').replace(',', '.'))

        # Ordina le categorie per il totale decrescente
        sorted_categories = sorted(categories_total.items(), key=lambda x: x[1], reverse=True)

        # Estrai le categorie e i totali ordinati
        categories, totals = zip(*sorted_categories)

        # Crea il grafico a torta senza nomi delle categorie
        plt.figure(figsize=(8, 8))
        
        # Utilizza una funzione personalizzata per l'etichetta autopct
        def autopct_func(pct):
            return f'{pct:.1f}%' if pct > 1 else ''

        pie_chart = plt.pie(totals, autopct=autopct_func, startangle=140)

        # Aggiungi una legenda personalizzata
        legend_labels = [f"{category}: {total:.2f}€" for category, total in zip(categories, totals)]
        plt.legend(pie_chart[0], legend_labels, loc="upper right", bbox_to_anchor=(1, 0, 0.5, 1))

        plt.title(f"Distribuzione delle spese per categorie - {year}")

        plt.show()