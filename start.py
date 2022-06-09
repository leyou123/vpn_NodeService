from servers.servers import Servers
from speedtest.main import SpeedTest
from apscheduler.schedulers.blocking import BlockingScheduler


def main():
    servers = Servers()

    # 节点网速监测。得到上传速度、下载速度、ping值
    st = SpeedTest()
    scheduler = BlockingScheduler()
    scheduler.add_job(servers.start, 'interval', seconds=60)
    scheduler.add_job(st.start, 'interval', seconds=60*10)

    try:
        # 定时任务启动
        scheduler.start()
    except Exception as e:
        print(e)
        print("启动错误")




if __name__ == '__main__':
    main()
