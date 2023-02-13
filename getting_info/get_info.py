import vk_api
import time
from login_credits import phone_number, password
from MySQLDaemon import MySqlDaemon
from mysql.connector import connect, Error
from pprint import pprint
import yaml
from tqdm import tqdm

# Record system
try:
    with open("getting_info/configuration.yaml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
except FileNotFoundError:
    with open("configuration.yaml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

recordDaemon = MySqlDaemon(config=cfg)


vk_session = vk_api.VkApi(phone_number, password)
vk_session.auth()

vk = vk_session.get_api()

# GROUP_ID = -188660528
GROUP_ID = -172053584


def getData(vk_api, group_id, voting_flg=True):
    users_and_answers = []
    items = vk_api.wall.get(owner_id=group_id)["items"]
    for item in items:
        attachments = item["attachments"]
        for attachment in attachments:
            if attachment["type"] == "poll":
                poll = attachment["poll"]
                answers = poll["answers"]
                answer_ids = list(map(lambda x: x["id"], answers))
                answer_texts = list(map(lambda x: x["text"], answers))
                poll_id = poll["id"]
                tmp_query = f"SELECT * FROM FORMS_TABLE WHERE vk_form_id={poll_id}"
                if recordDaemon.mysql_get_execution_handler(tmp_query) is None:
                    
                    insert_query = f"""INSERT INTO FORMS_TABLE (vk_form_id, form_vk_created_date, form_scrapped_date, multiple_answers, form_content) 
                                      VALUES ({poll_id}, {item['date']}, {int(time.time_ns() / 1_000_000)}, "{int(poll['multiple'])}", "{poll['question']}")"""
                    recordDaemon.mysql_post_execution_handler(insert_query)
                #pprint(item)
                if voting_flg:
                    vk_api.polls.addVote(
                        owner_id=group_id, 
                        poll_id=poll_id,
                        answer_ids=answer_ids[:1])
                if not poll["anonymous"]:
                    voters = vk.polls.getVoters(
                        owner_id=group_id,
                        poll_id=poll_id,
                        answer_ids=answer_ids,
                        count=1000)
                    
                    for voter in tqdm(voters):
                        answer_id = voter["answer_id"]
                        tmp_query = f"SELECT * FROM FORMS_DETAIL_TABLE WHERE vk_answer_id={answer_id}"
                        if recordDaemon.mysql_get_execution_handler(tmp_query) is None:
                            answer_text = [ans["text"] for ans in answers if ans["id"] == answer_id][0]
                            ans_id = recordDaemon.mysql_get_execution_handler(f"SELECT form_id FROM FORMS_TABLE WHERE vk_form_id = {poll_id}")[0]
                            insert_query = f"""INSERT INTO FORMS_DETAIL_TABLE (vk_answer_id, form_id, vk_form_id, answer_content)
                                            VALUES ({answer_id}, {ans_id}, {poll_id}, "{answer_text}")"""
                            recordDaemon.mysql_post_execution_handler(insert_query)
                        for user_id in tqdm(voter["users"]["items"]):
                            user_info = vk_api.users.get(user_ids=[str(user_id)],
                                                   fields=["photo_400_orig", "sex", "bdate", "city", "country", "career", "education", "folower_count", "status"])
                            tmp_query = f"SELECT * FROM USER_TABLE WHERE vk_user_id={user_id}"
                            
                            if recordDaemon.mysql_get_execution_handler(tmp_query) is None:
                                user_info = user_info[0]
                                _user_vk_profile_url = user_info["photo_400_orig"] if "photo_400_orig" in user_info else "null"
                                _first_name = user_info["first_name"] if "first_name" in user_info else "null"
                                _last_name = user_info["last_name"] if "last_name" in user_info else "null"
                                _sex = ("male" if user_info["sex"] == 2 else "female") if "sex" in user_info else "null"
                                _bdate = user_info["bdate"] if "bdate" in user_info else "null"
                                _city = user_info["city"]["title"] if "city" in user_info else "null"
                                _country = user_info["country"]["title"] if "country" in user_info else "null"
                                if "career" in user_info and len(user_info["career"]) != 0:
                                    if "company" in user_info["career"][0]:
                                        _career = user_info["career"][0]["company"]
                                    elif type(user_info["career"][0]) == "str":
                                        _career = user_info["career"][0]
                                    else:
                                        _career = "null"
                                else:
                                    _career = "null"
                                _education = user_info["university_name"] if "university_name" in user_info else "null"
                                _friends = 0
                                _status = user_info["status"] if "status" in user_info else "null"
                                
                                insert_query = f"""INSERT INTO USER_TABLE (vk_user_id, user_vk_profile_url, user_first_name, user_sec_name, user_sex, 
                                            user_birth_date, user_city, user_country, user_job_place, user_education_place, user_number_of_friends, user_status)
                                            VALUES ({user_id}, 
                                                    "{_user_vk_profile_url}", 
                                                    "{_first_name}", 
                                                    "{_last_name}",
                                                    "{_sex}",
                                                    "{_bdate}",
                                                    "{_city}",
                                                    "{_country}",
                                                    "{_career.replace('"', "").replace("'", "")}",
                                                    "{_education.replace('"', "").replace("'", "")}",
                                                    {_friends},
                                                    "{_status.replace('"', "").replace("'", "")}")"""
                                recordDaemon.mysql_post_execution_handler(insert_query)
                                
                            tmp_query = f"SELECT * FROM USER_ANSWERS_TABLE WHERE vk_user_id={user_id} AND vk_answer_id={answer_id} AND vk_form_id={poll_id}"
                            if recordDaemon.mysql_get_execution_handler(tmp_query) is None:
                                us_id  = recordDaemon.mysql_get_execution_handler(f"SELECT user_id FROM USER_TABLE WHERE vk_user_id = {user_id}")[0]
                                pl_id  = recordDaemon.mysql_get_execution_handler(f"SELECT form_id FROM FORMS_TABLE WHERE vk_form_id = {poll_id}")[0]
                                ans_id = recordDaemon.mysql_get_execution_handler(f"SELECT answer_id FROM FORMS_DETAIL_TABLE WHERE vk_answer_id = {answer_id} AND vk_form_id = {poll_id}")[0]
                                insert_query = f"""INSERT INTO USER_ANSWERS_TABLE (user_id, vk_user_id, answer_id, vk_answer_id, form_id, vk_form_id)
                                            VALUES ({us_id}, {user_id}, {ans_id}, {answer_id}, {pl_id}, {poll_id})"""
                                recordDaemon.mysql_post_execution_handler(insert_query)
                            

    return users_and_answers

pprint(getData(vk, GROUP_ID, voting_flg=False))
