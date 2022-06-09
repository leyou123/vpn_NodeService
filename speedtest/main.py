import datetime
import subprocess

import json
import settings
from tools import HOST, Requests


class SpeedTest(object):
    """
        节点网速测试
    """

    def __init__(self):
        self.address = settings.ip_address
        self.headers = {'Authorization': f'Bearer {settings.VULTR_API_KEY}'}
        self.ip = HOST.get_ip()
        self.upload_node_url = f"{settings.NODE_SERVER_URL}/trojan_node_network_status"

    def _test_speed(self):
        """
        测试速度
        :return:
        """
        # 在每天0、8、16点的30~40分钟的之间的时间点，监测一次速度
        # 错开时间，以便得到更好的监测效果
        now = datetime.datetime.now()
        if now.hour not in [0, 8, 16]:
            return
        if now.minute < 30 or now.minute >= 40:
            return

        try:
            result = subprocess.run(['/usr/local/python3/bin/speedtest-cli', '--json'], stdout=subprocess.PIPE)
            print(result.stdout)
            data = json.loads(result.stdout.decode("utf-8"))
            print(data)
            # print("###")

            upload_data = {
                "ip": self.ip,
                "download": int(data["download"]),
                "upload": int(data["upload"]),
                "ping": data["ping"],
            }
            print(upload_data)
        except Exception as e:
            print(e)
            return

        response = Requests.post(url=self.upload_node_url, json=upload_data)
        print(response.status_code)

    def start(self):
        self._test_speed()


if __name__ == '__main__':
    st = SpeedTest()
    st.start()
