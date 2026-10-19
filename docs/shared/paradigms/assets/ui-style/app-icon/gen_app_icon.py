# -*- coding: utf-8 -*-
"""Ultima AI 桌面图标资产生成器（透明底 · 占满 100%）
产出：app-icon.ico（Win 多尺寸 16-256）/ app-icon.icns（macOS）/ app-icon-256.png / app-icon-512.png
图形：宇航员半身像（astronaut.png）
重跑本脚本即可按当前规范重建全部桌面图标资产。
"""
from PIL import Image
import os

SRC = r"H:\UltimaAI\_shared\brand\ultima-logo\astronaut.png"
OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

helmet = Image.open(SRC).convert("RGBA")


def fill100(size: int) -> Image.Image:
    """透明画布 + 宇航员半身像占满 100%（完全贴满，无呼吸边），水平垂直居中"""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    h = helmet.resize((size, size), Image.LANCZOS)
    canvas.paste(h, (0, 0), h)
    return canvas


# 透明底 PNG 源（256 / 512）
for s in (256, 512):
    fill100(s).save(os.path.join(OUT, f"app-icon-{s}.png"))

# Windows .ico：单文件内嵌多尺寸
ico = fill100(256)
ico.save(
    os.path.join(OUT, "app-icon.ico"),
    format="ICO",
    sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
)

# macOS .icns：Pillow 自动内嵌 16-1024 多尺寸
icns = fill100(1024)
icns.save(os.path.join(OUT, "app-icon.icns"), format="ICNS")

print("generated:", sorted(os.listdir(OUT)))
