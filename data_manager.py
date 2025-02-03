import os
import requests


class DataManager:
    # This class is used for talking to Google Sheet

    def __init__(self):
        self.endpoint = os.getenv("SHEETY_ENDPOINT_STAT")
        self.header = {
            "Authorization": os.getenv("SHEETY_KEY_STAT")
        }
        # self.approved_users = self.get_users()
        self.data = {}

    def update_data(self, date, volume):
        parameters = {
            "egg": {
                "date": date,
                "volume": volume
            }
        }
        response = requests.post(url=f"{self.endpoint}eggs", json=parameters, headers=self.header)
        if response.status_code == 200:
            return "Данные успешно сохранены"
        else:
            return f"Ошибка при отправке данных: {response.status_code}"

    def get_average(self):
        response = requests.get(url=f"{self.endpoint}averages", headers=self.header)
        response.raise_for_status()
        self.data = response.json()["averages"]
        return self.data

    # def get_approved_users(self):
    #     pass
