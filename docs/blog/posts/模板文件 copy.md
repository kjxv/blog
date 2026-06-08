---
date: 2025-01-01
categories:
  - 工具视频教程
slug: muban
tags:
  - 福利
  - AI
---

# 🎁 [主标题] 

![封面图](../../assets/images/muban.png){ width="300" align=left style="border-radius: 8px; margin-right: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 10px;" }

**本期要点：** [这里简述视频的核心价值，吸引读者往下看]。本教程手把手带你通过验证，建议收藏！

<div style="margin-top: 25px; text-align: center;">
  <a href="[YouTube链接]" target="_blank" class="md-button md-button--neutral" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 24px; font-size: 0.85rem; border-radius: 20px; text-decoration: none; font-weight: bold; border: 1px solid rgba(0,0,0,0.1); transition: all 0.3s ease;">
    <svg viewBox="0 0 576 512" style="height: 1.1em; fill: #FF0000; margin: 0; display: block;"><path d="M549.655 124.083c-6.281-23.65-24.787-42.276-48.284-48.597C458.781 64 288 64 288 64S117.22 64 74.629 75.486c-23.497 6.322-42.003 24.947-48.284 48.597-11.412 42.867-11.412 132.305-11.412 132.305s0 89.438 11.412 132.305c6.281 23.65 24.787 41.5 48.284 47.821C117.22 448 288 448 288 448s170.781 0 213.371-11.486c23.497-6.321 42.003-24.171 48.284-47.821 11.412-42.867 11.412-132.305 11.412-132.305s0-89.438-11.412-132.305zm-317.51 213.508V175.185l142.739 81.205-142.739 81.201z"/></svg>
    立即观看完整视频
  </a>
</div>

<br clear="left">
<!-- more -->
---



# 🚀 极简主义！VPS 纯图片轮播 + 音乐 24h 直播搭建指南

放弃繁琐的代码渲染，回归本质。本教程教你通过最原生的 Bash 脚本 + FFmpeg，打造一个坚如磐石的 24 小时图片轮播直播间。随时拖拽上传新图片，无缝热更新！

## 🛠️ 第一步：极简环境配置

🛠️ 一键开启 1G Swap 
```
# 1. 创建一个 1G 大小的交换文件
dd if=/dev/zero of=/swapfile bs=1M count=1024

# 2. 设置正确的安全权限（防止其他用户读取）
chmod 600 /swapfile

# 3. 把这个文件格式化为 Swap 专属格式
mkswap /swapfile

# 4. 立即激活 Swap
swapon /swapfile

# 5. 写入系统配置文件，保证重启后 Swap 依然自动生效
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# 6. 查看当前的内存和 Swap 状态，确认是否成功
free -m
```

## 安装 FFmpeg 和 screen（仅需这两个！）
```bash
apt install -y ffmpeg screen
```


---

## 📂 第二步：创建目录与上传素材

规范文件夹，方便日后通过 WinSCP 管理。

```bash
mkdir -p /root/live/images
cd /root/live

```

**【WinSCP 拖拽时间】**
请将你的素材上传到指定位置：

1. 🖼️ **轮播图片：** 把你做好的所有图片（支持 `.jpg` 或 `.png`）全部拖入 `/root/live/images/` 目录下。*(提示：最好用数字 01, 02, 03... 命名，它会按顺序播放)*
2. 🎵 **背景音乐：** 将 `bgm.mp3` 拖入 `/root/live/` 目录下。

---

## ⚙️ 第三步：编写核心脚本

直接在 VPS 终端内复制运行以下命令，我们将创建两个脚本：一个负责“换图”，一个负责“推流”。

### 1. 换图引擎 (`loop_images.sh`)

这个轻量级脚本会每隔 5 分钟（300秒），从你的图库里抓取一张图替换为 `current.jpg`。

```bash
cat << 'EOF' > /root/live/loop_images.sh
#!/bin/bash

# 只要不断开，就一直循环
while true; do
    # 遍历 images 文件夹下的所有文件
    for img in /root/live/images/*; do
        # 防错机制：如果文件夹是空的，休息 10 秒再试
        if [ ! -f "$img" ]; then
            echo "未找到图片，等待上传..."
            sleep 10
            break
        fi
        
        # 将当前图片覆盖为推流读取的文件
        cp -f "$img" /root/live/current.jpg
        echo "[$(date +'%H:%M:%S')] 切换图片 -> $(basename "$img")"
        
        # 停留时间：300秒 = 5分钟
        sleep 300
    done
done
EOF

chmod +x /root/live/loop_images.sh

```

第2版本
```
#!/bin/bash

# 只要不终止，就一直循环
while true; do
    # 遍历 images 文件夹下的所有 png 文件
    for img in /root/live/images/*.png; do
        
        # 防错机制：如果文件夹是空的，休息 10 秒再说
        if [ ! -f "$img" ]; then
            echo "未找到图片，等待上传..."
            sleep 10
            break
        fi

        # 【核心修复区：使用 cat 原地覆盖内容】
        # 这样做不会改变 current.png 的底层文件编号(Inode)，FFmpeg 就能瞬间捕捉到画面变化
        cat "$img" > /root/live/current.png

        echo "[$(date '+%H:%M:%S')] 切换图片 -> $(basename "$img")"

        # 停留时间：300秒 = 5分钟
        sleep 300
    done
done
```


### 2. 推流引擎 (`run_stream.sh`)

读取 `current.jpg` 和 `bgm.mp3`，并利用 `-update 1` 参数实现画面的无缝刷新，推送到 YouTube。

```bash
cat << 'EOF' > /root/live/run_stream.sh
#!/bin/bash

# ⚠️ 记得确保下面这行是你真实的 YouTube 直播码
STREAM_URL="rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"

# 移除废弃参数，使用标准的无限循环模式
ffmpeg -re -stream_loop -1 -i /root/live/bgm.mp3 \
-loop 1 -i /root/live/current.jpg \
-c:v libx264 -preset veryfast -b:v 2500k -maxrate 2500k -bufsize 5000k \
-r 30 -pix_fmt yuv420p -g 60 \
-c:a aac -b:a 128k -ar 44100 \
-f flv "$STREAM_URL"
EOF

chmod +x /root/live/run_stream.sh

```

第2版本
```
cat << 'EOF' > /root/live/run_stream.sh
#!/bin/bash

# ⚠️ 请确保这里填入了你 YouTube 后台获取的 RTMP 地址和直播码
STREAM_URL="rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"

# 1080P 静态图极速推流指令
ffmpeg -re -stream_loop -1 -i /root/live/bgm.mp3 \
-loop 1 -i /root/live/current.jpg \
-c:v libx264 -preset ultrafast -tune stillimage -b:v 1500k -maxrate 1500k -bufsize 3000k \
-r 1 -g 2 -pix_fmt yuv420p \
-c:a aac -b:a 128k -ar 44100 \
-f flv "$STREAM_URL"
EOF

# 赋予执行权限
chmod +x /root/live/run_stream.sh
```

第3版本
```
#!/bin/bash

STREAM_URL="rtmp://a.rtmp.youtube.com/live2/ar0w-zhz2-xp07-f5pc-033a"

# 优化后的 1080P 静态图极速推流指令
ffmpeg \
-re -stream_loop -1 -i /root/live/bgm.mp3 \
-loop 1 -framerate 10 -i /root/live/current.jpg \
-c:v libx264 -preset ultrafast -tune stillimage \
-b:v 500k -maxrate 500k -bufsize 1000k \
-g 20 -pix_fmt yuv420p \
-threads 1 \
-c:a aac -b:a 128k -ar 44100 \
-f flv "$STREAM_URL"
```

第4版本(稳定一晚上)
```
#!/bin/bash

# ⚠️ 请确保这里填入了你 YouTube 后台获取的 RTMP 地址和直播码
STREAM_URL="rtmp://a.rtmp.youtube.com/live2/ar0w-zhz2-xp07-f5pc-033a"

# 优化后的 1080P 静态图极速推流指令 (包含奇数分辨率自动修复)
ffmpeg \
-re -stream_loop -1 -i /root/live/bgm.mp3 \
-loop 1 -framerate 10 -i /root/live/current.jpg \
-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
-c:v libx264 -preset ultrafast -tune stillimage \
-b:v 500k -maxrate 500k -bufsize 1000k \
-g 20 -pix_fmt yuv420p \
-threads 1 \
-c:a aac -b:a 128k -ar 44100 \
-f flv "$STREAM_URL"
```

第5版本
```
#!/bin/bash

# 请确保这里填入了你 YouTube 后台获取的最新的 RTMP 地址和直播码
STREAM_URL="rtmp://a.rtmp.youtube.com/live2/ar0w-zhz2-xp07-f5pc-033a"

# 纯净版推流指令（完美适配 screen 窗口）
ffmpeg \
-re -stream_loop -1 -i /root/live/bgm.mp3 \
-stream_loop -1 -framerate 1/2 -i /root/live/current.jpg \
-vf "fps=10,scale=trunc(iw/2)*2:trunc(ih/2)*2" \
-c:v libx264 -preset ultrafast -tune stillimage \
-b:v 500k -maxrate 500k -bufsize 1000k \
-g 20 -pix_fmt yuv420p \
-threads 1 \
-c:a aac -b:a 128k -ar 44100 \
-f flv "$STREAM_URL"
```

第6版本
```
#!/bin/bash

STREAM_URL="rtmp://a.rtmp.youtube.com/live2/ar0w-zhz2-xp07-f5pc-033a"

# 终极防错版：先读图片，再读音频，并强制映射轨道
ffmpeg \
-re -f image2 -loop 1 -framerate 1 -i /root/live/current.png \
-re -stream_loop -1 -i /root/live/bgm.mp3 \
-map 0:v:0 -map 1:a:0 \
-vf "fps=10,scale=trunc(iw/2)*2:trunc(ih/2)*2" \
-c:v libx264 -preset ultrafast -tune stillimage \
-b:v 500k -maxrate 500k -bufsize 1000k \
-g 20 -pix_fmt yuv420p \
-threads 1 \
-c:a aac -b:a 128k -ar 44100 \
-f flv "$STREAM_URL"
```

第7版本（720调整为1080）
```
#!/bin/bash

STREAM_URL="rtmp://a.rtmp.youtube.com/live2/pcjq-f3ta-6vvw-hxc8-9701"

# 终极防错版：先读图片，再读音频，并强制映射轨道
ffmpeg \
-re -f image2 -loop 1 -framerate 1 -i /root/live/current.png \
-re -stream_loop -1 -i /root/live/bgm.mp3 \
-map 0:v:0 -map 1:a:0 \
-vf "fps=10,scale=1920:1080,format=yuv420p" \
-c:v libx264 -preset ultrafast -tune stillimage \
-b:v 3000k -maxrate 4000k -bufsize 8000k \
-g 20 -pix_fmt yuv420p \
-threads 1 \
-c:a aac -b:a 128k -ar 44100 \
-f flv "$STREAM_URL"
```

第8版本（增加实时时间）
```
#!/bin/bash

STREAM_URL="rtmp://a.rtmp.youtube.com/live2/pcjq-f3ta-6vvw-hxc8-9701"

ffmpeg \
-re -f image2 -loop 1 -framerate 1 -i /root/live/current.png \
-re -stream_loop -1 -i /root/live/bgm.mp3 \
-map 0:v:0 -map 1:a:0 \
-vf "scale=1920:1080,format=yuv420p,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='%{localtime}':x=w-tw-40:y=40:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5" \
-c:v libx264 -preset ultrafast -tune stillimage \
-b:v 3000k -maxrate 4000k -bufsize 8000k \
-g 20 -pix_fmt yuv420p \
-threads 1 \
-c:a aac -b:a 128k -ar 44100 \
-f flv "$STREAM_URL"
```

第9版本（关键帧调整）
```
#!/bin/bash

STREAM_URL="rtmp://a.rtmp.youtube.com/live2/pcjq-f3ta-6vvw-hxc8-9701"

ffmpeg \
-re -f image2 -loop 1 -framerate 1 -i /root/live/current.png \嗯嗯。
-re -stream_loop -1 -i /root/live/bgm.mp3 \
-map 0:v:0 -map 1:a:0 \
-vf "scale=1920:1080,format=yuv420p,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='%{localtime}':x=w-tw-40:y=40:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5" \
-r 30 \
-c:v libx264 -preset ultrafast -tune stillimage \
-b:v 3000k -maxrate 4000k -bufsize 8000k \
-g 60 -keyint_min 60 -sc_threshold 0 -pix_fmt yuv420p \
-threads 1 \
-c:a aac -b:a 128k -ar 44100 \
-f flv "$STREAM_URL"
```

---

## 🎬 第四步：双核启动！

一切就绪，我们用 `screen` 把它们挂在后台，即使关掉电脑它们也会默默打工。

**启动【换图引擎】：**

```bash
# 看到打印出时间后，按 Ctrl + A，松开再按 D 隐藏到后台
screen -S swapper bash /root/live/loop_images.sh
```

**启动【推流引擎】：**

```bash
# 看到滚动的代码后，按 Ctrl + A，松开再按 D 隐藏到后台
screen -S stream bash /root/live/run_stream.sh

```

关闭推流命令：
```bash
killall ffmpeg
```

关闭screen会话命令：
```
killall screen
```

WinSCP下载地址：[https://winscp.net/eng/download.php](https://winscp.net/eng/download.php)

查看后台运行
```
screen -r swapper
```

```
screen -r stream
```

一键部署命令：
```
bash install.sh
```

更新推流密钥：
```
bash /root/live/change_key.sh
```

安装字体
```
apt-get update
apt-get install fonts-dejavu-core -y
```

---

## 💡 运营维护贴士 (热更新)

这套架构最大的优势在于**无需重启，所见即所得**：

* **➕ 增加新图：** 直接用 WinSCP 把新做好的图片丢进 `/root/live/images/` 文件夹即可，下一轮循环它就会自动加入播放。
* **➖ 删除旧图：** 直接在文件夹里删掉对应的图片即可，永远不会报错。
* **⏱️ 修改时间：** 如果觉得 5 分钟太长，用 WinSCP 打开 `/root/live/loop_images.sh`，把最下面的 `sleep 300` 改成你想要的秒数，然后重启一下换图引擎即可。