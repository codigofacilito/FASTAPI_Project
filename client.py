import requests

URL = 'http://localhost:8000/api/v1/users/'

USER = {
    'username': 'eduardo_gpg',
    'password': 'password'
}

response = requests.post(URL + 'login', json=USER)

if response.status_code == 200:
    print('Usuario autenticado de forma exitosa.')

    user_id = response.cookies.get_dict().get('user_id')

    cookies = { 'user_id': user_id }
    response = requests.get(URL + 'reviews', cookies=cookies)

    if response.status_code == 200:

        for review in response.json():
            print(f"> {review['review']} - {review['score']}")
