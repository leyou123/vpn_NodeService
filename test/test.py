# from speedtest.main import SpeedTest
#
# st = SpeedTest()
# st.start()
#
# s1 = 907444873 / 1024/1024 / 8
#
# print(s1)


import requests

headers = {
    'Content-Type': 'application/json',
}


data = '{"host":"tj25","type":"A","answer":"149.248.51.249","ttl":300}'
response = requests.post('https://api.name.com/v4/domains/9527.click/records', headers=headers, data=data,
                         auth=('huangzugang', '2da3aa15a099209056c90543cb9e5b62e3fcfa5a'))

print(response.status_code)
print(response.text)




