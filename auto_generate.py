#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, random, datetime, textwrap

SITE_DOMAIN = "botdefi.io"

# Ảnh an toàn (không chặn hotlink) — ưu tiên picsum/pexels
IMAGE_POOLS = [
    "https://images.pexels.com/photos/8372683/pexels-photo-8372683.jpeg?auto=compress&cs=tinysrgb&w=1600",
    "https://images.pexels.com/photos/8370677/pexels-photo-8370677.jpeg?auto=compress&cs=tinysrgb&w=1600",
    "https://images.pexels.com/photos/8370753/pexels-photo-8370753.jpeg?auto=compress&cs=tinysrgb&w=1600",
    "https://images.pexels.com/photos/6770612/pexels-photo-6770612.jpeg?auto=compress&cs=tinysrgb&w=1600",
    "https://picsum.photos/1600/900?random=5182",
]

# Backlink “mềm” (luân phiên 6–8 link/ngày)
FRIENDS = [
    "https://botweb3ai.com", "https://botblockchain.io", "https://metaversebot.io",
    "https://nftgameai.com", "https://bottradingai.com", "https://botgame.io",
    "https://aiesports.io", "https://botesports.com", "https://esportsai.io",
    "https://pronftgame.com", "https://hubgaming.io"
]

GUIDE_TITLES = [
    "Hướng dẫn kiếm lợi nhuận với DCA Bot trong DeFi",
    "Cách setup Grid Bot trên DEX để tạo dòng tiền đều",
    "Tối ưu lợi nhuận bằng Yield Aggregator + Auto-Compound",
    "Chiến lược Bot Arbitrage trên AMM (dành cho người mới)",
    "Quản trị rủi ro cho Bot DeFi: cài đặt stop, max drawdown",
    "Săn APR an toàn: Bot quay vòng farm & compound",
    "Tự động hóa chiến lược LP với Rebalancing Bot",
    "Backtest bot lợi nhuận: cách làm & đọc kết quả đúng",
    "Đổi thưởng & bảo toàn vốn: chiến lược 50/50 với Bot",
]

SECTIONS = [
    "Chuẩn bị ví & mạng lưới",
    "Cấu hình bot & thông số an toàn",
    "Chiến lược vận hành từng ngày",
    "Mẹo tăng lợi nhuận & giảm rủi ro",
]

BULLETS_POOL = [
    "Dùng ví phụ, hạn mức nhỏ khi thử chiến lược mới.",
    "Luôn bật slippage hợp lý và giới hạn khối lượng.",
    "Ghi log lệnh/balance mỗi 24h để theo dõi drawdown.",
    "Ưu tiên DEX/Pool có thanh khoản dày & phí rẻ.",
    "Tránh token kém thanh khoản hoặc biến động sốc.",
    "Tách vốn: 60% chiến lược chính, 40% sandbox.",
    "Luôn có kế hoạch thoát khi APR giảm đột ngột.",
    "Dùng oracles/price feed để hạn chế MEV trượt giá.",
]

def choose_title():
    return random.choice(GUIDE_TITLES)

def choose_image():
    return random.choice(IMAGE_POOLS)

def choose_bullets(n=4):
    return random.sample(BULLETS_POOL, k=min(n, len(BULLETS_POOL)))

def choose_friends(k=7):
    return random.sample(FRIENDS, k=min(k, len(FRIENDS)))

def slugify(s):
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-")

def make_markdown():
    today = datetime.date.today()
    title = choose_title()
    desc = "Practical DeFi bot walkthrough for stable, compounding returns."
    image = choose_image()

    # Nội dung chính (markdown thuần, không Liquid)
    intro = textwrap.dedent(f"""
    Trong bài hướng dẫn này, bạn sẽ **thiết lập bot DeFi** theo từng bước để tạo dòng tiền đều đặn.
    Tư duy trọng tâm: **an toàn vốn trước – tối ưu sau**. Hãy bắt đầu với khối lượng nhỏ và mở rộng khi
    chiến lược chứng minh hiệu quả.
    """).strip()

    # 4 mục nội dung với bullet tùy biến
    sections_md = []
    for s in SECTIONS:
        bullets = "\n".join([f"- {b}" for b in choose_bullets(4)])
        sections_md.append(f"### {s}\n{bullets}\n")
    sections_md = "\n".join(sections_md)

    # “Pro tip” khác nhau để tránh trùng lặp cảm giác
    pro_tip = random.choice([
        "Ưu tiên pool có **TVL cao** và volume ổn định; bot sẽ khớp lệnh mượt hơn.",
        "Đặt lịch **rebalancing** theo mốc 24–48h thay vì chạy liên tục để giảm phí.",
        "Luôn có **quy tắc dừng** khi APY/volume tụt mạnh hoặc tin tức rủi ro.",
    ])

    friends = " • ".join([f"[{u.replace('https://','')}]({u})" for u in choose_friends()])

    body = f"""
_{pro_tip}_

{intro}

## Key Insights
- Chọn bot phù hợp: **DCA**, **Grid**, **Arb**, hoặc **LP-Rebalance** tuỳ khẩu vị rủi ro.
- Tách vốn – mỗi chiến lược một ví để quản trị rủi ro.
- Ghi chép & backtest giúp bạn biết điều gì thực sự hiệu quả.

{sections_md}

## Friendly Network
{friends}
"""

    fm = f"""---
layout: post
title: "{title}"
date: {today}
author: "BotDeFi Team"
description: "{desc}"
image: "{image}"
tags: [DeFi, Bot, Guide]
---
"""
    return fm + "\n" + body.strip() + "\n"

def main():
    os.makedirs("_posts", exist_ok=True)
    content = make_markdown()
    # tránh đè bài trong ngày: slug theo tiêu đề
    title_line = [l for l in content.splitlines() if l.startswith("title:")][0]
    raw_title = title_line.split(":",1)[1].strip().strip('"')
    slug = slugify(raw_title)[:80]
    today = datetime.date.today().isoformat()
    fn = f"_posts/{today}-{slug}.md"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(content)
    print("Wrote:", fn)

if __name__ == "__main__":
    main()
