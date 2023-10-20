import tkinter as tk
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkcalendar import Calendar
import os


# Função para adicionar a logomarca ao PDF
def add_logo(pdf_canvas, logo_path):
    pdf_canvas.drawImage(logo_path, 100, 700, width=100, height=40)


# Função para criar o recibo em PDF com logomarca e informações da empresa
def create_receipt_with_logo(name, email, service, valid_from, valid_until, items, payment_method, amount, logo_path):
    pdf_filename = f"receipt_{name}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    add_logo(c, logo_path)  # Adicione a logomarca

    c.drawString(100, 670, "Academia Boa Forma M. T. Carvalho Lopes")
    c.drawString(100, 655, "Rua Gilberto Camara, 987 - São Gerardo")
    c.drawString(100, 640, "Fone: (85) 99717-2461 - Fortaleza - Ceará")

    c.drawString(100, 620, "Recibo")
    c.drawString(100, 600, f"Nome: {name}")
    c.drawString(100, 580, f"E-mail: {email}")

    # Calcula a data de validade com base no último dia do mês correspondente
    if valid_from.month in [1, 3, 5, 7, 8, 10, 12]:
        valid_until = valid_from + timedelta(days=31)
    elif valid_from.month in [4, 6, 9, 11]:
        valid_until = valid_from + timedelta(days=30)
    else:
        # Verificar se o ano é bissexto
        if (valid_from.year % 4 == 0 and valid_from.year % 100 != 0) or (valid_from.year % 400 == 0):
            valid_until = valid_from + timedelta(days=29)
        else:
            valid_until = valid_from + timedelta(days=28)

    c.drawString(100, 560,
                 f"Pagamento: {valid_from.strftime('%d/%m/%Y')} até {valid_until.strftime('%d/%m/%Y')}")
    c.drawString(100, 540, f"Serviço: {service}")
    c.drawString(100, 520, f"mensalidade: {items}")
    c.drawString(100, 500, f"Forma de pagamento: {payment_method}")
    c.drawString(100, 480, f"Valor: R$ {amount}")

    c.save()

    return pdf_filename


# Função para abrir o PDF
def open_pdf(pdf_filename):
    os.system(pdf_filename)


# Função para calcular o total com base nos mensalidade e na forma de pagamento
def calculate_total():
    items = items_entry.get()
    if items:
        items = int(items)
        payment_method = payment_method_var.get()
        if payment_method == "Dinheiro/Pix":
            total = items * 60
        else:
            total = items * 65
        amount_label.config(text=f"Total: R$ {total}")
        return total  # Retorne o valor total
    else:
        amount_label.config(text="Total: R$ 0")
        return 0  # Retorne 0 se não houver mensalidade


# Função para enviar o recibo
def send_receipt():
    name = name_entry.get()
    email = email_entry.get()
    service = "Musculação"
    items = items_entry.get()
    payment_method = payment_method_var.get()
    valid_from_str = cal.get_date()
    valid_from = datetime.strptime(valid_from_str, "%Y-%m-%d")

    total = calculate_total()  # Calcular o total

    # Substitua pelo caminho completo para sua logomarca
    logo_path = "./img/logo.jpg"

    pdf_filename = create_receipt_with_logo(name, email, service, valid_from, None, items, payment_method, total,
                                            logo_path)

    # Abra o PDF após a geração
    open_pdf(pdf_filename)


# Crie a janela principal
root = tk.Tk()
root.title("App de Recibos")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

name_label = tk.Label(frame, text="Nome:")
name_label.grid(row=0, column=0, sticky="e")

name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=1, sticky="w")

email_label = tk.Label(frame, text="E-mail:")
email_label.grid(row=1, column=0, sticky="e")

email_entry = tk.Entry(frame)
email_entry.grid(row=1, column=1, sticky="w")

cal = Calendar(frame, selectmode='day', date_pattern="yyyy-mm-dd")
cal.grid(row=2, column=0, columnspan=2, sticky="we")

payment_label = tk.Label(frame, text="Pagamento:")
payment_label.grid(row=3, column=0, sticky="e")

payment_method_var = tk.StringVar()
payment_method_var.set("Dinheiro/Pix")
payment_method_radiobutton = tk.Radiobutton(frame, text="Dinheiro/Pix", variable=payment_method_var,
                                            value="Dinheiro/Pix")
payment_method_radiobutton.grid(row=3, column=1, sticky="w")

payment_method_radiobutton2 = tk.Radiobutton(frame, text="Cartão de Crédito", variable=payment_method_var,
                                             value="Cartão de Crédito")
payment_method_radiobutton2.grid(row=4, column=1, sticky="w")

items_label = tk.Label(frame, text="mensalidade:")
items_label.grid(row=5, column=0, sticky="e")

items_entry = tk.Entry(frame)
items_entry.grid(row=5, column=1, sticky="w")

calculate_button = tk.Button(frame, text="Calcular Total", command=calculate_total)
calculate_button.grid(row=6, column=0, columnspan=2)

amount_label = tk.Label(frame, text="Total: R$ 0")
amount_label.grid(row=7, column=0, columnspan=2)

# Botão para enviar o recibo
send_button = tk.Button(frame, text="Gerar Recibo em PDF", command=send_receipt)
send_button.grid(row=8, column=0, columnspan=2)

root.mainloop()
