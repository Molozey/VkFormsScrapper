import vk_api
from login_credits import phone_number, password
from MySQLDaemon import MySqlDaemon
from pprint import pprint
import yaml

with open("configuration.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

recordDaemon = MySqlDaemon(config=cfg)

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
                tmp_query = "SELECT * FROM tablename WHERE vk_form_id=%(poll_id)s"
                cursor.execute(tmp_query)
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
                    for user_id in voter["users"]["items"]:
                        user_and_answer = {
                            "user_id"  : user_id,
                            "answer_id": answer_id,
                            "poll_id"  : poll_id
                        }
                        users_and_answers.append(user_and_answer)
    return users_and_answers

pprint(getData(vk, GROUP_ID, voting_flg=False))
