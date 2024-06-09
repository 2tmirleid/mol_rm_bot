import os

import yaml


async def load_lexicon() -> dict:
    # Получаем путь к директории, в которой находится этот скрипт
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Формируем полный путь к файлу lexicon.yaml
    file_path = os.path.join(script_dir, 'lexicon.yaml')

    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.load(file, Loader=yaml.FullLoader)
