from vk_api.vk_api import VkApiMethod

from src.database import BlackListDb

class Crawler:
    def __init__(self, vk: VkApiMethod, db: BlackListDb, enemy_person, enemy_group):
        self._db = db
        self._enemy_person = enemy_person
        self._enemy_group = enemy_group
        self._vk = vk

    def find_enemy_friends(self):
        friends = self._vk.friends.get(user_id=self._enemy_person)["items"]
        followers = self._vk.users.getFollowers(user_id=self._enemy_person)["items"]
        return friends + followers

    def find_enemy_members(self):
        offset = 0
        go_on = True
        members = []
        while go_on:
            batch = self._vk.groups.getMembers(group_id=self._enemy_group, offset=offset)["items"]
            count = len(batch)
            if count == 0:
                go_on = False
            else:
                members += batch
                offset += count
        return members

    def update_black_list(self):
        start_count = self._db.count()
        enemies = self.find_enemy_friends()
        reason = "A friend of %d" % self._enemy_person
        self._db.add_person(enemies, reason)
        enemies = self.find_enemy_members()
        reason = "A member of %d" % self._enemy_group
        self._db.add_person(enemies, reason)
        end_count = self._db.count()
        print("Crawler: %d new enemies were added" % (end_count - start_count))

