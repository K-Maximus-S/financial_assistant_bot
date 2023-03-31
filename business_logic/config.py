# импортируем модуль emoji для отображения эмоджи
from emoji import emojize

# версия приложения
VERSION = '0.0.2'
# автор приложния
AUTHOR = '@K_Maximus_S'

# кнопки управления
KEYBOARD = {
    'FINANCE': emojize(':bookmark_tabs: Финансы'),

    'List_goal': 'List_goal',
    'Edit_goal': 'Edit_goal',
    'Add_goal': 'Add_goal',
    'List_income': 'List_income',
    'Edit_income': 'Edit_income',
    'Add_income': 'Add_income',
    'GOAL_EDIT': emojize(':open_file_folder: Изменить цели'),
    'INFO': emojize(':speech_balloon: О проекте'),
    'SETTINGS': emojize('⚙️ Настройки'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'X': emojize('❌'),
    'DOUWN': emojize('🔽'),
    'UP': emojize('🔼'),
    'COPY': '© Finance'
}

