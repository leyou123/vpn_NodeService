#### 节点微服务启动



依赖
```
    git clone https://github.com/yanjigame/vpn_NodeService.git
    pip3 install -r /root/vpn_NodeService/requirements.txt
```

启动
```
nohup python3 /root/vpn_NodeService/start.py  > /root/vpn_NodeService_log.txt 2>&1 &
```

