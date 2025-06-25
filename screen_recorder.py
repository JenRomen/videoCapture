import subprocess
import signal
import sys
import os
from datetime import datetime

def main():
    # 输出文件名，带时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"screen_record_{timestamp}.mp4"

    # FFmpeg 可执行文件路径（如果已加入 PATH，直接写 "ffmpeg" 即可）
    ffmpeg_cmd = "ffmpeg"

    # 音频设备名称，请根据实际设备管理器中的名称调整
    audio_device = "立体声混音 (Realtek(R) Audio)"

    # 录制参数
    framerate = "15"           # 帧率
    video_size = None          # None → 全屏；也可以写 "1920x1080" 等

    # 构造 FFmpeg 命令
    cmd = [
        ffmpeg_cmd,
        # 捕获系统声音
        "-f", "dshow",
        "-i", f"audio={audio_device}",
        # 捕获屏幕视频
        "-f", "gdigrab",
        "-framerate", framerate,
    ]
    if video_size:
        cmd += ["-video_size", video_size]
    cmd += [
        "-i", "desktop",
        # 编码设置：libx264 + AAC
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        # 保证兼容性
        "-pix_fmt", "yuv420p",
        output_filename
    ]

    print("Starting recording. Press Ctrl+C to stop.")
    print("FFmpeg command:")
    print(" ".join(cmd))

    # 启动 FFmpeg 子进程
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    try:
        # 等待用户中断
        proc.wait()
    except KeyboardInterrupt:
        print("\nStopping recording...")
        # 向 FFmpeg 发送 Ctrl+C 信号以优雅结束录制
        proc.send_signal(signal.CTRL_C_EVENT)
        proc.wait()

    print(f"Recording saved to: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    main()
