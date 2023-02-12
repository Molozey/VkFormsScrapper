import vk_api
import time
from login_credits import phone_number, password
from MySQLDaemon import MySqlDaemon
from pprint import pprint
import yaml

try:
    with connect(host="localhost") as connection:
        create_db_query = "CREATE DATABASE VK_forms_scrapper"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
except Error as e:
    print(e)
    
create_tables_query = """create table FORMS_TABLE
(
    form_id              bigint auto_increment comment 'system form id'
        primary key,
    vk_form_id           bigint          not null comment 'vk form id',
    form_vk_created_date bigint          null comment 'When form was created at VK',
    form_scrapped_date   bigint          not null comment 'When form was scrapped by system',
    multiple_answers     enum ('0', '1') not null comment 'User can select several answers',
    form_content         text            null,
    constraint FORMS_TABLE_pk
        unique (vk_form_id)
);

raise NotImplementedError
vk_session = vk_api.VkApi(phone_number, password)
vk_session.auth()

vk = vk_session.get_api()

GROUP_ID = -188660528

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
                poll_id = poll["id"]
                tmp_query = "SELECT * FROM FORMS_TABLE WHERE vk_form_id=%(poll_id)s"
                cursor.execute(tmp_query)
                if cursor.rowcount == 0:
                    form_info = {
                        "vk_form_id"           : poll_id,
                        "form_vk_created_date" : item["date"],
                        "form_scrapped_date" : int(time.time_ns() / 1_000_000),
                        "multiple_answers"     : poll["multiple"],
                        "form_content"         : poll["question"]
                    }
                    insert_query = (
                        "INSERT INTO FORMS_TABLE (vk_form_id, form_vk_created_date, form_scrapped_date, multiple_answers, form_content) "
                        "VALUES (%(vk_form_id)s, %(form_vk_created_date)s, %(form_scrapped_date)s, %(multiple_answers)s, %(form_content)s)"
                        )
                    cursor.execute(insert_query, form_info)
                    
                if voting_flg:
                    vk_api.polls.addVote(
                        owner_id=group_id, 
                        poll_id=poll_id,
                        answer_ids=answer_ids[:1])
                           
                voters = vk.polls.getVoters(
                    owner_id=group_id,
                    poll_id=poll_id,
                    answer_ids=answer_ids)
                
                for voter in voters:
                    answer_id = voter["answer_id"]
                    tmp_query = "SELECT * FROM FORMS_DETAIL_TABLE WHERE vk_answer_id=%(answer_id)s"
                    cursor.execute(tmp_query)
                    if cursor.rowcount == 0:
                        form_info = {
                            "vk_form_id"           : poll_id,
                            "form_vk_created_date" : item["date"],
                            "form_scrapped_date" : int(time.time_ns() / 1_000_000),
                            "multiple_answers"     : poll["multiple"],
                            "form_content"         : poll["question"]
                        }
                        insert_query = (
                            "INSERT INTO FORMS_TABLE (vk_form_id, form_vk_created_date, form_scrapped_date, multiple_answers, form_content) "
                            "VALUES (%(vk_form_id)s, %(form_vk_created_date)s, %(form_scrapped_date)s, %(multiple_answers)s, %(form_content)s)"
                            )
                        cursor.execute(insert_query, form_info)
                    for user_id in voter["users"]["items"]:
                        tmp_query = "SELECT * FROM FORMS_TABLE WHERE vk_form_id=%(poll_id)s"
                        cursor.execute(tmp_query)
                        if cursor.rowcount == 0:
                            form_info = {
                                "vk_form_id"           : poll_id,
                                "form_vk_created_date" : item["date"],
                                "form_scrapped_date" : int(time.time_ns() / 1_000_000),
                                "multiple_answers"     : poll["multiple"],
                                "form_content"         : poll["question"]
                            }
                            insert_query = (
                                "INSERT INTO FORMS_TABLE (vk_form_id, form_vk_created_date, form_scrapped_date, multiple_answers, form_content) "
                                "VALUES (%(vk_form_id)s, %(form_vk_created_date)s, %(form_scrapped_date)s, %(multiple_answers)s, %(form_content)s)"
                                )
                            cursor.execute(insert_query, form_info)
                    
    return users_and_answers

pprint(getData(vk, GROUP_ID, voting_flg=False))
