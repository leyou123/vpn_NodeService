import subprocess
import re

class Nginx(object):

    @classmethod
    def query(self):
        s = subprocess.Popen(f"ps -C nginx -o pid", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

        out = re.compile(r"\x1b[^m]*m").sub("", s.stdout.read().decode("UTF-8", "ignore"))
        print(out)
        s.stdout.close()
        pass


# def add_user(name, port, password):
#     """
#         通过脚本创建用户
#     """
#     try:
#         s = subprocess.Popen(f"sudo {path}/ssrmu.sh", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
#
#         run_option = [
#             "7",  # 选择用户配置
#             "1",  # 选择增加用户
#             str(name),  # 输入用户名
#             str(port),  # 输入用户端口
#             str(password),  # 输入用户密码
#             "10",  # 选择协议
#             "2",  # 协议插件
#             "y",  # 是否兼容
#             "1",  # 选择混淆
#             " ",  # 连接数量
#             " ",  # 单线程流量
#             " ",  # 多线程流量
#             " ",  # 流量上限
#             " ",  # 禁止端口
#             "n"  # 是否继续
#         ]
#
#         for i in run_option:
#             s.stdin.write(bytes(i + "\n", encoding="utf-8"))
#         s.stdin.close()
#
#         out = re.compile(r"\x1b[^m]*m").sub("", s.stdout.read().decode("UTF-8", "ignore"))
#         # print(out)
#         s.stdout.close()
#     except Exception as e:
#         print(e)
#         return False
#     return True



if __name__ == '__main__':
    Nginx.query()