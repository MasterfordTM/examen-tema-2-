import requests
class API:
    def __init__(self, base_url):
        self.__base_url = base_url

    def fetch_records(self):
        try:
            response = requests.get(self.__base_url)
            response.raise_for_status()
            return response.json() if isinstance(response.json(), list) else []
        except (requests.RequestException, ValueError):
            return []

    def fetch_record_by_id(self, record_id):
        records = self.fetch_records()
        for record in records:
            if str(record.get('generacion')) == str(record_id):
                return record
        return None