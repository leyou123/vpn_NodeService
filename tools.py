import socket
import requests
from apscheduler.schedulers.blocking import BlockingScheduler


class HOST(object):

    @classmethod
    def get_ip(cls):
        """
            获取当前主机ip
        :return:
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip


class Requests(object):
    @classmethod
    def get(cls, url, headers={}, timeout=15):
        try:
            response = requests.get(url=url, headers=headers, timeout=timeout)
            return response
        except Exception as e:
            print(e)
            return None

    @classmethod
    def post(cls, url, json,headers={}, timeout=15):
        try:
            response = requests.get(url=url, json=json,headers=headers, timeout=timeout)
            return response
        except Exception as e:
            print(e)
            return None


class Scheduler(object):
    @classmethod
    def start(cls, func, time):
        """
        :param func: 函数
        :param time: 时间 单位:秒
        :return:
        """
        scheduler = BlockingScheduler()
        scheduler.add_job(func, 'interval', seconds=time)
        try:
            # 定时任务启动
            scheduler.start()
        except Exception as e:
            print(e)
            print("启动错误")