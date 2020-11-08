import vk_api
from src.settings import *

session = vk_api.VkApi(token=my_app_access_token, app_id=my_app_id)
vk = session.get_api()
res = vk.groups.getRequests(group_id=my_group_id)
print(res)


