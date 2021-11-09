import requests

ip = '192.168.212.66'

if (ip == ''):
    print('Setup ip-address of Tekronix oscilloscope')
    quit()

url = 'http://' + ip + '/Image.png'
r = requests.get(url, allow_redirects=True)

open('breath.png', 'wb').write(r.content)