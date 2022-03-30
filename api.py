from queue import LifoQueue
import requests

API_BASE_URL = "https://api.adviceslip.com/advice"

class Requests:
    """ A class used for API """

    def __init__(self, id, search):
        """
        Parameters
        id : int
            advice id
        search : str
            Search query
        """
        self.id = id
        self.search = search


    def random_advice():
        """ Returns a random advice """

        resp = requests.get(API_BASE_URL)

        return resp.json()['slip']


    @classmethod
    def advice_by_id(self, id):
        """ Returns advice by id """

        resp = requests.get(f"{API_BASE_URL}/search/{id}")
        return resp.json()['slip']


    @classmethod
    def search_advice(self, search):
        """ Returns array of advice """

        resp = requests.get(f"{API_BASE_URL}/search/{search}")
        return resp.json()['slip']
