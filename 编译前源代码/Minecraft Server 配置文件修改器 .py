import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import re
import os
import base64
import io

# 检查是否在Windows系统上运行
if os.name == 'nt':
    try:
        import ctypes
        # 隐藏控制台窗口
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
            "difficulty": "难度级别",
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
            "motd": "服务器消息",
            "network-compression-threshold": "网络压缩阈值",
            "online-mode": "在线模式",
            "op-permission-level": "管理员权限级别",
            "pause-when-empty-seconds": "空闲时暂停秒数",
            "player-idle-timeout": "玩家闲置超时",
            "prevent-proxy-connections": "阻止代理连接",
            "pvp": "玩家对战",
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
            "view-distance": "玩家可见的区块距离",
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

        # 配置项说明
        self.option_descriptions = {
            "accepts-transfers": "是否接受从其他服务器转移的玩家",
            "allow-flight": "是否允许玩家在生存模式下飞行",
            "allow-nether": "是否允许玩家进入下界",
            "broadcast-console-to-ops": "是否将控制台消息广播给管理员",
            "broadcast-rcon-to-ops": "是否将RCON命令广播给管理员",
            "bug-report-link": "错误报告的链接地址",
            "difficulty": "游戏难度级别",
            "enable-command-block": "是否启用命令方块",
            "enable-jmx-monitoring": "是否启用Java管理扩展监控",
            "enable-query": "是否启用服务器查询协议",
            "enable-rcon": "是否启用远程控制协议",
            "enable-status": "是否启用服务器状态查询",
            "enforce-secure-profile": "是否强制使用正版验证",
            "enforce-whitelist": "是否强制使用白名单",
            "entity-broadcast-range-percentage": "实体广播范围的百分比",
            "force-gamemode": "是否强制所有玩家使用服务器设置的游戏模式",
            "function-permission-level": "函数命令的权限级别",
            "gamemode": "默认游戏模式",
            "generate-structures": "是否生成结构（如村庄、要塞等）",
            "generator-settings": "世界生成器的自定义设置",
            "hardcore": "是否启用硬核模式（死亡后无法复活）",
            "hide-online-players": "是否在多人游戏列表中隐藏在线玩家",
            "initial-disabled-packs": "初始禁用的数据包列表",
            "initial-enabled-packs": "初始启用的数据包列表",
            "level-name": "世界的名称",
            "level-seed": "世界生成的种子值",
            "level-type": "世界类型",
            "log-ips": "是否记录玩家IP地址",
            "max-chained-neighbor-updates": "最大连锁邻居更新数，防止红石连锁导致服务器崩溃",
            "max-players": "服务器允许的最大玩家数量",
            "max-tick-time": "单个游戏刻的最大处理时间（毫秒）",
            "max-world-size": "世界的最大大小（方块）",
            "motd": "服务器消息，显示在多人游戏列表中",
            "network-compression-threshold": "网络压缩的阈值，小于此值的数据包不压缩",
            "online-mode": "是否启用正版验证",
            "op-permission-level": "管理员的权限级别",
            "pause-when-empty-seconds": "服务器空闲时暂停的秒数",
            "player-idle-timeout": "玩家闲置多长时间后被踢出服务器（分钟）",
            "prevent-proxy-connections": "是否阻止代理连接",
            "pvp": "是否启用玩家对战",
            "query.port": "服务器查询协议使用的端口",
            "rate-limit": "IP地址的连接速率限制",
            "rcon.password": "RCON远程控制的密码",
            "rcon.port": "RCON远程控制使用的端口",
            "region-file-compression": "区域文件的压缩方式",
            "require-resource-pack": "是否要求玩家使用资源包",
            "resource-pack": "服务器使用的资源包URL",
            "resource-pack-id": "资源包的唯一标识符",
            "resource-pack-prompt": "请求玩家接受资源包时显示的提示",
            "resource-pack-sha1": "资源包的SHA1校验和",
            "server-ip": "服务器绑定的IP地址",
            "server-port": "服务器使用的端口",
            "simulation-distance": "服务器模拟实体行为的距离",
            "spawn-monsters": "是否生成怪物",
            "spawn-protection": "出生点周围的保护范围（方块）",
            "sync-chunk-writes": "是否同步区块写入磁盘",
            "text-filtering-config": "文本过滤的配置文件",
            "text-filtering-version": "文本过滤的版本",
            "use-native-transport": "是否使用本地传输层优化",
            "view-distance": "玩家可见的区块距离",
            "white-list": "是否启用白名单"
        }

        # 常用选项列表
        self.common_options = ["max-players", "difficulty", "gamemode", "server-port", "view-distance"]

        # 配置项控件映射
        self.controls = {}
        self.config_data = {}
        self.current_file = None
        self.is_modified = False  # 跟踪文件是否被修改
        self.is_translated = True  # 跟踪是否使用翻译

        # 创建界面
        self.create_widgets()

        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # 顶部按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        open_button = tk.Button(button_frame, text="打开配置文件", command=self.open_config)
        open_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(button_frame, text="保存配置", command=self.save_config)
        save_button.pack(side=tk.LEFT, padx=5)

        translate_button = tk.Button(button_frame, text="切换翻译", command=self.toggle_translation)
        translate_button.pack(side=tk.LEFT, padx=5)
        
        # 关于开发者按钮
        about_button = tk.Button(button_frame, text="关于开发者", command=self.show_about)
        about_button.pack(side=tk.LEFT, padx=5)
        
        # 新增支持开发者按钮
        support_button = tk.Button(button_frame, text="支持开发者", command=self.show_support_image)
        support_button.pack(side=tk.LEFT, padx=5)

        # 温馨提示
        hint_label = tk.Label(self.root, text="温馨提示: 滑块的左右空白区域鼠标点击后可以微调数值", fg="blue", font=("Arial", 10))
        hint_label.pack(fill=tk.X, padx=10, pady=2)

        # 创建滚动区域
        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 绑定滚轮事件
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # 支持Windows和Mac的滚轮事件
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # 支持Linux的滚轮事件
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        self.scrollable_frame = scrollable_frame
        self.canvas = canvas

    def show_about(self):
        """显示关于开发者窗口"""
        about_window = tk.Toplevel(self.root)
        about_window.title("关于开发者")
        about_window.geometry("450x350")
        about_window.resizable(False, False)
        
        # 关于开发者内容
        about_text = """
此脚本由"我一定天下无敌【网名】"借助AI辅助开发制作。

如需联系:
"""
        
        # 创建文本标签
        text_label = tk.Label(about_window, text=about_text, justify="left", padx=20, pady=10)
        text_label.pack(fill=tk.X, anchor="w")
        
        # 创建联系方式和复制按钮
        contact_frame = tk.Frame(about_window, padx=20)
        contact_frame.pack(fill=tk.X, pady=5)
        
        # QQ
        tk.Label(contact_frame, text="QQ:", width=8, anchor="w").grid(row=0, column=0, sticky="w", pady=2)
        qq_label = tk.Label(contact_frame, text="548733917", width=20, anchor="w")
        qq_label.grid(row=0, column=1, sticky="w", pady=2)
        qq_copy = tk.Button(contact_frame, text="复制", width=6, 
                            command=lambda: self.copy_to_clipboard(qq_label["text"], "QQ"))
        qq_copy.grid(row=0, column=2, padx=5, pady=2)
        
        # 邮箱
        tk.Label(contact_frame, text="邮箱:", width=8, anchor="w").grid(row=1, column=0, sticky="w", pady=2)
        email_label = tk.Label(contact_frame, text="548733917@qq.com", width=20, anchor="w")
        email_label.grid(row=1, column=1, sticky="w", pady=2)
        email_copy = tk.Button(contact_frame, text="复制", width=6, 
                              command=lambda: self.copy_to_clipboard(email_label["text"], "邮箱"))
        email_copy.grid(row=1, column=2, padx=5, pady=2)
        
        # 快手ID
        tk.Label(contact_frame, text="快手ID:", width=8, anchor="w").grid(row=2, column=0, sticky="w", pady=2)
        ks_label = tk.Label(contact_frame, text="ac180000", width=20, anchor="w")
        ks_label.grid(row=2, column=1, sticky="w", pady=2)
        ks_copy = tk.Button(contact_frame, text="复制", width=6, 
                           command=lambda: self.copy_to_clipboard(ks_label["text"], "快手ID"))
        ks_copy.grid(row=2, column=2, padx=5, pady=2)
        
        # 哔哩哔哩UID
        tk.Label(contact_frame, text="哔哩哔哩UID:", width=8, anchor="w").grid(row=3, column=0, sticky="w", pady=2)
        bili_label = tk.Label(contact_frame, text="3493078665005855", width=20, anchor="w")
        bili_label.grid(row=3, column=1, sticky="w", pady=2)
        bili_copy = tk.Button(contact_frame, text="复制", width=6, 
                             command=lambda: self.copy_to_clipboard(bili_label["text"], "哔哩哔哩UID"))
        bili_copy.grid(row=3, column=2, padx=5, pady=2)
        
        # 感谢信息
        thanks_label = tk.Label(about_window, text="\n----特别鸣谢：你----", justify="center", pady=10)
        thanks_label.pack(fill=tk.X)
        
        # 复制成功提示标签
        self.copy_success_label = tk.Label(about_window, text="", fg="green")
        self.copy_success_label.pack(pady=5)

        # 支持开发者按钮
        support_button = tk.Button(about_window, text="支持开发者", command=self.show_support_image)
        support_button.pack(pady=10)
        
        # 确定按钮
        ok_button = tk.Button(about_window, text="确定", command=about_window.destroy)
        ok_button.pack(pady=10)
        
        # 设置窗口模态
        about_window.transient(self.root)
        about_window.grab_set()
        self.root.wait_window(about_window)

    def show_support_image(self):
        """显示支持开发者的图片窗口"""
        support_window = tk.Toplevel(self.root)
        support_window.title("支持开发者")
        support_window.geometry("400x400")
        support_window.resizable(False, False)

        base64_image = "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nRk/fnyLdFNr167loYceYteuXeDtfl599dWMHTu2xcSHF1X9+c9/5qKLLuI3v/kNN954I9dcc80Bpamt2DdaCesQwTCMlDaRWbNmMXHixJQdqZbgmGOOYfjw4f7lNWvWMHXqVKqqqlLW7Q9HHXUUhYWF/uXq6mriLSSd//3vf/z85z/nZz/7GS+99NKXihybC6UU27dvZ83atX6anZaWRv/+/SksLGx2S45Sijlz5vDuu+/613Xr1o2zzz77gFLBZGQ1ceJEysvL/euT7UKtOLhoJaxDhDFjxjB06FD/cjwe57nnnuPDDz88IO/yvLy8FDFjNBpl7ty5zJ8/P2Xd/jBixAiOO+44CgoKyM7OZsSIEXTo0KHZSvOqqiqmTp3Ka6+9xltvvcWrr756wLbLLYHjOCxYsIAtW7b49aqMjAyGDBnSImua6upqFi5c6HuC5ebmMm7cOAYOHNjsz6Ah1q5dyyOPPMLatWv963JzcznppJMOKFprxb7R8m+oFc3C+PHjOe+881JSlbVr1/L+++8fsIFesv8uifXr1/POO++0SEvVsWNHLrvsMq666iouu+wyfvazn9G1a9dmn6xlZWUp7hHbtm07oEbqlsJxHD777DNqqqv96zIzM1tMNPF4POXzGjhwIGeeeWbKmuYiEokwd+5c3n77bf86y7IYM2YMl156abOjvlY0H83/plvRImRmZnLqqady+umnp5xQ69atO+ATvFOnTgwdOtRvZSktLWXatGksX768RWnZyJEjueOOO3jggQeYMGFCi1KhYDCY0p4Ti8WorKxMWbMvJBIJIpEI8Xi8RTt7juOwevXqFL1V27Zt6devX4tef5s2bRg+fDg9evSgqKiIk0466YDbcCoqKli9enXKrmDPnj254IILDos+7duAVsI6hOjbty8/+MEPUvyo2rZte8A6n8zMTC677LKUJt8NGzYwceLEA0ozDwTZ2dkp7TnxeLzZos14PM4777zD7bffzssvv9win69EIsH27dv99xkMBunSpQsdO3ZscSRz2mmn8cwzzzBx4kSuueaaFkVoDZGZmUlR+/b+Zdu2+d73vscZZ5yRsq4VBw8H9k21olkwTZPhw4fzj3/8g5///Of86le/4vrrrz9gJXUgEODMM89kyJAhvmCzsrKSd997L8XI7lBCCJHyPEqpZuuOli1bxi9/+UseeeQRbrvtNl544YXGS/aKpJVyMp0rKChg5MiRB1TYzsrKYujQoYwcOfKAHB6SyMjI4PTTTuPvf/871157LQ8//DCXX375Afd8tmL/aCWsQ4xwOMzxxx/P9ddfz3XXXcfIkSNTUqqWQAhBXl4eJ5xwAkVFReA18K5ft45p06b5gx2aC9d1WblyJdOmTWPLli3NSitt2yYcDvtRSTQabfZO5bZt21i9ejWlpaWsXr2aRYsWNZvsQqEQl156KZdccgmnn34611577ZeKZCzL+tIuEYZh0KVLF6688kp+/vOfc9FFF1FcXNx4WSsOIloJ6ytAsu3jQASOe8LJJ5+cUiOpq6vjueeeS9mp2h/i8Tjz5s3zHU3vvvtulixZ0nhZEwQCATIyMvy6UbIm1RwUFBTQo0cPMjMz6dy5MyUlJY2X7BWBQICTTz6ZX/ziF9x6661cddVVLbLbqaioYO3atezYsaNFmxTNQX5+Pj169PDbnlpx6NBKWIcBNbW1vP3221xwwQXcfffdLZYF9OnThx/+8Ie+bMJ1XT788EMee+yxZrfsbN26leeee45nnnmGadOmce+99/Lcc881XtYEQgjC4bAvJYjFYs2OsIYOHcr06dOZPn06H374ITfeeGOLUrpAIMCgQYMYOXKkH2HuD47jMG/ePM444wzGjh3LSSeeyOOPP954WSu+JmglrIMEpVSza0hr1qzhqaef5tVXX+XBBx/ksccea5HSHG+n7zvf+U7KdVOnTm22mj4QCDTpBWxuETwcDvvpVH19fbNN/JItMEOGDKFr164HJdrcH6qqqnj55ZeZPXs2W7duZdHixcybN6/ZUeHBQEuOjVbsG62EdYCIRCIsW7aMyZMn8/jjj/PAAw/w4IMP8p///IfJkyezcuXKvbatVO7axerVq3Echy+++IJnn32Wt956q0UHdX5+PiNGjEhJi9asWcPMmTNTFNd7Q05ODj179kwRXe7YsaNZday8vDzaeGp5wzCO2FRISsnKlSuZNGmS/9laltUioemBYvv27bz55pv861//8o+Nhx56iFdeeYU5c+ak9EO2ovkwMzMzb2t8pRCC3Nw8amtrSCQSLd423heEEMTjcQKBAP379+fkk09uvOSIRiwWY8OGDUyePJlnnnmGJ554gueff5533nmHyZMn88EHHzB37lw2btxIPB4nKyuL9PT0lK3zSCTC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MP/5z38YNmxYChm5rsu6dev8Lfb09HTatWu3Xy3RgUIIwTHHHMODDz7ISy+9xPXXX99sucK6deu46qqrOPPMM/n973+fsjmwJ1RVVeG6LlVVVdTX1zeJOL5q5Oflcccdd/D888/z7LPPctlllx1UzVVjZGZm+iPTlCdHSc46xDs2TjvtNJ544gmefvpprr322iYOp4lEggULFlBbW4thGHTo0GGfdbpvOw6rDmvAV6zDShZBp02bxqpVqxBCkJWVhWVZe3yPtm1TVVXFZ599RkVFBdFolFAoRJcuXcjPz/elBw3bL2zb9h/LdV2WLVvGgw8+yOeff46UkqFDh3LBBRe0yLwOjzDj8TiO4+xX8mB74+S7du2aUjvbH2bNmsXvf/97NmzYwMaNG+nSpcteozPLsqiuriYrK4tjjz2Wiy++mJKSkr3uxMViMXbs2EFFRQXBYHCvn/mXgWEY5OXl0bNnTzp37tysuteXgfL6B+fMmeNHSp06daJnz57+D1IoFKJNmzYUFRWlNMEn17/22ms8++yz1NbWUlxczE033US7du32GmUlPG/7mTNn8sEHH1BTU0NhYeFXSnKtOqyvCAsWLOC8887juuuu49JLL+Xss8/mnnvu2adW6bjjjuMHP/gBeB/oY489xq233srChQsbL22CuXPn8stf/pKXXnoJx3EQQnD++edz+umnN166X6xfv54nnniC++67j40bNza++aBACOGnNKZp7pV88E7EP//5z7z55pv85z//4Ywzzthn1Dhx4kTOP/98xo0bx5tvvtnsfskjGd26dePSSy+le/fuCCFYtWoVt956K//5z38aL22CiooK/vOf//CjH/3Ij75Hjx693ylAU6ZM4eqrr+b000/nxz/+MT//+c990fG3AYc1wvqqle4rV67k6aef9i9XVlayfPlyFi5cSE5Ozh4Ff8FgkIyMDJYtW+YTxZYtW1izZg3pGRl07dKlyQFWX1/PSy+9xL333suMGTN8EjjrrLO44oormtVy0xCO63L33Xfzr3/+k48//pjs7OxDYsmbl5dHx44dOeqoo7jssss4+eST9xulNOfYqKur48477+TDDz+koqKCrKws+vfvn1Lr+7oiFAphmiZTp05FKUVtbS1r1qxh+/btHHvssU2ODYBFixbxwAMP8Pjjj/uSk4KCAq655hqGDBnSeDl405HuvPNOHnroIRYuXOgfU5mZmRxzzDEMHjy48V0OGQ5nhPWtIizHcZg5c2aKFiZ5gK1cuZLy8nIKCwtTmmOFEOTk5FBUVMSqVavYtm2br5dZtWqVT2SrV69myZIlfPzxxzz99NM8//zzzJs3zy9Ejx49ml/+8pccffTR+4xE9oREIsF999/P3Llzqauro3PnzgwdOvSgN/GGw2FKSkoYNGgQAwcObJYafX9QSrFlyxYef/xxNm/eDN58xdGjRzfb5vhIRjAYpGPHjkSjUZYuXUoikaC8vJxVq1axY8eOlOPks88+48033+SZZ57hvffe8/Vi2dnZXP+Tn3DBBRc0qTfGvdFo99xzD5MmTWL9+vX+bqxhGHznO9/hoosu8mtpXwVaCesrQrJImkgkKC0t9RXFUkq2bNnCokWLKC0tJRQK0a5dO78uYFkW3bt3Jzc3l+3bt7NlyxYcx2Hr1q3MnTuXRYsWMWfOHD7++GMmT57MRx995Lt32rbNqFGj+M1vfsN3vvOdA94dXLVyJVu2bCEYDHLWWWcxbNiwgx5h4UUMWVlZzSbVuro6ysvLEV4trzGklKxfv56XXnrJd9kcOnQoxx133Fd6kh0qJH/QevXqRW1tLVu3bqW2tpa6ujrmzZvHwoULmT17Np988gkffvgh77//PkuWLPGb3Tt16sT/+3//j2t/9CM6derkP65SirVr1zJx4kQeffRR3nvvPf8+SVx++eVceeWVHHPMMQf1HN0fWgnrK4JlWfTt25d+/fohpaS0tJS6ujpfB1NXV8eCBQtYtWoVoVCIXr16+SehYRj079+f3NxcqqurqaurIx6P47ou1dXVlJaWUlpa6mue0tLSaNeuHePGjeNnP/sZp5122j5rQvuCYRi0b9+egoIC+vbty3nnnUdxcXGLvxfXdYlEIgghDvi1NMSWLVt4//33mTx5Mlu3bqVjx46EQqGU1yWlZO3atbz66qt+rXDMmDGMGTOGvLy8Bo/WciQlI0qpPaZeXyXy8/Pp378/rpSUlZXhOA719fW+I8POnTupqKggHo8jvHFtvXv35tJLL+UXv/hFE9eKtWvX8sijj3LX3//eZBpSUq5y//33M2TIkBYfB18WrYT1FUEBwmv5GDduHJ07d2b79u1s3749RbyXPBFLSkro3LkzgUDA/wz69OnD2LFjKSwsJB6P+8pk27YJBAIEg0HatWvH6NGj+cEPfsDPfvazJnUJx3Goqqqirq7OFxbuDwUFBYwYMYLjjz+e/Pz8Fn8nsViMzz//nE8//ZSamhqys7ObqPaTUJ7iOhqN4jgO5l7sjJ9++ml+97vf8dZbb/HRRx/Rs2dPevTokRJpua7LkiVLeO+99/wt/1GjRjVp1GYPz7uvnUTHcVi7di0fffQR27dvJzc3twlZftXIzc1l9OjRDBw0iKBts3nz5pRjI+CNSOvTpw9nn302v/jFL7jkkkv2+D088cQTPPjQQ1RWVvrXWZZFhw4duPzyy/nTn/50SIwIm4NWwvqK0PBdWJZFz549GT16NMLb4WnYdOq6LjNnzqS0tJTu3bun1IuysrIYNGgQEyZM4MQTT2TEiBGMHTuWE088kfPOO48f//jHXHHFFQwfPnyPsoJPP/2U//u//+O1114jMzOzxRKHlsJxHObPn88111zDU089xdSpU8nIyNirr3llZSXPPfcc//jHP/j888/p2LHjHknyySef5KOPPvIvt23bluHDh6e4IjiOw9y5c5k6darvHX/WWWf5tjoNUV1dzcSJE7nvvvuYM2cOw4cP3+tJsWDBAn77299y//33M2nSpEO2EdFS2JZFp06dOH78eEaPHs3IkSMZN24cJ554IqeeeipXXnkl119/PRMmTKBz5857lS+8/fbbTJs6NUUZP378eP7whz9w1VVX0aZNmybfx1eFVsI6TDBNk/z8fAYMGMCAAQOoqqriiy++QHkCyNraWlauXMnOnTs59thjCYfDCCEQnttmOBymbdu29OjRg379+jFgwAD69u1Lp06dyMjI2GNkUl5ezpNPPsmTTz7p9/iNGTOmycl7MFFdXc17773HxIkTiUQiVFRUYBhGk2bdJF599VUeffRRPvnkE1auXElNTQ3jxo1rUqN64403fCtmwzDo2LEjJ5xwQkqx3nVdFi5cyEcffeQT1imnnMLRRx/d5ICfNGkSjzzyCJ988glLlixh3Lhxe4wi4vE4L774Iv/+97+pr68nFosRCAQ4+uij91nInzNnDu+88w47d+6kffv2Td7PwUJSsd6+fXt69uxJ//79GTBgAP3796dHjx4UFBTsV9Eej8fZtm0b27Zto1u3bvzwhz/khhtuYPjw4f5xeLhwOAlr75/YtwRCCN8C5o9//CO//e1vGTlypP9LXVlZyeeff+5b3zaG5U0+ycnJIScnxyeqvcGyLF9cmjywD3X9xbZtioqKUqK9efPm8eKLLxLbQwvO5s2b2bRpk++U+v7777NmzZomvYLZ2dkpJ33DemASSil27drlb8MHAgHy8/ObpEGRSIQpU6bw+eefU1dXx65du1JU40kopZg+fXqKlsswDDp16rRXvyvXdVmwYAF///vfueuuu/jLX/7Cv//978bLDjpsryE6eWzsKw1vjJEjR/K73/2ORx99lHvvvZdrr72WIUOGHFBT/DcJ33rCSiIUCjFixAhuu+02Xn31Ve6++27atm1L+/btGT9+PB06dNjnL2JzkZ2dzQ9/+EMeeugh7r33Xm655ZYmtZyDjfT0dE455RTOOOMM/6Tetm0bTz71FLNmzWpCRN26dUvZwdu0aRP/+9//qK2tTVmXlZXl73omey0b9xMmCSv5HKFQiLy8vJQT13VdVq9ezaeffuo7LaSlpe1Rp1VZWcmTTz7J9OnTwYuSe/XqxTXXXEPPnj0bLwcvLZ0zZw5Tpkxh1apVzJgxgxdffLHxsiMKOTk5jBkzhssvv5zTTjutiQfbtxVf/gz8BqJt27ZceOGF/ij3n//85we1NlJUVMT555/P9773vWYNYTgYCAaDnH7GGSk6n5rqaqZNndqEsPr375+SKiql+Pzzz5u4PqSnp6cQ1qZNm5p4byV3Y+NeJGcYRpPiuOM4zJo1y08Z8Yi94TZ/Eu+++y6LFy/2LxuGwSmnnLLPVNC2bcYedxynnnoqRUVFjBw5kquuuqrxsq8M0Wi0Cfm3onloJay9IDl1Zvz48f7QiIMFwzDIysoiOzvbTx+VUr5e6YUXXjjoHlamaXLc2LEMHjzYfy+JRIKcnJwm761z5850797dvxz3BsI21mZZluUXhZVS5OTkNKlrKE/9ndQQtW/fvkkB33VdFi1alDLqKjn3sDF27Njh67nw5ARnnnnmPiUShmHQo3t3brrpJh5++GH+9re/MWHChMbLUlBeXs4HH3zA008/zezZs5tEjgeCsrIynn32WW688UZ+9rOf8dxzz/lE3orm4VtddD+SUFVVxT/+8Q+eeOIJpk+fTiwWo3///getGC+EIBwOI6WkoqKCcDjM8ccfzxVXXEFhYWFKumvbNtFolLKyMkKhEEcffTRXXnklPXr0SCGturo6f5RZt27duOSSS5psICjPZ72iooL8/HyuuOIKxo4dm7ImGYVVV1cTDAYZPHgwl1122R4nyAghqK6uJpFI0LFjR7773e9y0UUX7be2Y5omRUVF9O7dmy5duuzzc3Uch/fff5+77rqLd955h2XLltG7d+99NiXvC7FYjLlz5/Lkk0/y+OOP89577zF//nzKy8sZNWpUEwI/0nE4i+6thHWEYNu2bdx0003+rmRdXR3Dhg2juLi48dIvheLiYjp06MBRRx3FxRdfTN++ffd4EhYVFfm7nxdffDHHHntskwgruQvWvXt3Tj75ZC644IIm9TjTNOnevTsdO3ZkzJgxXHLJJU1afizLol+/fhQXF9OvXz/OPuccTj/9dMw9vK6OHTtSUlJC165dGTduHBdddNEea11fBvX19X57VbLNZujQofTv37/JZ7A/VFVVMWXKFO6++26efPLJlOhQCMH48eMpLi7e43dwpOJwEtZh/ZSa7rl9OTiOQywWa1KT+TogEAj4SvFAIEBhYeFBrZslkZOTw4QJE7jiiiuamMk1RG5uLt/5zne4+uqr96rXCgaDHH300Vx11VV7nYEohCA/P5+zzz6b8847b68HedCbMHT11VczdswY7H3snPbu3ZvLLruMCy64YI9p45eFaZq+ENW2bcLhcEr63lxIKXn//ff55S9/yXvvvZdyWyAQ8GdZtvRxm4ukJVFS3PxNwGGNsA6mH1YsFuPjjz/2d7Py8/MPuG/vcCAUClFUVIRSir59+3LJJZcwduzYr9Uv7zcFlmWRn59POBwmKyuL//f//h9nnnkm2fuY2LMnlJWV8fzzz/Puu++mEEZaWhrnn38+t9xyCyUlJYfkO5ae4eTkyZNZuXIleXl5TRqrDxSHM8I6rIR1sFLC6upqJk2axK233sr777/v63kcxyEvL2+v+pwjCaZp0rFjR0aOHMkJJ5xA//79m63ZacXBhfAamgcPHswJJ5zAyJEjD7jONHPmTD7++GP/8uDBg/nlL3/Jj370I3r27HnQNXhKKebNm8djjz3Gvffey+uvv86UKVMoKyujW7duByV9PpyEJYqKilJiRaUUQgi6du3Otm1bqa+vO6i/AEIIamtrSU9P56KLLuKee+5pvKTF2L59O3fffTd33XWXf104HKZnz56UlJQwcuRIhgwZQklJCfn5+S2uQxxuOFJRWh2hrCZGLO5imgYo/V2BAmGAkuQFBDlBCBoK13GI11UjYzFwXUAhDIFAIEwT07axgkGEZSMESEx2xSTbYxLDCCBEUqWfPGCSh8nuy7sPJQUYKBRCgMBAKgVKkWZI2qaBJVxcJ45TVw+JOAIJwns9gBBK/zv5lEqhvCcQhokZTMMKhKiXgtKESa00EcIApUBJULoDQRiiwWfjvVrhvUT/BQsMBBKFUoqgbVCQFSInPYhptJyU9gYpJbNnz+bll1+moqKCdu3aMXbsWI455ph97moeCOLxODNmzOD9999nzpw5LF++nO3bt/u3Dz/mGP7+978zdsyYlPsdCH79619z//33H/T3IKUkHE6nqH171q9b63NRQ3wjCCsSiTBt2jRuueWWlKnKDWFZFsceeyw33XQTxx57bIvD+8MFRyqWbqlg6pJNbNsVwTBMDEMAhj7VhUAhCMs4I9pa9MiWWJFqaspKqdm0FlFfh6kkhgGmbWIaJoZlYYZCBDMzCebmY6SnYxk2W+pgytZ6KmQ6IpCBZQdACZASpfRzGUITjFKA0JIGoQTCMDVhKU1aCakwURSHYHRblwB1RKqrqd6wHitah6UkwtCPZwiBgX6NhiF0ZVUplNBEaKalk9amHaGMPNZHLebWBtnqhDANE+VKHCeBgYFpmFi2hVQK15EIqRCmR4JoQkuylomBoySO6yAEtMsLc/KgTrTPSTuopPVVYfXq1ZxyyimsW7eu8U1kZmZy4403cs011+xR29ZSHE7C+kakhJZl0b59e0aOHElxcbHvS9QQUkq2bdvGjBkzmDVrFjU1NbRt2/ag5fWHCglXMXPNDrZV1CMMQdA2sS2ToGUSDFgEbJOAKWifIeiTJwjLOurKdlJXthMRrSdgCQKhAIFQkEAwRCAUxA4EsA0DgQJXYtkBjLQQaWkhstKC1EcdHDOAHQphm2AZYJsmliWwTIFlgmkqLEsQME3sgEEgYGFbAtNQmBaYlkk4YNA53aBDugQkTiyBrK0hYIBlBzADQUw7gGVbBIIBLDuIFQhiBWws20aYJkYoRCArh2BuG7DT2JQIUuqmIc0AQdPANgWmYRCwLQKWSdCysE2DgKn/HbRsApZF0LIIWN7nZRmYloFpgGXpFqm4dMlND9ImK4RlHrwf6K8KVVVVvPDCCylatvbt23PBBRdw0003cfbZZx+wLKMxDmdK+I0gLOGZx3Xo0IGSkhIGDBhASUkJwWCQ8vJyv93DdV127drF6tWrWblyJZ9//jm7du2isLCQrKysg/o+94S6ujrmz5/PggULUEo1q56QcFw+21BGXdzFMk0s08ASeMShE6qgIeiaadPBjuJUlVJVuhOntpqQAXYwgG1rMrDtIKZtY9gWlmFgCAOkQikXEQgQCKWRnZEOrkttXBLFxLZsHQEZphcRgSF0FGUIgWWZ2LblRSU6TTQEYJqEbYPiMOQHJK6SuLEIZk2VJho7gGFZGLaFME2kaaOMANK0wPOTtyyTQHo6aXltCKTnUKMs1kWDVMoQwjCxhP7uTdPUhCpMTMPAMgx92TAwhcA0hP7cTH1ZB1z69SYb1JVSFGSGaJ8bJmB9+ZP6q0ayGd/wJu+cfPLJXHPNNZx77rmMHDmSnJycg0JWtBLWlyeshsjIyKBbt24MHTqUnj170qFDB1+RnWwbUUpRXl7O0qVLWbZsGUopjj766EO+q/j666/z2GOP+WLEPn367Je0Eq7Lki27iCQkhiEw0bUew9AnnlRgC+ieYZHlVBLdtZNYdSWWmyAU0HMVDcvCNC1My8IwDV3LMjQpCEOg3ARCKsxgiGB6OmFbUBdJUBlTSDOAaZi6TuYVgwwBCEOTl2nsPhGU8ohAoDBItww6hl1yTQelJG40glNdSUwJ6lxFdUJRHncpjbvsjEtKY5KymENF3KUqKokKE5WWhZ2dhzLT2BoVbIjaRJSFKYRHtjpCMgyd8inQtS2E95J1aikMQ780qXTKqJSuygmQrotSiqKcMB3y0o84wqqpqfEb5veGYDBI79696dmzJyNHjmTChAmMHTuWgoKCgy6baCWsQwDbtikuLmbMmDEMHDiQdu3a4TgO5eXlKW0Wu3btYvv27Xv00z6YUEpx2223MWnSJN+OOR6Pk5eXR15e3l6tThKuZNnWSuriutZiepGNaZgIw0AhCBpQnAZhpxqnpgoVjRA0tHGcZZoYpiYqy9BkBYYmLtPAME198jsOwrYxMsNkBG2kK6mKutS4BqZtI5Q+4QWapExTRzPC0LU0gQIBhmGia10GGRZ0CCuyTJeE61JdV8fm8l3siEq2Rhw21yfYHEmwpd5hS32CbVGH7VGHHRGXHfUuFSJEXVo2UTuDKtdgc8Rml2uBEJgCpEoSlD6uhCF0Dd6rUwkBhqH/4fEoUkmklEiSPlMS6bqgoF1uOh3zwwSsg3uCHyiqqqqYPXs2U6dOpbS0lLy8PNLS0vZ6PgYCATp16kS3bt2aCHgPJg4nYR1ZPyWHCIMGDeKGG27g4Ycf5pJLLqGkpIS0tDRs2yY9PZ2OHTs22V52XZf6+vqDJrqTUhLwXCeT+Ne//sWNN97Ia6+9Rn19vd+Xlwp98oOOYHRwIxCmwLAMbNvEMk0vuNEpXMAKYJo2hmljWDaWafmpjyBZ6NaRkZ/uIZCxKCRiIBSFWUGKwgLTiSDl7lRPRzOarEyzwXxEzydMCKGjLlOTScxVVLmCHXHFypo48ysiLK2Osq4+wba4pNoRxJSJKyyksJCGTUJY1CmDMiODLxIhFlYmmFvmsDURRAlbEyyajExDYRgKYSiEUJgCLCExhcJQemvCEiYGBgp0aqp0RJUkYP1Ypv4c9kIGhwOffPIJ1113HT/+8Y+56qqr+PDDDw9KT+PXGd/YCGtPyM3NZfz48YwZM4aioiKysrIYMWIEP/jBD+jdp48fOsdiMRYuXMg///lPKisr6dy585dOFw3P+2rVqlUpGwI7duzwJ/n06tWryc6L4ypW76whEnMRSj+O6aU3uwnIIMuyKLATBNwYMh5HuC5W0Ma0bEzL9EgkSTY6FRRCE07ycYRSWKEgKhAkGLRwXJeK2gR16MGnlikwvF03YehdQ+ERn8AAoTANE1MYKAEJJ0ZNfR07Ygk2RRPsqIkSqanGMkwMy8T0UlXDsDC9GpNlmDqds2zS2xRhhsNIw0RZmVh22EvttHWyISSWIRCmfj7TMLBNA8vQhXgDgVDe61EKiUIKifKiMcs0MYQme0dJ2h1hKeFrr73GxIkTwat/9urVi/79+x92XeHhjLC+VYQlhMD2piL379+fcePGcfzxx1NSUkKoASEtW7aM+++/n4kTJ7Jy5UoyMjIOyty3Dh060LdvX+LxuF87U56bwerVq/nss8/Izs6mS4NZh46rWLGtivq460U1po64FCipcKUCBQHDpV2aIs2SKNdBug62l/IZXuqWjCCEMLR0S4dMDUhHp02EwgRCQVylqIo4lMcgENSpSJIoFTo1NUwtJzCEqdMzPxpVuNKlLhYhqlwcTNyEg1tTpQvfQuuoDJGM8jzZgdIqKSstnWBeHoZtY5lpBIJZOsfT4gmElxaaydfgPY6lHwKl9PsSSt/HRSI9bZfSbyKZOOJKiStdinIOT0qYjJoaF8U3bNjA9OnTqa+vxzAMLrnkkq+k1ro/tBLWVwzDMAiHw+Tm5u7RNmXdunW8+uqrLF++HIB+/fpx7LHHpqw5EAQCAYqLi+nVqxddu3ZlzZo11NfX+9NsvvjiC1avXo1hGP6odcdVrNhaSSTherthliYuw8AgWQgHV0oygoKsoEnQNvQJ6TpaN2UampiSkZkhwC++e2SVrG9JiRFMwwqGMSybuOOwsyYKdhhhmLsjO+GRoNA7h/oQ8QhF6BQRJXHdGKZQmqSkxInUIaTyhJ5ehKfjRJ3uCo+scvMx0sIYZhDbzsAygyj0/ZQul2EaYCaJDuGlzIanGfPI0BQoobTmSkktFvWIN4lkLax9bjqd8g9thOW6LrFYjNLSUubMmcOrr77Kf//7X95++20cx6FPnz7+2pycHLp3705JSQnnnnsup5xyCoWFhQf1fDwQtBLWEYZwOEwoFGLLli2cfvrpXHbZZQdtaKlhGP5UnaFDh1JVVcXKlSv9+tW2bdsoKyujb9++dO/eHUcqVm6rJuoonc550Yhl2dh2ANsyEEIRl1DjWmQGLfKyQlgZaTiRGMqJa0LR/wfJ+pehU8kkafisIyWGHcAIhgkFw1jArpp66lUQM5iGMC2E0PUe0yMrhJdqoXWmhqHTT1wXN1GPJaSOiwwTgYEbj4KUmH605glOlSCQnkmooBA7Jw9hBLADGZh2GKlcTVjeziig5RUACF1IlxKpBNI7zkxDi1AdJAnl4hq6ECeErm0ZGCDAVQqUQVFumA55h1bWsGTJEp544gl+//vfc9ddd/H+++/z2WefMX/+fHbu3Mlll13mn2/Z2dkMGTLEH3SSl5d3UM/FA8XhJKxD9818jZGbm8vZZ5/NM888w0033UTXrl0bLzkoGDZsGH/4wx/429/+lmLv26tXr922MgpM08IyvR0/P6LQt+noRNdvahyTtXUm26IWZigdO68NIiMbZZgpxfqU8MI7KIxk1GGAkhIlJUIpQrZBdshEuPGUXUAQKCWQugNHF+VRCCVR0gU3jiHjGG4CV0qUxzLBzGwvekpDCpCuBFe36dhZmQTy8zHTM1BKYlkhLEu7k2qC1bUn09ulNAxdSNctQclPQm9OSClJNPhzlPRTcKUUCuUp7HUkqJTUTPjl91eaIBaL8d577/Hzn/+cK6+8kgcffJDPP/+8if99Xl5ek7SwFak4rBFWv/79OeUIjLCEEIRCIQoKCsjMzDxkB5FpmhQUFNCzZ0/69u1Lly5dGDNmDOeddx79+vXDtm1ddC+tIZJwtA7L0OlL8tyUupiFIXQ9KqIM4hgETYPcDBvTshAK3U8opb6fx0zJk1xflfyOJSIYwgplYAUCKCWpicXZvCuKCoQxTAuhpG6lQSKEi4mLhcTCxVQupkxgKP1nKompFIYEQ2o9lGHZWl1v21h2EDMYJpCRRSBHk5U0TaQSmHYmwgigy+UeK3p/Oi5TyQv6Pfk6LH21BF238lo8hBD6s/AjNB1hSakfpyg37NWwDs73vXXrVqZMmcJ//vMfnn76aaZNm8b69eupq6tL2XkuKChg3LhxXH755fTt2zflMY5EHM4I67ASVv8jlLAOBpK+XI3lEntCeno6JSUl/gj3Xr16+XU1TVjV1Mcdf0dQ16D0ySilbvw1DS2UlMIk6ppEHEW7TJP0tACGaetIxHVAupqivOZmPy4x9HeslMQMhTHTMjEDQaSU7KqPs6WiDhEIEbAFFi62kNiGiyVcLKGwlcQ0XEwhMYT+ryUEtmkSEAYWBiZCk50w9O6lHcQOpWGmpWNmZGCE0lDCQGFgGCGEFUYJgfLSTf0CNSEp7wDHqz/pPE8TsenV53QEqMkqGU1579JXYYHSEaIhtHD0ICjdq6urWbx4MY8++ij//e9/efPNN9m0aZPfcZFEcXExo0aN4rLLLvPthBrXU49EHE7C+nLfzJfEwaPBIwdSSlauXMkrr7zCSy+9xJLFi5uE/ntDckxYCnztk6430UA/pYMLT+ltmhhAQIBUBtuiJhtqBHUqgJmZQyC/LVZ2HkYgTdey/Khk9xehFGCYeo1tEXUllVGXupgiHAqQbiYIiRhppkPAVIS8v6CpW4UMw9uxs00tg/BGmgWDIUJpaQTTtDmhbZiYGFiGhWkHMAM2yjSQ0kG5DiYmthUGoRuqfSilpR0evxreTl+DoAkjuSHRULLhvc3kYyipQEqkkp7QVKeVXyYflJ7N88KFC3nuuee47bbbuO+++/jss89IeCPO8HzPOnbsyHe+8x2uu+467rrrLm666SZGjRp10Angm4jDSlgHgkQiQU1NDZWVldTX15NIJPYiuDw8qKmp4fbbb+fKK6/k8ssv549/+hPl5eWNl7UIpvD65Lyte6UUrusiUNiWhW1ZmiwM3dBsmRLTFKyqhFWVglpsRHo6gby2BPLaYKaFwfCSKqVQGCipd8/M9GysjGziwmRLZYQV22rZGVFk5GSTEQ5qcvKaoL3enKSC09s1NDCEhWHo5mVlmkjTRFkmImBhBgPYaUGCaUHsgI0JGK6LmXARCRekwjBsLCuI4eVvChDJep23s2l6yn3TFBgGKKFbbkDXy6TUKaGndvWiL/1+pZQoV0d6/ueQSo3NhuM41NTUsGjRIh555BGuvvpqfvKTn/D222/7a4TX65qXl8cJJ5zAH/7wB5555hl+9atfHZYUMCmKrqmpIRqNpqSnRzq+doQ1depUfvKTn3D22Wfz5z//mTfffNOXBxxuuK7Lxo0bmTNnDnFvGsqiRYtYu3Zts6OsPcFEYGFgKEC6OK6D40gcR+G4XpTg6shBt564mEJRryzW1giWVShqEhZmKIidU4Bd0B47qwAjEALT8mo9YKSlEywsot6w+aIswpqdEcodE8IZBEJhArZNwLKxDcNzcRBoxYTSKSBKSxgMPLmEhWHaYFoo00QZhnZgsC1Mz5HBDujmbFMY4IIhAhhmCDwJhSkMzGS9zds0EF4B3rIMbEsTua5bacmDI5V+P8IjcS8C1aJWE8vQHQG6YdrwfhAs3TPZAsRiMWbMmMHNN9/MhRdeyB133OEbRzZEYWEhF198Mc888wxPPvkkl156KW3btk1Z81Vi4cKF3HzzzVx00UU88MAD1NTUfG1I62tFWOvXr+epp57ipZde4pNPPuGf//wnN910ExdffDHXXnstU6dOJRKJNL7bVwbDMCgqKkrZVSwqKtrjENbGB/W+INFyAYQiIV1NUt72nPK283WtR3jCSF3fEgZEEGyoUywqcymLWhi2TTAjg0BuAaH8IgL57bDyCwkWtiOQ35Yq12JdWYRttS6unUZ6ejrhYIhQIEjQsrWtjWUSNA2ChiBgCIJC6DqVl6pq7tBF8qReSxgmwtBODJ7xFYZlYlg2phnAsnSLkfAkCrpQntSI6ejIReJIV9+e3KWUSu9C6kIWCl1E98r04EU4ydTZsm1M20IYAifhoORuz6XmxlhlZWW8/PLLXHfddVx77bU8++yzrFq1ytfUJTFgwAB+/etf88QTT/CnP/2J8ePHU1BQQCAQaFKb+aoQi8V44IEHeOKJJ/wxZh9++GGLjsfDicNedG+JDquiooI333yTFStW+GLLyspKtm3bxpo1a4jH44wcOTLFnC+RSFBeXs6OHTuoq6vDNE1/16gxiXxZCCEIBoO0b9+ebt26ceyxx3LRRRcxcOBAv/heXl7OW2+9xX333cfs2bP9dDEYDPpb9Q0/b0cq1pXVE0m4SCVxXb0Fn3z9htCRgw4xvEpMUmpgaPJyFNQ6UO8oJEITjq1dR4UdxEhLg2A6tcpmc3WCmoSBCNiEQkHSgjZBS/tOWYZWkluGwDYEloEurAuhhaGGwFTJ+lGyTOYVxTXjeiSW/LfwBKOGF31534dSgG7P0RV2XWn3lfF4DdsopCtxXFeTlQJHakV78n5JiYbySNDjNSTguA4oLRyVUtIuK22POizHcYhEIqxatYqXX36Zf/3rX7zyyit8/PHHbN261S+mB4NB8vPz6du3LyeeeCI33HADZ5xxBkOGDCEnJ6dZGzBfFq7rMnPmTF544QWmTZtGeXk5nTp18ntYXdfl5ZdfZtmyZbiuS0ZGBuPHj6d3797NdnU4nEX3r5XjqFKKGTNmMHHiRD766COWL1+eEsqecsopPPTQQ/405Vgsxpw5c7jttttYs2YNOTk5jBgxgmHDhjF48GB69ep1SB0a9oTXXnuN3//+9ynOqAUFBRx33HFcfPHFHH/88Sn9hJGEy5QVZZTWxnTdymcjQAgM5Z3w6AZgUChXoqQ+MRGAYSAROK7ERtItHfpkKwqCDq5ycZVBRX2CnbUO9dgE7AC6O8UjFc0NHrT2SiqFK7QOShOD7seTUuAqTQiukjhK4Sj0dVKnrQqlhaDSRUkteXC8GArXRSZcXCzsjHywLI+vdvtWoUAI7VCqJLjSRSlBQiqibgKFlw56n5U+RgSO6yKli2GaCNtEugpLCZQUONJlSJd8hvcoID24m1jq6+t9Anj33XfZsmWLf1tDtG/fnjPOOIPzzz+fY4455rD1+61dt47rfvxj3n//ffB2oN955x1Gjhzp70AuX76cl156ifXr1zNq1CguueSS/c51bIhWx9FmQghB27ZtGTp0KKeffjoDBgyge/fu9OzZk3HjxvGDH/yAkpIS/4upqKjg2WefZdKkSZSWllJaWsrq1auZNWsW7733HlOnTmXhwoWsX7+e+vp6CgsLD/m28q5du5gzZ06KlW19fT0bNmxgxowZFBcX061bN/8XUcsaaqmNJgCB5dnKJIMUnQOB8JRJeFcJ39jOwjIsLEub1ylhUOtA1FWkGYqQJamOxqmIuCSETSgQ1I6cnubL0l08WJ40wELompEBoPsaDQEWnrmf91+R9O3ymU77Uinf+riBsMB7Xck3JDwBKoaFYVpePUtgmvo4lMrRwlZvo0GhI0dJA5JWuuqu9wV0BCqV8lNKpNBGf140JVFe8/PuCKu6uppXXnmF3/3ud8yaNSvFzTOJwYMHc/XVV/OrX/2K7373u/Tp06dFJ//BRqS+njfeeIO1a9eC5w93xRVXpJQlcnNz6d+/P2PGjGHIkCEtJtfDGWF9rQgLz1kxMzOTtm3bUlJSwsCBAxkxYgSjR4+mf//+KY2h9fX1zJkzhylTpoD3gcRiMaqrqyktLWXNmjWsWLGChQsX8umnn7J69WratWt3SAuimZmZ5OXlEY/HWblypX99IpGgsrKSkSNHctRRR/nvIykcrY8mMISu8xjJ9E9pDZGmB60LVcrbxveanRGGl2FpOxUExBTUJyDmGFgoEgkXBy0xSLOs3alf0q3T0M3FSQdPrwSlm1uEwgQsgdZXCeENlNApqekNl9BlKL2TpyMeHSnp16t7H30G9ghP9/mYYAa8CE+r0/W79fRTIllk14QkpesRo34009DWOvre3h2ELvQJwDAESioSjkNhVpCOeel+83NtbS1TpkzhxRdfTLF1CYfDjBkzhiuuuIKrr76aU089lQEDBpCVlXXQ0j7XdQ8oswkEAv77LS4u5qKLLuLEE08kPT3dP48NwyA9PZ3s7OwDmszUSlgHiGAwSG5uLoWFheTl5TXJwU3TJBQKsWPHDgzDIBaL+bt3SUQiEcrLy9m4cSPz58+nS5cuHHXUUQftwGuMUChEjx496NWrF67ndBmNRhFC0L9/fy655BJ69uzpvxdHKtaX1RN1tONo0m88SVQkIyrvovDaWIRXO9J1G1330v/WROEqA6lMQkiCBthJz3PPRthENxYndU2mR0a6CO49j0dEvsJBGF5/oP4zPMIzfV2qJhpNObv/dss5d/8/JFtmDDD1ZJ/dxTn9H1181zU6FLigva68zyPp2WUYpiZLkq/Lk4egUEriuBLXdWmXHaZTQYZPWMljdcWKFZSWlpKZmcmoUaO48MILufzyyzn//PPp3bv3QSsrKKWoqanhvffe4/XXX2fdunVkZGS0KPWyLIvu3bvTt29fRowYwSmnnEKbNm0O6jncSliHCJZl0blzZ38Mem5uLtFolPT0dEzTREp9oCbhOA6DBg1i1KhR+/3lcRyHRCLRpEjeHJimSYcOHRgzZgydOnUiJzeX7t278/3vf5/jjz8+JaVwlOKLsghRRxfaBTqSgKTbgY5Gklv4SVM9w6svJQv0+DUkiUAQsixygoLcoEPY0tGTZWopgSYf7w9Nfp7jlacW9wSZaHsXIXSkotclidMjNYVn66xJJElRKIFsqFj3oLzivBICpPfdCFOPJhPeDqJPxMnIStfskhyefC6SVOi9f813CgP0qDSvl9FxdPG9fV46HfN3E1bStTYnJwfHcRg1ahS/+tWvuPTSS+natauftrcUjuPgOI7+DBscO67r8umnn/Lb3/6WZ555htmzZxMKhRgzZkyLjrFAIED79u19x4+DjVbCOsRo164dQ4cO5dRTT2XcuHEMHjyYtm3bEgqFMAzDb6FJhtB7G82OVxjcunUrixcvZs2aNdTU1BAMBv2TrnGUty+kpaXRt29fTj31VCZMmNAkpcVLCdeV1RFJuDqqalhzN3Y3myTDmqTmKDWd2J0GKXQRPtMWFIVc8m3dQmOYegdOn+ReWulFSUmiNH0iACGUR2Z6jS5c6ZgpGUUZKpXkksGTV4rSurGUQ8ujGY90lJL6DRsKYelURx+L3m6oF3Q5CRdHSoQXVeHpsZTUu6rS1b2WesPCe6bdT4Lr6h7LorwMOubvTgnxfvQGDBjAqaeeyplnnnlAY7Jc1yUejxOLxdi2bRvLli1jzZo1xGIxcnNz/WMmHo/z+uuv8+6771JXV0dtbS3hcJhzzjnnkNdWW4LDSVhfq13Cg4FkVOU4DnV1dWzatIl169ZRVVVFSUkJ/fr1Iycnp/HdfGzYsIE77riDF198ESklBQUFlJSU0L9/f0aNGsUpp5xyUA+uSMLlg6VllNZGdZ+f8AZHeDUsffo22PpH65YMY3f0oJTyazUY2n2zna3olQnpQX1AmIYmF10QF57xnYZK2rh4u4OeqxTKI0Dp7Ry6aOGq1kdpQlJKq85dpS1w4q52Toi7irhUxF1JIjkUQuldQKX04+C66P+ZYKZh22k6vcPbpfQEr67rFdIVWN7J70qFKx0dQUuJMAwdYSalDUnXC6lIuC6uUgztVsionm3JCB287y+RSLB06VKmTpvG8mXLWL58OV988QW1tbUMHDiQX//615x88sm60d1xmDx5Mtdeey0bN24kIyODH/7wh/z9739vcuIeTrTuEn6FEMndM9smHA7Ttm1bunbtSu/evenSpct+Q+gFCxYwceJEVq1aRTQapaKigo0bN7J48WKmT5/u7z5+9tln7Ny5k3A4TE5OzgF/ho6rWL2jhtqobn5OnpAqqTHyogYhvOu86EtHDi5CNHApRRNH2FC0T1O0TdOqdF3n0X7ouh6VNObTJ3Vy8IWOSnZHVUmRKN7nqpJRmRdR6bRSaduZZCE+2QvoFb2Fp16WCiRSp2teDU0mi/RCojAwTT2AQimFq0cq7iYhpdATcaR3HToSS+aJgEFyI8IjPMdFulqIi4COeRl0apASfllEo1Gee+45br75Zj6YPJmFCxfyxRdfUF1dTSwWo6amho4dOzJq1ChsbypOUVERAwYMYPTo0Vx00UV897vfPejE8GVxOCOsgxc6fU1heO6je3Ie3ROKi4t9YgsEAhiGQTQapby8nLVr1zJ58mSeeuop/vznP3PVVVfx97//vUmhH+/XJB6PN0thnCQlhK7XuMlURymt6vaV3h4jNMgbhaFlCMnJyKYwyA6a5IUNArbO5EyhsMArjisMIUG4IKQmGo9pBMkhD7stiQ2vMdswtJf67p1FXbsyvIK7aQhsobw/QUBAwICAIbANg4AwCAlFhnLJVjGyiBGWMQLK0ZOrldag+ZGe1Kmc8lI+6RXOpdfUDEpvAjSoMQoDTMvAsvQQDdAqeSmlX6Pb38+K4zj+96b8D33PqK6uZt68eXz++eds376dmpoapDeMJBwOU1xczKBBg/wNHiEEmZmZnHbaafz4xz/mwgsv9DWFrdA4rBHWkeqHtS/k5OQwaNAg+vTpQ05ODqZpEo/H99jLmCSjc845J2VbOR6Ps3btWj786COqqqrIysra66+V4yrWltURS6BPJ+EVzrWGQZ+Ymsv8oo5AD2GwTFPbziRPRqGjnoKAojAIIVNo9wfvRBVe9KQMHdUgpFZ3CaXH0vvhlCcvULrZWgi8mpV2DU1GTj7ZNYRKPq7EVQJHglIuWSpOW0MRllGcaB2JWISCdJO8EFgyQSzm4BgBhGmjDBPpRXsArqNTvyR9JFNg09tRdV3Xb5KXychUeh0DXrRnGQYdcjPo0KiG1RA1NTXMmDGD2bNnU1NTs19ZQFpaGhUVFSxcuJDq6mpyc3Pp27cvxx9/PN/73vf4wQ9+wPjx45v1Q3kk4XBGWN+6GtbBgJSS2tpaqqqqqK6uZsuWLaxYsYKZM2cydepUX2AYCoW4/PLL+cc//pFSTJ8+fTp33nknS5cuJT09neLiYvr06cOxxx7L8ccfnzJTLhJ3eW/pDirqHLTXkxZcKakdMrW2SA+jUFITiWVaCMP0xJn6+zQ9rZNA0Tks6RKWpNt6hfAK43hyKBePWMAjyd0Kcx1UGF6ko+tIylO2S6U3Bvzallfv0u1EnnDTcXGlJOFKoo5upckkiqyvZ96yVXw0fxEbdpZhhtLp1X8Qwwb0oF+nfGQkwuaoRX2oEGkEvden08BEIoF0XYTQanallO+JlVTXJ6FPAEnS4EMIcBNaSzakeyHDexWS3qCGVVtTw5y5c/n0009ZsGABCxcuJB6PEw6Hueqqq7jhhhv2uVtYVlbGsuXL2bxpE7m5uXTs2JHs7GwyMjLIzMz82pEVrTWsr1eEhfcegsEg2dnZFBYW+oMCBg4cyLBhwxgyZAgDBgzg7LPP5oILLqBjx44p93/jjTd44IEHqKqq8gWsK1euZNGiRXTt2pXOnTunGPitLa33PN2FdvoUuyUNOk3UhKV1T0nvLOFNNNZREl6NyxKKwqAgL6hTwGTUlNRWgZ584/Uu6+gpKRVI1qGS64RXPPPSPl+y4JGYjrv07lzyMUEitB0VBpI0WUfVzq28Mu0j3pjyEeu+WM/2TRtZtXwRG9euZVNZLSqzgM4dCsmUdcQdg6i0cJRASBe8OhceQSYSCd/u2PVuMwzP6QFNvNJVuI6WRxho6YV0Fe3ywnRooMOqqa3l3Xff9b3X58+fT1lZGVVVVZSVlREIBBg3blxK72pjhMNhOnfuTElJCb1796Zt27ZkZ2eTlpbWoh3lIwmHM8I6eKHTtxw5OTkMHDiQiy66iJ/97Gfceuut/PjHP97jeLCMjIwmk3l37drFggULWLVq1R5rXkrpCcXS0U4NmoQ0kwgh9FAI08YUlichkJhCpzpGsi3FcRFSYguwvesNoecBJifxmKa2WdEnd8PUSROfgSYa7VW1u6iu00pdCUrWrTSJ7SY+A6nrZICpIEyCyK4dvPPxDJ55eRLVVVVMOOF4TjhmCLK6lPJ1nzP7/bd49a1pzN1URyAYIpd67EQtTiKOk9B6Jl3DSyrodWbsenIF15U4CYdELEE8liAWjRONxIhEosRiMdyEg3JdHNfFTeq+PESjUZYsWcL06dPZsmULiQZGfIZhkJeX1+wIaV9RWCuaj1bCOgQIh8O0adNmr79AI0eO5Morr6RLly7k5+cTCoWwbZt27drtcWirQhfWZTK18kgkWYOxDJOgrR0+heFJHJTCskwClqVTRAxcqRBSYRsK29AOCxYKExehHIR0EK6r+/+0bEvLF5LlMpLs47XmeCmmnl6jGghOhZ7ILDyCMzw3Uu3sDEDIlKhEPUvXrufFyR9TtnEdXQoLGNS/Px07FfsDVanbxto5H/LhrM/ZHAsQtiFd1aOcKI5UOJ5ExXF0wV1HLcKXrrjxBPFojGgkRjQSJxqJE4nGiMRixOMJXf9yXO12mpyo4SEtFKJ379507tzZ31kuLCyka9eunHLKKZx99tm0a9fOX9+KQ48jPiVUSuE4DtFolHg8TiKRwHVdv9fqYL62rwpt2rRh3LhxdOnShaKiItLT02nXrh1XXXUVZ511VkqKoYvuEaIJrVi3DBPhNRFLr65kGNrITqdsOu8X3mRjnQqhT2KpyLAFRWGDnABIN04iUktddRVVNdXUVdcQq61Buq7vYKq7nHcr6fHTUX19MqpJkpf+OpK1By/E8lJD0LUxpRQZlsvO8lLe+nQ+H06fAfF6Sksr+Oh//+PTOXOIRGO6j1BJkAlEOIfuffvRPstGOopaxyQuLARaviHd3WPAnEQCJxHXfYXJnVSltLOqLnuhtCQN05+8Ax0KsujUJouArWk1EAjQqVMnDMOgsrKSrl27cskll3D55Zdz7bXX7lNgfCQjuQmR/IvH48Tjcb1b2oxz6nCmhEd80b2uro6PPvqIt99+m5qaGrKyssjJySEnJ4cJEyZQUlLS5E19XZBIJHC8Fp9YLEZmZibBYDDl/UQSLh8sK6OiTqcjhhK4MoErHZRQnoOmgWVZ2szP3S1nsL3xXsorfscdSU7AYECmQ8dQhKr6epZsrOCzFV9QUVNLyLQobldA7/ZtKM5PIz0jDOFMDMv0ik46IQRdP9NkkAy/kiO/vDqRn0SCdNBWMrhIN0HCccg2EsxfvZZ7n3+L916ZBDKi9zKF0pUww9KCWDcGdoDCo0ZzzS9+xXEdc3Hr4myM2FQaYSylvF3ChB8cOY7+UQN0eisM77UZuK4XraKwA4aeFO1IpIIRfTpwbL8OZKTtTt+U1zC/fft2Ap7NsWlqz/qv43EnpWT+/Pl8/vnnbN68mcrKSqqrq4lEIgwbNozvfve7+x1r11p03wuU53/105/+lJkzZ7Js2TKWLl3KggULmDNnDjNmzCAQCDBw4MCU+y1fvpznn3+eF154gSVLllBUVERWVtY+iddxHMrKyti5cyeVlZXU1dVRX1/vR3axWMz/APf1OC1BMs0IBoOkp6fv8SRwpGL9znrq49qkzvDqUwLPPtj3chc64pFejcswtEtWg1ROKcgUCbJULcvXb+CZD+fy3sz5lJXu5OPpH/K//01n1vwFzF/xBWV1EtsOkmYqrauybf3+2S0nEMm2HW3d4MMLqrx/C4RyEZ6UQTOHJM2Q7Civ4NPFK1m9fLnWWRmm/hNe4qgUKBczFKboqBEcN3okHcM2iWiCXXFFvTQQng7Nb0dS2mlV1/RMfb2pLWiU5/cOYJgCy7IwhEHClSRcRYeCDDq3zSboRVh479GyLHJycsjMzMSytPtD4++ppVCesDfRgn5Ux3HYvn07y5YtY+GCBcz69FNmzZrFvHnzKC8vJz8/v8kPXkNEo1Huvvtu/v73v/PWW28xa9YsFixYwJIlS1i+fDlz5swhHA4zaNCgfco1DmeEdcQT1uLFi3n88cf9gROxWIxIJEJtbS0bN26kY8eOnHrqqSn3e/DBB7n11luZOXMmkydPpnPnzvTp02evH7DruixbtownnniCp556ismTJzN37lw+++wzli1bxqpVq1i6dCnbtm2jvLycQCBAWlpaE+JS3i5VUlSY/Evexh6+gP1BO47WUZ9wdOFagE7RNH3h1Yj8Kcxei0rD5xFC2wlbyqFTsJ7SygoenfQ+/3n2Rbrlp/H9S87m88/msHjRZ+wq3cr6NUuZt64MJ5RHl7b5hEWcUFq658OVtIJpQFjeZS9j1LcpvAs64RLo3UeUbusJIYnF46zbUcpnS5cjEvX68zQ1aQt0VAaKtIIiBp32XU4eWEI+CXbVxiiNKeodgXIlKIll2Rimru8JoUWyhqHtmQEtJhXCu16nyoYwEErgeMr4TgWZdClMJazmoOF3nRSvJmtoDVOu2tpaqqur2bFjB5s3b2b9+vWsXr2auro6wuGwr3bfGzZs2MC9997Lb3/7Wx7/97959dVXefvtt3n77bd599136d27d4qXWmPU19fz17/+lRkzZlBdXZ3yg5xIJKirq2PgwIGMGjVqnx0frYS1F+jXkUtOTg719fUopVJcFo466iguvvhi+vfvn3K/999/n08++QS8OsSoUaM4+uij92qsVlNTw2233cZ///tfli5dyurVq1m0aBFz587lk08+YcqUKUyePJnXX3+dl19+mU2bNtGpUyc6dOiQ8ji7du3i7bffZv78+WzcuJGdO3f61sxVVVU6FfHqBM3d0nal4ovyCFHH9TyovFFXnomeJjGdBhp4kU2yZcYjSYlACEW+GaM43WXa/KW8+vY7VK5eiECyYtU6Fi9ZSl1dvWYdpXBqK4mIEIXFPelemE7ItrGDth5BjxaYpoRV6MtC6AI7SXsbtEGfT0KemMCULqGARdQwmL9xB1Wbv0CPr7cwhA4HpYxDeg4djx3PdyeczrA2Gaj6WrbVJtiVsHCFhVCavJVXqwLdw5iye+j1MmIaeicVAa6+TeD1WApFpzaZTSKsfSF5ktfU1LBt2za2b9/O2rVrWbV6NcuWLuWTTz5h2rRpvPrqq7z66qs8+eSTPP/88zz99NM888wzTJw4kYkTJ/LGG29gGAZdu3Ylcx9mepMmTeK///0vX3zxhf8DmISUkk6dOnH00Uc3HRXnQSlFdXU1q1atorKyEsMwyMjIICcnh06dOnH66adz+eWX77fMcjgJ64ivYUkp2bVrF6WlpezYsYPq6moqKyuprKxkyJAh9O/fv0mz8kcffcQjjzzCZ599Rv/+/bnlllsYPHjwXn95ysrK+O53v8uMGTMa37RHFBQUcPPNN/Pzn/885fqHH36YO++8EyklljeXzzRNwuEwlmX5O4KZnolfcg5hWloaOTk5vhdXw3A8knCZtqyU8rq4TnWUp9I00HTg6YxAuxNoYzrDa9vR5KhnGSp6BmvJMGPc/d9XefLp/+Ls/IJAIIBpWcTjji5MK4VAyxlyivtw2jkXc+2pw+mal05OYRuEHdQDpL0DqdF5470mHei5ShOFlJ4GS7m4TgKpBDhxgipGaU0Nz85dwX9emMTW+Z9BvGr3Q4Wy6DruJM656BIuPKY/+YkqNu+sYlmVyc5EQG8oKN32o7wISn8kuq6l0DU+IUxcJK4AS9hYykDJ3Q4PCUc3P4/sU8RxAzqRGd59nDiOw6xZs9i0aRO7du3yf3zq6+uprKxk165dxGIxKioqiMVixGIxEo6D9BwakhGW611O/tjKpHLVw9Bhw7jzzjs5fty4lOsbYuLEifzud79jzZo1jW+iTZs23H///UyYMGGfhFVeXs7cuXNZv349lmXRpk0bf1e7oKCAwsLCfaaDHOYa1hFPWI0hpfSN+PYm2KutrWXt2rVs3bqVNm3a0L9//31+CXV1ddxzzz3897//ZcOGDSnukntCTk4Ot912GzfccIN/XTQa5eqrr+a5555LWdsQokHjdSgUIhTyBot6l/Py8vjjH//I6NGj/f6ySNxl8tIdlNfEMAywTE9ljlZwC89SRRh6K9/w/KQctXuL3pUKS7gMyYoSVXH+9PBTvPbcc1DfYF6iV5zWhAVKOqS168KxZ17EdWeNp2+moKhje6y0dNwGynF80tLFdv+1KYHrTbXRrwWQLtLRnuuOK7GdKKYTZWfM5Z21W3jvf5+wetlyaqqrMe0AQ0aN4YSxx3Ji/xKKzTilZaUsqYAvYiGimFgeSQnvuFVe643wiAu/advAUZKY62AiSDOCBEyTqOPgSknc0Q3Qo3oXMW5QsU9Y0WiUTz/9lD/96U+UlpYSiUSIx+NEo1G/PBGLxfxI7stg2PDh3HXXXYwdM6bxTT42bdrEM888w/vvv09VVRXt2rUjKyuL9u3bM2DAAM444wzatGmz3/PVdV3q6uoQQpCWluYfa81FK2EdZkgp2bBhA9OmTWPdunVUVFRQW1vrexIl61L19fUEg0FGjBjBJZdcwtFHH+0/RjQa5aabbuKhhx5KeeyW4t577+Xqq6/2U4NI3GXysh1U1MQQQmm3Bi+KUHK31ME0Da3LUrvtXJQXZTmuxCTBMbkOCUvx+4ef5NVnnoG6cn+MPejgCE+SIN0E4Y7dOfa8y/nhScdSEojTuUsnAhkZJKRHQMm7NSAs0P2ONLCYcTwVupAS5epUzQVkPIYdj5BhKqrTwizcXsbyLTupqIlgBoKMGtiHfgVZZCcilJbtYs2uGCujYapVQDc2ewmmEDqtk96QCdMw9DgxzWQIBI5yiTkOhlSEjQDBQJC46xJ3XaJxB3cPhFVeXs4jjzzCb3/7291v9ksgWfdMT0/3a1bpnlXx+RdcwDlnn01RUVHju6Vg27ZtLF68OIWwDrWtd2O0EtYRhvr6eiKRiB/+R6NaFV1WVkZWVhb9+vXb4wHy3nvvccstt1BXV6dFiw0Kr1JKEp6GTErtU5WssyQRDoe55557uPjii33b3WjCZdqKUnbVJfRgBs9aRSqvfcbfJdzt7CmllgboKTEK1xOHHpUeIzc3wF+fe41//fM/OFtWYxqWHgIB4OmtUArXdcjtN5RTLrmSq4aW0MlI0KFrZwLp6TgN3SFAywYkvpgVpVB6TI5Oz3SS6annkz2G4LoOKhbFjNYRNiRp6ek4aWHidgAhDNKceuK1NWyrirC+1mBDzKBChZDKwvKGX0jpJrNQpJIIqTchMA0d+UjdLakn+kgMqfRQWtPUUaCURGI60mpMWBUVFf5Mwaoqnaom64/JaDn5F/BmDdq2jW3b/nXhcNhP+5PpVps2bcjLyyM9PZ38/Hw6deq03525IwmthPUNgQLWr1vHtm3bqKqqora2lsrKSsrLy4lEIuzYsYNoNOoTYbImUltbS319PWPHjuUPf/hDikwjmnD538oyqiKOjp5cl4QnhBReMVuhrzeS8wGFgUIQT+gWH2FZ2IagC1UM6pTOxDnL+PsjT7LywzcwXAfDsJGGPgxMBAlHCzV7n3o2F19wHqfmQbtwiLz2HbBCIT24VGgpvBD6jbtS4ibikIijnATKkeBqqxelPGNA00YF05DC1CPCpAtOApVIEIvFsVyHoCExTW2RXBtLUBGTbHMstrshIhJi0kJh6Z5JpYnfdV0d2AmBITy1v9CfiZt0cfA3InStz5GeRENBLOEiXcXoPh04bmBHn7CklKxYsYJf//rXfPrppwSDQQoKCsjKyiIQCPjRUVpaGu3atSMUCpGfn09+fj7p6em0adOGjIwMsrKyCIVCX8oX7UjCt5awLrzoIu79BhEW3ueXrGkk/xpfdhyHWCzma71qamqorq6mb9++tG3bNqU/LZpwmbGqnMq6mE5vhK5POa6rrX0VIHSEJZMqd8+gLhaLIZTANC1sy6DArWNUO6gJWNz/3qfc9+A/SSz/NOX1J1Fw7Bmce+nlnDOgM51qt1LUrj1puXlgWVphb5gIZSCdOG68DjcWxY3GEfE4ynF9CxdtqOc5lBoBCKUhQmkQCqNMSxOK65CIKxKOxJUuCdclJqHGgTopqHEVdVLhJBwibgBhBrFMC5QuZDuejY8QBpYdQAmFlC7ScXyVe9AOYBsGUmmnCEdqR1YlFU5Ch2gj+xYxdmAHMhsIRx3HYcuWLaxZs4ZwOExBQQFpaWm+fi4pRUieI4anqdrT3zcFrYT1LYbytDuu6zbpIcQjrOnLd1BVp6MlwwtppFQkXG3mh9f8rOUDeBGXJBqLoaTEEia2bRKUkg5WhO75JtVunA9XbOST+UtYtXQplaU7kEBumyK6de/B8CEDOLpLOzrZikzLIKtNG4xgIHUnrrYGN1KLjEdQ0kG5CqWlUx5RueANV9V1ev1fYRiasNKzIZSGUuA4koSrLZRjriTqSmocRcRV1LuSescllnCJuwEMIwQCEm7cG1PvbRQAyiMlvJ1Jha5jBU2TgJc6e5U26uMuCUcST+hoa2TfdowdmKp0TyIej2N4HQXfdhxOwjqsOqwB+9FhfRuQ/HXe24ngSMWGsjoicQeVbIwR+iTE690zDAMUejCo58IgQG+vSxcDPV7eRVAWgUhdPd0ybcYN6sa4MSM4asQxHD3yGMaOH8c5E07mgjFHc0zbEG1lhHAwRFZhW0QooE90IcBxkPW1JCq2Q7QGw3W8HkFPze7pyrUiX7OGTlNBOQ4iHsWNxnS3TyCIsCwUejq1ZHeNLo6WRiSkIiF1VATaxCueSBB3Er6fVzI1jTu7hbsIw6vPKT1R2tWRn4F2RVVS4bgSx9G/2Z0Ksyhum7VHHZbZZLDHtxeHU4fV+g18DaDTyqQxne4PJOmOgADHxZAulpJYSmK7LpbjYEgXQ0ksFJbS9sSBoM0uI5PFuwTrvygjvXQzw4JxzuqSw3e7ZDLEKCdr1yZELEIgO5e0gjZI20KhW16UUjixGE51JcJ1MISeRJ0coqqtZlxtQYPWdGlP92QEBFgGCImbqCceqfYU7bpuJdHe8AitsVLeWDOpdPrrOA7ReIx4Iq7rYyjtJa+LWBimhWlZCFMPkRXC9Gp0FgnDIipM6iXUJyQJ6YCQmIYmf73nmJJwtOIIQythfcWor6+nrKyMbdu2sWLFChYsWMDHH3/MW2+9xbx585pqwHz/cq/Nx9umNzH0IAeldIRm6iI0roN0EjhOAunoYrJ2KtDr0mwDKxCgRqRR6oaJG+kIZUFcIeIS2wgSyswlnFeInZUFAc8FQgid0jkJZKQeGY96/Yv6z/9X0ud9d8uhvq9nnazr3ELfI5FARqIox9ntRe8RhrfaiyR1a5ErdRtNQnnjwbz0l2R90HtkvN1D6SYQ0sVEt+TYpoVtWRimgYMiLqU3XFVPGUpGgw3hOA6zZ8/mzTffZNq0aSxatIgVK1awadMmdu7cSVVVlf5eWvGV4LDWsL5pu4SNsX3HDubMns3GjRspKysjFotRXV1NdXU18XicmpoaXwQbjUbJzMzkt7/9Lccee6xfeI/GXT5cto3y6iimaRA0LZR09eAFpWMCnW5pcz4B2rTOkdRLF0cpLMMgaOp0MWDoOfOuVOTY0L9NgPw0hXQTgESYAsPQEYoSuwlDJKfV1NXgVFagInWeD1YqlL/RoDyZg0JJgasM9Mahg5B6sk3CBRlMw84rRKVlEHcFMVcX3eOOpDohqXcktY6kLuFS7xjEXIEr0Smo0PmxodAaL6UFsAqJ6zrggiG07EChp/EkPcNc6RKNRZAOSFcT6Mg+7Tl2QIcU4eiMGTO48847qaio8HVTtjdxKRgM+juDtm2Tm5tLmzZtOOqooxgwYECjT+abg8NZw2olrH2guroapRRZWVlNPrhYLMYXX3zBggULEEJw1FFH0blzZ7/9p7Kykhdfeol/P/44mzZtoqamxt8d3Ncv8j333MPVV1+9W4flEdau2hgIofvg8Mz82D001HUT2jHTnxehcE1D652kQrkulgFBw8AwDVwJQSHomRugpK2NZXge6cZu/3bNho0Iq6oCp7IclYj7jqINoQlK4nq6LG9PAISJ64Dj6rqaT1iWjZnbBpWRS0IK4q5LzCOs2kTyz6HOhYhrkFCm7hlM+sej3SvwdvwMUzdoKyHBc74RQnuBCRRByyJgBxACaiL1JBISJ6G7BUY1IqyysjIeffTR/QpHAwE95DUtHCY/L4+TTjqJH/3oR016XBujqqqK9evXo5SiW7due+3cONJwOAnr4DHREQ7Hcaip0ZsIzUFVVRXPPvssTz/zDHPmzNFanwbYtGkTjz32GD/5yU/4yU9+wjPPPMO2bdtSbn/3nXeYM2cO27Zto7a2lmg0uk+ySooMG39JybsopbwTXg8GNS1tnSIFOFIQdRT1CZeokriGIGhZpNk2tqEjjASKBLpVxjUgKiXbq6PURuO6QO7ZMPtPmMzhhG5g1i/C9exidHSXhM5Wd0dXUiocVxF3XGJxLcEwPcM8/90JncYlm5b18/ijMzzO1M8jpTdHMOH65KRc15NQaLcFpaROhaWLKUwClo1tW779jUSScBK48Ti40ks7DZ1yeq+h4UdveM3B+yOSeDxOJBKhoryc1atX8/rrrzN9+vTGy1Kwa9cuJk+ezJ///Gf+/Oc/884771BRUdF42X4RjUbZtWsXkUik8U3fSHxtCEt52/9J5XgsFmtCInuDlJKFCxcyadIk5syZs8eRXA0hpWT27Nlcf/31/PQnP+Evf/kLZWVlKWSzatUq3njjDcrKyigtLWXKlCls3LjRv900TX8qSlIdbVkWtm0TCAQIhUKEw2HS09NJT08nz/tlHjFiRErHvj5/vPoVaE8nV2EJQdDwZvuZAtPSfYDal1w3RNumiSUEAQPSAiZBrxnbNEwsYeCiKIvEKa2J+0MsDCV0hJYcQqGf1IdKviihi93JmwRaX5ZIaNW4Ji6B4yrqowkqq+uIxBO6SN/gsFPoHcEkNSmlB1b471mXqHBcSX0kSrS+nng8hutN30mmxXoKrHYUTXhiUkNBUBnYSmB5waIjJREnQTQe8wJKbXOhlFfra/Bec3JyOOWUUxgzZgz5+flkZGSQnp5OWloaoVDI12ElG92T33NOTs5+d9BWr17Nv/71L1555RUmTZrEQw89xPLlyxsv2yeqq6v5+OOPefLJJ/nggw98R5MDwYHe76vGYZU17M9epiF27NjB6tWrWb16NZ9//jmzZs0iGAySn5+/z5RVSsn69eu54YYbePTRR5k5cybDhw+nU6dOjZf6qK6u5oMPPuC9994D7xf0pJNOol27dv5zJbvev/jiCwCGDRvmrwHIzc0lEAj4Nh5dunShZ8+e9OnTh6FDhzJ69GjOOOMMJkyYwIQJE7jsssu44oor6Nq1a4r1jOsq1u2sIhLXFsCGFy253pRj0GZ9SulCs2UYpNkWIdPE9grxhpIETQshTITUhKCkJv+4o3cRC7NsQrZ25sT7ngRJX/dkJAIqWoeMRWg4J0sISHgDISzLwrRshKEjG8M0se0A9XGX6po6wqEAluENxXAlrhCIYBgzmI5UWsahi+vo1ND1tFiOIhZ3UQ2NT/H8uUwQppZNuI4mHSGSIzE86BAMF4WDxPXIKjkKDIm2l2m3215Gnwe5jBo1iuOPP57jjjuOsWPHMnToUAYMGEBJSQmdO3emXbt2dOjQgVAoRJcuXbjwwgu54IIL9uqaALBu3TrefPNNtmzZAkBWVhYnnnhiiwanPvfcc/z2t79l0qRJfPDBB3Tp0oWuXbvu1ZVkX6ioqNir/VJjHE5ZwxFdw1JKsXr1ah599FHmzp1LeXm534MXj8cpLi7mhz/8IVdccUXju/pwXZeFCxdyzTXXsGDBAvLy8njmmWc4+eSTU4ihIRzHYe68edx4ww04jsP48eP51a9+RUFBgf8B1tXV+Tt8QgjGjRvHwIEDU7702tpaduzYQW1tLYFAwLebSf4iB4NBXQQWwo+6GiOWcJm6ZAtlVVEUCtOydDzj6kjKNgwMAxIJV0cNoAdMGAaWpV1CkXo0GEp/HgodTSQSDgmpCAgY1CGdHvkBQpY2BU1mg0mpQTI1dGsqcSvLELF6pNY5kIhGiUQivqurJGlJrJuftbrcpbY2QsgKELQtEo5D1HGRgSB2bjtUWiZxpYg62so56ipqY3FqEpKqhKI6JokmNEH60RhaTqG8CT6Oq1NGgXa10AV2rVGTruMN8fAGbCiBKQBhEk8o3ITLyL5FjBtcTGa4qYA3uTnSMMpP/tvxekIjkQi2bftWLY1PtobYWVrKB5MnM3nyZJRSjB8/nlNOOaVFQy3uuOMO/nb77VRVVpKRkcEf//hHrrjiimbXllzXZfHixTzyyCOsXLmSwsJCLrvsMk4++eR9kt7hrGEd0YSVSCR48cUXufTSSxvf5OOnP/0p999/f+OrU1BTU8Nf//pXPvjgA4466ih+85vfNOuXbM2aNSil6Nq1616FnYcakbjL1MWbKa/x6l9CYFqWrjV5aZzyiu2O1CclgDAFQligdDVISZeQ18KDof2yXNfBUZCQgsJ0i6Pbp9Ep2yDu6kNCk5bQU5bRjdYyFsXZVY6srkCYJm4iQaS+loTjUpCfj1Ja5CmVDs+EUijlauW7MnG0dQOOk8ARBmZ6NnZuG2LCJuZIYq5L1HWJOlAXT1ATl1TGJdVxRcz16mlenqizGP3adEqXHIEGpjA1uZuaqLXMw0G4avdYetMEQxNWwnEY0beI4wd3JmsPhHUkYsbMmTz00EPM+OQTBg4cyG233cbAgQNTWrv2hZqaGp588kl++tOf+td9//vf57bbbmtiTtkQh5OwDh4THQLYtk1RUVGTQaRJHHPMMRx33HGNr26CjIwMbrnlFiZNmsRdd91Fly5dGi/ZI7p160b37t0PG1nhn45aIGqZJiYgE47evPMcGeKOgxQCaRhI08A1tHTTcSWxhEM0niCecIm6iriCqOMSTTgkXE1IlimojkvKIzr6El7EkvwlM5TSY+ilwrRszEAQZdrguphCEA7rJmDXbxXSj6FFpPoPdLQFum3HBYxAGlZ6FsKyEZ4qXjuqKgxPEuEqSUK6XvE+TjQWIxaLE4snSMS1OV4iEcdx9ZguQ1kgTZQE4UpsV2FJhaX0QAopFDE3QdyJa9J3JMLVw1197dfXBMcMH86999zDe++9x+OPP86gQYOaTVZ4djcdO3ZMqZm2b99+v5sMhxNHfA0rOzub3r17ayO+AQMYd9xxnHTSSZx66qn8+Mc/Zvjw4XvswWsI0WBS875M+htDfEVNqzt27ODTTz+lurqaPG8qSxIJr4ZVH3MwTV3UdV3deiKSBWtPPOoq7Y+lazMGSG9qjVJ4mnCUECSk1FEQaD2TdKmPJrCFokteWrJa5dNlymdgmDotcxxkLKKTRUObzXvegR69aqW6hp6ioyUIoFwXYdpYGdmYGZk6gvMK6K7350ildz1dqHcg5qD1V0kkX5MvGhWA7h9MNlwbSmIbeISpZSBuMhoTCqH0Z4VHVp0Ks+nSoIaVxIwZM5g1axZCCAoLC1NuO5xI7mImXSFamgkZhkFubi49evSgS5cunHvuuZzteXLt67hvrWHtB9FolM2bN5NwHEKeWM+2bQoKChov/VqgtraWrVu3MnfuXNauXcuKFStYv349ubm5/P73v2fYsGH+Zx6Ju0xZvImKmjimaWAoSLgJvaPlSFwlMQ0L0zKJO3GdMhoGUgl9u6d5EgZYQhOeI11iCUcbACrd1iOlQV6axZhuWRRlWQhDF8CTUYd/4BgCpELW1xMr3QyJKAjdVpM8kAR6jZCaJKXSRW4pwXWFrj2lZWBk5aICIRyphZ6xhCLqKiKurmPtiknKYy7lUUkkDm5SLOpJGJQ3MceVEiHwhkrodFcphQUELS3/AEh4u41SuUgkhhSYmOiMWjCyX0fGDtptkRyPx1m0aBE333wzO3fupLi4mBEjRtC5c2e6detGcXExhYWF+6z3fB1QW1tLaWkpWVlZ5Obm7vd8P5wp4REfYQFYlkVeXh5tCgrIzc0lMzOz2TsaRwJqamrYuHEjK1as4OOPP+bNN9/kzTff5Pnnn+edd95h/vz5bN68mTVr1nDUUUfRt29f/yRwXMmabbuIxHV44UrX3/tyvSKyYVoYhm7yNQzd8Ou6uvfQK/dgorBMC9s0MYR2NNAGf7r+ZZuemV08Sl44SJqdjLO8tpuUKMvQ3lbSBeWCJy8R7D7AhFIIpW37PNpCKYFhBLDSMzGzshFB7dQgvcnWrlQ4ng+8KxX1jtRF94hDLL67wVpKrReT3kgzpfRnY3pTcJD6dUvhPZYnMNUTdvQ0amEkR395dj1IOhZm0bVdjh9hVVdX8+qrr/LYY4+xY8cOVq1axZw5c1i0aBGLFy9m8eLFLF++nPLycurr632frK8bAoEAubm5hMPhZp3rhzPCOqyE1a9/f05pBmF9neA4DrW1tVRUVLBlyxaWLFnChx9+yGuvvcYLL7zAs88+yzvvvMPnn39OWVlZipDVsixOOukkBgwY4O8YOq5k7dYqIgkHQdKGWNeD9OmmletKKd99NFlQ1yGP0K6b0tGFaN8vyyMspSlJoP2odlTXELZNctNsQrbpuyHQ+OARAjNgg2npQrfU9sy7V3iDJ7w0UKJAWNjhTKysbEQoTbszeH5VUnpRmEdYCVdRk5BUxhJU1kWJRnXNyUk4erKz57mF0IV4w7OKtpTQGw1CD3tNkp+QXojnkejuepUmLFcpOhVm07VdNkFb1yzr6+uZO3cus2bN8r+neDxOWVkZq1evZt68eUyZMoVZs2axatUqwuEwRUVFB/1EPtJwOAlr37HfIcbBo8HDB9XAkG/Xrl3MmjWLl156ib/97W/84Ac/4KKLLuLaa6/l0UcfZfr06ezcuTPl/oZhYNs2GRkZDBs2jKOPPjql6GkILU8whK4dGcLQ2+mujoxMw/B83pO2xLqCZBp6uz9ZPUJoInOkJOHqk165LkhNXPUJl0giQX1CsWxbFRsr6nGkxGigaFfJepGXSgo7gJWZi51XiJWZhQgEtUOCJ/5UoGMrzzXBTgtj5eRiBMMgvAjOMxvUNvG7HRskgoRSxBMSJ6GtYRKOnhqdcLRyXr8e7zgSup5lKIkpJKZyMaXEVoqgAktpj7CEI3Fdr8YlhLbkEQapclaN7Oxsxo8fT//+/cnMzCTg2SA3xoYNG3jttdf44x//yLx58xrfjOsNTJWNJuW0ouVo/B21ooXYvn07M2fO5N///jfXX3895557LjfccAP//Oc/mTFjBjt27Gh8lxQUFxczYcIEbrvtNh599FGGDBmScrtSCmEKLMv0p+Mkm36FIbSTgpIpEYTeZdNpmfR694QA0zLA1P160UScuJMAqaMx19F/AcOiMi5Yvr2GTWW1mN7cQx3Z6eI1QqKERCkXDIURTsPMy8fMzcXIyIBACKwgwg6CHUSE0rAyc7BychChMAgtd9DeWbtV8VoyphujfXJ1XBxXoZRAeI3MuiUJ3eQsXaTrYLgKU0oMpTA9mx1LKSwJNoKAaeiOAMMr/DtgSoGttPWO6X1uDWFZFkcddRT/+te/uPPOOzn//PP36OWfxIoVKygtLU25rr6+noULF/L222/zxRdfNLs7oxV7xtei6H4koa6ujv/973989NFHrF27lh07drBz505qa2upqqqirq4uZX1yDH04HCYnJ4f27dvTuXNnfxp1x44dadOmDdnZ2WRnZzcRs0biLlMW6aK7HvAgcZXSk2HQhKSkwsBACfz00PXaZJQ3t9CybQJ2AMd1iHqyAFe6KG9QBUqiXKkL84EAyo3TLmwwpFM2Xdpm6hRKKK8ZWkOAr9Ey0OJMXBccrRHTpSWFMkyUAcowkdLyxssrPWLLdYi5CscRxB1JRLrUO4qICxt21bOhrJby6nptf2yZ3gxGPcRCSIWhBLYlCFkmQdPC8OYMOrLBziRal2YIvcupvIZxCx0Nxh09o3D0wM4cf1TXJsJRKSU1NTVUVlayZcsWduzYwY4dO9iwYQNffPEFpaWlCCEYMWIEl156KSUlJeBtFv33v//l/vvvp66ujvbt2/PHP/6RsWPHpkhl4p5zh23bftP7kYzDWXRvJaw9IKmkT6rTG2LWrFn87Gc/Y/bs2SnXJ5FUsdu2Tdu2bSkpKaFv37707t2bIUOG0KdPnz0q2veGaNzlg883sb2iBtATYZTS476E8JqhXYlQnpRB6BREug7K9aa8WCbBUBDTMInGIkQiURKurhslEnE99cZLDw1vZFgsESfdkPRtl85RnXPJDIe0NKIBYSWhUtJ7odtl0OPIhBf1Ocrz5nKTO3x6cEVCusQchZOAuKuol5K6hKLOUawpq+aLHdVU1kQIWBam5UVIWnuKknonMGRbhCzdI+lKnfYlG6ilJzR1FbrGZVuYptcMndAPlHC0pGLM4M6MP7obWen7lsk0Rl2dPkca13RKS0v5wx/+kDL67aGHHuKyyy7ztU/xeJw5c+bw8ccf065dOy655JIjvnB/OAnr4DHRNwTxeJyPPvqIW2+9lVmzZjUJ4Xfu3NnUZM9DRkYGY8aM4frrr+fRRx/l5Zdf5qmnnuIPf/gDl156KQMHDmwRWZEsOnobFdFoDEdKXY/S+24Iy8AKaFmDZZo4riQSjxFLJEhIl4Srp0HjTbWJxxMkXBfXTSCloyM1zyEhAcSkQ00kSnbIpFthJgXpQWJxBzeRQDnat13omvvu15j8hyc3kN5gCSFdnaq6CuF6CwClLUL9O+qYSb8fvcYz3/MiRkN4ynRfc+Xdz3sY3WYkicRd7dPuGU5o8arEEmB7vYW4oBwFjrfjmKyfKR11HQiSDdGNkZ+fz8iRI+nevTvhcJhx48YxfPjwlB7DDRs2cPPNN/OnP/2J3/7ud8ycNYt4XPv3t6IpWgmrEaZMmcIdd9zBU089xYMPPsicOXNSbh88eDCjR4+mXbt25OXl0adPH84880xuueUWHn/8cR577DF+8YtfcOaZZzJgwADy8/NJS0sj4HkmtRQKhTIUVjAAnp7IFIKA592uUz7dN2eaJpapR2BpoaiXIgKJRJxEPI6SEtPw2laE0KPklfbBEoYWlWYGTDrnplOcEyLDBoEnJfCGO+jiti7ua4lo8rVqoiDJRZ6kAj8102mlbhVKujF4f0KvkcnoSUHAsggFLK/upHAdiZPQRXO9Q4r2bccgoQQJV2m1vZKa/JTCVGB6mixDgSHBkArTV9N7ei6lNLEfRBiGwSmnnMKTTz7J008/zQMPPED//v39qMF1XXbu3MnChQv1GLjt21m7Zg3RaNR/DMdxWLt2Lc899xxvvvkm27dvb/AM3z4cVllDc3VYBwu7du3i448/ZsaMGSxbtgzDMJool9966y2effZZqqqqiMfjDBkyJMU9MjMzky5dujB8+HBOOukkzjnnHE499VTGjRvH0KFDKSwsJCMjY687SntCIpFg1apV2HtogE64kjVbK4klkie4xBRgW6Z2zlRaC2Co5DAKLwpR0ksbDc9ZQRezFVLP9PPITkseNAkaQtd5uhdk0yUvjWwbTMPFNg1s2/IjIk/H7odIybepUDrqSeqhkuQlQE8HVOANmNAXvVFgoK1oZHJ6jiShIKqEjprq47iuwlXaaVXX7PTQDUsIhExKNyS6pu5JKqQOHXXbjW6CTkZp4FnTSE10UkLnohy6dcglFEgtA5SVlbFy5UrfabQlCIfDFBcX06tXL9q1a9ekxBCPx5k/fz4bN26kqKiIa6+9luLiYv/HbfXq1dx+++28+OKLzJgxAyEEPXv2bPHrOJg4nLKGbyxhua5LeXk569evZ8mSJcyePZvXXnuNZ599lnfffZcZM2ZQVVVF165dUxTzO3fuZN26dZSVlTFq1ChOPvlkOnfu7N+eJLm+ffsycOBAevToQfv27cnKyjqgCGrLli28+OKL/Pe//2X9+vUUFxeTk5Pj3+54hFUX1dGR4Qkx9bgvfaK63oxCgdA7fq6DANJCAe1IIKUmLiEAhSm8E9czwDOV0r7nAgoyQpS0yyE/bGLiYgg97MKytDg1GTYJ9E4laD8pPPoSGDr1apBeCb0X6BNWMrJKGv25ng7LcSWuVwBPKIgiiCVcauvixByvKuU9jInQaZ4ClXRhUJowEZ54VOLNRtSyjt3JZLJPEaQ0SEit1+pSlE33jnk+YUkp2bJlC48++iivvPIK27ZtY8iQIQdUY9pTHVgIQXp6OkVFRRQWFnLiiSdy5plnpvxozZ8/n1tuuYWtW7eydetWAoEAw4YN2+du5aFGK2EdBMTicWpraigrK2P9+vXMnj2byZMn8//bO+84qcrzb1+nTdvZ2UbZZWF3KUsXlCYoRbE3DFGjxhZNNPklsSRq7MbYY4wmvmowscWoaRobYK9YAekivS8sZfv0U573j+fMsLO7wC6CCMzlZ2TKmbNTzvnOfd/PXV566SWef/55/vWvf/Hmm2+ydu1aampq2Lp1K1u2bKFPnz4MHTo0vZ+uXbvSuXNnAoEAP/zhDxkzZsxuHaDtwXEcXnvtNW644QY+++wzPv30U0aOHEm/fv3S4mfbDsuq62mIxBBC4NMNUNwyFXf2HumRXjIIb9kyNuX3eNMjwRRFRdFkcF3YDtg2timHjcp9OHh0lf4l+XTL8+LTpECAdAlVQNdSPZHlBJtUDSGKtLhkTElaealjRkqc604iUy9kr/ftSaKWLWcYWqZsvGcLh7gjiKOSsARN0TiJpCUHb7jqKP+WzF63HZn2IN3K5hafI/8Tstlg+gUBjpBtk6VbLONXPUvyMwQrGo3y5ptvcuONNzJ//nwWLVrEscceS5cuXXbrx6ktdF2nsrKS4447jiOPPLJV8XJVVRXvvfcekUgEj8fD4Ycfzrhx4+jcuXPGdrgnvOIuam3atIna2loE4PP59ug5vC8Fq7Xs72ek6gxnzJjBM888w+23387FF1/Mueeey4033shzzz3HnDlz2LZtW8unEggEWn3oBQUFnHXWWfztb3/jlFNOIScnJ+PxPYlpmnz11VfpXK14PM6qVatobGxMbyNcYRNCoCsySVTXDbmy505U1lRVdtO0LATCtYZUEqZs0OcghcY0TeLxOGbSktYFshtCwjKJJhLoKpTkBwh4QFMVWbvoNgdMJBJYponu1iraQiCELXOxHCGVQCATSoXbTF06XshXIO+TLWC2x8K2W1sOphnHdrsoOLa0ClVVQVWlK6wosv+VdGch6QiZEuE4mEKkhUcIgapp6IaBrhvohuE+R9YsygG0qQ6jbieK5iahSyQSYf78+elUlc2bN7No0aKMGNOeoi0LDGDQoEFceeWVHHnkkRx33HFMnjyZvn37ttwM3JPbcRzeeecdrr/+eq644gqeeeYZwuFwy033W/abtAb3lGD9+vV8+eWXLFq0iPnz51NVVcW2bduoqakhHo+nm6vJOMV2fD4fXbt2paysjG7dutGvXz/GjRvHmDFj9qoo7QwhBF988QVPP/00K1asoKSkhCuuuIJhw4alf8Hjps1bs1ezsaYJXdPxGjpClaU1svjXtUyEg6rKchSZrwUBw53+kkiQtCwS8TgCUFUdoYDtyJU423KIJ5L0Ly7ghME9UJGWTkpchJXAMRPEIk14dZ28UC4enw9TOEgtVGR9oSLdQZHOcpe90oWbkS7cqgDHQaY4uNOrI5Eo1Vu3YjsCjy+A7QnQqGiEhYf6iMn66lq21DRhaAa6AhrIVAVHdl6Vr0B21lAVuQihapoM1ruvT3YWlYsH8kPArW1UsYV87RMOq+DYET3TaQ3JZJKFCxfyxBNPsHz5cnr06MGtt95Kjx499piFtSuEECQSCSKRCIZh4Pf7W1lhzVm/fj2/+MUveO2118D1GF555RVGjBiRfs3btm1j8eLF1NXVUVZWxuDBg3e6z5bsy7SG/UawAGKxGH/5y1945JFHWLVqVcuHM/D5fOTm5pKXl0dhYSH9+/dnyJAhjB49mn79+u3VTg+JRIKmpiZUVU33dd8ZjY2NrFq1im7durVaBIibNm/PWk1VXRNCUQh4vOi6imXZsgGfbZF03XZd1xFuNwJFUQh4PCAE0XiCeDyOY9uoqoai6bLPlG1Kd09RsSzBYd2LmNC3k+yJLtw+o0KALQVrzYYN1NY30a1LF/pU9MARyXRMyVEVt9xGxthSXUqlBeWKlxBY7qxE213Ri8UTbNm6jS01NQRD+QSCISzDR1jRaLQ16sMm6zbXUr21Aa/uwZAdkRFuf3bLASftKKaQ4iVdVnnMqYqsl1TclArZ80tFURRkv0KFow7ryTEje7fKw4pEIqxcuZKioqKdNrbDPX/C4TCxWIyioqJvTdhSbN68mZtvvpmXXnoJy7Lo27cvTz75JAMHDkRVpVX+j3/8g7/97W+sWbOGo48+mptvvpnKysp2n+f7UrD2qxjW8uXLeeihh5gzZ07G/apbj+fxSP+3rKyMUaNG8b3vfY9LL72Un/zkJ1x00UWMHTuWsrKyvbbCYlkWDQ0NfPrpp7z88sssWLAAv9+/y/5CXq+X4uLiNi09y3ZYUVVHQyyBoqp4FAWvJgXQsi1ZF4eQ7pquSyvCdlcIVRXbkXWHTrpTgZC1c+5KoSYAWwbmK4qClHfKkSuPSmrlUMbF6pvCLKveypw11dQlBJ2KisjxyIA3bkIruAMkml2255pLi0q4HRZwBIlEkvr6Bmpq68gN5RLMzcPj84OuIxSVuKMSMy0awlEawzG3GwM4joXluKkLbqJqysJKfc6KKx6Om+IgSLVrlnErBeleq25/eeE4VBTn06t7Id4Wq4Qej4euXbu2Kwt948aNvP7660ybNo2KigoKCgp2+t3vaYLBIOXl5RQVFTFw4EAuvfRSRo4cud1ij8e55ZZbeP/992lyY779+vVj0KBB7RbXbAyrnaTSBZrj8/kYNGgQp59+OldffTVPPPEEL7/8Mn//+9/5zW9+w7HHHvutdQ39+OOP+eEPf8gFF1zAPffcw2233cbNN99MVVVVKxe1vQgBkUQcM5lEceSYqngynk761DUNn9cr0yjcse6ywFm2l5EukIOma9KNAkwchCLQDR2Px5DdD5IJNFW4TQIVPJps0le7rY75y9bw5qyv+Hjecr5atZ65qzYwY/kG5myO8WV1lKU1cWpiDo5QMTQNj67iVcDAQcMtlHZMVMdCcwQ6NopjEQs3Eok0kZeXS2FhIQF/AF03MHQdjy5dOoEbK7MsLEt2Ck1aFqYjrUAUUDUFRXOD/yqomkBRhUy8UlxBU6Sophr2yWEWKobHwPDoaIaCo8jFgG/CM888wzXXXMMDDzzA008/TZ174n2bDB48mKuvvpo77riDiRMnZhz7uq5TUFCQvk/TtDbnbn5X2acWVkfby/j9fvLz8wkEAnTq1ImzzzmHn//sZ1z6k59w2mmnMXbsWAYOHJhu8ZEKPu/J198Sx3HYuHEjf/jDH/jzn//Ml19+SUNDQ8ZwgpNOOilj4k5HSFoWC1dXk7RkTaDq5lYJd9Kx6g610FQN0zRlVwD3c1bTAXtpXViWzIYi1SHBcgeaWiaq4lDROY/uRUFs26axqYn1m7eyZss2toZjWA4EdR3FTFJfV8fGrTXUmBob6uOsr49QVR+nOhynMWGTtBWE0uyzd0XCcaTF2JSw2VRbT6QpQq7fS35hAV6/H03zoOq6jIkpClFLIZwwaQxHiUWScgEAEK4rp6KgKhqqu3qpKHLlUlGQaQyuxaW6QzkU3G2Qo8w0Q8UwNGT6mkOPLvn0Ki1qlYfVXpLJJI8//jiff/45lmXRvXt3Ro0aRVFRUctN9yqqm0hsuCPmWj7WtWtXcnJyKC0tZfLkyXzve99rcx7mjtiXFtY+FaxDOugSappGaWkphxxyCGPGjOGYY45hxIgRdCstJT8/nxx3jPiefL27IpFI8Oyzz/K3v/2NpUuXYllW+jFN0zjmmGM466yzdvtXzLIdVlY3YrkVQgqyN7l0a1zxsWVvKMuSTe1UVcVreBCWdAftVIGzi6rKAmnHbVPjOA66plJWlEu3Aj9NkRg1TVFq4yYJoaF6PAT9fvKCAQqCQQxFIRaJYAlBIh6job6RmrpGNtbUsm5LLWs217FuWx1VNXVsqGmiqj7KxoY4VU1x1jbE+XpzPau31OLVVSq6dsIf8KFoOoqqyzcku+QQtaEhlqSuPkw8ZqJqbvKnIjdTXTFSXGFUlFQeVkqwZSKsqqjomi7jWG4KhtyPiqbJFU/bcSjr+s0EC2DdunWsWLGC+vp6zj77bCZMmLDHT+xvgqIo6UWn0aNHc8QRR9C1a9cOHZsHrWB1NIaFG0/o1KkT3bt33+1kzT1JMpnkX//6Fx9++GG67jA3N5fBgwczefJkLrzwQg455JDd/gxtR7ByYz2RaELGoBRk4FxRZQq3Y2MlkjiODKirgFfT8Hk8mEkT250UnerqkDIz0sFy20ZTZUyrtCBAl6CHhmiCqAlC8+Dx+fF4DLyGgWFoeH0+fF45BDYvN0iu1yBH1/BrCpqwsRImkVicpkiU2sYw2+qb2FwXYVNdmPW1TaypqWdpVTV1TTE65efSs7gTfq8uR1Wke2TJVcWwDXXhGLW1DZgJU7qrquv2qa6L56ZeSDFCxtHc3lYqbtKrpqKr8vOX7mHK6pCxLdO2MG2b8uJ8en8DwVLdpOLS0lIGDBjAD37wg4yk4+8KmqZRWFhISUlJugi7I+xLweq4j3IQkqr5WrduHY2NjTIu5KLrOmPGjGHIkCGUlpZy6KGHcu6553Lrrbdyzz33cPTRR7f60DuEAMtKkkzEcBwHRdFcAZIj25V0INtBw62Rcxw0x80tSreike6h42aTC1s2X9EUMDSZP2/bgoTlINDwGgYBw4PfY+A3vPgMD7pmYFoCPF6KunWje/celHfrQWVZOQPLyxhSUcbQih4MLutGny6dKcnPJ+Tz41VBsZPY8ShWuAklGkW1HKJJQW3cRNN0dE1BV2X+l64qsuQGgW2a2IkEmmPhwcGrKfh0GWMzNAVVc3PG3OaGiiKFSk7hcdBVga7hWl+pBQB5IgghFy6SpmwK2NwK3V169+7NpZdeyu9//3sGDx7c8uEs35D9zsL6thFCsHr1av7617/ywgsvkEgk6NatW7riXtM0+vXrR48ePTjssMP4+c9/zo9//GMGDBiwy2k+7cG0HZauqyESS7qtUaRgyV5QsrzGQWBbNqaZJGGZJG1TWmPuVGNd11E1OaOQVP2g21tLRaBpCopwKMkLUFIQwLJkvpJwA9UeVcdQFBxbntgJR2ABhqpiqLrsteXxohteDK8fvy8gk3J9OQRycsnJzSWUGyQvmEN+IEBRKI9gThBN0zEMjc65Oei6DI6nuiY4AuriDtW1DdTU1KLZAo+u4dE0dFW2etbcJNbUqh/uaqFMtJLxLE3TUDVNepruYSy7oaZ8R4ElZD1lz5JC+nTvtNsW1sHCvrSwsoK1C6qrq3nqqae466670v3ZKysrOfTQQ9Pb6LpOz549GTp0KCUlJXvUTTVtm2UbaombMtPbdOTEHNUdvuDgyJIbxx22oLo9oBzwaBqOsGXPLEf6gHISsiOTTS1LWmDuCZ3j0SgrynO9RoGhKm7ekwOOjUdTyAsF6VpUQElBHkW5ORQGfeT5PQS8Bj6fh4Dfi9/nwePZnmWuGwaa7kHzeNF9fvyBHHJyczB8XhxFxULFoxsy6VRxe7wLhXV1YdZu2kpDYwSvZqDpOoYmax5lbMq9rsoUDlXXUHVDirN7n6KpCFV1h6aq6bwsRQVNV1BVDRwFx4GeJQX06b77LuE3paGhgVdeeYX33nuPlStlHlJBQcEePZ72BPtSsLIuoUs4HGbLli3U1dVlBM4VRUlX6acyjdtKkTAMA6/Xu1cOLk2XZSaKqmK7AmTallwN1HVSM2s0zUBTNHRVR9PkOHjLtrAdGxTZw1y6SjJ6Yzo2Sdt25xTC1sYIteEYmqbgM2RLYY+qoiMwFAjlBCjMDVIY9JPn85DrNQj6DHJ8Ojk+jaBPIehTyPWr5Pp1cgMGoYBBnt9LfsBHnt9HKBAgN+AnFAiQH8wh4PMStRzCCZu4merVDiBoCEdoiMSwFLANFUtVMIXbFtkd1YXr1moq6LqC4dHRDWn1qYaOommuoMm4n6IoKBpoOhi6wNDAcNMd3GWMfcbXX3/Nr371K6688kquuOIK7r77bv73v/+lg/hZDnILSwhB0p2CMnXqVKZOncrKlSsJBoN06dIFRVEIBoPpjN6SkhLOO+88TjzxxG9tOq5lOyzdsI1oLImKQFdVHMtBUxQM3UAAsXhcBt01FU1R0N0kSqHI8l/blpnvqkh1blCwhWxPrOo6Xp8P0xbEYnEUx6RzXg4+Q89oA6NrKh6PXIFNxczkCd6sjYyasnzcjhBuhrmmyunSuqZg6BpeXcdrqPgMBb+h49dVmRQKbuBcIWELFq/fypa6sNyPLi0mRyjuwAoXRZbhKKpbd6hp4HaY0FSZF5aK4YlU7SDyMzJU+Xk5tsByLMp3w8JqKxt7d/nkk094+umnwa3q+Oqrr5g2bRrz588nkUjQqVMn/H6/XGTYjRSZPUXWwtpHVFdX89xzz3HhhRdy+eWX8+CDD3LjjTfyyCOP0NDQkN6uf//+3HXXXTz11FP89Kc/3WV5xp7EEQLLTKK4K144As0NTjuORTKZwLFNmWBpW7JZnaIgHJuEmcS2HTRFc+f1CXRVw3DbOKuqPJmFLTBcMVi6fgurq2owTQe/x0BVBbqqyEROxPaLoqC5B5CqqG5vKh0dDR0dXdVlHy1d9lzX3SC5T1cJGCoBXcOv6/gMHY+myveGgm3LuF0smaSpKQKOwGsY6JoBqo6NimkrmBZYtiIHxgK6rmLoKjo2huJgqAJDU9B1uUKoKwJdEWiKO45MqAhHipXdTJjbi+M41NbV7dGGem3la8XjcT766CNuuOEGzj77bO69914WLFjQcrODhoNSsOLxOP/4xz+46KKL+O1vf8tHH31EY2Mj8XicaDTKihUrMqafaJpGIBAgGAzi9Xq/1V83RTbbJG4mZbtjVUMoqlu7J+vqDDedIZlMknTHSRkoeBQNXVExdA1VVeU+TBPHln21fLqBoWpYSWm9GbpOJGkza/k6vl67ETNpEfR4wZ13mCqBkflPoKgyo1xaVm4qgfuvAuiqdLd0VaAr4FUVfCp4VAevCj5Vw6eqeNy0A7mKJ22ncFR+F7oq41ua+0vrABYOZqrkRpEBLTnSTMbpNOHgwcGnCHwKGFjowkYXDprbxM8WNklLusSWsGSv+g4YSv/817+44PzzOffcc7nuuutYtGhRy006zLBhw7j33nsZN25cxjFmWVZ6+s5f/vIXfvrTn/KLX/yCFStWZDz/YOCgdAm/+OILHnnkEd566y0aGxsz+raHQiEmTZrECSec0Kr7577AchyWrt9KQyQBiorP8KbLi21HtgtWcd20dJuWJEkzidcdoqEo0iKIxeNy5UxVZQAeUBQVyzTdvCzpLtaHY9Q3RfDoKp3zg+iabDGT8gABKSyuQaK4y2/pusFUmywEqiJ7dmmqK2CKItsVq24agyIvMoAuMHSVcDTO8rWb2LC1Ed3wyuRQZLM92dLZtZJU2QlVM3Tpqgrk6qgtWyPrKujyiThuY0A5CVqWMMkuNzJp1BIOFd3at0q4YcMGHnnkEV5++WXWrFnDsmXL+Oqrr1BVlfLy8t1eHfb7/fTr149DDz2U3r17oygKdXV16XY2Qgii0SgbN25k6dKlrFq1ii1btuD3+7/Vhn770iU8KAVr1qxZvPjii9TU1KTv69KlCyNGjODcc8/lrLPOoqKiIuM5u8OmTZv46KOPePvtt1m6dCl5eXnk5uZ2yEKzbcGKjXWEI3LMl0/TZcGyW0cnFEXmVbmthi3bwnTsdIsqVZXxLNM0pTC7CZaKG+dykHMJHdvGMU1UFDRNlxZOMknAa1CU48Oju7V6aUMkFUVy70/vV85OlHV7rsWlyLpAXVUxVOQoMVVaVZoiMBQFQ1Px6RrJRIIV6zaxYPlaYo6Kquty3KK7cij/ooKmyPITj6GnM+Bluob73txXKLuaytXWpNt62QbZ8E91pwy5fe17lhS1S7Bqa2t58YUX0hZOyipftWoVjuNQUlKS0TW2I+Tk5FBWVsawYcPo3bs3ZWVl+Hw+TNPMCFMkEgm+/vprFixYkO5EWl5e3uaC0J4mK1h7GCEE9fX1bNq0iW3btmFZFj6fLy0UlmWxYsUKampqCIVC9O7dm7POOotf/vKXnH/++RQXF7fcZYeIxWIsW7aM559/nj/+8Y/885//5P3336ekpIS+fft2qFuEZTssX1dLJBpHWLbspy5k73LDDTabiaRb9CzzpFRdx+f3kUzEZb93RSUej2O4tXi2Iy0hTVVlzyshx8yY8SRWMk5uThBNV2mKJwhH4+ToKnkBA6/ukcmZgpQJBe53qiCD7akWyangO6mBFW4KgkxDkEF2FYGGg+4KcCKeZPmajcxZupr12xpRfQEECrbrKArXJdUUObpMNzQMd1VWpBJokS6qo6hY7mAKy5HN/pKO28zQtTI19/OzHAFCoVdJIb3bEXQPBAJs2LCBr7/+OmMOZXV1NfPnz6eoqIiRI0d26IepJR6Ph549ezJu3DiGDx+eXvgxTZNkMpleyW5qamLBggVs3bp1rzecTJEVrD3M8uXLeeGFF3j00Ud58cUXWb9+PZWVleTn56MoSrqRX8+ePRk/fjw///nPueCCC+jevXvLXe0Wb7/9NnfeeSdPPvkkW7dule5YLIbf72f48OEdMt8ty+HrFdXUNoSxHIGqKVhCthG2HXdisyOn0CQsORxVVVQ8mo6GbKBn2hbxRAJd96CqKknTlK6k6lomthQsy7IIR6KuxSRwLIeGxgibN2/DgyA/FMTnMRCpBFTbRNgmWCbYFiTiKMkYmFFEIoaIRxHJKEoyDlYcxUyAZSGsJLaZQCTjiEScaFOEqo3bmLt0NZ8sXM6qLfUIjw9FM7BdK9JRwHIUaVjKIT+oCghLDoB1LBvb7d8uEDiqiik0Eracd5hwBElkIaJH1WVtoaYgFIWEJSdM9+leRJ/SolbtZVqiaRoDBgwgLy+PlStXUltbm34sHA4TCAQ47bTTWnUW2V06derEmDFjOPbYYykrK8M0Terq6jLE0jAMzj333G9l9XpfCtZ+1cBvR1iWxZo1a3jxxRf5/PPPWbBgAdXV1SSTyXR86tlnn+XMM89MH0S2bad/pXR3RNY3Zdu2bVx77bW88cYbacsuxZAhQ7j22ms55ZRTKCgoyHjezrAdwbJ1W5n11RpqG2N4PV4MXQ6bSCSTmLYlT0LNkLMK3e6eiuNg6FraTRS2g2ILDMPAEQ4J03TrDxWEZcrHFQXbtkkmkjh2EhXZ/tiOxfApDqWdQ/Qq7YomHGq2bqEiqFEU8LjToGXLmFTqAKR9MoTjNu8TYDsKtmOTsGzCpsOmiMna2hjV4QRNjkoSTXZ6UNy6xYAf3efFFpC0ZG96FenNCRSE7XZoQLZ0VnR3lL3hwUbFsqVvLNx2zRrg0zQMXXU7t4KqaHQuyOGEUZWUd81PW207Q7idQFevXs17773HW2+9xaZNm+jcuTPnnXce5557bquT7ZsihMA0TaLRKFVVVbz00kusWLGC3NxcjjnmGE466aR0/KypqYl58+bx7rvv4jgORx99NMOHD29XT69dsS8b+B0QglVbW8vjjz/O9ddfv/1kcTEMg27duvGXv/yF4447bq/6+CtXrmTkyJEZPZAKCgs5dOhQLrvsMiZNmtQhdzCFQLB83VY21TRhJm08ho6CwLQsEmYSBwj4/OlmdI7tYFmW2ydKwxEOmgNWwpRBd8PAcgVP11Q04WBZMq9KN3Ti8QRmMoaKDOjbloVjWZiJOKGAH03YNDbU0a9TDt3ycmRpj2KjKO46nVBkbAukJebI9yC7jMq2zglbUJuwqQqb1MZtHM0At2ODtPxUvF4PhkdmrjtCtlNOxeAAOYrecd1TIdKuoqJqqJrqjg+TE3MUd6lCdYdpaG4gH0UhN+CjvFshPYvb/0PSkpUrV7J06VK6l5bSv39/PLsZeO8o8XgcRVFaBfoXLFjAHXfcwQsvvADAySefzO23387w4cMzttsdDlrBOvucc3hwDwjWhg0buOWWW3j++edJulNzPW730ZEjR3LxxRdz4okn7pFfl52xefNmfvjDHzJr1iwsy6K4uJjJ3/8+P/vpT6msrGy5+X6LtFmyfJd57733uOaaa5g7dy4Affv25c9//jMnnnhiy007zL4UrD2nRLvBnjroQ6EQ48aNSwtSfn4+kydP5m9/+xt///vfmTx58m610egoRUVF3HXXXfzmN7/huuuu47HHHuOO22+nd+/eLTfdIc07QXxX2VPf2/5A85SXb4Y75iyVC7KXKSsrY/To0enbRx555Hey1U1H2acW1p5yCR3Hoba2lo8++oiNGzdSVl7O4MGDKe7adbdcsF1RW1vLF198wfr16xk2bBgjRoxIP5ZMJmlsbEQIQSgUamWq74xXX32V6dOnY1kWp556KqeffnqrX5gdIYQgFovtlfd7MPLVV1/x73//mzVr1jB8+HDOPffcVgNCdoRtRYnXryNcvQg7VoOdbALHlLVLwkHRPGieEJqvAD3YhUBRL7y5pXu0ljGZTLJmzRo++ugjHMdh/Pjx9OzZs0PH447YlxbWASFYKUzTJBaLkRMMpuvH9jSWZfH444/z5JNP0tDQQO/evbn33nsZMGDALqfj7AjLsvjf//7Hgw8+yFdffYVt25x66qnceuutDBo0qOXmGaQWHJ599lnWrl3LiBEjOPnkk+nZs2fLTdNEo1EEkLMLcUsmk8Tj8V260o2NjXi93p2eDPF4HCHETleWLMtKi+6uFkGi0ShCiL2yjB+NRpkyZQp/+MMfqK+vp7i4mD/96U+ceOKJO3yPjp0gvPVrYpuXEK9bSbJhPfH6tQgrJldShYy/gUBRNBTVQNF9KN4Q/vwe6LndyS0ZQl7FeFR1z8VZ98bntC8F64BKa9A0TZbO7MHX25JYLMaDDz7IO++8Q01NDStWrGDChAlUVlbulmCFw2GmTp3Kvffey6xZs0gmZfmM1+tlwoQJuzTjGxsbeeWVV7j33nv57LPPWLx4MaWlpTsMrm7YsIH//Oc/TJ02jWg0SkVFRZsLEevWrePll1/mpZdeYvPmzZSWluL3+zOOhS1btvDGG2/wr3/9iwULFpCfn09+fn6G2Ni2zZIlS3j22WeZMWMGRUVFbW6zatUq+bqmTmX9+vUUutu1pKmpibfffpvnn3+eefPmEQqF0oXqe4p4PM5rr73G22+/jWVZ1NfXc/TRRzNkyJBW37GdDBPZspi6FW9R+/WrNKx4h+jGWcRrV2LHahHJCNgJhJ1E2Al5ScZxEo3Y8VqspmoStauJbv6KRP0aHEtO+Na8uajaN0+LSE2T2pPsy7SGA0qwvg2SySSff/45y5YtQwhB9+7dOeOMM+jZs2erg3lXhMNh3njjDX7/+9/z5Zdfpu/PycnhmGOOYfLkybvMq2loaGD69Om89957ANTX1zNo0CCOPfbYlpsC8J///Ie77rqLadOmsXLlSgYNGkT37t1bWdFTp07l9ttvZ+rUqXz55Zf06tWLnj17Zhz87733Xnol6v3330cIwbBhwzIssng8zqOPPso999zDW2+9BW7NXPNtUvMmf//73/POO+8wa9YsfD4f48aNa3XsffDBB9xzzz0899xzzJgxA9u2GTt27B4to9J1nc2bN7Nw4UJ8Ph99+/blvPPOo1evXunXIxyLROMG6ld/wJb5z1O7+BWSW74GqwlV01E9fjTDj6p7UTWPvOgeVNVA1Qx5v8ePpnlljaZIkmyoIlw1m3hDFUIBw5+HZgRkY8PvUOxwXwrW3vGbDmCCwSDnnXce55xzDuPGjeMnP/kJo0eP3q0v78033+Tuu+9m9uzZGfdPnDiRyy67jB49emTc3xaBQIChQ4dSWFiIrusceuihHHbYYS03A8C0LN544w02bdoEwKJFi3jssceIxWItN2XBggWsW7cO3Fl7zz77LFu2bMnYZtWqVaxfvx5cK+nll19mw4YNGds4jsOyZcvSt1955ZX0c1Ikk0k+/fTT9Ej1TZs28aLb3bUl06ZNY968eeA+b+rUqaxYsQLRIp3lm6BpGpMmTeLhhx/muuuu45GHH+Hwww/PEPXItqVUffEYGz78PZG1M9CwMQJ5aN4QiuZ1u8qL7Rdh45gx7EQTVqIRK9mEY0ZlTEvVUY0Ahi8XDUFk7YdUffQHNnz2FyI18rOTzmSWrGC1QSKRYPbs2dx0003cfMstTJ8+PZ0uATBy5Ejuv/9+XnjhBa655po2XZed0dDQwNRp0/jNb36T0Sqkf//+PPDAA/zpT39i5MiRGc/ZEcFgkMmTJ/PGG2/wxhtv8Pzzz3Paaae13AzTNPnTgw/y6aefphNaCwoKGDNmTCuXcNGiRSxYsCC9naqqdO/evVX8pnliruYONmi5jaqqdOvWLX1/PB6nvr4+Q2ACgUCroPam6upWwgZwzjnnZCxybNmyhfvvv5/Vq1dnbPdNyc/P59hjj+VnP/sZI0eNdC04QWTrYtZ+cCdrXr+GpuWvo2FheEPSfWs+3MJN4MWtcXQEGHll5FYcRX6/UwlVHIWRVyF7ewlLrh4qKopmyP05ScLLX2ft9GtY8/7tRLYs3t7+5iBWrqxgNUMIwebNm5k6dSp33nknd999N3fdeSf3338/W7ZsSZ9kuq4TDAbJz8/H5/O1Mlt3hmVZfPbZZ9x5++2sWrUK27ZRVZXevXvz61//ml/84hf06tVrl0HnFIqiEAgEGDFiBMcccwwDBgxoZe05jsOmTZv497//nbaSUuUlZ555ZiuRmTt3btq6wp1MPXbs2FbuaVNTU7qTgOKWPKV63adQFIXCwsK0uxyPx4lEIhlVAIZhMGbMGDp16pS+r66ujqqqqvTtFEcccQTjxo1Lr4Ymk0mmT5/O7Nmz069lT6AoCrqu423WRTbZVM3GL6awbd4/SdQsl+WUqiGD6aljwBUpxS21FI6FUDS8nfrTecj5lBxxJd3HX0u3I66ky5DzCHQ7DKHosnBb9pCVTQlVAwVBom4FW+c/x6YvHye6bSnCsb47vuE+ICtYLo7jsGbNGv70pz9x+eWX88orr6Qfq66uZsuWLXskR6qxsZE333yTL2bOBNcC6dmzJzfddBM//vGP93iAFDdW9vrrr7N06dK0RdS1a1eOOuqoVjPphBAsXrw4ox9YKBSiT58+reJEjiOHVeCe4G0N7sRN4k39DdM0iUQimKaZflxVVUpLSzMWABKJRCsXNMX48eMZNWpU+nZTUxNvvvkma9euzdhuTyIcm/o1H9KwZJrsLR8oANX9UXF7lkmxSYmXdOIcx8IIdqHroT+ky5BzyOncH8PfiUCn/nQe8gNKR/8cT0FvdyaILfelIFVP1dB9IQzDT/2S6Wye9wyx2lWpP3ZQ0vroOggRQrBlyxZuuOEGHn744YwukoZhMHDgQMrKytpt9eyMltZY7969+c1113Heeee1ebLvCTZu3Mjzzz+fEasaPHgwkyZNytgOdxl8+fLl6fIij8dD//7921xNrK+vT8eZFEUhNze31TaqqlJUVJQW4mQySW1tbav4VK47y7F5182qqqo2EzfHjh3LxIkTM+7bvHkzTU1NGfftScLV86hb/ia6rqHqHleQmnesQLqCzf5zbBNFM/AV9iG/bAwoCpHNC6lZ8hpNVbNA0fB3HkBBn4movhCO5Yp4cz0SCqpmoBse6pdMp2bJVJLR7T8mBxt75wzZz7Btm7lz5zJ79mzC4XDa9SssLOSnP/0pt9xyS5sFy01NTXz22Wc8//zzPPbYYzz22GM8//zzzJw5k2g02nJzcK2V008/nTPPPJNJkyZx66238oOzztorlhWuCzZv3jxmzZqVPvmLioqYMGEC/fr1y9jWcRzWrl3LqlWr0i5bIBBg4MCBbVYKJBKJ9GflOE6rdIUULe+Lx+MZLiGu4PXq1Ssjt2fJkiWtgvgAPp+PY489Nl1mEggEGDd+fLsWKTqKQGDGati68AWim79C9QRcPUkF1FMbSuVK2VYKCjgOqurFk9sF1VcACOpXvk/VJw+xadbjRKrno+p+QqXD0AOd01aZ0nxH7l5V3Ytix6lf/hb1qz/c/ncPMrKC5RIKhTJEo6ioiN/+9rdcccUVDB06NOOkW7lyJY8//ji//vWvuf7667nnnnt44IEHeOCBB7j33nv5zW9+w69//Wv+8Y9/sGbNmvTzcE/ekSNHcvPNN3PrrbcyadKkDgftO8KqVat4/fXXM6yrIUOGMHbs2FYiaVkW8+bNy2hsmJOT02b+Ea6VluodVlhYyBFHHNEqyVRVVQoKCjKeX1tb26ag9+3bN8PCWrJkScYKY3OGDBnCzTffzH333ceDDz7IGWeckRED22M4DrXL3ya8/nNEMgxqyrpqjiysbn2fuwKoB+Rtx8IMbyHZsJbY1kVEtywGwJvXA0+wK2hu657mu09dFwqqJ0CyfjV1K96mafM3b8m8P5IVrGYB6IsvvpjTTjuNM844g6uvvppLL700o2jZtm3ef/997r//fu69914ef/xxPvroIxYtWsSyZctYtmwZCxcu5MMPP+Sxxx7j7rvv5o9//COff/55xt/Lyclh6NChe6zdx85YsmRJOkcL18WdMGEChxxySMZ2uII1c+bMDNeqsLCQww47rJWrB3DiiSdyzTXXcNFFF3HllVcyceLENoPuBQUFGc8Ph8MZq64p+vXrR1lZWfr2xo0b2wy8436GRx55JL/+9a+57LLL6NO7dytL7psihE28cS01S6Zix2rQtNaivXMEqKqckwgIx5QTunUf2CZmxF0A8YbQ/fmomrGT+JRAUT2oqkKseiE1S6fLxosHGQeVYJmmyeLFi3n33XdZsGABjY2N4J5UhYWFXHXVVTzyyCP8v//3/7jhhhsyVtvi8TgffvABt912G1OmTGHlypXguiMlJSWUl5dTXl5OcXFxOji9ZMkSHn74YW699VY+//zzNk/SvU04HM5oMDdo0CDGjx/fposbi8WYM2dOOh9K0zTKy8vp169fm/G1fv36cfXVV/OXv/yFG2+8kbKysja3CwQCGYKVSCRauYS4jepGjBiRtrK8Xm+rQH9L9rRINcc2IzSs/Zj41sXSQ9M921225rS0ilLRLIGbqiAtWeHYOHZSCplwcCx5PCiax53MLQfWppxNIXck9+bGyDRPDk6igfC6T7ES8vg9mGh9dB3ArFu3jssvv5yzzz6bX/7yl7z11lsZ+UCGYdCjRw9KSkoynoe71H/tb37DJ598kr6vsLCQk08+meuuu457772Xe++9l6uvvprjjjsuw7V59913uf7661m8WLoA3ya9evVi9OjRGIaBz+fj/PPPb9O6wm1AuHTp0vQKXigUom/fvq2sppa0TKNojqqq6aTWFBs3btxhgPyYY45J9w2bMGHCDpNgvw2saB31Kz4EO4mSzrGSizTbr8t/3SbRIGQXVxQQdtJNDM0ULCGsVMjLxZ3cnYhgxRpwkmGEbWWEyGR0C4SigaKQbKoi2bTnRoztL+xTwdqR8bu3WL9+Pe+99x41NTV8/PHHfPzxx7vMkI5Go0ybNo3LLruMBQsWYNs2/fr149Zbb+XNt97iqaee4mc/+xlnnHEGZ5xxBr/85S959tlnee2117juuuvo1asXjuPw8ccf83//939MmzZtl38zRSKRYMGCBfzzn//k1VdfbTORcleMGjWKJ598krfffpsZM2Zw6aWXtjn/Djc21zx+VVlZ+Y1Lp1IpC8cddxwlJSXk5uZyxBFH0K1bt5abgmsB3nfffcycOZPbb7+dPn36tNxk7+J+NVa8gYZ1nxCrni9nIrpuHbgrgsIdICscmWuVqhV0EggniZOIoOh+ckpHEiofC0B08yLMpg0oqAjbJtGwHisq3cLOg8+k+9E302XUZQR7HIHqycWxkm5sLB3GRwE03YtIhAlv/BLH3nO5Z/sD+7SW8JBvuZYwGo3y8ccfYxgGvXv35pRTTtlhkXCKFStWMGXKFN555x0cx6GoqIgrr7ySq666ivLycjzuKC1N09A0LZ1s2KNHD4YPH45t2+mkxg0bNpCXl8fw4cPbXHVryerVq7n77rt55JFHePvtt+natWtGlnd70DSN/Px8Kioq0hnnO/o+Z86cyYsvvpi+PWbMGC655JIdWlgbN25k3bp1NDU14ff72wzM41quJSUl+P1+KisrufDCC9NjrFqiqiqBQIAuXboQCATadDH3Ku5LSjRuoHb568Sr56PqXrdraepxae8IIacVoajbE0dTlpaiESofS6dDfkCw5FDsRCNbF71IZOMcFEdaT45tovnz8OZ2w1dQQU7xIeSVj8GbX45txjCbqnGsKKqqb/c63YlHWHHUQBH+zn0xfK3d+71JtpbwW6Jfv35MmTKF3/3ud/zpT3/i7LPPbrlJBkIIlixZwgcffADuh3fuuecyefLkVn2nZClGpuVUUFDABRdcwAknnJA+mWfPns1MN2l0V6xYsYL//e9/bN26lXXr1mUUSO8KIQS2bbd6TTsjJycHwzDQNI1QKMTAgQN3ODDDtm3+8Ic/cOaZZ/KrX/2KTz75pM24VIohQ4bwu9/9jkceeYTBgwe3OhD3FMIdptFW/lZHSEa3Ed22Ur7OZm2ZUwhhg2KgB4vxdxlEoOuQ7ZduI8jvezLdx/6KvPIjcaw4kU3zaFz7McKMujErDSu6ma3z/k3tsmlENs0l2bQJ4QiCJcMoPuxCQhVH4jg2OBaKItze+TKNXtF0orWriNZmrkIf6BxUgqVpGqNGjeL888/niCOO2KWVE41GWbhwYXqlKi8vjxNOOKHNmYWbt2yhevPmlndTVFTEWWedlRa4ZcuWtTuWlZubS+fOndO3dxWATmHbNuvWrWPOnDnU19e3fHiHHHLIIZxyyikccsgh/OQnP+EHP/hBy03SbNmyhddff51ly5bxwQcf8Ne//nWPlsbsDkIIampqmDFjBgsXLiTcbKpMR7Fi9TjRWhRVl9aT2J4k6thJBBrBHmMoO+oGKk64i4rj76TihDupOOEuep5wF+VH34yvsA/CSdC0/lOqZv0Ns2kjiqqApoGmoyoqycY1VH8xhdWv38jqt25i29LXsBNhfIW9CZWNQQ90xrHN1mkTqoaI12NHt88POBg4qAQLV7RSbtyuqK2tZdOmTTiOg6Zp9OnTh549e2a4KaZpyhjXpZfyo4su4pNPPsk4cf1+P3379k0X9jY2NrJx48aM0pQd0b9/f2677TYuvvhirrjiip0KSHNmzpzJL3/5Sy688EIefPDBjFXCnVFWVsYDDzzA888/zzXXXEPfvn1bbpJGVVUSiQSO4xCJRPbqal172VZTw7XXXsv//exn/OhHP+Lpp57aPUtL2DiJehwzguJ+12nBEALHjBPoMoDCAaeR22M03lAZntzueHJ74MntjhHojGr4CVfPY+MXf6Xq878Q27IIVZXlNhI3BuZYmNFarGg1ser5bJv/T+J1q0BRMYIleIKdcRwTJaMqTE4PEmYcJ3lwrRQedILVEZLJZLqEJFVi0tJvj8fjPPfcc7zxxhu88847/O9//8uYmpMqWQmFQiiKHHcVjUbbleJQVFTE97//fa699lquvPLKdsWvampq0p0blixZwvvvv8+SJUtabtYmhmHQs2dPBgwYQElJyQ5jUrjdDM444wxGjx7NGWecwUUXXdSqiPrbZsvmzbzwwgssXbaM+fPn8+6777K5Dat3VwgniWOG5Sof21f95IMCBHjzywl07geqh8iWxWz96mW2ffUS2xa/zNYF/2LTF4+y6bOHqV38PxI1S1FxZKdRVOlmOia2GQXVS0GfowmVj0LzBojXrsIMy9U/zZOD4S9o+zRVFPd1RrZ3cTgIaOOTyJKiZVyqrQCwEIJwOIxpmmlro2WRtKqqqKp7oLq03KYtFEUhLy+PAQMG0KtXr1Zi2Raff/45r7/+ejqe1JEYVkfwer385Cc/4cYbb+Tqq6/m+OOP36nAfRukYm8pgsHgbll+MphuuULQMtYmQNFQDT+a7sMxo4TXf86mmVPY9MUjVM+aQvWsv7Jl7jM0rf0Yq2mT/P51r3u6CZxkDMcyMUI9KOh/CnllR6B6gjI25XYxRQhU3YPmyWkW0G+OIl+fsIDdsCL3U1qfgVnSGIaRPgkdx8ko9k3h9Xo544wzOPzwwxkyZAgnn3xyRqlNyqJK1Sgq7gy5lie34zhs2LCBRYsWsXbt2jab6u2KSCTC22+/zfz588F9bYMGDWLAgAEtN21FJBKhrq6uXZZfiv79+3Paaae1am63J4nH42zbto2GhoZdim+3bt3SDRVPPPFEJk2atMNFg53jrvQ1Oz1S8W7hPiwc98dM2FixOpL1a0jUrcasW4MZrkaYYTRPjqw9FMgp2Y6Vjn/5igbQafAZFPU7iXjjJsJV87Cj9TJmJmyEcEDRUFTddUabm3nN/21LzA5c9s5RdoCQn5+fLsZ1HIfVq1e3igd5vV4uvPBCHnnkER5//HEmTZqU0fBfURQ2btzI1q1bEUJOXi4sLGwVQF+zdi2333475513HjfeeCNffPFFxuPt4csvv+SLL75Ii06/fv044YQT2sxqb44QgrfffpunnnqKOXPmtBLlfUUkEuHjjz9mypQp/POf/8xoedMWoVCI3/72t/z73/9OT/rePWQmukiN5ErpgiJdsfQ2rogoug/Nm4vuy5VlNp4gqupB9xfgyS9H8+VjxRswo7U4jiDUcwI9jrqWogEnU7/6Y7Ys+C9WeAtKs/jW9u4PzSWp2S0hZP8smU6f3uJAJytYOyEUCjFx4kSGDRuGcJv73XfffRnZ7riidOihhzJs2LCM+y3L4qMZM7jjjjvSq3Xjx4/n+OOPT2+TSCR4//33ueCCC3j22WdZtGgR//nPf3j11Vd3aVGkEEKwbds2pkyZwqJF24tiL7rooh32dk+RTCZ59NFHufrqq7n55pu59NJLO5Q+0RFs22b9+vVs3LixXZbcCy+8wJVXXsndd9/N9ddfz5VXXsmqVatabpaBqqr06NGDoqKi3U6dUDQPqpGDqnldkdguT+7N5lcy7Rz3hiNsVE8ORQNOpdcpf6THMXdQPPoqep/2CKVHXEG8YQOr3riZbQv+jYqFashcLwwfmr8AFA07GcOK1aK0GaNyZCtmIwBKx93e/ZWsYO0ERVEYMmQIp59+OrquI4Tg1Vdf5cknn2TRokUZK1CpxNEUpmkye/ZspkyZwkcffYRlWfj9fo455piM4PnXX3/NlClT+PSTT4jFYjiOQzAYpFOnTu0+4UzT5M033+TDDz9M1wH6/f6M4bI7oikSYdq0aaxbt45YLMaaNWvSNZZ7muXLl/Poo4/K9/vpp7t0e7ds2cKGDRuIxWI0NDQwbdo0Vq1atcv4X/PPLRaLUV1dzbZt23aaJ9YcRfGg+wpRjYBsX5z64cgQqx25Y1LaFE0n0bCBpo3zAYUuQ8+j+9irCJWNIbxpPtWzn6BpzUcojulaVnJfui8fI0dWItjJMFYqbSHDspO2l6L7UH15O3gdByZZwdoFxcXF6dyklCA988wz3HHHHcydOze94mfbNrZtk0wmiUQifPHFF9x333388/nnwf3lHz9+PBMnTkznZEWjUaZOncp//vOf9N9TVZXjjjuuQyPF6+rqePbZZ9PuqqIo9O7de6ezCXEts41VVSxZsgTLslDcnlSpljF7munTp3Pvvfdyxx138PDDD++wdUyK8vLyjJy3pqYmli5dSqSd+VUNDQ188MEH3HfffTz22GOsXLlyl2KXQvXmoflCbutiUITiFsfswuoVuDlbGjgmDSvfZ92H99O47lMcM8rWhf+ievbfSNauwBPIR9E9bjm13K831A3d1wkQWLEazFi9TIVQaCZMAhyBYgTRPDufqnSgkRWsdjBgwABuvfVWSktLwXX1XnrpJc4//3xuuukmXn31Vb744gu++OILXnzxRa677jouueQSpk6dCq6A9O3bl6uuuiqjFGj+/PmtWs9UVlZyzjnnMHTo0Iz7d0Q8HmfOnDnMmjUrnf9VWFjI8ccfv8OawRSxWIxlS5emY0OGYXDooYfu8QGZKbZt25a+vmXLlh22QE5R2bcvlS1ywRYsWJCe+rMrPv/8c2666SYeffRR7rrrLp555pkdtqtpiZFThLewAtICl3YKYSf2VeoBBVB1L5qqkahZRtUnf2Ld+7ezdf5zWOFqdE+OTP509+kIB1SNQJdB6L4QTjJKvGYVVrQWVcsUNQDHsfDm98Cb373ZHz/wyQpWOwgEAkycOJF77rknveJmmibLli3j73//O9deey2XXHIJl1xyCTfccAPPPfccy5cvTyeHDh48mPvuu4+xY8dmuI2GYWT84nu9Xi6//HImTpzY7uX4hoYGXnvttYzuB7169eLUU0/dpUsZDoeZO3du2lXSdZ0RI0bssgJgd+nXrx+GO9hz2LBhGb3G2qJXz56ttlm4cGG7c6uqq6v56quvSCQSaXd3R10iWmIEivAVVuIoqnQJ3WXC5o5ZSmzk/1MW2PZ7QJHxMCBRt4KGVe9hRTZLF1DVt1tNwsaO1aMYQfJ6HYXmCRJvXEe8dhnCiroxqmbfpXDAcfB36ou/YOeDdg80soLVTkKhEJMmTeK2225LDzgVQlBXV8eaNWtYunQpS5cuZe3atekAe1FREWeffTZ33nknxx9/fKsi4t69e3P22Wdz2mmnceKJJ3LDDTdw+umnt7sDqWmaLFiwgNdeey0tjrquM2zYsHYlmYbDYebPn5+OxQUCAQ477LBWr7Mltm2zYsUKHn30Ud5+++12u2gTJ07kgQce4KGHHuLiiy9OW6w7IhQKMWjgwAxLcfny5W22TW6LyspKjjvuOEKhECUlJYwcObLdXUl1XwGBzgNQfYWyGwOyhi/TIZRWj7AT2MlGrESjO3ewKf2vlWzCNqPydmQbdiKCnYzKx+Jh7FgDVqwR9BzyKsbiL6oERSVSvZDotqWomoqiwPa/rCBsE1QNf1ElurHz7+pAY592a9jfJj97PB4GDRpEr1696Ny5M16vN51T5fP5yMnJIT8/n/LyckaNGsU555zDRRddxFFHHdVmKZDf76dnz54MHDiQI444glNPPbVDeUMbNmzgmWee4e23307fN2jQIC6++OJ29ZFatmwZf/3rX9MtZcrKyrjmmmt2Gahft24dTz31FA899BDr16+ntLSUXr16tdysFXl5eYwaNYoRI0ZQXFy8SytSURQaGhr48ssv065cPB5n0KBBjBw5slWL55bk5+fTq1cvysvLOe644zjllFPo3r17u45nRZV9p6I1K0g2rJHTmV1rSzgWgeKh5JaOQNE8xGpXEG/Y4KY2FMj4lzeE6pVpDqo3F82Xj+4vRPPmpe/XfPkYOZ3xFVWS3+c4Og06HU9uN6Jbv2bbVy8S3bwITfdk9OICBceKo3pz6Tr8YjyB7bWm3xb7slvDPhWsQYMHc+J+JFgpSktLmTBhAiNGjKCn67YccsghDB8+nDFjxnDaaadxySWXcPrpp7fZDLA5Pp+P7t27U15e3uED4PPPP+ehhx7KyA07//zz+eEPf7hLKymRSPDJJ5/w3HPPpa2zAQMG8POf/3yX3/cXX3zBAw88wOrVq9m8eTP5+fkcd9xxLTfbI0QiEb7++uv0wFkhBKWlpRx66KG7tJa8Xi8VFRWMGzeOUaNGUVhYuMv31hxVM3CESeP6mWBbqK7ACtPE32UgwdIRsnRG1TFyS8jpdig5Je6leCiB4iHkFA8lp3gIOV3lbXmfe+l2GKGyIyjqdxKdBn0fI6crZria6jl/p2ntx2DFUHWZrydcpxPHxLEsjILeFB92Xvrxb5ODVrC+7X5Ye5pOnToxdOhQJkyYwLHHHssxxxzDhAkTGDJkSJsBb9u2+fLLL9Nj2bt33/2A6VdffcXDDz/Mhx9un6By/PHHc/nll7eahtMWVVVVvPzyy8yYMSN938SJE5k8eXLGdm0xY8YMXnBHyQeDQQ499NCM3LJd0dTUlDGrcGeEQiFM02Tq1Klp1zUajdKzZ892WZHfBFXz4M8rx7ZNYluX4CQjsh87Dla8HuFYGDld8BWUEew6iGDxYHK6upfiwQSLh+z80mUQ/vwyFFUjuu1rar9+jfUf3kt001wUYbrlPLhSJUtxzHgTvq6HUDL65wQ7D4SMiNm3w74UrGwM61tk6tSp3Hfffdx1113cf//97V7taolpmrz++uvpPl247uqpp57aKki9I7xeb8YkZ6/Xy+DBgzO22RHxeDydDe/3+3eZSZ+iqamJZ599lnvuuYcnn3xyl0mguK+rsrIyw5VLlTC1J/m0ObFYjHnz5vH6668ze/bsdnVy0Dy5dBpwGoHiIbLVseOg6l7McDV1y15n85dPsmXus2ye+w82z32m2eUf2y/z2riktp/zNJtnP8GmmY+xbeG/SNavQUHIEp0WWIkIak4X8nodTX7Z6JYPHxTsUwtrf4thfROWLVvGzTffzPTp09m8eTNLli5l8uTJuzVLb/Xq1fxlyhTmzpkDbu7WYYcdxhVXXNFmr6628Hq9CCFYu3YtPp+P8ePHc8455+zS6nMch88++4y33noL27YpKipi7NixjB696xNoyZIlXHLJJUyfPp3PPvuMzp07M3r06F0eX5ZlsXDhQpYvX47jONv/7rhxFLRzgQK37c6f//xnnnjiCZYsWcLRRx+9S9cZRa4YomrE69Zghzei6F4UFKxoLdEtXxGumke4apa8bJhNeMMs9zJTXqpm0bQ+9fgswuvdf6tm0rTxS6Kb5pOoXwNOEs2Xi0Iq78pdoFQUhC1b+eRVHkeXQ87EG9wealC+ReuKrIV14NPQ0MCf/vQn5rgCA+D3+Xa7YHj+/PlUNVspCwQCXHjhhRkjsnaF4Y77evrpp3n66ad55JFHMsa/74hEIkFjY2PauvH5fLsM0qeoqqpKB8+3bt3KokWL2tUXLDc3lzFjxmQsXFRXV7P4q68yttsVr7zyCtOnT2f58uVMnz6dFStWtNxkhxT1PYH8XkdhmXGELbPTNcOH5vGjagJVcdyLvf2CexEWGpYswcm4OGiqgubxo/tCqIZfBvVb5Hth21hmEn/pMDoN/B6Boh33KTvQ2b0zJku7iUajvPXWW/z3v//NyAHq3r07vXv3zti2veTk5GScvD179uT444/PcPHag67rlJeXp5f7W/6atYXjOBklLqke9u2huLg4nZRaWFhI3759d7nSh/t+Bw4cmPF3amtr06PW2ovH40mvTKqqustVyuYoik5Bn2Pxdh6AbZk4VgJURa4eqjpoBopqoKie7RfNQNEMUI1mj8vruI8pqg6qJq0o6QxmdJMRjolpRjGK+tFt5GWESnedrnIgkxWsvczixYu57777qKmpSRcz9+jRg4svvni3M8oPP/xwLrzwQk488US+//3vc+ONN1JeXt4uwWmJoihomjxh2kM4HKahoSF9W9f1drsGffv25dFHH+XOO+/kgQceaHcHVY/HQ//+/TPcXdu2W7Xo2RVnnHEGF1xwAUcddRQXXnjhTjuqtoWvoDfdx12Nt+tgLDOBHZd1myJdtKNIH869pK4quHmnruOWbs8un+zmWLlpp+nuCwInGcEyE/i6DqFs7JWESkdIwTuIycaw9iLr169nypQpvPLKK2mxMgyD733ve1x55ZXtThBtid/vp6ysjGHDhnH00UczevToVkMx2kMymeyQlYHryr377rvMnTsXgIqKCk466aR25WF5PB769OnD4MGDGTp0aLtzzhRFwee60PX19fh8Po455hjOPPPMdu8DoHPnzlRWVjJ69GgmTpxIjx49OnRsK6qON1SKN1SCYyeJN23EiTe6VpbsJirVSUaV5P/d/2VeSSNSm7uPKYCwE1iJMKonSKhiAsUjf0RejzGoevt+GPY22RjWAUhjYyNTp07lhRdeyCi/GT16NOedd94ug9u7oqSkhFGjRnHYYYd1uJRm/vz5PPzww/z5z3/m448/blccKUU8Hs/oWW8YRocOXJ/PR5cuXXYd7G6Bz+fj7LPP5rrrruOmm27isssua/eqZgpd16msrOSII46gf//+rU6G9qBqXvIrJlA84sd0GvwDvEWVOLYcgurY8e3tihW3oLBdf0IBBMJJYifD2LaNp7CSwsE/oHjEj8kvG4+itc/tPtDJCtZeYvbs2fz73/9m48aN6ftCoRDnnXceRx11VMa23yZNTU089dRTXHPNNVx//fXcdtttbNy4sd29tyKRSEYpTkcF65tQVFTEpEmTuOiiixgxYsRuL1rsFi0+nmDxUEpH/x9dhl+Cv3QkqjcPxzYx3bIcx4qCsN02xqlW2/Iix9g7bitmE8eMYicaccw4ijcPf+nhdBlxCd0O/xnBkkMz//BBzrf4jR9cvPTSSxlJnd27d+eJJ57gvPPO67AbtidpbGxkzZo16Yk3X3/9NfX19e0WrNra2ozM+lAolJ4ItD9h2zb3338/3/ve9/jlL3/JzJkzd/4ZtGEp6d48ugw+k76nP0zlmX+n4pQH6XL4z8mpOAottzu27WCbcaxkVNYPJiNYyQi2GcWxEzjCQRg5eDsNJNTvdLodfSt9z3yGvt97mK6DzkT3dmwR5WAgG8PaS6xYsYKlS5eSSCTo0aMHP/nJTzj33HPbnQKwt/B6vSQSCRKJBD179mTy5Mkce+yxGW2dd8a8efN45513qK6Wk12GDx/O6aef/q1ZWSlqa2upqqrCsqx2v/bmNDY2cuWVVzJjxgzmzp2LaZpMmDBht96HqhkYgSL8hX0IdBmAv6g33sI+eHK64M2vwFdQhregHF9hL7yFFfiKKuXw1W7DCJYdSWGf48jvcyx5ZWPw5HRG/Y4H1vdlDCsrWHuJLl26UFRURKdOnTjppJO49NJLd3tVcE+i6zoDBgxgzJgxHHXUUZx22mkdCv7PmTOHd999N10wfcwxxzBp0qQ9eozsijVr1vDKK6/w8ssvs3r1aioqKsjJyemQi1hTU8OUKVOor6/HcRyqqqqYMGECpaWlu2UBp9b2NN2HN1hMTuf+BLuPIKd0GLndhxHqMYpQj9Hk9hhFqPwIQhXjya+YQH6P0fgLe2H4C1HcVsepfX1X2ZeC1f5vOEuH6NmzJ5dffjlPPvkk11577S4LdXeGaZpEIpFdthRuL36/n/79+zNs2LAOB79LS0spLy9H13VKSkqoqKjokFDsCV599VV+97vf8Ze//IVbbrmFF154ocNtnYPBYIYr29jYyEsvvbTLQRc7oi2B0XQ/3pyu+PJ64Svoi6+gEn9BP3x5vfDmdEUzOr6ye7Dz7R5pWTqMbdtMnz6dyy+/nAceeKDdLX73Focffjjnn38+hx9+OJdddhmnnnpqy032OuvXr08LixCCDz/8MCM3rD2EQiEOOeSQ9O1kMslLL73EmjVrMrbbF7Qlflkk+1SwdhLizOLW0M2dOzdtRTzxxBN8+eWXHUpD2NMEAgEmTZrEk08+yc9//nPKy7/9jpedOnVKZ/WnFg5ajl/bFYqicOSRR6aTR4UQVFVV8c477+x2UXqWvc8+FazsL8nOSbkpixYtoqmpiQ0bNlBVVdWuLgMtiScSvPbaa1x//fXce++96cTP3SEvL4++ffvSpUuXNhsT7m0qKirS3Uodx2HdunWsWrWqw90bJk6cmJFiYts2r776KkuWLMnYLst3h30qWFl2jOM4LFu2jJdeeikdeCwsLKSkpKTDQWHHcVizZg333XcfDzzwAPfddx//+te/Ohz3+a7Qs2fPDMsuFouxePHiDltZ5eXljB8/PiO+uGDBAmbOnNnuts9Zvl2ygvUdpaamhg8//JCvv/46HbeqqKhg8ODBHa6hs22bjVVV6az2uro6Zs6c2eET/LtCRUVFq1KgrVu3ZmTgt5dDDjmEsWPHpm+bpsmMGTNYuHBhxnZZvhtk0xq+o3z66af84Q9/SI/CUlWVyy+/nKOPPrrlprtE0zRyc3MpKCggGAwyYsQILrroIkaOHNlha21P8N577/HQQw/x5JNPsnr1anr37k1OTk67j7OcnBx69OhBKBQiLy+P8ePHc+mll1JZWdnh91NUVERp9+58NGMGde5S+ooVKygqKtrl1OyDlWxaQ5ZW5OXlpYtzFUVhwoQJjBs3ruVm7aZTp0789Kc/5cYbb+Smm27i5JNP7rCltieIx+M888wzPPLII/z3v//l8ccfZ9asWe2eypxi0KBBXHXVVdx0003cdNNNHHbYYbv1fnRdZ8ghh3DeD3+Yzkfr2rXrXhsmm+WbkRWs7yiVlZVcdNFFnHTSSZx88slceeWVGcvwu0NhYSGjRo1iwIABe/zXsb0kEgk2bdqUXumMRCJs3bq1w+kaiqJQXFzMEUccQc+ePb9RLlheKMT5553HmWeeyfjx4/nxj3/coR71Wb49dv9bzrJXKSgo4Ac/+AHPPvsszz77LJMmTepwkufewLKsjJ7uHSUUCnHcccfRt29fcnNzGTRoECNGjNgnq40pVE2jb79+PPTQQ7zwwgvccsstDBwoBzxk+W6RFazvMDKWWEB+fn4rX35fYFkWM2bM4OGHH+af//znbmXeK4rCZZddxmOPPcbf//53HnzwQQYNGtTh2NPewO/3p+dNZvlukhWsA5z6+nqmTZvGHXfcsVslLM35+OOPeeCBB/jjH//I7bffzqJFi1pu0i5CoRBHHHEEJ5xwAgMGDPhGYiWEYPbs2dx33308++yzLR/OcoCRFawDnPfff5/bbruNKVOmcNddd/H+++8TjUZbbtYuZs6cyZdffkl1dTWrV69m+fLlLTdpNx6Ph0Ag8I1iT0II1q1bx+9//3seeeQR/vznP7NgwYJ9WgmQZe+y+0dLlu88QggWLFjA7Nmz2bhxI/PmzWPu3Lm7lRQphGDNmjWEw7KPOa6LuC8RQrBp0yamTp3KunXrmD17NkuXLs0K1gFMVrAOYIQQdO3alaKiIlRVJT8/n+Li4t1a/rcsi4aGhozyl460pWlJU1MTixcvZs6cOen8p90hGAxSWVmJrut07dqVzp07fyMXM8t3m6xgHcCoqsoFF1zAe++9x/Tp03n33Xe54IILOiw0QggaGhrYsmVLenXQMIwO95JPsXbtWn79618zfvx4Jk6cyOmnn86yZcs6nNqgqioDBw7k5Zdf5vXXX+fVV19l/IQJ2aD5AUxWsA5wcnJyGDJkCCeccALDhg3bre6cuAmWzVMPdF3vsPClqK+vZ+HChdTU1NDQ0MCcOXN2ezFAVVV69erFsccey6hRo1C/A6upWfYeWcHKsksURSEvL4+xY8cycOBAunbtymGHHUZJyfZx6R2huLiYYcOGUVpaSnFxMUcddRSdO3f+RgH4LAcH+7SWcNDgwZyYrSXcL1AUhT6VlXQvLWXQwIGcc+65DB06tOVm7SIYDNKnT5/01OmLfvQj+vXtmxWs/YSDtpZwz8lglm+DkuJifvCDH3DlVVcxceLElg93iMrKSn70ox/xi1/8gsMOPTQbKM/SLvapYGXZv1AUBY/Hg8/n+8alNKqq4vV68Xq9WbHK0m6ygpUlS5b9hqxgZcmSZb8hK1hZsmTZb8gKVpYsWfYbVOHO2lIUefk2EO4f/aaB2yxZsnz7aJqWPof3Ns11SQhQcvO6CMuRKQaqCpoKhq7Sp3cfqqs3Eo1F0PZgfoyiKITDYYLBIJMnT+aWW2751t58lixZvhmqqnLHHXfwxBNP7Halw46wHYeAP4fikm6sWLEC03KwHXAcOcNUV0F5+KZhYl11ko3bTKq3mWyrN6kPO3Qt6cmq1etpCkdQVRVFUdBU0DTQNQVVUdhdHbMsC13X6dOnD+PGjcNxnKxoZcmyH+D1evnggw9YtGjRbtdsOg44QmDZAtsG25Fel+M45Obm0KuiB5s3rSI/qNEp36Ckk7yUFXtQamccKxTAtAXxhKApYlPbZBGOG6yvjrB+U5zqGpPqGpOt9RZ1TTZNEZt4wiFhClI6I60zBU2VQqYqoKpK2pxTFDnqubksqaqadQuzZNmPUBQF0zTTheqK+7+UDggBjiNwhBQm2xHYjiBV164o4DUUfF6V3ByNglyNzvk6xUUGxUUGPYp99CjJIegzKczVyc3R8HkVDE1BAMrq148WStpXVNIWlIKDrsuEPscRJExBLOFQH3aobbDYWmeypdaiusZkc43F1nqTbfUW9eGUoAlMS75YIeT+dU3uX1UVtLRf6mSKWnNaCFyWLFn2LikBak5zMRKAVAcFxxbYDlj2dsNF1xQMXcHnVQjlaOQFNTrl63TONygu0ulaZNC10KBTgU5hnk5+UMXvVfEaCqoq/7Bl2QjUtAUmhNx/WrCavbY0wv1fKuilqgqqIq0oVQNdVVBUV1FtQTwpBa0x4lDfaFHTaLGl1mKzK2xb60zqGm1qm2zCEZtwzCFpOli2FERcwdIUuX9VlS5oykprqWVZsmTZc6QEwXGkCDmOwLHBdsUC5Lmoa+AxVIJ+lWBAozCkURDS6Fxg0LVQp0uBQZdCnaI8nfxcnVCOFCSfR0HV5LksHLBS+09bY64oSUXc4fm+Q8HqCIoCajrGlSk0AI4Ay3KIxgWRmENDxKa+yaKm3mJrvc22eilo2xos6htt6poswjGbWFwQTzpYlsBypIBKd9N1O5tdVxQpqG1Za9nwWJaDgbaOeSHk+SdjRDJ25LiB7NR1FNBdz8rnUfH7FIJ+jYJcnfyQRqc8nc4FhmspaRTlSzHKy9HI8asEfAq6ruIaSGm30HbAdq0wp5nwfRP2iGDtirSV5oqLpirS7VSk6AghA2+m5RBPCKJxh6aITV2TvGxrMKmpt6ltsKhttKhtsGgI29SHHaIxm3hSkDCd9IeTckFT+28eW1MARVXSCt7KDc2S5TtMWogA4QjXKtoeKxJOSqBcj8U1IryGtHICfo38oEpeUKMgT6coJK2honyNojyDglwZV8rN0Qj4VBk/0lU0Ve7Pcc8vy94em0qJ0Z4QpF3xrQhWW6TeXEowpHWUGbCXVtR2yyml2ElTilo04dAUcWgIW9Q3yQWBbfXSeqtrlP/Wh20iMYdwVG6fTMrFAtuWX3bz15Gy0lIiJ0VWClzq1yNLlr2BI6QApcRmuxhI6yjjOCUlQgoej0rAqxIMqOQEVPJypGVUENLIz9XplC8FKD9XJy+ok5sjtw/4VDyGkvaIUpaYk/q7zQLnQsjrtHHeftvsM8HaXTIsNW27wKjNrCYA05LLpklTuqGRuEMkZtMQtmkM29SH7QxRawg7NDTZhGO2FMO4QzzpYJoC0xZYVguBA5QMl1QGI7dflwKYsvRSZHzRzX4ts3z3SX91bbheqevysv1YkTlE2y0fR8jrqaeljhVdlythhiHdsoBPXoJ+jbxcjbygSn5QCk9BSAazU5ccv3TNclwRSgW+06/LjU2lBNC2My2j/Yn9TrDaQ+ogoJnFtH3RYHt8LXWAyZUOB8uCRFKKWzTuEIlJ17QhYktLLmLTELZoCjs0RW2aYg7hiPw3npACF0sIkqZMeLPdVQ6njaMiJbxS9NzrrrilL270sbnG7atftgOVDMFx/yfY7uKkLo5rZUjhaftEV91V9pTV4jFU/F4pQD6vSq5fJZijkeuXS/q5OSr5QZ1QUCPXtY5CORoBvxSrHJ+K16Oi66Br292y1LGbDpA3t4xcpWz+43ogcUAK1o5IHZAgfyWlFdTMGnLFoy0xScXahJD7sByZtmFa0oqLJRz3IojF5SpoU9QmHHWFL2YTiUrXNByzM7aNJQWJpEPSEphJmUJi2aKZWb49NidSP/AKKK3ei7yScl+3C5/7WLP70tdTcthCGFvdboOWj+/oQGrvdikyvqcWt1NigntCbr++/SRN3SdP3u2PpfehuPe7r01p9kOWCkforstleBQ8uoLXo+L3qPh9UoT8Xmn9pFyxXNfKCQZUcgMaQb+K36elt/V7pfVj6PKiu3k9qe8jHQRvIYqp2xnvr9l7ac/3dCBxUAnWNyF1cKdIi1rKglOkKKRWLpuLQgpHCBAKtit2lp0SPWnZxZNy0SHe7Ho0Lq23aNIhFhfE4g6xpEM8IXPdYknhJvE6JE1Imo7cp+kKnyPjdbYj008cRy5Vp+IUqWXllBA3P+nTlgbNTvY9fLSkP5+MH5Bm1qb7WOqHRC6euCGB1OftWjSa5gqNLl0rQ1fwGCoeAxl09qr4PTJHyOfVtguQTyHgWkGpQLPPo7qWkbzu9agYOmmxMXS5kIMiMgZfNBfT1CpcKgaUCli3tNBaHltZdkxWsL4lUide6p9UfCt1oqZ+2aUAbs89S53Eqeem4h+pk0C4FphlS6vPtrcvJdu2jL+ZprTeLBtsS4qY5QqmvIBludu6VmNKSLdnKqfyc1Luh3sytvjVb+n+qu4b2S5GzVz0lPC4t1OruSlhSF9SAuEuveuagq4r6KqCpru5QbqCYagY2vZAsuYmKutu/lD683V/XBRkHFJ+sNvfR+o9pXKDUpZu6j1KQXetttR96XecZW+SFazvGKmTIk0zkUvf1fy+ZhZJc2FIbZe2VtLbNttn6jbyBE7T7H73ZuYdzUlZFG3c1/w56as72U/zfbT8HFK1pikxSd1Ii4h7fyuXMfW4+1jzv9PSysm80vpzyLLvyQpWlixZ9ht2s99ClixZsnz7ZAUrS5Ys+w1ZwcqSJct+Q1awsmTJst+QFawsWbLsN2QFK0uWLPsNWcHKkiXLfkNWsLJkybLfkBWsLFmy7DdkBStLliz7DVnBOihQEMJGOGbLB3aBQNgxWXEtqxQRdgLhJNooCnT/hrARdsIt1FOg+X2492U8x0IIa/u2djz9qHDMzIK/HdKq8jHLAUpWsA54BAgHVfOjefJS5cMtN2oDKS6eUCWqkQPCQThJjGAFRrAC4VgttndQVANFNTByuoOiSGFTDFTVg5HTDYRwxS5VneygeQpRNT+OHUU1ghjBCrk3K4rmyUfRvOnXIhwTx4ogrCiOFUXYcXk9WY9jNrqXhmYCm+VAIytYBzjCjmMn6wh0OYKCvj9FWHF5sqesmjZRcJJNqJqfooG/QlF92GYDwkmSX/kjfAVDsBJbcayYux9wzDB5vc4lWHoS+X0vwxOqRNgJQhVnkNvjVPIrf4KRW46iBwA579JObMMTrKDT4N+AoqJ5O1M04Aqs+Fb8RcMpGnwNKAqOGQZhY+R0J9BlDN6Cwfg7jcAb6k9Ot4nk97mI/D4/Iq/PReSWTUb1hHbDmsyyP6BddX7P21remeVAQOCYTYQqzkLz5qPqOXhClSQav6aw309J1C1AWBEU1Wj5RGn5+DoRLJtEoMto4nXzpZVmBMjvcxHx2nmoRi6Gv4t06cxGdH9X8ntfhOrJxVcwCM1XhOYpINDlCDRfEb78Qei+rnhyK0g0LEHYUfxFIzACpQRLj8Ub6o/u70Sg8+EIO0HR4F/hJBsRVgQhbKz4ZoLFRxPqeTah8u/jKxwKmgGKijdUiaJ50X1dyC0/neimD7HjW9t+b1n2a7KCdYBiJ+oIlh5Pp4FX0rTuVVRPCE9OGeEN08gtO52ckqOIVr+P4yRbnNgCx45SNOhqcrocSTK8hpzio9EDxaiql0CXI1CNIIFOIwiVT8ZJ1hPb+jmhijNRVQ9NG6bhLxpOuOoNQKAA0c0f48sfRGTjO5jRDdiJbQg7QefDbkfzdSJa/QFCAUXRSTQuQ/d1IVH/NVZkLXm9fojAJlEzh2TTSuK18/B3HsWWOTcR3jANzQihGLlsm38HyaYVBDodTmTj2zhWBEXVm72vLAcCWZfwAMSxYwSKx9Np4NXUfPUA0S0z0IxcVD2AY0XY/OWNKIpOl2F3oulBaBWPUlF0H/Ur/0HVjB9Rv/xJPLmV5FacxZa5v6V65jVUz7yKeO18FNUHqhfHiqNoHooG/BI7sY1Q2ekIYeEIi4K+l+JYTeSUHk9O8QQ8uX0QjoWTrKdp/SugGuCYCCuKsBM4ZhOq5sWMVtFUNQ0FOWRP2HH8RcNJNi4nXr8IYVt4QpUYgW6gaOi+ziBsHDvSrJVolgOJ7Ld6gCGcJLq/hKIBv6Ru5dM0rp+K5u2MGa0iVjsPRc9BOCab59yM6ikkt8fJOHa05W5AODhmE3aiBtusBwThjW9jJxsRThLHljEiYcdQVYOGlf8gXreQ2NbPaVj9XxTNjzAjWPGtRKrfo3Ht/0g2LiHRsAwjtwKw2bbwXoQVJ1R2OlZ0E8nIBvlv00oUzUdez7NpWvsKTeuno2h+FNVDTslEvHkDKB7+e3yFQ1FUAztRg2NFUI08HCuClah1BWtHMbos+ytZl/AAQ44GU4htm0mk6i1QdIQVRfd3RfPkEdv6BYqiYCcbiG7+CCu2CSGcjBbJwjHJKT4Kb6gvRqCEnG7HYifqaFj9T4qH302ycQVWZB25PU7FDK8mUTOXUPn3ye1xCjVfPYju64IQJjgm/qJh1C1/Csdswt/1SIxANyKb3sVO1OFYTQgrgqoHUfUcVCMX1ciVq4OKRnzbLGLbZqZXKHNKjiGv19k0rv4vnrxKhLBQNT/B0hPxFw0j2O1YPKHeaN4CknVfgTCzltYBRlawDjQUBWFHUVDILTsdX8FQvPn9yC09kUDXsQB4C4fiLxqOAtKaUb0ZuxB2kpzio/Dk9kJVdTyh3gg7TsOqf6IaOeRXXkJk80cEuozGDK8l2bgCzcglXreQvIoz8RceCgiMQHdUzYu/0whyuo7FCq+j5qsHZUBc86IoGsHS49H9XVE0H4oiVw81T74cSustABzMyAYURSev1w/RA8XULPoDiqqh6n4aV/+HZOMyzMg6optnkGxcTrD0JCJVb+LY8fQ+sxwYZH9+DkSEQPN1xlcwBF/hIPyFh6ZFwVc4BF/BYHwFg9GDZa7b1CIvS1FB1alf8TQbP/0/6pb+VaYdGCEa175MZONbaJ6QmxtloWgeYjVzsJN1+IqG0bj2fzSueRHHbCS6bRb1y58kXrcAf5fRKIoqg+HCQQhBsPRkhBBEt36KFatGNULEa+cRq5mNN68fvqLhCCeJonmpX/YEsW2z0XxdZMzK2xlv/kBQDfkOFA07vhUrthnHyVpXByLZb/SAQ0FRPSTrF7N59m/YPOt6Nn1xBQ2r/0OibiHVM3/F5lm/oXr2tTSt/Z8MeO8g1iOEcDPR3Qx1RQMhqFv6N5JNa1BUD7h5WIrmRdH92MkGIpvel6t5XcagoBDZ+C6xrbMQji33kUJRQThENr5F3dK/gapjBLoR3jCd+uVPEa+dh6JoaXfVjFaBsJtZYgUES08gt/spBEtPItj9JDz5A6QrKMztQ2KzHDBkp+YcaAiBonlQPfnpshbHbCJUNgl/p5Fsnfc7UL2gqCiKgmPFcMym7bPBEDhWhC6H3YHu60y8dh6+wkNx7ATVM3+FZoRA1dCMEJ0Pu4Parx8itu1LOTLMCJLTZRyOHSW3xyQ0byF2fBtWogYrthEn2UTjuv+hql5QNBwrSk7x0Th2DF/+QHJKJmJG1qHqfhINyxB2jFjNHOI1c1CNEI4Zo+uIu/AEyxGoNK79D/Ur/oFm5MkVSbORvN7nk9v9ZDZ9drm05LJW1gFFVrAOMIQdxVt4GEUDL5dWkbARQqBoPlRVl1njrjgpWoBw1Rs0rHwGRfOn3cOUYGlGiHjDYhTFQ6JhMZGqNwmWnkher3NRjSDJyAa2zr8DJ1mPv3A4uT3PQNVyUDUf0S2f0rD2BVTVR6Drkfg7jUDzFmGG11C77K8IK0Z+7wsxcnvK+yPrZTyqaQXe/EHkdB2LJ9QXcGhaP5Vo9Ueg6BQNugozup54zTzsRA1WogbNyKOw/89QPXkYwV40rXtJxtv0nJYfT5b9nKxgHXAIFNWDaoSaxaZkkTFC1vttR0XYMRwr3MwtFAjh4An1wYpWY0U3oCgGqAaq7kXRctB9nWT2eXSTzJ9C4An2xFs4hETD15iNK3CsMIomBUPYUZmRnjcQT14fotUzcOwYOV3GIoRNon4xVqwaRdVRNB+OFQcngWrk4+88EjvZQKJ+EYrqQdG8OGaTjGupPhRVA1Q8ef3Q9ABWfCvJplVu0mjWJTzQyArWgYhw0jV+O0UgT/hWK2kKjh1FUXQZp2oWlBfCBrdOT1EN97myMFnYESkqqqeNfQrZ6UFYruWjukIpUFRv2wIjbLnSpxruSqaMqckYltrsdQkcOy6LnhUVVfO13leWA4KsYGXZg7Sx4rhTtlt1O6Yj++zItln2R7IRySx7kI6KhWjHc3b1eHM6sm2W/ZGsYGXJkmW/IStYWbJk2W/IClaWLFn2G7KClSVLlv2GrGBlyZJlvyErWFmyZNlvyApWlixZ9huygpUlS5b9hqxgZcmSZb8hK1hZsmTZb8gKVpYsWfYbsoKVJUuW/YasYGXJkmW/IStYWbJk2W/4/0X+8pAKYj8ZAAAAAElFTkSuQmCC"

        try:
            # 使用内置库处理图片
            img_data = base64.b64decode(base64_image)
            
            # 尝试使用tkinter内置的PhotoImage (仅支持GIF, PGM/PPM)
            try:
                photo = tk.PhotoImage(data=img_data)
                label = tk.Label(support_window, image=photo)
                label.image = photo  # 保持引用
                label.pack(pady=20)
            except:
                # 如果图片格式不支持，显示文本提示
                messagebox.showinfo("提示", "无法显示图片。请使用GIF、PGM或PPM格式的图片。")
                text_label = tk.Label(support_window, text="请使用GIF、PGM或PPM格式的图片", pady=20)
                text_label.pack()
                
        except Exception as e:
            messagebox.showerror("错误", f"无法显示图片: {str(e)}")

        # 设置窗口模态
        support_window.transient(self.root)
        support_window.grab_set()
        self.root.wait_window(support_window)

    def copy_to_clipboard(self, text, label):
        """复制文本到剪贴板并显示提示"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.copy_success_label.config(text=f"{label}已复制到剪贴板!")
        # 3秒后清除提示
        self.root.after(3000, lambda: self.copy_success_label.config(text=""))

    def open_config(self):
        # 检查是否有未保存的更改
        if self.is_modified:
            response = messagebox.askyesnocancel("未保存的更改", "当前文件有未保存的更改。是否继续打开新文件？")
            if response is None:  # 用户点击了取消
                return
            elif response:  # 用户点击了是
                pass
            else:  # 用户点击了否
                return

        # 清空现有控件
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

            # 解析配置文件
            self.parse_config(content)

            # 创建控件
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
            # 获取翻译后的说明
            description = self.option_descriptions.get(key, "该配置项的说明暂未提供")
        else:
            display_name = key
            # 使用英文说明
            description = self.option_descriptions.get(key, "No description available for this option")

        # 创建标签
        label = tk.Label(self.scrollable_frame, text=display_name, anchor="w")
        label.grid(row=row, column=0, sticky="w", padx=5, pady=2)

        # 根据配置项类型创建不同的控件
        if key in self.option_values:
            # 创建下拉菜单（带翻译）
            var = tk.StringVar(value=value)
            # 获取翻译后的选项列表
            translated_values = list(self.option_values[key].values())
            combobox = ttk.Combobox(self.scrollable_frame, textvariable=var, values=translated_values)
            combobox.grid(row=row, column=1, sticky="we", padx=5, pady=2)

            # 查找当前值的翻译
            current_value = value
            if current_value in self.option_values[key]:
                current_value = self.option_values[key][current_value]
            var.set(current_value)

            # 绑定值变化事件
            combobox.bind("<<ComboboxSelected>>", lambda e, k=key, v=var: self.update_config(k, v.get()))
            var.trace_add("write", lambda name, index, mode, k=key, v=var: self.update_config(k, v.get()))
            self.controls[key] = var

        elif key in self.option_ranges:
            # 创建滑块和显示值的标签
            min_val, max_val = self.option_ranges[key]
            try:
                current_val = int(value)
            except ValueError:
                current_val = min_val

            var = tk.IntVar(value=current_val)
            scale = tk.Scale(self.scrollable_frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                             variable=var, command=lambda v, k=key: self.update_config(k, v))
            scale.grid(row=row, column=1, sticky="we", padx=5, pady=2)

            # 使滑块支持方向键微调
            scale.bind("<Left>", lambda e, k=key, s=scale: self.adjust_scale(s, -1, k))
            scale.bind("<Right>", lambda e, k=key, s=scale: self.adjust_scale(s, 1, k))
            scale.bind("<Up>", lambda e, k=key, s=scale: self.adjust_scale(s, 1, k))
            scale.bind("<Down>", lambda e, k=key, s=scale: self.adjust_scale(s, -1, k))

            value_label = tk.Label(self.scrollable_frame, textvariable=var)
            value_label.grid(row=row, column=2, padx=5, pady=2)

            var.trace_add("write", lambda name, index, mode, k=key, v=var: self.update_config(k, v.get()))
            self.controls[key] = var

        elif value.lower() in ['true', 'false']:
            # 创建复选框
            var = tk.BooleanVar(value=(value.lower() == 'true'))
            checkbox = tk.Checkbutton(self.scrollable_frame, variable=var)
            checkbox.grid(row=row, column=1, sticky="w", padx=5, pady=2)

            var.trace_add("write", lambda name, index, mode, k=key, v=var:
                          self.update_config(k, "true" if v.get() else "false"))
            self.controls[key] = var

        else:
            # 创建输入框
            var = tk.StringVar(value=value)
            entry = tk.Entry(self.scrollable_frame, textvariable=var)
            entry.grid(row=row, column=1, sticky="we", padx=5, pady=2)

            var.trace_add("write", lambda name, index, mode, k=key, v=var: self.update_config(k, v.get()))
            self.controls[key] = var

        # 添加配置项说明
        description_label = tk.Label(self.scrollable_frame, text=description, anchor="w", wraplength=300, justify="left")
        description_label.grid(row=row, column=3, sticky="w", padx=5, pady=2)

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
        # 对于下拉菜单，需要将翻译后的文本转换回原始值
        if key in self.option_values:
            # 查找翻译对应的原始值
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
            # 读取原始文件以保留注释和格式
            with open(self.current_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # 更新配置值
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith('#') or not line:
                    continue

                if '=' in line:
                    key, _ = line.split('=', 1)
                    key = key.strip()
                    if key in self.config_data:
                        lines[i] = f"{key}={self.config_data[key]}\n"

            # 写入更新后的配置
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
            if response is None:  # 用户点击了取消
                return
            elif response:  # 用户点击了是
                self.save_config()

        self.root.destroy()

    def toggle_translation(self):
        self.is_translated = not self.is_translated
        # 清空现有控件
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # 重新创建控件
        self.create_config_controls()

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftConfigEditor(root)
    root.mainloop()
