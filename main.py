import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField(label="Tipo", value="")
    input_marca = ft.TextField(label="Marca", value="")
    input_anno = ft.TextField(label="Anno", value="")

    mostraprezzo = ft.TextField(width=100,
                          disabled=True,
                          value=0)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def aggiunta_strumento(e):
        try:
            int(input_anno.value)
            if mostraprezzo.value > 0:
                deposito.aggiungi_strumento(input_tipo.value, input_marca.value, input_anno.value, mostraprezzo.value)
                aggiorna_lista_strumenti()
            else:
                alert.show_alert("Prezzo non valido")
        except ValueError:
            alert.show_alert("Inserire un numero valido per la data")
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        mostraprezzo.value = 0
        page.update()

    def aumento(e):
        valore = mostraprezzo.value
        mostraprezzo.value = valore + 1
        mostraprezzo.update()

    def diminuzione(e):
        valore = mostraprezzo.value
        mostraprezzo.value = valore - 1
        mostraprezzo.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi_strumento = ft.ElevatedButton(text="Aggiungi", on_click=aggiunta_strumento)

    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           on_click=aumento)
    btnMinus =ft.IconButton(icon=ft.Icons.REMOVE,
                            icon_color="red",
                            on_click=diminuzione)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),

        # Sezione 3
        ft.Text(value= "Aggiungi un nuovo strumento", size=20),
        ft.Row(controls=[input_tipo, input_marca, input_anno,btnMinus, mostraprezzo, btnAdd],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[pulsante_aggiungi_strumento],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.app(target=main)
