from ApiService.TestFlask import db
from pprint import pprint

users_form_to_answer = dict()

for form_id, answer_id in db.mysql_get_execution_handler("SELECT form_id, answer_id FROM USER_ANSWERS_TABLE WHERE user_id = 1", multi=True):
    if form_id not in users_form_to_answer.keys():
        users_form_to_answer[form_id] = [answer_id]
    else:
        users_form_to_answer[form_id].append(answer_id)

pprint(users_form_to_answer)
