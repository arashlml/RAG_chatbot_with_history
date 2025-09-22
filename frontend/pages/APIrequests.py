import requests


def get_access_token(username, password):
    API_URL = "http://backend:8001/auth/token"
    response = requests.post(
        API_URL,
        data={"username": username, "password": password}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
    else:
        token = None
    return token

def register(username,password,first_name,last_name,email):
    API_URL = "http://backend:8001/auth/"
    payload = {
        "email": email,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "role": "member",
        "password": password
    }
    response = requests.post(API_URL,json=payload)
    if response.status_code == 201:
        return True
    else:
        return False

def get_user(token):
    API_URL = "http://backend:8001/users/"
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    else:
        return None

def get_session_ids(token):
    API_URL = "http://backend:8001/chatbot/chat_history/user/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        response = response.json()
        return response.get("session_ids")
    else:
        return None
def get_chat_history(token,session_id):
    API_URL = "http://backend:8001/chatbot/chat_history/sessionID/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(API_URL,headers = headers, params={"session_id": session_id})
    if response.status_code == 200:
        return response.json()
    else:
        return None

def invoke(token , session_id , message):
    API_URL = "http://backend:8001/chatbot/chat"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"session_id": session_id, "message": message}
    response = requests.post(API_URL,headers= headers, json=payload)
    if response.status_code == 201:
        response = response.json()
        return response.get("response")
    else:
        return None

def get_user_collections (token):
    API_URL = "http://backend:8001/RAGapp/user_get_collections"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        response=response.json()
        return response.get("collection names")
    else:
        return None



def make_new_retriever(token, collection_name, splits):
    API_URL = "http://backend:8001/RAGapp/make_new_retriever"
    headers = {"Authorization": f"Bearer {token}"}
    splits_as_dicts = [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in splits
    ]
    payload = {"splits": splits_as_dicts, "collection_name": collection_name}

    response=requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 201:
        return "You good to go!"
    else:
        raise Exception("Something went wrong")


def rag_invoke(token, session_id, message, collection_name):
    API_URL = "http://backend:8001/RAGapp/chat"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "session_id": session_id,
        "message": message,
        "collection_name": collection_name
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 201:
        response_data = response.json()
        return response_data.get("response")
    else:
        return None
