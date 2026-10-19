# -*- coding: utf-8 -*-
"""Ultima AI 桌面图标资产生成器（透明底 · 宇航员 112%，与主形态同比例）
产出：app-icon.ico（Win 多尺寸 16-256）/ app-icon.icns（macOS）/ app-icon-256.png / app-icon-512.png
图形：宇航员半身像（astronaut.png），放大至边长 112% 居中，四周各超 6%，画布边界裁边
重跑本脚本即可按当前规范重建全部桌面图标资产。
"""
from PIL import Image
import os

SRC = r"H:\UltimaAI\_shared\brand\ultima-logo\astronaut.png"
OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

helmet = Image.open(SRC).convert("RGBA")


def fill112(size: int) -> Image.Image:
    """透明画布 + 宇航员半身像放大至边长 112% 居中（四周各超 6%，画布边界裁边），与主形态同比例"""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s2 = int(size * 1.12)
    h = helmet.resize((s2, s2), Image.LANCZOS)
    canvas.paste(h, ((size - s2) // 2, (size - s2) // 2), h)
    return canvas


# 透明底 PNG 源（256 / 512）
for s in (256, 512):
    fill112(s).save(os.path.join(OUT, f"app-icon-{s}.png"))

# Windows .ico：单文件内嵌多尺寸
ico = fill112(256)
ico.save(
    os.path.join(OUT, "app-icon.ico"),
    format="ICO",
    sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
)

# macOS .icns：Pillow 自动内嵌 16-1024 多尺寸
icns = fill112(1024)
icns.save(os.path.join(OUT, "app-icon.icns"), format="ICNS")

print("generated:", sorted(os.listdir(OUT)))
