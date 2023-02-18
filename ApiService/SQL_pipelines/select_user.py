def select_user_by_id(system_user_id: int):
    query = f'SELECT * FROM USER_TABLE WHERE user_id = {system_user_id}'
    return query
