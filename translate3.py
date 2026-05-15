import os
import re

translations = {
    'en': {
        'Кабинет': 'Dashboard',
    },
    'ky': {
        'Кабинет': 'Кабинет',
    }
}

for lang in ['en', 'ky']:
    po_path = f'app/locale/{lang}/LC_MESSAGES/django.po'
    if not os.path.exists(po_path):
        continue
    
    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for ru_word, translated_word in translations[lang].items():
        # Add new translation block if it doesn't exist
        pattern = r'(msgid "' + re.escape(ru_word) + r'"\nmsgstr )""'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1"' + translated_word + r'"', content)
        else:
            # If "Кабинет" doesn't exist in the po file, we might need to run makemessages first
            pass
            
    with open(po_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Translations applied successfully.")
