def select_user_by_id(system_user_id: int):
    query = f'SELECT * FROM USER_TABLE WHERE user_id = {system_user_id}'
    return query


def select_forms_by_user_id(system_user_id: int):
    query = f'SELECT form_id, answer_id FROM USER_ANSWERS_TABLE WHERE user_id = {system_user_id}'
    return query


def all_answers_by_form_id(system_form_id: int):
    query = f'SELECT answer_id FROM FORMS_DETAIL_TABLE WHERE form_id = {system_form_id}'
    return query
