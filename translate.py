import os
import re

translations = {
    'en': {
        'Главная': 'Dashboard',
        'Устройства': 'Devices',
        'Мониторинг': 'Monitoring',
        'Уведомления': 'Notifications',
        'Настройки': 'Settings',
        'Выйти': 'Logout',
        'Аналитика и Мониторинг': 'Analytics & Monitoring',
        'Текущая нагрузка': 'Current Load',
        'Потреблено за 24ч': 'Consumed 24h',
        'Пик нагрузки': 'Peak Load',
        'Сэкономлено CO₂': 'CO₂ Saved',
        'Общее потребление энергии (кВт·ч)': 'Total Energy Consumption (kWh)',
        'Потребление по зонам': 'Consumption by Zone',
        'Устройства организации': 'Organization Devices',
        'Всего устройств': 'Total Devices',
        'Онлайн': 'Online',
        'Офлайн': 'Offline',
        'Суммарная мощность': 'Total Power',
        'Суммарная энергия': 'Total Energy',
        'Реле включено': 'Relay ON',
        'Добавить устройство': 'Add Device',
    },
    'ky': {
        'Главная': 'Башкы бет',
        'Устройства': 'Түзмөктөр',
        'Мониторинг': 'Мониторинг',
        'Уведомления': 'Билдирүүлөр',
        'Настройки': 'Жөндөөлөр',
        'Выйти': 'Чыгуу',
        'Аналитика и Мониторинг': 'Аналитика жана Мониторинг',
        'Текущая нагрузка': 'Учурдагы жүк',
        'Потреблено за 24ч': '24с сарпталган',
        'Пик нагрузки': 'Эң жогорку жүк',
        'Сэкономлено CO₂': 'CO₂ үнөмдөлдү',
        'Общее потребление энергии (кВт·ч)': 'Жалпы энергия керектөө (кВт·с)',
        'Потребление по зонам': 'Аймактар боюнча керектөө',
        'Устройства организации': 'Уюмдун түзмөктөрү',
        'Всего устройств': 'Бардык түзмөктөр',
        'Онлайн': 'Онлайн',
        'Офлайн': 'Офлайн',
        'Суммарная мощность': 'Жалпы кубаттуулук',
        'Суммарная энергия': 'Жалпы энергия',
        'Реле включено': 'Реле күйгүзүлдү',
        'Добавить устройство': 'Түзмөк кошуу',
    }
}

for lang in ['en', 'ky']:
    po_path = f'app/locale/{lang}/LC_MESSAGES/django.po'
    if not os.path.exists(po_path):
        continue
    
    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for ru_word, translated_word in translations[lang].items():
        # Match msgid "RU_WORD"\nmsgstr ""
        pattern = r'(msgid "' + re.escape(ru_word) + r'"\nmsgstr )""'
        replacement = r'\1"' + translated_word + r'"'
        content = re.sub(pattern, replacement, content)
        
    with open(po_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Translations applied successfully.")
