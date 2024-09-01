import os
import pandas as pd


class PriceMachine:

    def __init__(self):
        self.data = []
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

        Допустимые названия для столбца с весом (в кг.):
            вес
            масса
            фасовка
        '''
        for filename in os.listdir(directory):
            if 'price' in filename.lower() and filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                print(f'Загружаю файл: {file_path}')
                data_frame = pd.read_csv(file_path, sep=',')

                # Находим индексы нужных колонки
                product_col, price_col, weight_col = self._search_product_price_weight(data_frame.columns)

                for index, row in data_frame.iterrows():
                    if product_col is not None and price_col is not None and weight_col is not None:
                        self.name_length += 1
                        self.data.append({
                            'Номер': self.name_length,
                            'Наименование': row[product_col],
                            'Цена': row[price_col],
                            'Фасовка': row[weight_col],
                            'Файл': filename,
                            'Цена за кг.': row[price_col] / row[weight_col] if row[weight_col] != 0 else 0
                        })

        # Сортировка данных по цене за кг
        self.data = self.find_text(self.data)

        # Присвоение номера каждому элементу после сортировки
        self.name_length = len(self.data)
        for idx, item in enumerate(self.data):
            item['Номер'] = idx + 1  # Присваиваем номер начиная с 1

    def _search_product_price_weight(self, headers):
        '''
        Возвращает индексы столбцов: продукт, цена, вес
        '''
        product_col = price_col = weight_col = None

        for header in headers:
            if header.lower() in ['товар', 'название', 'наименование', 'продукт']:
                product_col = header
            elif header.lower() in ['цена', 'розница']:
                price_col = header
            elif header.lower() in ['вес', 'масса', 'фасовка']:
                weight_col = header

        return product_col, price_col, weight_col

    def export_to_html(self, fname='my_output.html'):
        '''
        Экспортирует все данные в HTML формат.
        '''
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
                    <th>Наименование</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

        for item in self.data:
            result += f'''
                <tr>
                    <td>{item['Номер']}</td>
                    <td>{item['Наименование']}</td>
                    <td>{item['Цена']}</td>
                    <td>{item['Фасовка']}</td>
                    <td>{item['Файл']}</td>
                    <td>{item['Цена за кг.']:.2f}</td>
                </tr>
            '''

        result += '''
            </table>
        </body>
        </html>
        '''

        with open(fname, 'w', encoding='utf-8') as file:
            file.write(result)

    def find_text(self, text):
        '''
        Получает текст и возвращает список позиций, содержащий этот текст в названии продукта.
        '''

        return sorted(text, key=lambda x: x['Цена за кг.'])


# Пример использования
if __name__ == "__main__":
    pm = PriceMachine()
    pm.load_prices(os.getcwd())  # Замените на путь к вашей директории

    pm.export_to_html('my_output.html')
    print("Данные успешно экспортированы в my_output.html")
