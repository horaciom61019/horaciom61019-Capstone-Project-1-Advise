from queue import LifoQueue
import requests

API_BASE_URL = "https://api.adviceslip.com/advice"

resp = requests.get(API_BASE_URL)

def random_advise():
    """ Returns a random advise """

    resp = requests.get(API_BASE_URL)
    print(resp.json())


def advise_by_id(id):
    """ Returns advice by id """

    resp = requests.get(f"{API_BASE_URL}/search/{id}")
    print(resp.json())


def search_advise(search):
    """ Returns array of advice """

    resp = requests.get(f"{API_BASE_URL}/search/{search}")
    return resp.json()

