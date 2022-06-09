import time
import requests
import datetime
import settings
import os
import sys
import time
import json
import re
import psutil as p
from tools import HOST, Requests
import paramiko
from settings import HOST_NAME, PASSWORD, PORT,IP

class Servers(object):
    """
        服务器
    """

    def __init__(self):
        self.address = settings.ip_address
        self.headers = {'Authorization': f'Bearer {settings.VULTR_API_KEY}'}
        self.ip = HOST.get_ip()
        self.upload_node_url = f"{settings.NODE_SERVER_URL}/node_status"

    def status(self):
        """
            获取服务器状态
        :return:
        """
        instace_data = self.get_instance_list(self.address)
        instace_id = instace_data.get("instace_id", "")
        total_flow = instace_data.get("total_flow", "")

        already_flow = self.get_instance_bandwidth(instace_id)

        cpu = self.cpu()
        memory = p.virtual_memory().percent
        net_io = self.net_io_convert(show_simple=True)
        flow_send = net_io.get("sent")
        flow_recv = net_io.get("recv")
        connected = self.user_link()

        data = {
            "ip": self.ip,
            "cpu": f"{cpu}%",
            "memory": f"{memory}%",
            "flow_send": flow_send,
            "flow_recv": flow_recv,
            "instace_id": instace_id,
            "total_flow": total_flow,
            "connected":connected,
            "already_flow": round(already_flow / 1024 / 1024 / 1024, 2)

        }
        response = Requests.post(url=self.upload_node_url, json=data)
        print(data)
        print(response.status_code)

    def cpu(self):
        """
            处理器使用情况
        """
        cpu = p.cpu_percent(interval=1, percpu=True)
        cpu_avg = round(sum(cpu) / len(cpu), 2)
        return cpu_avg

    def net_io_convert(self, show_simple: bool = False, decimal: int = 4, interval: int = 1) -> dict:
        """网络带宽使用情况

        Args:
            show_simple (bool, optional): 显示方式，是否为MB 即 值/1024/1024. Defaults to False.
            decimal (int, optional): 保留几位小数. Defaults to 4.
            interval (int, optional): 计算时间间隔. Defaults to 1.

        Returns:
            dict:
                sent: 发送流量带宽
                recv: 接受流量带宽
        """
        net_io1 = p.net_io_counters()
        sent1, recv1 = net_io1.bytes_sent, net_io1.bytes_recv

        if not isinstance(interval, int) or interval <= 0:
            interval = 1

        time.sleep(interval)

        net_io2 = p.net_io_counters()
        sent2, recv2 = net_io2.bytes_sent, net_io2.bytes_recv

        divisor = 1
        if show_simple:
            divisor = 1024 * 1024

        sent = round((sent2 - sent1) / divisor / interval, decimal)
        recv = round((recv2 - recv1) / divisor / interval, decimal)

        return {"sent": sent, "recv": recv}

    def get_instance_bandwidth(self, instance_id):
        """获取实例的流量使用情况
            vultr 默认算使用高的
        Args:
            instance_id (str): 实例编号
        """
        url = f"https://api.vultr.com/v2/instances/{instance_id}/bandwidth"

        r = Requests.get(url=url, headers=self.headers)
        res = eval(r.text)

        incoming_count = 0
        outgoing_count = 0

        month = datetime.datetime.today().month
        if month < 10: month = f"0{month}"
        for k, v in res["bandwidth"].items():
            if not f"-{month}-" in k:  # 不是本月的数据，跳过统计
                continue
            # 换算为GB 需要 / 1024 / 1024 / 1024
            incoming_bytes = v["incoming_bytes"]  # 进站流量
            incoming_count += incoming_bytes
            outgoing_bytes = v["outgoing_bytes"]  # 出站流量
            outgoing_count += outgoing_bytes
            # print(
            #     f"日期：{k}\n\t进站：{incoming_bytes} 转换为GB={incoming_bytes/1024/1024/1024}\n\t出站：{outgoing_bytes} 转换为GB={outgoing_bytes/1024/1024/1024}"
            # )
        # print(
        #     f"本月总数据：\n\t总进站为：{incoming_count} 转换为GB={incoming_count/1024/1024/1024}\n\t总出站为：{outgoing_count} 转换为GB={outgoing_count/1024/1024/1024}"
        # )
        return incoming_count if incoming_count > outgoing_count else outgoing_count

    def get_instance_list(self, ip):
        """
            获取所有实例
        """
        url = "https://api.vultr.com/v2/instances"
        r = Requests.get(url, headers=self.headers)
        res = eval(r.text)
        nodes_data = None
        instances_all = res.get("instances", None)

        for instances in instances_all:
            main_ip = instances.get("main_ip", None)
            id = instances.get("id", None)
            total_flow = instances.get("allowed_bandwidth", None)
            temp_data = {
                "instace_id": id,
                "host": main_ip,
                "total_flow": total_flow
            }
            if ip == main_ip:
                nodes_data = temp_data
        return nodes_data

    def get_ip(self, string_ip):
        datas = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", string_ip)
        ip = ""
        if datas and len(datas) > 1:
            return datas[1]
        else:
            return ip

    def user_link(self):
        ##1.创建一个ssh对象
        client = paramiko.SSHClient()

        # 2.解决问题:如果之前没有，连接过的ip，会出现选择yes或者no的操作，
        ##自动选择yes
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 3.连接服务器
        client.connect(hostname=IP, port=PORT, username=HOST_NAME, password=PASSWORD)

        # 4.执行操作
        stdin, stdout, stderr = client.exec_command('lsof -n -P -i')

        # 5.获取命令执行的结果
        result = stdout.read().decode("utf-8", 'ignore')

        datas = result.split("\n")
        ip_list = []
        for data in datas:
            if "ESTABLISHED" in data and "443" in data:
                ip = self.get_ip(data)
                ip_list.append(ip)
        link_count = len(list(set(ip_list)))

        # 6.关闭连接
        client.close()
        return link_count

    def start(self):
        self.status()


if __name__ == '__main__':
    servers = Servers()
    servers.status()
