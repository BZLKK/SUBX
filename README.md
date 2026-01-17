# subx

一个基于 Python 的全能 Clash Meta (Mihomo) 配置生成器，支持图形化界面操作。

## ✨ 功能特点

- **全协议支持**：支持 Hysteria2 / VLESS (Reality/Vision) / VMess / Trojan / Shadowsocks。
- **双模式输入**：
  - 📁 **本地模式**：读取包含链接的 TXT 文件。
  - 🌐 **订阅模式**：直接输入机场订阅链接（自动解析 Base64）。
- **高级控制**：
  - 可视化开关控制 **UDP** 转发。
  - 可视化开关控制 **XUDP** (Meta 专属优化)。
- **完全离线**：本地生成 YAML 文件，保护隐私
- 进行订阅链接转换时会联网先把它下载下来，解密成一行行的 vmess:// 或 hysteria2:// 链接。

## 🛠️ 如何运行源码

如果你想自己运行或修改代码：

1. 安装 Python 3.x
2. 安装依赖库：pyyaml；pyinstaller；
   ```bash
   pip install -r requirements.txt
