import os
import csv


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, directory=''):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        for filename in os.listdir(directory):
            if 'price' in filename and filename.endswith('.csv'):
                with open(os.path.join(directory, filename), newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    headers = next(reader)
                    product_col, price_col, weight_col = self._search_product_price_weight(headers)

                    for row in reader:
                        if product_col is not None and price_col is not None and weight_col is not None:
                            product = row[product_col]
                            price = float(row[price_col])
                            weight = float(row[weight_col])
                            price_per_kg = price / weight if weight > 0 else 0
                            self.data.append({
                                'product': product,
                                'price': price,
                                'weight': weight,
                                'file': filename,
                                'price_per_kg': price_per_kg
                            })
        # Сортировка данных по цене за кг
        self.data.sort(key=lambda x: x['price_per_kg'])

    def _search_product_price_weight(self, headers):
        '''
            Возвращает индексы столбцов для товара, цены и веса.
        '''
        product_col = next(
            (i for i, h in enumerate(headers) if h.lower() in ['товар', 'название', 'наименование', 'продукт']), None)
        price_col = next((i for i, h in enumerate(headers) if h.lower() in ['цена', 'розница']), None)
        weight_col = next((i for i, h in enumerate(headers) if h.lower() in ['фасовка', 'масса', 'вес']), None)

        return product_col, price_col, weight_col

    def export_to_html(self, fname='my_output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table border="1">
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

        for index, item in enumerate(self.data, start=1):
            result += f'''
                <tr>
                    <td>{index}</td>
                    <td>{item['product']}</td>
                    <td>{item['price']}</td>
                    <td>{item['weight']}</td>
                    <td>{item['file']}</td>
                    <td>{item['price_per_kg']:.2f}</td>
                </tr>
            '''

        result += '''
            </table>
        </body>
        </html>
        '''

        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)

    def find_text(self, text):
        '''
            Получает текст и возвращает список позиций, содержащий этот текст в названии продукта.
        '''
        filtered_data = [item for item in self.data if text.lower() in item['product'].lower()]
        return sorted(filtered_data, key=lambda x: x['price_per_kg'])


def main():

    pm = PriceMachine()
    pm.load_prices(os.getcwd())  # Укажите путь к директории с прайс-листами

    while True:
        user_input = input("Введите текст для поиска (или 'exit' для выхода): ")
        if user_input.lower() == 'exit':
            print("Работа завершена.")
            break

        results = pm.find_text(user_input)
        if results:
            print(f"{'№':<3} {'Наименование':<30} {'Цена':<10} {'Вес':<5} {'Файл':<15} {'Цена за кг.':<10}")
            for index, item in enumerate(results, start=1):
                print(
                    f"{index:<3} {item['product']:<30} {item['price']:<10} {item['weight']:<5} {item['file']:<15} {item['price_per_kg']:.2f}")
        else:
            print("Товары не найдены.")

    pm.export_to_html()

if __name__ == "__main__":
    main()
