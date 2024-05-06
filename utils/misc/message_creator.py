def get_info_message(data: dict):
    text = ''
    for key, value in data.items():
        if key.lower() in ('фио', 'дата рождения', 'категория', 'должность', 'деятельность'):
            text += f'<b>{key}</b>: {value}\n\n'
    return text
