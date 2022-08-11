import json
import requests

# tools 


headers = {
        'Content-type':'application/json', 
        'Accept':'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}


HOST = "localhost"
PORT = "8000"



# apis functions 

def list_words_api(telegram_id, *categories):
    if "all categories" in categories or categories == None:
        r = requests.get(f'http://{HOST}:{PORT}/api/flash-card/{telegram_id}/words/')
        return r.json()
    
    elif categories != ():
        category = ""
        for c in categories:
            category += c
            category += ','
        r = requests.get(f'http://{HOST}:{PORT}/api/flash-card/{telegram_id}/words/?categories={category}')

        return r.json()

def create_word_api(telegram_id, english, persian, category):
    data = {
        "telegram_user_id": int(telegram_id),
        "english": english,
        "persian": persian,
        "category": category
    }

    r = requests.post(f'http://{HOST}:{PORT}/api/flash-card/create/word/', headers=headers, data= json.dumps(data))
    if r.status_code == 201:
        return "Created!"
    else:
        return "Something went wrong!"


def delete_word_api(telegram_id, word_id):
    r = requests.delete(f'http://{HOST}:{PORT}/api/flash-card/{telegram_id}/words/{word_id}/')
    if r.status_code == 204:
        return "Deleted!"
    else:
        return "Word Not Found!"


def list_categories_api(telegram_id):
    r = requests.get(f'http://{HOST}:{PORT}/api/flash-card/{telegram_id}/category/', headers=headers)
    return r.json()


def create_category_api(telegram_id, title):
    data = {
        "title": title,
    }

    r = requests.post(f'http://{HOST}:{PORT}/api/flash-card/{telegram_id}/category/', headers=headers, data=json.dumps(data))
    if r.status_code == 201:
        return "Created!"
    else:
        return "Something went wrong!"


def delete_category_api(telegram_id, category_id):
    r = requests.delete(f'http://{HOST}:{PORT}/api/flash-card/{telegram_id}/category/{category_id}/')
    if r.status_code == 204:
        return "Deleted!"
    else:
        return "Category Not Found!"
    

def retrieve_user_api(telegram_id):
    r = requests.get(f'http://{HOST}:{PORT}/api/flash-card/user/{telegram_id}/')
    if r.status_code == 200:
        return r.text
    return "User Not Found!"


def create_user_api(telegram_id, username):
    data = {
        "telegram_user_id" : int(telegram_id),
        "username": username
    }

    r = requests.post(f'http://{HOST}:{PORT}/api/flash-card/user/', data= json.dumps(data), headers=headers)
    if r.status_code == 201:
        return "Created!"
    else:
        return "Something went wrong!"

