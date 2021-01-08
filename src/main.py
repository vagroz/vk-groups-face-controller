import vk_api

from src.crawler import Crawler
from src.database import BlackListDb
from src.settings_my import *

session = vk_api.VkApi(token=my_app_access_token, app_id=my_app_id)
vk = session.get_api()
db = BlackListDb(db_file)
crawler = Crawler(vk, db, enemy_user_id, enemy_community_id)
