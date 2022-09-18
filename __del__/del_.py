import os
import time
from pathlib import Path
from docxtpl import DocxTemplate

DESKTOP_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
LIST_1 = [
    {'poz': 1, 'pr': 1, 'weight': 1, 'count': 1},
    {'poz': 2, 'pr': 2, 'weight': 2, 'count': 2},
    {'poz': 3, 'pr': 3, 'weight': 3, 'count': 3},
    {'poz': 4, 'pr': 4, 'weight': 4, 'count': 4},
]

LIST_2 = [
    {'poz': 10, 'pr': 10, 'weight': 10, 'count': 10},
    {'poz': 20, 'pr': 20, 'weight': 20, 'count': 20},
    {'poz': 30, 'pr': 30, 'weight': 30, 'count': 30},
    {'poz': 40, 'pr': 40, 'weight': 40, 'count': 40},
]

path_template = Path(__file__).parents[1]
doc = DocxTemplate(f'{path_template}\\__del__\\test.docx')
context = {}
context['table'] = LIST_1
context['table_2'] = LIST_2
doc.render(context)
text = str(int(time.time()))
doc.save(f'{DESKTOP_PATH}\\{text}_test.docx')
