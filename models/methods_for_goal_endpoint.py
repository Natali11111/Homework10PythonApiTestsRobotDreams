import requests

from constants.constants import BASE_URL, HEADERS, BASE_PATH, BASE_PATH_WITH_TEAM_ID

def create_goal_with_all_fields(random_name, random_description, random_color):
    body = {
        "name": random_name,
        "description": random_description,
        "color": random_color
    }
    response = requests.post(BASE_URL + BASE_PATH_WITH_TEAM_ID, headers=HEADERS, json=body)
    return response

def create_goal_with_invalid_token(random_name, random_description, random_color, token):
    body = {
        "name": random_name,
        "description": random_description,
        "color": random_color
    }
    response = requests.post(BASE_URL + BASE_PATH_WITH_TEAM_ID, {"Authorization": token}, json=body)
    return response

def create_goal_with_invalid_body(random_description, random_color):
    body = {
        "description": random_description,
        "color": random_color
    }
    response = requests.post(BASE_URL + BASE_PATH_WITH_TEAM_ID, headers=HEADERS, json=body)
    return response

def create_goal_with_name(random_name):
    body = {
        "name": random_name
    }
    response = requests.post(BASE_URL + BASE_PATH_WITH_TEAM_ID, headers=HEADERS, json=body)
    return response

def create_goal_with_invalid_team_id(random_name, random_description, random_color, team_id):
    body = {
        "name": random_name,
        "description": random_description,
        "color": random_color
    }
    response = requests.post(BASE_URL + "api/v2/team/" + str(team_id) + "/goal", headers=HEADERS, json=body)
    return response

def update_all_fields(goal_id, updated_name, updated_due_date, updated_description, updated_multiple_owners,
                      updated_owners, updated_color):
    body = {
        "name": updated_name,
        "due_date": updated_due_date,
        "description": updated_description,
        "multiple_owners": updated_multiple_owners,
        "owners": updated_owners,
        "color": updated_color
    }
    response = requests.put(BASE_URL + BASE_PATH + goal_id, headers=HEADERS, json=body)
    return response

def update_goal_name(goal_id, updated_name):
    body = {
        "name": updated_name
    }
    response = requests.put(BASE_URL + BASE_PATH + str(goal_id), headers=HEADERS, json=body)
    return response

def update_goal_name_with_invalid_token(goal_id, updated_name, token):
    body = {
        "name": updated_name
    }
    response = requests.put(BASE_URL + BASE_PATH + goal_id, {"Authorization": token}, json=body)
    return response

def delete_goal(goal_id):
    response = requests.delete(BASE_URL + BASE_PATH + str(goal_id), headers=HEADERS)
    return response

def delete_goal_without_authorization_header(goal_id):
    response = requests.delete(BASE_URL + BASE_PATH + goal_id)
    return response

def get_goal(goal_id):
    response = requests.get(BASE_URL + BASE_PATH + str(goal_id), headers=HEADERS)
    return response

def get_goal_with_invalid_token(goal_id, token):
    response = requests.get(BASE_URL + BASE_PATH + goal_id, {"Authorization": token})
    return response

def get_all_goals():
    response = requests.get(BASE_URL + BASE_PATH_WITH_TEAM_ID, headers=HEADERS)
    return response

def get_all_goals_with_invalid_token(token):
    response = requests.get(BASE_URL + BASE_PATH_WITH_TEAM_ID, {"Authorization": token})
    return response

def get_all_goals_with_invalid_team_id(team_id):
    response = requests.get(BASE_URL + "api/v2/team/" + str(team_id) + "/goal", headers=HEADERS)
    return response