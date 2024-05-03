import random


class User:
    async def get_timezones(self, quantity: list) -> list:
        timezones = ['Africa/Nairobi', 'Europe/Moscow', 'America/New_York']

        result = []
        for item in quantity:
            timezone_dict = {'user_id': item, 'timezone': random.choice(timezones)}
            result.append(timezone_dict)
        return result
