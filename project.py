import os
import csv

class PriceMachine:
    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, directory=''):
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
        print(directory)

    def _search_product_price_weight(self, headers):
        product_col = next(
            (i for i, h in enumerate(headers) if h.lower() in ['товар', 'название', 'наименование', 'продукт']), None)
        price_col = next((i for i, h in enumerate(headers) if h.lower() in ['цена', 'розница']), None)
        weight_col = next((i for i, h in enumerate(headers) if h.lower() in ['фасовка', 'масса', 'вес']), None)

        return product_col, price_col, weight_col

    def export_to_html(self, text, fname='my_output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
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

        for item in text:
            result += f'''
                        <tr>
                            <td>{item['index']}</td>
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
        filtered_data = [item for item in self.data if text.lower() in item['product'].lower()]
        return sorted(filtered_data, key=lambda x: x['price_per_kg'])

def main():
    pm = PriceMachine()
    pm.load_prices(os.getcwd())
    while True:
        user_input = input("Введите текст для поиска (или 'exit' для выхода): ")
        if user_input.lower() == 'exit':
            print("Работа завершена.")
            break
        results = pm.find_text(user_input)
        if results:
            print(f"{'№':<3} {'Наименование':<30} {'Цена':<10} {'Вес':<5} {'Файл':<15} {'Цена за кг.':<10}")
            output_data = []
            for index, item in enumerate(results, start=1):
                output_data.append({
                    'index': index,
                    'product': item['product'],
                    'price': item['price'],
                    'weight': item['weight'],
                    'file': item['file'],
                    'price_per_kg': item['price_per_kg']
                })
                print(
                    f"{index:<3} {item['product']:<30} {item['price']:<10} {item['weight']:<5} {item['file']:<15} {item['price_per_kg']:.2f}")

            # Экспорт в HTML после вывода в консоль
            pm.export_to_html(output_data)
        else:
            print("Товары не найдены.")


if __name__ == "__main__":
    main()


