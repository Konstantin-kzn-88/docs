import requests
import fake_useragent

session = requests.Session()

link = 'https://fermer.ru/user'
user = fake_useragent.UserAgent().random
header = {'user-agent' : user}

data = {
	"name": "test_user",
	"pass": "1501kZn1501!",
	"remember_me": "1",
	"form_id": "user_login_block",
	"op": "Войти"
}

resp = session.post(link, data = data, headers = header)
# print(resp)

profile_info = 'https://fermer.ru/user'
profile_resp = session.get(profile_info, headers = header).text
print(profile_resp)

if __name__ == '__main__':
    ...