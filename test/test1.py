

import subprocess
import re

def install_certificate():
    """

    """
    path = "/root"

    try:
        s = subprocess.Popen(f"{path}/deploy.sh", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

        run_option = [
            "1",  # 安装证书
            "443",  # 端口
            "testtj2.9527.click",  # 输入域名
            "0"  # 退出脚本./
        ]

        for i in run_option:
            s.stdin.write(bytes(i + "\n", encoding="utf-8"))
        s.stdin.close()
        out = re.compile(r"\x1b[^m]*m").sub("", s.stdout.read().decode("UTF-8", "ignore"))
        print(out)
        #
        s.stdout.close()
    except Exception as e:
        print(e)
        return False
    return True


if __name__ == '__main__':
    install_certificate()