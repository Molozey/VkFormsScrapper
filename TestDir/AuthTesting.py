import random
from LoginCredits import login, password
from pprint import pprint
import vk_api


def two_factor():
    code = input('Code? ')
    return str(code), True


def auth():
    vk_session = vk_api.VkApi(login, password)
    vk: vk_api.vk_api.VkApiMethod = vk_session.get_api()

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return -1

    # GROUP_ID = -188660528
    KPSO_ID = -172053584
    GROUP_ID = KPSO_ID
    print('ok!')
    # wall = tools.get_all('account.getInfo', 100, {'owner_id': 503295363})
    # wall = tools.get_all('account.getInfo', 1, {'fields': "country"})
    # print(vk.account.getProfileInfo())
    number = str(random.randint(0, 666))

    # print(vk.users.get(user_ids=["503295363", "212585042"],
    #                    fields=["bdate", "city", "country", "sex"]))
    # print(wall)
    kpso_wall = vk.wall.get(owner_id=GROUP_ID)["items"]
    obj = kpso_wall[0]
    pprint(obj)

    answer_ids = obj["attachments"]
    print("=========" * 30)
    inside_poll = answer_ids[0]["poll"]
    pprint(inside_poll)
    list_id_answers = list(map(lambda x: x["id"], inside_poll["answers"]))
    pool_id = inside_poll["id"]

    voting = vk.polls.addVote(owner_id=GROUP_ID, poll_id=pool_id, answer_ids=list_id_answers[:1])
    kpso_members = vk.polls.getVoters(owner_id=GROUP_ID,
                                      poll_id=pool_id,
                                      answer_ids=list_id_answers,
                                      count=1_000)

    pprint(kpso_members)


if __name__ == '__main__':
    auth()
