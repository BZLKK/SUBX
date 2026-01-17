# 🚀 subx - Clash Meta 配置生成器 (GUI)

> 一个基于 Python 的Clash Meta (Mihomo) 配置生成器，集成本地与在线模式，支持可视化操作。

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

## 📖 简介


## ✨ 功能特性
完美支持以下主流协议：
* **Hysteria2**
* **VLESS** (支持 Reality / Vision 流控)
* **VMess**
* **Trojan**
* **Shadowsocks**

### 🔄 双模式输入
* 📁 **本地模式**：离线读取包含节点链接的 `.txt` 文件，保护隐私，安全无忧。
* 🌐 **订阅模式**：支持直接输入机场订阅链接（URL）。工具会自动联网下载内容，并智能解析 Base64 编码，将其解密为标准节点格式。


## 🛠️ 安装与运行

如果您希望直接从源码运行或进行二次开发，请按照以下步骤操作。

### 1. 环境准备
确保您的电脑已安装 [Python 3.x](https://www.python.org/downloads/)。

### 2. 安装依赖
打开终端（CMD 或 PowerShell），运行以下命令安装必要的库：

```bash
pip install pyyaml pyinstaller
```
### 3. 运行程序
```Bash

python subx.py
```
📦 编译为可执行文件 (EXE)
如果您希望将程序打包为独立的 Windows 可执行文件（无需 Python 环境即可运行），请使用 PyInstaller 进行编译。

准备工作： 请确保目录中包含图标文件 000.ico，这将作为生成的 EXE 程序的图标。

编译命令：

````Bash
pyinstaller -F -w -i "000.ico" subx.py
````
-F: 生成单个 EXE 文件。

-w: 运行时不显示黑色的命令行窗口。

-i: 指定程序图标。

编译完成后，您将在 dist 目录下找到生成的 subx.exe。

📝 许可证
本项目采用 MIT License 许可证。
