def select_form_by_id(system_form_id: int):
    query = f'SELECT * FROM FORMS_TABLE WHERE form_id = {system_form_id}'
    return query


def select_form_answers_by_system_id(system_form_id: int):
    query = f'SELECT * FROM FORMS_DETAIL_TABLE WHERE form_id = {system_form_id}'
    return query