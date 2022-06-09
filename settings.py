from json import load
from urllib.request import urlopen


# ip地址
ip_address = load(urlopen("http://httpbin.org/ip"))["origin"]
print(ip_address)
# 秘钥
# VULTR_API_KEY = "TRRT2DMP5PD6WYYBM6PIQJPNBKPEW4OHEZIA"

# 北京秘钥
VULTR_API_KEY = "HAPGVVPV33HBOOW4KFLSR3QF44BP7BHQLSLQ"

NODE_SERVER_URL = "https://nodes.9527.click"


IP = ip_address
PORT = 22
HOST_NAME = "root"
# PASSWORD = "2%ZgJG@T.Ls-RT$V"
# PASSWORD = "x=E4Nzbpy{p39Xw."
PASSWORD = "Leyou2020"
