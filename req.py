import requests


def get_contests_created_by_user():
    d = {}
    url = f"https://codeforces.com/api/contest.list?gym=true"
    response = requests.get(url)
    if response:
        data = response.json()
        for i in data['result']:
            if i['id'] == '467724':
                return 'XDDDDD'
            print(i['id'], i['name'])


print(get_contests_created_by_user())
