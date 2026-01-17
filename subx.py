import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import urllib.parse
import urllib.request
import sys
import os
import base64
import json
import yaml  # 需安装 PyYAML

# ================= 资源路径=================
def resource_path(relative_path):
    """获取资源的绝对路径，适配 PyInstaller 打包后的临时目录"""
    try:
        # PyInstaller 创建临时文件夹，路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        # 如果是普通运行，则使用当前目录
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ================= 核心工具函数 =================

def safe_base64_decode(s):
    if not s: return ""
    s = s.strip().replace("\n", "").replace("\r", "").replace(" ", "")
    s = s.replace('-', '+').replace('_', '/')
    missing_padding = 4 - len(s) % 4
    if missing_padding and missing_padding != 4:
        s += '=' * missing_padding
    try:
        return base64.b64decode(s).decode('utf-8')
    except Exception:
        return None

def fetch_subscription(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8')
        decoded_content = safe_base64_decode(content)
        if decoded_content:
            return decoded_content.splitlines()
        else:
            return content.splitlines()
    except Exception as e:
        raise Exception(f"网络请求失败: {str(e)}")

# ================= 节点解析逻辑 =================

def parse_vmess(link, original_name):
    b64_str = link[8:]
    json_str = safe_base64_decode(b64_str)
    if not json_str: return None
    try:
        data = json.loads(json_str)
    except: return None
    
    name = data.get("ps", original_name)
    if not name: name = f"{data.get('add')}:{data.get('port')}"
    
    node = {
        "name": name, "type": "vmess", "server": data.get("add"),
        "port": int(data.get("port")), "uuid": data.get("id"),
        "alterId": int(data.get("aid", 0)), "cipher": data.get("scy", "auto"),
        "udp": True, "xudp": True, "network": data.get("net", "tcp")
    }
    if data.get("tls") == "tls":
        node["tls"] = True
        node["servername"] = data.get("sni") or data.get("host") or ""
    if node["network"] == "ws":
        ws_opts = {}
        if data.get("path"): ws_opts["path"] = data.get("path")
        if data.get("host"): ws_opts["headers"] = {"Host": data.get("host")}
        if ws_opts: node["ws-opts"] = ws_opts
    if node["network"] == "grpc":
        if data.get("path"): node["grpc-opts"] = {"grpc-service-name": data.get("path")}
    return node

def parse_trojan(parsed, params, name):
    node = {
        "name": name, "type": "trojan", "server": parsed.hostname,
        "port": parsed.port, "password": parsed.username, "udp": True,
        "sni": params.get("sni", [parsed.hostname])[0],
        "skip-cert-verify": params.get("allowInsecure", ["0"])[0] == "1"
    }
    net_type = params.get("type", ["tcp"])[0]
    node["network"] = net_type
    if net_type == "ws":
        ws_opts = {}
        if "path" in params: ws_opts["path"] = params["path"][0]
        if "host" in params: ws_opts["headers"] = {"Host": params["host"][0]}
        if ws_opts: node["ws-opts"] = ws_opts
    if net_type == "grpc" and "serviceName" in params:
        node["grpc-opts"] = {"grpc-service-name": params["serviceName"][0]}
    return node

def parse_ss(link, name):
    body = link[5:].split("#")[0].split("?")[0]
    if "@" not in body:
        decoded = safe_base64_decode(body)
        if decoded: body = decoded
    try:
        if "@" in body:
            user_part, server_part = body.rsplit("@", 1)
            if ":" not in user_part:
                decoded_user = safe_base64_decode(user_part)
                if decoded_user: user_part = decoded_user
            method, password = user_part.split(":", 1)
            server, port = server_part.rsplit(":", 1)
            return {
                "name": name, "type": "ss", "server": server, "port": int(port),
                "cipher": method, "password": password, "udp": True
            }
    except: pass
    return None

def parse_hy2(parsed, params, name):
    node = {
        "name": name, "type": "hysteria2", "server": parsed.hostname,
        "port": parsed.port, "password": parsed.username,
        "sni": params.get("sni", [""])[0],
        "skip-cert-verify": params.get("insecure", ["0"])[0] == "1", "tfo": True
    }
    if "obfs" in params:
        node["obfs"] = params["obfs"][0]
        if "obfs-password" in params: node["obfs-password"] = params["obfs-password"][0]
    return node

def parse_vless(parsed, params, name):
    try: port = int(parsed.port)
    except: port = 443
    node = {
        "name": name, "type": "vless", "server": parsed.hostname,
        "port": port, "uuid": parsed.username, "udp": True, "xudp": True,
        "packet-encoding": "xudp"
    }
    security = params.get("security", ["none"])[0]
    net_type = params.get("type", ["tcp"])[0]
    node["network"] = net_type
    if "flow" in params: node["flow"] = params["flow"][0]
    if security in ["tls", "reality"]:
        node["tls"] = True
        node["servername"] = params.get("sni", [""])[0]
        if "fp" in params: node["client-fingerprint"] = params["fp"][0]
        if security == "reality":
            node["reality-opts"] = {
                "public-key": params.get("pbk", [""])[0], "short-id": params.get("sid", [""])[0]
            }
    if net_type == "ws":
        ws_opts = {}
        if "path" in params: ws_opts["path"] = params["path"][0]
        if "host" in params: ws_opts["headers"] = {"Host": params["host"][0]}
        if ws_opts: node["ws-opts"] = ws_opts
    if net_type == "grpc" and "serviceName" in params:
        node["grpc-opts"] = {"grpc-service-name": params["serviceName"][0]}
    return node

def parse_link(link):
    try:
        link = link.strip()
        if not link or link.startswith("#"): return None
        name = "Unknown"
        real_link = link
        if "#" in link:
            parts = link.split("#", 1)
            real_link = parts[0]
            name = urllib.parse.unquote(parts[1]).strip()
        
        parsed = None
        params = {}
        if not real_link.startswith("vmess://"):
            try:
                parsed = urllib.parse.urlparse(real_link)
                params = urllib.parse.parse_qs(parsed.query)
                if name == "Unknown" and parsed.fragment: name = urllib.parse.unquote(parsed.fragment)
                if name == "Unknown": name = f"{parsed.hostname}:{parsed.port}"
            except: pass

        if real_link.startswith("hysteria2://"): return parse_hy2(parsed, params, name)
        elif real_link.startswith("vless://"): return parse_vless(parsed, params, name)
        elif real_link.startswith("ss://"): return parse_ss(real_link, name)
        elif real_link.startswith("vmess://"): return parse_vmess(real_link, name)
        elif real_link.startswith("trojan://"): return parse_trojan(parsed, params, name)
        return None
    except: return None

# ================= 图形界面逻辑 =================

class ClashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SUBX(clash配置生成器)")
        self.root.geometry("520x520")
        self.root.resizable(False, False)

        try:
            icon_path = resource_path("000.ico")
            self.root.iconbitmap(icon_path)
        except Exception:
            pass

        style = ttk.Style()
        style.configure("TButton", padding=6, font=("Microsoft YaHei", 9))
        style.configure("TLabel", font=("Microsoft YaHei", 10))

        # 顶部栏
        frame_top = ttk.Frame(root)
        frame_top.pack(fill="x", padx=10, pady=5)
        btn_about = ttk.Button(frame_top, text="关于", width=6, command=self.show_about)
        btn_about.pack(side="right")

        # 选项卡
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab 1
        self.tab_file = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_file, text="📁 本地文件")
        ttk.Label(self.tab_file, text="请选择包含节点链接的 .txt 文件：").pack(anchor="w", pady=(0,5))
        self.file_path_var = tk.StringVar()
        frame_file_input = ttk.Frame(self.tab_file)
        frame_file_input.pack(fill="x")
        ttk.Entry(frame_file_input, textvariable=self.file_path_var, width=40).pack(side="left", fill="x", expand=True, padx=(0,5))
        ttk.Button(frame_file_input, text="浏览...", command=self.select_file).pack(side="left")

        # Tab 2
        self.tab_url = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_url, text="🌐 订阅链接")
        ttk.Label(self.tab_url, text="请输入订阅链接 (http/https)：").pack(anchor="w", pady=(0,5))
        self.url_var = tk.StringVar()
        ttk.Entry(self.tab_url, textvariable=self.url_var, width=50).pack(fill="x", pady=5)
        ttk.Label(self.tab_url, text="* 自动下载并解码 Base64", foreground="gray", font=("Arial", 9)).pack(anchor="w")

        # 高级选项
        frame_options = ttk.LabelFrame(root, text="高级功能开关", padding=10)
        frame_options.pack(fill="x", padx=15, pady=5)
        self.udp_var = tk.BooleanVar(value=True)
        chk_udp = ttk.Checkbutton(frame_options, text="开启 UDP 转发", variable=self.udp_var)
        chk_udp.pack(side="left", padx=15)
        self.xudp_var = tk.BooleanVar(value=True)
        chk_xudp = ttk.Checkbutton(frame_options, text="开启 XUDP (Meta专属优化)", variable=self.xudp_var)
        chk_xudp.pack(side="left", padx=15)

        # 底部
        frame_bottom = ttk.Frame(root, padding=15)
        frame_bottom.pack(fill="x")
        ttk.Separator(frame_bottom, orient='horizontal').pack(fill='x', pady=(0, 10))
        ttk.Label(frame_bottom, text="输出文件名:").pack(anchor="w")
        self.output_name_var = tk.StringVar(value="config.yaml")
        ttk.Entry(frame_bottom, textvariable=self.output_name_var, width=50).pack(fill="x", pady=5)
        self.btn_generate = ttk.Button(frame_bottom, text="🚀 生成配置文件", command=self.generate)
        self.btn_generate.pack(fill="x", pady=10)
        self.status_label = ttk.Label(frame_bottom, text="准备就绪", foreground="gray")
        self.status_label.pack()

    def show_about(self):
        messagebox.showinfo("关于作者", "联系邮箱：zl5@outlook.de")

    def select_file(self):
        filename = filedialog.askopenfilename(title="选择文件", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filename: self.file_path_var.set(filename)

    def generate(self):
        output_name = self.output_name_var.get()
        if not output_name.endswith((".yaml", ".yml")): output_name += ".yaml"

        current_tab = self.notebook.index(self.notebook.select())
        raw_lines = []
        enable_udp = self.udp_var.get()
        enable_xudp = self.xudp_var.get()

        try:
            if current_tab == 0:
                input_path = self.file_path_var.get()
                if not input_path:
                    messagebox.showwarning("提示", "请先选择文件！")
                    return
                self.status_label.config(text="正在读取文件...", foreground="blue")
                with open(input_path, 'r', encoding='utf-8') as f:
                    raw_lines = f.readlines()
                output_dir = os.path.dirname(input_path)
            elif current_tab == 1:
                url = self.url_var.get().strip()
                if not url:
                    messagebox.showwarning("提示", "请输入订阅链接！")
                    return
                self.status_label.config(text="正在下载订阅...", foreground="blue")
                self.root.update()
                raw_lines = fetch_subscription(url)
                output_dir = os.getcwd()

            self.status_label.config(text="正在解析节点...", foreground="blue")
            valid_nodes = []
            for line in raw_lines:
                node = parse_link(line)
                if node:
                    node['udp'] = enable_udp
                    if enable_xudp:
                        node['xudp'] = True
                        if node['type'] in ['vmess', 'vless']:
                            node['packet-encoding'] = 'xudp'
                    else:
                        node['xudp'] = False
                        if 'packet-encoding' in node:
                            del node['packet-encoding']
                    valid_nodes.append(node)

            if not valid_nodes:
                self.status_label.config(text="❌ 失败：未找到有效节点", foreground="red")
                messagebox.showerror("错误", "未能解析出任何有效节点。")
                return

            node_names = [n["name"] for n in valid_nodes]
            config = {
                "port": 7890, "socks-port": 7891, "allow-lan": True,
                "mode": "rule", "log-level": "info", "external-controller": ":9090",
                "dns": {"enable": True, "ipv6": False, "enhanced-mode": "fake-ip", "nameserver": ["8.8.8.8", "1.1.1.1"]},
                "proxies": valid_nodes,
                "proxy-groups": [
                    {"name": "⚡ 自动选择", "type": "url-test", "url": "http://www.gstatic.com/generate_204", "interval": 3000, "tolerance": 55, "proxies": node_names},
                    {"name": "🚀 节点选择", "type": "select", "proxies": ["⚡ 自动选择"] + node_names},
                    {"name": "🐟 漏网之鱼", "type": "select", "proxies": ["🚀 节点选择", "DIRECT"]}
                ],
                "rules": ["GEOIP,LAN,DIRECT", "GEOIP,CN,DIRECT", "MATCH,🐟 漏网之鱼"]
            }

            output_path = os.path.join(output_dir, output_name)
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

            self.status_label.config(text=f"🎉 成功！{len(valid_nodes)} 个节点", foreground="green")
            messagebox.showinfo("成功", f"配置文件已生成！\n\n节点数: {len(valid_nodes)}")

        except Exception as e:
            self.status_label.config(text="❌ 发生错误", foreground="red")
            messagebox.showerror("系统错误", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClashApp(root)
    root.mainloop()
