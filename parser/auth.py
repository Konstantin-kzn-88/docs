import requests

session = requests.Session()

link = 'https://fermer.ru/user'


data = {
	"name": "test_user",
	"pass": "1501kZn1501!",

}

data['form_id']='user_login'
data['op']='Войти'
data['form_build_id']='form-dgI6znPk8kD3t5jDQL79Gl8BoC26t7-_l04wznp6cfQ'

resp = session.post(link, data = data,)

print('Выйти' in resp.text)
print('test_user' in resp.text)

if __name__ == '__main__':
    ...