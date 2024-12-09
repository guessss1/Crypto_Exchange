from tkinter import *
from tkinter import ttk, messagebox as mb
import requests
from datetime import datetime

# Список криптовалют
cryptocurrencies = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum",
    "ripple": "Ripple",
    "cardano": "Cardano"
}

# Список денежных валют
currencies = {
    "usd": "Доллар США",
    "eur": "Евро",
    "rub": "Российский рубль"
}

# Функция для получения курса обмена выбранной криптовалюты к денежной валюте
def get_exchange_rate(crypto_id, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        current_datetime = datetime.now()
        return data[crypto_id][currency], current_datetime
    except requests.exceptions.RequestException as e:
        mb.showerror("Ошибка", f"Ошибка запроса к API: {e}")
    except KeyError:
        mb.showerror("Ошибка", "Не удалось получить данные о выбранной криптовалюте.")
    return None, None

# Функция для отображения курса обмена
def display_exchange_rate():
    crypto_id = crypto_combobox.get()
    currency = currency_combobox.get()

    if crypto_id and currency:
        rate, current_datetime = get_exchange_rate(crypto_id, currency)
        if rate is not None and current_datetime is not None:
            # Определяем количество десятичных знаков
            if crypto_id in ['bitcoin', 'ethereum']:
                formatted_rate = f"{rate:,.2f}".replace(",", " ")
            else:  # Для Ripple и Cardano оставляем шесть десятичных знаков
                formatted_rate = f"{rate:,.6f}".replace(",", " ")

            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            result_label.config(
                text=f"1 {cryptocurrencies[crypto_id]} = {formatted_rate} {currencies[currency]}\nДата и время: {formatted_datetime}")
        else:
            result_label.config(text="Ошибка при получении курса обмена.")
    else:
        mb.showwarning("Внимание", "Пожалуйста, выберите криптовалюту и валюту.")

# Создание графического интерфейса
window = Tk()
window.title("Курс обмена криптовалюты")
window.geometry("450x350")

# Заголовок окна
title_label = Label(window, text="Курс обмена криптовалюты", font=("Arial", 16))
title_label.pack(padx=10, pady=10)

# Базовая криптовалюта
Label(window, text="Выберите криптовалюту:").pack(padx=10, pady=5)
crypto_combobox = ttk.Combobox(window, values=list(cryptocurrencies.keys()))
crypto_combobox.pack(padx=10, pady=5)

# Целевая денежная валюта
Label(window, text="Выберите денежную валюту:").pack(padx=10, pady=5)
currency_combobox = ttk.Combobox(window, values=list(currencies.keys()))
currency_combobox.pack(padx=10, pady=5)

# Кнопка для получения курса обмена
Button(window, text="Получить курс обмена", command=display_exchange_rate).pack(padx=10, pady=10)

# Метка для отображения результата
result_label = Label(window, text="Курс на дату и время будет отображен здесь", font=("Arial", 14))
result_label.pack(padx=10, pady=20)

# Запуск приложения
window.mainloop()
