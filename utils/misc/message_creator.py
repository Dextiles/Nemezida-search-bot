def get_info_message(data: dict):
    text = ''
    for key, value in data.items():
        if key.lower() in ('фио', 'дата рождения', 'категория', 'должность', 'деятельность'):
            text += f'<b>{key}</b>: {value}\n\n'
    return text


def get_info_msg_offline(report: dict) -> str:
    for key, value in report.items():
        if not value[0]:
            report[key][0] = 'Нет данных'
    return (f'<b>ФИО:</b> {report["post_title"][0]}\n\n'
            f'<b>Дата рождения:</b> {report["data_rozhdeniya"][0]}\n\n'
            f'<b>Адрес проживания:</b> {report["prozhivaet_po_adresu"][0]}\n\n'
            f'<b>Категория:</b> {report["kategoriya"][0]}\n\n'
            f'<b>Деятельность:</b> {report["deyatelnost"][0]}')
