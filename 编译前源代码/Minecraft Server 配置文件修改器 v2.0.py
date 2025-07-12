import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import shutil
import base64
import re
from PIL import Image, ImageTk
import winsound
import psutil  # 用于获取系统内存信息

# 检查是否在Windows系统上运行并隐藏控制台窗口
if os.name == 'nt':
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

class MinecraftConfigEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft服务器配置编辑器")
        self.root.geometry("800x600")
        
        # 配置项翻译字典
        self.translations = {
            "accepts-transfers": "接受转移",
            "allow-flight": "允许飞行",
            "allow-nether": "允许下界",
            "broadcast-console-to-ops": "向管理员广播控制台消息",
            "broadcast-rcon-to-ops": "向管理员广播RCON命令",
            "bug-report-link": "错误报告链接",
            "difficulty": "游戏难度",
            "enable-command-block": "启用命令方块",
            "enable-jmx-monitoring": "启用JMX监控",
            "enable-query": "启用服务器查询",
            "enable-rcon": "启用远程控制",
            "enable-status": "启用服务器状态查询",
            "enforce-secure-profile": "强制安全配置文件",
            "enforce-whitelist": "强制白名单",
            "entity-broadcast-range-percentage": "实体广播范围百分比",
            "force-gamemode": "强制游戏模式",
            "function-permission-level": "函数权限级别",
            "gamemode": "游戏模式",
            "generate-structures": "生成结构",
            "generator-settings": "生成器设置",
            "hardcore": "硬核模式",
            "hide-online-players": "隐藏在线玩家",
            "initial-disabled-packs": "初始禁用的数据包",
            "initial-enabled-packs": "初始启用的数据包",
            "level-name": "世界名称",
            "level-seed": "世界种子",
            "level-type": "世界类型",
            "log-ips": "记录IP地址",
            "max-chained-neighbor-updates": "最大连锁邻居更新数",
            "max-players": "最大玩家数",
            "max-tick-time": "最大刻时间",
            "max-world-size": "最大世界大小",
            "motd": "服务器名称",
            "network-compression-threshold": "网络压缩阈值",
            "online-mode": "是否开启正版验证",
            "op-permission-level": "管理员权限级别",
            "pause-when-empty-seconds": "空闲时暂停秒数",
            "player-idle-timeout": "玩家闲置超时",
            "prevent-proxy-connections": "阻止代理连接",
            "pvp": "允许PVP",
            "query.port": "查询端口",
            "rate-limit": "速率限制",
            "rcon.password": "RCON密码",
            "rcon.port": "RCON端口",
            "region-file-compression": "区域文件压缩",
            "require-resource-pack": "要求资源包",
            "resource-pack": "资源包",
            "resource-pack-id": "资源包ID",
            "resource-pack-prompt": "资源包提示",
            "resource-pack-sha1": "资源包SHA1校验和",
            "server-ip": "服务器IP",
            "server-port": "服务器端口",
            "simulation-distance": "模拟距离",
            "spawn-monsters": "生成怪物",
            "spawn-protection": "出生点保护范围",
            "sync-chunk-writes": "同步区块写入磁盘",
            "text-filtering-config": "文本过滤配置",
            "text-filtering-version": "文本过滤版本",
            "use-native-transport": "使用本地传输层优化",
            "view-distance": "渲染距离",
            "white-list": "是否启用白名单"
        }

        # 配置项可能的值和翻译
        self.option_values = {
            "difficulty": {
                "peaceful": "和平",
                "easy": "简单",
                "normal": "普通",
                "hard": "困难"
            },
            "gamemode": {
                "survival": "生存",
                "creative": "创造",
                "adventure": "冒险",
                "spectator": "旁观"
            },
            "level-type": {
                "minecraft:normal": "普通",
                "flat": "平坦",
                "largebiomes": "大型生物群系",
                "amplified": "放大",
                "default_1_1": "默认1.1"
            },
            "region-file-compression": {
                "deflate": "压缩",
                "none": "无"
            }
        }

        # 配置项状态翻译
        self.status_translations = {
            "true": "启用",
            "false": "禁用",
            "peaceful": "和平",
            "easy": "简单",
            "normal": "普通",
            "hard": "困难",
            "survival": "生存",
            "creative": "创造",
            "adventure": "冒险",
            "spectator": "旁观",
            "minecraft:normal": "普通",
            "flat": "平坦",
            "largebiomes": "大型生物群系",
            "amplified": "放大",
            "default_1_1": "默认1.1",
            "deflate": "压缩",
            "none": "无"
        }

        # 配置项范围
        self.option_ranges = {
            "max-players": (1, 100),
            "view-distance": (2, 32),
            "simulation-distance": (2, 32),
            "spawn-protection": (0, 100),
            "op-permission-level": (1, 4),
            "function-permission-level": (1, 4),
            "max-world-size": (1, 29999984),
            "max-tick-time": (1, 100000),
            "max-chained-neighbor-updates": (1, 10000000),
            "network-compression-threshold": (-1, 1000),
            "player-idle-timeout": (0, 60),
            "pause-when-empty-seconds": (0, 3600),
            "rate-limit": (0, 1000),
            "query.port": (1, 65535),
            "rcon.port": (1, 65535),
            "server-port": (1, 65535),
            "entity-broadcast-range-percentage": (1, 500)
        }

        # 颜色代码映射
        self.color_codes = {
            "大红": "§4",
            "浅红": "§c",
            "土黄": "§6",
            "金黄": "§e",
            "绿": "§2",
            "浅绿": "§a",
            "蓝绿": "§b",
            "天蓝": "§3",
            "深蓝": "§1",
            "蓝紫": "§9",
            "粉红": "§d",
            "品红": "§5",
            "白": "§f",
            "灰": "§7",
            "深灰": "§8",
            "黑": "§0"
        }

        # 常用选项列表
        self.common_options = ["max-players", "difficulty", "gamemode", "server-port", "view-distance"]

        # 配置项控件映射
        self.controls = {}
        self.config_data = {}
        self.current_file = None
        self.is_modified = False
        self.is_translated = True
        self.motd_color_var = None

        # 创建界面
        self.create_widgets()

        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # 顶部按钮区域
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 左侧按钮框架
        button_frame = tk.Frame(top_frame)
        button_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        open_button = tk.Button(button_frame, text="打开配置文件", command=self.open_config)
        open_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(button_frame, text="保存配置", command=self.save_config)
        save_button.pack(side=tk.LEFT, padx=5)

        translate_button = tk.Button(button_frame, text="切换翻译", command=self.toggle_translation)
        translate_button.pack(side=tk.LEFT, padx=5)
        
        icon_button = tk.Button(button_frame, text="更改服务器图标", command=self.change_server_icon)
        icon_button.pack(side=tk.LEFT, padx=5)
        
        generate_button = tk.Button(button_frame, text="生成服务器启动文件", command=self.generate_start_file)
        generate_button.pack(side=tk.LEFT, padx=5)
        
        # 右侧按钮框架 - 使用anchor='e'确保靠右
        right_frame = tk.Frame(top_frame)
        right_frame.pack(side=tk.RIGHT, anchor='e')
        
        about_button = tk.Button(right_frame, text="关于开发者", command=self.show_about)
        about_button.pack(side=tk.RIGHT, padx=5)

        support_button = tk.Button(right_frame, text="支持开发者", command=self.show_support_image)
        support_button.pack(side=tk.RIGHT, padx=5)

        # 搜索框
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(search_frame, text="搜索:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", self.filter_options)

        # 创建滚动区域
        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", tags="frame")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 绑定画布大小改变事件，确保框架宽度与画布一致
        canvas.bind("<Configure>", lambda e: canvas.itemconfig("frame", width=e.width))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 绑定滚轮事件（仅Windows）
        if os.name == 'nt':
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.canvas = canvas

    def filter_options(self, event=None):
        """根据搜索关键词过滤配置项"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            for widget in self.scrollable_frame.winfo_children():
                widget.grid()
            return
        
        for widget in self.scrollable_frame.winfo_children():
            widget.grid_remove()
        
        for widget in self.scrollable_frame.winfo_children():
            if hasattr(widget, 'key'):
                key = widget.key
                
                if self.is_translated:
                    display_name = self.translations.get(key, key)
                else:
                    display_name = key
                
                if (search_term in display_name.lower() or 
                    search_term in key.lower() or 
                    search_term in self.translations.get(key, "").lower()):
                    widget.grid()

    def change_server_icon(self):
        """更改服务器图标"""
        if not self.current_file:
            messagebox.showwarning("警告", "请先打开一个配置文件")
            return
        
        icon_window = tk.Toplevel(self.root)
        icon_window.title("选择服务器图标")
        icon_window.geometry("400x150")
        icon_window.resizable(False, False)
        icon_window.transient(self.root)
        icon_window.grab_set()
        
        tk.Label(icon_window, text="现在选择服务器图标", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(icon_window, text="大小建议64X64像素，建议png图片以支持背景透明").pack(pady=5)
        
        button_frame = tk.Frame(icon_window)
        button_frame.pack(pady=15)
        
        select_button = tk.Button(button_frame, text="选择本地图片", width=15,
                                command=lambda: self.select_icon_image(icon_window))
        select_button.pack(side=tk.LEFT, padx=10)
        
        exit_button = tk.Button(button_frame, text="退出", width=15, command=icon_window.destroy)
        exit_button.pack(side=tk.LEFT, padx=10)

    def select_icon_image(self, icon_window):
        """选择图标图片"""
        icon_window.destroy()
        
        file_path = filedialog.askopenfilename(
            title="选择服务器图标",
            filetypes=[("图片文件", "*.png;*.jpg;*.jpeg"), ("所有文件", "*.*")]
        )

        if not file_path:
            return

        try:
            with Image.open(file_path) as img:
                width, height = img.size
                if width != 64 or height != 64:
                    response = messagebox.askyesno(
                        "图片大小警告",
                        f"选择的图片大小为 {width}x{height}，不是推荐的64x64像素。\n是否继续使用此图片？"
                    )
                    if not response:
                        return

            config_dir = os.path.dirname(self.current_file)
            target_path = os.path.join(config_dir, "server-icon.png")
            
            shutil.copyfile(file_path, target_path)
            
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in ['.jpg', '.jpeg']:
                messagebox.showinfo("成功", "服务器图标已更新 (JPG格式已重命名为PNG)")
            else:
                messagebox.showinfo("成功", "服务器图标已更新")

        except Exception as e:
            messagebox.showerror("错误", f"无法设置服务器图标: {str(e)}")

    def show_about(self):
        """显示关于开发者窗口"""
        about_window = tk.Toplevel(self.root)
        about_window.title("关于开发者")
        about_window.geometry("450x350")
        about_window.resizable(False, False)
        
        about_text = """
此脚本由"我一定天下无敌【网名】"借助AI辅助开发制作。

如需联系:
"""
        
        text_label = tk.Label(about_window, text=about_text, justify="left", padx=20, pady=10)
        text_label.pack(fill=tk.X, anchor="w")
        
        contact_frame = tk.Frame(about_window, padx=20)
        contact_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(contact_frame, text="QQ:", width=8, anchor="w").grid(row=0, column=0, sticky="w", pady=2)
        qq_label = tk.Label(contact_frame, text="548733917", width=20, anchor="w")
        qq_label.grid(row=0, column=1, sticky="w", pady=2)
        qq_copy = tk.Button(contact_frame, text="复制", width=6, 
                            command=lambda: self.copy_to_clipboard(qq_label["text"], "QQ"))
        qq_copy.grid(row=0, column=2, padx=5, pady=2)
        
        tk.Label(contact_frame, text="邮箱:", width=8, anchor="w").grid(row=1, column=0, sticky="w", pady=2)
        email_label = tk.Label(contact_frame, text="548733917@qq.com", width=20, anchor="w")
        email_label.grid(row=1, column=1, sticky="w", pady=2)
        email_copy = tk.Button(contact_frame, text="复制", width=6, 
                              command=lambda: self.copy_to_clipboard(email_label["text"], "邮箱"))
        email_copy.grid(row=1, column=2, padx=5, pady=2)
        
        tk.Label(contact_frame, text="快手ID:", width=8, anchor="w").grid(row=2, column=0, sticky="w", pady=2)
        ks_label = tk.Label(contact_frame, text="ac180000", width=20, anchor="w")
        ks_label.grid(row=2, column=1, sticky="w", pady=2)
        ks_copy = tk.Button(contact_frame, text="复制", width=6, 
                           command=lambda: self.copy_to_clipboard(ks_label["text"], "快手ID"))
        ks_copy.grid(row=2, column=2, padx=5, pady=2)
        
        tk.Label(contact_frame, text="哔哩哔哩UID:", width=8, anchor="w").grid(row=3, column=0, sticky="w", pady=2)
        bili_label = tk.Label(contact_frame, text="3493078665005855", width=20, anchor="w")
        bili_label.grid(row=3, column=1, sticky="w", pady=2)
        bili_copy = tk.Button(contact_frame, text="复制", width=6, 
                             command=lambda: self.copy_to_clipboard(bili_label["text"], "哔哩哔哩UID"))
        bili_copy.grid(row=3, column=2, padx=5, pady=2)
        
        thanks_label = tk.Label(about_window, text="\n----特别鸣谢：你----", justify="center", pady=10)
        thanks_label.pack(fill=tk.X)
        
        self.copy_success_label = tk.Label(about_window, text="", fg="green")
        self.copy_success_label.pack(pady=5)

        support_button = tk.Button(about_window, text="支持开发者", command=self.show_support_image)
        support_button.pack(pady=10)
        
        ok_button = tk.Button(about_window, text="确定", command=about_window.destroy)
        ok_button.pack(pady=10)
        
        about_window.transient(self.root)
        about_window.grab_set()
        self.root.wait_window(about_window)

    def show_support_image(self):
        """显示支持开发者的图片窗口"""
        support_window = tk.Toplevel(self.root)
        support_window.title("支持开发者")
        support_window.geometry("400x400")
        support_window.resizable(False, False)

        try:
            # 这是一个示例base64编码的图片数据
            base64_image = "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nRk/fnyLdFNr167loYceYteuXeDtfl599dWMHTu2xcSHF1X9+c9/5qKLLuI3v/kNN954I9dcc80Bpamt2DdaCesQwTCMlDaRWbNmMXHixJQdqZbgmGOOYfjw4f7lNWvWMHXqVKqqqlLW7Q9HHXUUhYWF/uXq6mriLSSd//3vf/z85z/nZz/7GS+99NKXihybC6UU27dvZ83atX6anZaWRv/+/SksLGx2S45Sijlz5vDuu+/613Xr1o2zzz77gFLBZGQ1ceJEysvL/euT7UKtOLhoJaxDhDFjxjB06FD/cjwe57nnnuPDDz88IO/yvLy8FDFjNBpl7ty5zJ8/P2Xd/jBixAiOO+44CgoKyM7OZsSIEXTo0KHZSvOqqiqmTp3Ka6+9xltvvcWrr756wLbLLYHjOCxYsIAtW7b49aqMjAyGDBnSImua6upqFi5c6HuC5ebmMm7cOAYOHNjsz6Ah1q5dyyOPPMLatWv963JzcznppJMOKFprxb7R8m+oFc3C+PHjOe+881JSlbVr1/L+++8fsIFesv8uifXr1/POO++0SEvVsWNHLrvsMq666iouu+wyfvazn9G1a9dmn6xlZWUp7hHbtm07oEbqlsJxHD777DNqqqv96zIzM1tMNPF4POXzGjhwIGeeeWbKmuYiEokwd+5c3n77bf86y7IYM2YMl156abOjvlY0H83/plvRImRmZnLqqady+umnp5xQ69atO+ATvFOnTgwdOtRvZSktLWXatGksX768RWnZyJEjueOOO3jggQeYMGFCi1KhYDCY0p4Ti8WorKxMWbMvJBIJIpEI8Xi8RTt7juOwevXqFL1V27Zt6devX4tef5s2bRg+fDg9evSgqKiIk0466YDbcCoqKli9enXKrmDPnj254IILDos+7duAVsI6hOjbty8/+MEPUvyo2rZte8A6n8zMTC677LKUJt8NGzYwceLEA0ozDwTZ2dkp7TnxeLzZos14PM4777zD7bffzssvv9win69EIsH27dv99xkMBunSpQsdO3ZscSRz2mmn8cwzzzBx4kSuueaaFkVoDZGZmUlR+/b+Zdu2+d73vscZZ5yRsq4VBw8H9k21olkwTZPhw4fzj3/8g5///Of86le/4vrrrz9gJXUgEODMM89kyJAhvmCzsrKSd997L8XI7lBCCJHyPEqpZuuOli1bxi9/+UseeeQRbrvtNl544YXGS/aKpJVyMp0rKChg5MiRB1TYzsrKYujQoYwcOfKAHB6SyMjI4PTTTuPvf/871157LQ8//DCXX375Afd8tmL/aCWsQ4xwOMzxxx/P9ddfz3XXXcfIkSNTUqqWQAhBXl4eJ5xwAkVFReA18K5ft45p06b5gx2aC9d1WblyJdOmTWPLli3NSitt2yYcDvtRSTQabfZO5bZt21i9ejWlpaWsXr2aRYsWNZvsQqEQl156KZdccgmnn34611577ZeKZCzL+tIuEYZh0KVLF6688kp+/vOfc9FFF1FcXNx4WSsOIloJ6ytAsu3jQASOe8LJJ5+cUiOpq6vjueeeS9mp2h/i8Tjz5s3zHU3vvvtulixZ0nhZEwQCATIyMvy6UbIm1RwUFBTQo0cPMjMz6dy5MyUlJY2X7BWBQICTTz6ZX/ziF9x6661cddVVLbLbqaioYO3atezYsaNFmxTNQX5+Pj169PDbnlpx6NBKWIcBNbW1vP3221xwwQXcfffdLZYF9OnThx/+8Ie+bMJ1XT788EMee+yxZrfsbN26leeee45nnnmGadOmce+99/Lcc881XtYEQgjC4bAvJYjFYs2OsIYOHcr06dOZPn06H374ITfeeGOLUrpAIMCgQYMYOXKkH2HuD47jMG/ePM444wzGjh3LSSeeyOOPP954WSu+JmglrIMEpVSza0hr1qzhqaef5tVXX+XBBx/ksccea5HSHG+n7zvf+U7KdVOnTm22mj4QCDTpBWxuETwcDvvpVH19fbNN/JItMEOGDKFr164HJdrcH6qqqnj55ZeZPXs2W7duZdHixcybN6/ZUeHBQEuOjVbsG62EdYCIRCIsW7aMyZMn8/jjj/PAAw/w4IMP8p///IfJkyezcuXKvbatVO7axerVq3Echy+++IJnn32Wt956q0UHdX5+PiNGjEhJi9asWcPMmTNTFNd7Q05ODj179kwRXe7YsaNZday8vDzaeGp5wzCO2FRISsnKlSuZNGmS/9laltUioemBYvv27bz55pv861//8o+Nhx56iFdeeYU5c+ak9EO2ovkwMzMzb2t8pRCC3Nw8amtrSCQSLd423heEEMTjcQKBAP379+fkk09uvOSIRiwWY8OGDUyePJlnnnmGJ554gueff5533nmHyZMn88EHHzB37lw2btxIPB4nKyuL9PT0lK3zSCTC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MP/5z38YNmxYChm5rsu6dev8Lfb09HTatWu3Xy3RgUIIwTHHHMODDz7ISy+9xPXXX99sucK6deu46qqrOPPMM/n973+fsjmwJ1RVVeG6LlVVVdTX1zeJOL5q5Oflcccdd/D888/z7LPPctlllx1UzVVjZGZm+iPTlCdHSc46xDs2TjvtNJ544gmefvpprr322iYOp4lEggULFlBbW4thGHTo0GGfdbpvOw6rDmvAV6zDShZBp02bxqpVqxBCkJWVhWVZe3yPtm1TVVXFZ599RkVFBdFolFAoRJcuXcjPz/elBw3bL2zb9h/LdV2WLVvGgw8+yOeff46UkqFDh3LBBRe0yLwOjzDj8TiO4+xX8mB74+S7du2aUjvbH2bNmsXvf/97NmzYwMaNG+nSpcteozPLsqiuriYrK4tjjz2Wiy++mJKSkr3uxMViMXbs2EFFRQXBYHCvn/mXgWEY5OXl0bNnTzp37tysuteXgfL6B+fMmeNHSp06daJnz57+D1IoFKJNmzYUFRWlNMEn17/22ms8++yz1NbWUlxczE033US7du32GmUlPG/7mTNn8sEHH1BTU0NhYeFXSnKtOqyvCAsWLOC8887juuuu49JLL+Xss8/mnnvu2adW6bjjjuMHP/gBeB/oY489xq233srChQsbL22CuXPn8stf/pKXXnoJx3EQQnD++edz+umnN166X6xfv54nnniC++67j40bNza++aBACOGnNKZp7pV88E7EP//5z7z55pv85z//4Ywzzthn1Dhx4kTOP/98xo0bx5tvvtnsfskjGd26dePSSy+le/fuCCFYtWoVt956K//5z38aL22CiooK/vOf//CjH/3Ij75Hjx693ylAU6ZM4eqrr+b000/nxz/+MT//+c990fG3AYc1wvqqle4rV67k6aef9i9XVlayfPlyFi5cSE5Ozh4Ff8FgkIyMDJYtW+YTxZYtW1izZg3pGRl07dKlyQFWX1/PSy+9xL333suMGTN8EjjrrLO44oormtVy0xCO63L33Xfzr3/+k48//pjs7OxDYsmbl5dHx44dOeqoo7jssss4+eST9xulNOfYqKur48477+TDDz+koqKCrKws+vfvn1Lr+7oiFAphmiZTp05FKUVtbS1r1qxh+/btHHvssU2ODYBFixbxwAMP8Pjjj/uSk4KCAq655hqGDBnSeDl405HuvPNOHnroIRYuXOgfU5mZmRxzzDEMHjy48V0OGQ5nhPWtIizHcZg5c2aKFiZ5gK1cuZLy8nIKCwtTmmOFEOTk5FBUVMSqVavYtm2br5dZtWqVT2SrV69myZIlfPzxxzz99NM8//zzzJs3zy9Ejx49ml/+8pccffTR+4xE9oREIsF999/P3Llzqauro3PnzgwdOvSgN/GGw2FKSkoYNGgQAwcObJYafX9QSrFlyxYef/xxNm/eDN58xdGjRzfb5vhIRjAYpGPHjkSjUZYuXUoikaC8vJxVq1axY8eOlOPks88+48033+SZZ57hvffe8/Vi2dnZXP+Tn3DBBRc0qTfGvdFo99xzD5MmTWL9+vX+bqxhGHznO9/hoosu8mtpXwVaCesrQrJImkgkKC0t9RXFUkq2bNnCokWLKC0tJRQK0a5dO78uYFkW3bt3Jzc3l+3bt7NlyxYcx2Hr1q3MnTuXRYsWMWfOHD7++GMmT57MRx995Lt32rbNqFGj+M1vfsN3vvOdA94dXLVyJVu2bCEYDHLWWWcxbNiwgx5h4UUMWVlZzSbVuro6ysvLEV4trzGklKxfv56XXnrJd9kcOnQoxx133Fd6kh0qJH/QevXqRW1tLVu3bqW2tpa6ujrmzZvHwoULmT17Np988gkffvgh77//PkuWLPGb3Tt16sT/+3//j2t/9CM6derkP65SirVr1zJx4kQeffRR3nvvPf8+SVx++eVceeWVHHPMMQf1HN0fWgnrK4JlWfTt25d+/fohpaS0tJS6ujpfB1NXV8eCBQtYtWoVoVCIXr16+SehYRj079+f3NxcqqurqaurIx6P47ou1dXVlJaWUlpa6mue0tLSaNeuHePGjeNnP/sZp5122j5rQvuCYRi0b9+egoIC+vbty3nnnUdxcXGLvxfXdYlEIgghDvi1NMSWLVt4//33mTx5Mlu3bqVjx46EQqGU1yWlZO3atbz66qt+rXDMmDGMGTOGvLy8Bo/WciQlI0qpPaZeXyXy8/Pp378/rpSUlZXhOA719fW+I8POnTupqKggHo8jvHFtvXv35tJLL+UXv/hFE9eKtWvX8sijj3LX3//eZBpSUq5y//33M2TIkBYfB18WrYT1FUEBwmv5GDduHJ07d2b79u1s3749RbyXPBFLSkro3LkzgUDA/wz69OnD2LFjKSwsJB6P+8pk27YJBAIEg0HatWvH6NGj+cEPfsDPfvazJnUJx3Goqqqirq7OFxbuDwUFBYwYMYLjjz+e/Pz8Fn8nsViMzz//nE8//ZSamhqys7ObqPaTUJ7iOhqN4jgO5l7sjJ9++ml+97vf8dZbb/HRRx/Rs2dPevTokRJpua7LkiVLeO+99/wt/1GjRjVp1GYPz7uvnUTHcVi7di0fffQR27dvJzc3twlZftXIzc1l9OjRDBw0iKBts3nz5pRjI+CNSOvTpw9nn302v/jFL7jkkkv2+D088cQTPPjQQ1RWVvrXWZZFhw4duPzyy/nTn/50SIwIm4NWwvqK0PBdWJZFz549GT16NMLb4WnYdOq6LjNnzqS0tJTu3bun1IuysrIYNGgQEyZM4MQTT2TEiBGMHTuWE088kfPOO48f//jHXHHFFQwfPnyPsoJPP/2U//u//+O1114jMzOzxRKHlsJxHObPn88111zDU089xdSpU8nIyNirr3llZSXPPfcc//jHP/j888/p2LHjHknyySef5KOPPvIvt23bluHDh6e4IjiOw9y5c5k6darvHX/WWWf5tjoNUV1dzcSJE7nvvvuYM2cOw4cP3+tJsWDBAn77299y//33M2nSpEO2EdFS2JZFp06dOH78eEaPHs3IkSMZN24cJ554IqeeeipXXnkl119/PRMmTKBz5857lS+8/fbbTJs6NUUZP378eP7whz9w1VVX0aZNmybfx1eFVsI6TDBNk/z8fAYMGMCAAQOoqqriiy++QHkCyNraWlauXMnOnTs59thjCYfDCCEQnttmOBymbdu29OjRg379+jFgwAD69u1Lp06dyMjI2GNkUl5ezpNPPsmTTz7p9/iNGTOmycl7MFFdXc17773HxIkTiUQiVFRUYBhGk2bdJF599VUeffRRPvnkE1auXElNTQ3jxo1rUqN64403fCtmwzDo2LEjJ5xwQkqx3nVdFi5cyEcffeQT1imnnMLRRx/d5ICfNGkSjzzyCJ988glLlixh3Lhxe4wi4vE4L774Iv/+97+pr68nFosRCAQ4+uij91nInzNnDu+88w47d+6kffv2Td7PwUJSsd6+fXt69uxJ//79GTBgAP3796dHjx4UFBTsV9Eej8fZtm0b27Zto1u3bvzwhz/khhtuYPjw4f5xeLhwOAlr75/YtwRCCN8C5o9//CO//e1vGTlypP9LXVlZyeeff+5b3zaG5U0+ycnJIScnxyeqvcGyLF9cmjywD3X9xbZtioqKUqK9efPm8eKLLxLbQwvO5s2b2bRpk++U+v7777NmzZomvYLZ2dkpJ33DemASSil27drlb8MHAgHy8/ObpEGRSIQpU6bw+eefU1dXx65du1JU40kopZg+fXqKlsswDDp16rRXvyvXdVmwYAF///vfueuuu/jLX/7Cv//978bLDjpsryE6eWzsKw1vjJEjR/K73/2ORx99lHvvvZdrr72WIUOGHFBT/DcJ33rCSiIUCjFixAhuu+02Xn31Ve6++27atm1L+/btGT9+PB06dNjnL2JzkZ2dzQ9/+EMeeugh7r33Xm655ZYmtZyDjfT0dE455RTOOOMM/6Tetm0bTz71FLNmzWpCRN26dUvZwdu0aRP/+9//qK2tTVmXlZXl73omey0b9xMmCSv5HKFQiLy8vJQT13VdVq9ezaeffuo7LaSlpe1Rp1VZWcmTTz7J9OnTwYuSe/XqxTXXXEPPnj0bLwcvLZ0zZw5Tpkxh1apVzJgxgxdffLHxsiMKOTk5jBkzhssvv5zTTjutiQfbtxVf/gz8BqJt27ZceOGF/ij3n//85we1NlJUVMT555/P9773vWYNYTgYCAaDnH7GGSk6n5rqaqZNndqEsPr375+SKiql+Pzzz5u4PqSnp6cQ1qZNm5p4byV3Y+NeJGcYRpPiuOM4zJo1y08Z8Yi94TZ/Eu+++y6LFy/2LxuGwSmnnLLPVNC2bcYedxynnnoqRUVFjBw5kquuuqrxsq8M0Wi0Cfm3onloJay9IDl1Zvz48f7QiIMFwzDIysoiOzvbTx+VUr5e6YUXXjjoHlamaXLc2LEMHjzYfy+JRIKcnJwm761z5850797dvxz3BsI21mZZluUXhZVS5OTkNKlrKE/9ndQQtW/fvkkB33VdFi1alDLqKjn3sDF27Njh67nw5ARnnnnmPiUShmHQo3t3brrpJh5++GH+9re/MWHChMbLUlBeXs4HH3zA008/zezZs5tEjgeCsrIynn32WW688UZ+9rOf8dxzz/lE3orm4VtddD+SUFVVxT/+8Q+eeOIJpk+fTiwWo3///getGC+EIBwOI6WkoqKCcDjM8ccfzxVXXEFhYWFKumvbNtFolLKyMkKhEEcffTRXXnklPXr0SCGturo6f5RZt27duOSSS5psICjPZ72iooL8/HyuuOIKxo4dm7ImGYVVV1cTDAYZPHgwl1122R4nyAghqK6uJpFI0LFjR7773e9y0UUX7be2Y5omRUVF9O7dmy5duuzzc3Uch/fff5+77rqLd955h2XLltG7d+99NiXvC7FYjLlz5/Lkk0/y+OOP89577zF//nzKy8sZNWpUEwI/0nE4i+6thHWEYNu2bdx0003+rmRdXR3Dhg2juLi48dIvheLiYjp06MBRRx3FxRdfTN++ffd4EhYVFfm7nxdffDHHHntskwgruQvWvXt3Tj75ZC644IIm9TjTNOnevTsdO3ZkzJgxXHLJJU1afizLol+/fhQXF9OvXz/OPuccTj/9dMw9vK6OHTtSUlJC165dGTduHBdddNEea11fBvX19X57VbLNZujQofTv37/JZ7A/VFVVMWXKFO6++26efPLJlOhQCMH48eMpLi7e43dwpOJwEtZh/ZSa7rl9OTiOQywWa1KT+TogEAj4SvFAIEBhYeFBrZslkZOTw4QJE7jiiiuamMk1RG5uLt/5zne4+uqr96rXCgaDHH300Vx11VV7nYEohCA/P5+zzz6b8847b68HedCbMHT11VczdswY7H3snPbu3ZvLLruMCy64YI9p45eFaZq+ENW2bcLhcEr63lxIKXn//ff55S9/yXvvvZdyWyAQ8GdZtvRxm4ukJVFS3PxNwGGNsA6mH1YsFuPjjz/2d7Py8/MPuG/vcCAUClFUVIRSir59+3LJJZcwduzYr9Uv7zcFlmWRn59POBwmKyuL//f//h9nnnkm2fuY2LMnlJWV8fzzz/Puu++mEEZaWhrnn38+t9xyCyUlJYfkO5ae4eTkyZNZuXIleXl5TRqrDxSHM8I6rIR1sFLC6upqJk2axK233sr777/v63kcxyEvL2+v+pwjCaZp0rFjR0aOHMkJJ5xA//79m63ZacXBhfAamgcPHswJJ5zAyJEjD7jONHPmTD7++GP/8uDBg/nlL3/Jj370I3r27HnQNXhKKebNm8djjz3Gvffey+uvv86UKVMoKyujW7duByV9PpyEJYqKilJiRaUUQgi6du3Otm1bqa+vO6i/AEIIamtrSU9P56KLLuKee+5pvKTF2L59O3fffTd33XWXf104HKZnz56UlJQwcuRIhgwZQklJCfn5+S2uQxxuOFJRWh2hrCZGLO5imgYo/V2BAmGA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"
            
            img_data = base64.b64decode(base64_image)
            
            photo = tk.PhotoImage(data=img_data)
            
            label = tk.Label(support_window, image=photo)
            label.image = photo
            label.pack(pady=20)
            
            text_label = tk.Label(support_window, text="感谢您的支持！", font=("Arial", 14))
            text_label.pack(pady=10)
            
            contact_label = tk.Label(support_window, text="支付宝：example@example.com\n微信：example")
            contact_label.pack(pady=10)
                
        except Exception as e:
            text_label = tk.Label(support_window, text="感谢您的支持！", font=("Arial", 14))
            text_label.pack(pady=20)
            
            contact_label = tk.Label(support_window, text="支付宝：example@example.com\n微信：example")
            contact_label.pack(pady=10)

        support_window.transient(self.root)
        support_window.grab_set()
        self.root.wait_window(support_window)

    def copy_to_clipboard(self, text, label):
        """复制文本到剪贴板"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.copy_success_label.config(text=f"{label}已复制到剪贴板!")
        self.root.after(3000, lambda: self.copy_success_label.config(text=""))

    def open_config(self):
        if self.is_modified:
            response = messagebox.askyesnocancel("未保存的更改", "当前文件有未保存的更改。是否继续打开新文件？")
            if response is None:
                return
            elif not response:
                return

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        file_path = filedialog.askopenfilename(
            filetypes=[("Minecraft配置文件", "server.properties"), ("所有文件", "*.*")]
        )

        if not file_path:
            return

        self.current_file = file_path
        self.is_modified = False

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            self.parse_config(content)
            self.create_config_controls()
            self.root.title(f"Minecraft服务器配置编辑器 - {os.path.basename(file_path)}")

        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件: {str(e)}")

    def parse_config(self, content):
        self.config_data = {}
        lines = content.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('#') or not line:
                continue

            if '=' in line:
                key, value = line.split('=', 1)
                self.config_data[key.strip()] = value.strip()

    def create_config_controls(self):
        row = 0

        # 先显示常用选项
        for key in self.common_options:
            if key in self.config_data:
                value = self.config_data[key]
                self.create_control(key, value, row)
                row += 1

        # 显示其他选项
        for key, value in self.config_data.items():
            if key not in self.common_options:
                self.create_control(key, value, row)
                row += 1

    def create_control(self, key, value, row):
        # 获取显示名称
        if self.is_translated:
            display_name = self.translations.get(key, key)
        else:
            display_name = key

        # 创建框架来包含整个配置项
        frame = tk.Frame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
        frame.columnconfigure(0, weight=1)  # 左侧标签占据剩余空间
        frame.columnconfigure(1, weight=0)  # 右侧控件框架不扩展
        frame.key = key
        
        # 创建标签
        label = tk.Label(frame, text=display_name, anchor="w", width=20)
        label.grid(row=0, column=0, sticky="w", padx=5)

        # 创建右侧控件容器 - 使用Frame并设置sticky="e"
        control_frame = tk.Frame(frame)
        control_frame.grid(row=0, column=1, sticky="e")

        # 特殊处理服务器名称(motd) - 添加颜色选择
        if key == "motd":
            self.motd_color_var = tk.StringVar()
            color_options = ["默认"] + list(self.color_codes.keys())
            color_combobox = ttk.Combobox(
                control_frame, 
                textvariable=self.motd_color_var, 
                values=color_options,
                width=8
            )
            color_combobox.set("默认")
            color_combobox.pack(side=tk.LEFT, padx=(0, 5))
            
            if os.name == 'nt':
                color_combobox.bind("<Enter>", self.on_combobox_enter)
                color_combobox.bind("<Leave>", self.on_combobox_leave)
            
            var = tk.StringVar(value=value)
            entry = tk.Entry(control_frame, textvariable=var, width=30)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)
            
            def update_motd(*args):
                color_name = self.motd_color_var.get()
                color_code = self.color_codes.get(color_name, "")
                
                text = var.get()
                
                converted_text = ""
                for char in text:
                    if '\u4e00' <= char <= '\u9fff':
                        converted_text += ''.join(['\\u{:04x}'.format(ord(char))])
                    else:
                        converted_text += char
                
                final_text = color_code + converted_text
                self.update_config(key, final_text)
            
            var.trace_add("write", update_motd)
            self.motd_color_var.trace_add("write", update_motd)
            self.controls[key] = var

        # 滑块配置项
        elif key in self.option_ranges:
            min_val, max_val = self.option_ranges[key]
            try:
                current_val = int(value)
            except ValueError:
                current_val = min_val

            var = tk.IntVar(value=current_val)
            
            scale = tk.Scale(
                control_frame, 
                from_=min_val, 
                to=max_val, 
                orient=tk.HORIZONTAL,
                variable=var,
                showvalue=0,
                command=lambda v, k=key: self.update_config(k, v),
                length=150
            )
            scale.pack(side=tk.LEFT, padx=(0, 5))
            
            spinbox = tk.Spinbox(
                control_frame,
                from_=min_val,
                to=max_val,
                textvariable=var,
                width=8,
                validate="key",
                validatecommand=(frame.register(lambda s: s.isdigit() or s == ""), '%P')
            )
            spinbox.pack(side=tk.LEFT)
            
            var.trace_add("write", lambda name, index, mode, k=key, v=var: self.update_config(k, v.get()))
            
            scale.bind("<Left>", lambda e, k=key, s=scale: self.adjust_scale(s, -1, k))
            scale.bind("<Right>", lambda e, k=key, s=scale: self.adjust_scale(s, 1, k))
            scale.bind("<Up>", lambda e, k=key, s=scale: self.adjust_scale(s, 1, k))
            scale.bind("<Down>", lambda e, k=key, s=scale: self.adjust_scale(s, -1, k))
            
            self.controls[key] = var

        # 下拉菜单配置项
        elif key in self.option_values:
            var = tk.StringVar(value=value)
            translated_values = list(self.option_values[key].values())
            combobox = ttk.Combobox(control_frame, textvariable=var, values=translated_values, width=20)
            combobox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            if os.name == 'nt':
                combobox.bind("<Enter>", self.on_combobox_enter)
                combobox.bind("<Leave>", self.on_combobox_leave)

            current_value = value
            if current_value in self.option_values[key]:
                current_value = self.option_values[key][current_value]
            var.set(current_value)

            combobox.bind("<<ComboboxSelected>>", lambda e, k=key, v=var: self.update_config(k, v.get()))
            var.trace_add("write", lambda name, index, mode, k=key, v=var: self.update_config(k, v.get()))
            self.controls[key] = var

        # 布尔值配置项
        elif value.lower() in ['true', 'false']:
            var = tk.BooleanVar(value=(value.lower() == 'true'))
            checkbox = tk.Checkbutton(control_frame, variable=var)
            checkbox.pack(side=tk.LEFT, padx=5)

            var.trace_add("write", lambda name, index, mode, k=key, v=var:
                          self.update_config(k, "true" if v.get() else "false"))
            self.controls[key] = var

        # 普通文本配置项
        else:
            var = tk.StringVar(value=value)
            entry = tk.Entry(control_frame, textvariable=var, width=30)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            var.trace_add("write", lambda name, index, mode, k=key, v=var: self.update_config(k, v.get()))
            self.controls[key] = var

    def on_combobox_enter(self, event):
        """当鼠标进入下拉菜单时，解除滚轮事件绑定"""
        if os.name == 'nt':
            self.canvas.unbind_all("<MouseWheel>")

    def on_combobox_leave(self, event):
        """当鼠标离开下拉菜单时，重新绑定滚轮事件"""
        if os.name == 'nt':
            self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def adjust_scale(self, scale, delta, key):
        """使用方向键调整滑块值"""
        current = scale.get()
        new_value = current + delta
        min_val, max_val = self.option_ranges[key]
        if min_val <= new_value <= max_val:
            scale.set(new_value)
            self.update_config(key, new_value)

    def update_config(self, key, value):
        """更新配置并标记文件为已修改"""
        if key in self.option_values:
            for original, translated in self.option_values[key].items():
                if translated == value:
                    value = original
                    break

        self.config_data[key] = str(value)
        self.is_modified = True

    def save_config(self):
        if not self.current_file:
            messagebox.showwarning("警告", "请先打开一个配置文件")
            return

        try:
            with open(self.current_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith('#') or not line:
                    continue

                if '=' in line:
                    key, _ = line.split('=', 1)
                    key = key.strip()
                    if key in self.config_data:
                        lines[i] = f"{key}={self.config_data[key]}\n"

            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.writelines(lines)

            self.is_modified = False
            messagebox.showinfo("成功", "配置已保存")

        except Exception as e:
            messagebox.showerror("错误", f"保存文件时出错: {str(e)}")

    def on_closing(self):
        """处理窗口关闭事件"""
        if self.is_modified:
            response = messagebox.askyesnocancel("未保存的更改", "当前文件有未保存的更改。是否保存？")
            if response is None:
                return
            elif response:
                self.save_config()

        self.root.destroy()

    def toggle_translation(self):
        self.is_translated = not self.is_translated
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.create_config_controls()

    def generate_start_file(self):
        """生成服务器启动文件"""
        if not self.current_file:
            messagebox.showwarning("警告", "请先打开一个配置文件")
            return
            
        # 获取系统总内存（GB）
        try:
            total_mem = psutil.virtual_memory().total
            total_mem_gb = total_mem / (1024 ** 3)
            max_mem_gb = max(1, int(total_mem_gb * 0.8))  # 使用80%的系统内存
        except:
            max_mem_gb = 32  # 默认32GB
            
        # 创建设置内存的窗口
        mem_window = tk.Toplevel(self.root)
        mem_window.title("设置服务器内存")
        mem_window.geometry("500x350")  # 增加高度以容纳手动输入框
        mem_window.resizable(False, False)
        mem_window.transient(self.root)
        mem_window.grab_set()
        
        # 设置窗口内容
        tk.Label(mem_window, text="设置服务器内存分配", font=("Arial", 12, "bold")).pack(pady=10)
        
        # 最小内存设置
        min_frame = tk.Frame(mem_window)
        min_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(min_frame, text="最小内存:", width=12, anchor="w").pack(side=tk.LEFT)
        
        min_var = tk.DoubleVar(value=4.0)
        
        # 用于显示最小内存的标签
        min_display = tk.Label(min_frame, text="4.0 GB", width=8)
        min_display.pack(side=tk.RIGHT, padx=5)
        
        min_scale = tk.Scale(
            min_frame, 
            from_=0.5, 
            to=max_mem_gb, 
            orient=tk.HORIZONTAL,
            variable=min_var,
            resolution=0.5,
            showvalue=0,
            length=250
        )
        min_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 更新最小内存显示的函数
        def update_min_display(val):
            val = float(val)
            if val < 1:
                min_display.config(text=f"{int(val * 1024)} MB")
            else:
                min_display.config(text=f"{val} GB")
        
        min_var.trace_add("write", lambda *args: update_min_display(min_var.get()))
        update_min_display(min_var.get())
        
        # 最小内存手动输入框
        min_input_frame = tk.Frame(mem_window)
        min_input_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(min_input_frame, text="手动输入最小内存:", width=15, anchor="w").pack(side=tk.LEFT)
        
        min_input_var = tk.StringVar(value="4.0")
        min_input = tk.Entry(min_input_frame, textvariable=min_input_var, width=10)
        min_input.pack(side=tk.LEFT, padx=5)
        
        min_unit_var = tk.StringVar(value="GB")
        min_unit = ttk.Combobox(min_input_frame, textvariable=min_unit_var, values=["GB", "MB"], width=4, state="readonly")
        min_unit.pack(side=tk.LEFT, padx=5)
        
        def apply_min_input():
            try:
                value = min_input_var.get().strip().lower()
                # 移除单位后缀（如果有）
                if value.endswith("g") or value.endswith("gb"):
                    value = value.rstrip("gb").strip()
                    unit = "GB"
                elif value.endswith("m") or value.endswith("mb"):
                    value = value.rstrip("mb").strip()
                    unit = "MB"
                else:
                    unit = min_unit_var.get()
                
                num_value = float(value)
                
                if unit == "MB":
                    # 转换为GB
                    num_value = num_value / 1024
                
                if num_value < 0.5:
                    messagebox.showerror("错误", "最小内存不能小于0.5GB")
                    return
                    
                if num_value > max_mem_gb:
                    messagebox.showerror("错误", f"最小内存不能超过最大可用内存 {max_mem_gb}GB")
                    return
                    
                min_var.set(round(num_value, 1))
                
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字（例如：4.0 或 4096）")
        
        min_apply_btn = tk.Button(min_input_frame, text="应用", command=apply_min_input, width=6)
        min_apply_btn.pack(side=tk.LEFT, padx=5)
        
        # 最大内存设置
        max_frame = tk.Frame(mem_window)
        max_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(max_frame, text="最大内存:", width=12, anchor="w").pack(side=tk.LEFT)
        
        max_var = tk.DoubleVar(value=4.0)
        
        # 用于显示最大内存的标签
        max_display = tk.Label(max_frame, text="4.0 GB", width=8)
        max_display.pack(side=tk.RIGHT, padx=5)
        
        max_scale = tk.Scale(
            max_frame, 
            from_=0.5, 
            to=max_mem_gb, 
            orient=tk.HORIZONTAL,
            variable=max_var,
            resolution=0.5,
            showvalue=0,
            length=250
        )
        max_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 更新最大内存显示的函数
        def update_max_display(val):
            val = float(val)
            if val < 1:
                max_display.config(text=f"{int(val * 1024)} MB")
            else:
                max_display.config(text=f"{val} GB")
        
        max_var.trace_add("write", lambda *args: update_max_display(max_var.get()))
        update_max_display(max_var.get())
        
        # 最大内存手动输入框
        max_input_frame = tk.Frame(mem_window)
        max_input_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(max_input_frame, text="手动输入最大内存:", width=15, anchor="w").pack(side=tk.LEFT)
        
        max_input_var = tk.StringVar(value="4.0")
        max_input = tk.Entry(max_input_frame, textvariable=max_input_var, width=10)
        max_input.pack(side=tk.LEFT, padx=5)
        
        max_unit_var = tk.StringVar(value="GB")
        max_unit = ttk.Combobox(max_input_frame, textvariable=max_unit_var, values=["GB", "MB"], width=4, state="readonly")
        max_unit.pack(side=tk.LEFT, padx=5)
        
        def apply_max_input():
            try:
                value = max_input_var.get().strip().lower()
                # 移除单位后缀（如果有）
                if value.endswith("g") or value.endswith("gb"):
                    value = value.rstrip("gb").strip()
                    unit = "GB"
                elif value.endswith("m") or value.endswith("mb"):
                    value = value.rstrip("mb").strip()
                    unit = "MB"
                else:
                    unit = max_unit_var.get()
                
                num_value = float(value)
                
                if unit == "MB":
                    # 转换为GB
                    num_value = num_value / 1024
                
                if num_value < 0.5:
                    messagebox.showerror("错误", "最大内存不能小于0.5GB")
                    return
                    
                if num_value > max_mem_gb:
                    messagebox.showerror("错误", f"最大内存不能超过最大可用内存 {max_mem_gb}GB")
                    return
                    
                max_var.set(round(num_value, 1))
                
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字（例如：4.0 或 4096）")
        
        max_apply_btn = tk.Button(max_input_frame, text="应用", command=apply_max_input, width=6)
        max_apply_btn.pack(side=tk.LEFT, padx=5)
        
        # 按钮区域
        button_frame = tk.Frame(mem_window)
        button_frame.pack(pady=20)
        
        def create_file():
            min_mem = min_var.get()
            max_mem = max_var.get()
            
            if min_mem > max_mem:
                if os.name == 'nt':
                    winsound.MessageBeep(winsound.MB_ICONHAND)
                messagebox.showerror("错误", "最小内存不能大于最大内存！")
                return
                
            def format_memory(mem):
                if mem < 1:
                    return f"{int(mem * 1024)}M"
                elif mem.is_integer():
                    return f"{int(mem)}G"
                else:
                    return f"{int(mem * 1024)}M"
            
            min_mem_str = format_memory(min_mem)
            max_mem_str = format_memory(max_mem)
            
            config_dir = os.path.dirname(self.current_file)
            
            jar_files = [f for f in os.listdir(config_dir) if f.endswith('.jar')]
            
            if not jar_files:
                messagebox.showerror("错误", "在当前目录下没有找到服务器本体（JAR文件）")
                mem_window.destroy()
                return
                
            jar_file = jar_files[0]
            
            content = f"java -Xms{min_mem_str} -Xmx{max_mem_str} -jar {jar_file}\npause"
            
            bat_path = os.path.join(config_dir, "start.bat")
            try:
                with open(bat_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                response = messagebox.askyesno("成功", "启动文件已创建！是否在桌面创建快捷方式？")
                
                if response:
                    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                    shortcut_path = os.path.join(desktop_path, "启动Minecraft服务器.bat")
                    
                    with open(shortcut_path, 'w', encoding='utf-8') as f:
                        f.write(f'@echo off\ncd /d "{config_dir}"\nstart "" "start.bat"')
                    
                    messagebox.showinfo("成功", f"已在桌面创建快捷方式：启动Minecraft服务器.bat")
                    
                mem_window.destroy()
                
            except Exception as e:
                messagebox.showerror("错误", f"创建启动文件失败: {str(e)}")
                mem_window.destroy()
        
        create_button = tk.Button(button_frame, text="创建启动文件", command=create_file)
        create_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(button_frame, text="取消", command=mem_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftConfigEditor(root)
    root.mainloop()    