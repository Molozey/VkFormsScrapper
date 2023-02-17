import vk_api
from vk_api.exceptions import ApiError
import time
from login_credits import phone_number, password, access_token
from MySQLDaemon import MySqlDaemon
from mysql.connector import connect, Error
from pprint import pprint
import yaml
from tqdm import tqdm


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device

def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


# Record system
try:
    with open("getting_info/configuration.yaml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
except FileNotFoundError:
    with open("configuration.yaml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

recordDaemon = MySqlDaemon(config=cfg)

global vk_session, vk
# vk_session = vk.VkApi(phone_number, password, auth_handler=auth_handler,)
vk_session = vk_api.VkApi(phone_number, password, token=access_token, captcha_handler=captcha_handler)
# vk_session.auth()


vk = vk_session.get_api()

# GROUP_ID = -188660528
GROUP_ID = -172053584


def getData(group_id, voting_flg=True):
    global vk
    users_and_answers = []
    # TODO: max request by get is 100. Need to use offset
    # 19000
    offset = 0
    while True:
        items = vk.wall.get(owner_id=group_id, count=100, offset=offset)["items"] # 0 -> 100
        # items = vk.wall.get(owner_id=group_id, count=100, offset=100)["items"] # 100 -> 200
        for item in tqdm(items, desc="Total Forms"):
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
                                            VALUES ({poll_id}, {item['date']}, {int(time.time_ns() / 1_000_000)}, "{int(poll['multiple'])}", "{poll['question'].replace('"', "").replace("'", "")}")"""
                        recordDaemon.mysql_post_execution_handler(insert_query)
                    if voting_flg and not poll["closed"] and poll["can_vote"]:
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
                        
                        for voter in tqdm(voters, desc="Form Answer", leave=False):
                            answer_id = voter["answer_id"]
                            tmp_query = f"SELECT * FROM FORMS_DETAIL_TABLE WHERE vk_answer_id={answer_id}"
                            if recordDaemon.mysql_get_execution_handler(tmp_query) is None:
                                answer_text = [ans["text"].replace('"', "").replace("'", "") for ans in answers if ans["id"] == answer_id][0]
                                ans_id = recordDaemon.mysql_get_execution_handler(f"SELECT form_id FROM FORMS_TABLE WHERE vk_form_id = {poll_id}")[0]
                                insert_query = f"""INSERT INTO FORMS_DETAIL_TABLE (vk_answer_id, form_id, vk_form_id, answer_content)
                                                VALUES ({answer_id}, {ans_id}, {poll_id}, "{answer_text}")"""
                                recordDaemon.mysql_post_execution_handler(insert_query)
                                
                            users = []
                            
                            all_fucking_users = vk.users.get(user_ids=voter["users"]["items"],
                                                        fields=["photo_400_orig", "sex", "bdate", "city", "country", "career", "education", "folower_count", "status"])
                                
                            for user_info in all_fucking_users:
                                tmp_query = f"SELECT * FROM USER_TABLE WHERE vk_user_id={user_info['id']}"
                                
                                if recordDaemon.mysql_get_execution_handler(tmp_query) is None:
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
                                    users.append((
                                        user_info['id'], 
                                        _user_vk_profile_url, 
                                        _first_name.replace('"', "").replace("'", ""), 
                                        _last_name.replace('"', "").replace("'", ""),
                                        _sex,
                                        _bdate,
                                        _city.replace('"', "").replace("'", ""),
                                        _country.replace('"', "").replace("'", ""),
                                        _career.replace('"', "").replace("'", ""),
                                        _education.replace('"', "").replace("'", ""),
                                        _friends,
                                        _status.replace('"', "").replace("'", "")
                                    ))
                                    
                                    
                                    
                            insert_query = f"""INSERT INTO USER_TABLE (vk_user_id, user_vk_profile_url, user_first_name, user_sec_name, user_sex, 
                                                user_birth_date, user_city, user_country, user_job_place, user_education_place, user_number_of_friends, user_status)
                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                            """
                            recordDaemon.mysql_post_execution_handler(insert_query, multi=True, input=users)
                            
                            for user_info in all_fucking_users:
                            
                                tmp_query = f"SELECT * FROM USER_ANSWERS_TABLE WHERE vk_user_id={user_info['id']} AND vk_answer_id={answer_id} AND vk_form_id={poll_id}"
                                if recordDaemon.mysql_get_execution_handler(tmp_query) is None:
                                    us_id  = recordDaemon.mysql_get_execution_handler(f"SELECT user_id FROM USER_TABLE WHERE vk_user_id = {user_info['id']}")[0]
                                    pl_id  = recordDaemon.mysql_get_execution_handler(f"SELECT form_id FROM FORMS_TABLE WHERE vk_form_id = {poll_id}")[0]
                                    ans_id = recordDaemon.mysql_get_execution_handler(f"SELECT answer_id FROM FORMS_DETAIL_TABLE WHERE vk_answer_id = {answer_id} AND vk_form_id = {poll_id}")[0]
                                    insert_query = f"""INSERT INTO USER_ANSWERS_TABLE (user_id, vk_user_id, answer_id, vk_answer_id, form_id, vk_form_id)
                                                VALUES ({us_id}, {user_info['id']}, {ans_id}, {answer_id}, {pl_id}, {poll_id})"""
                                    recordDaemon.mysql_post_execution_handler(insert_query)
                print("Wait until new vote")
                # time.sleep(30)
        offset += 100

getData(GROUP_ID, voting_flg=True)

