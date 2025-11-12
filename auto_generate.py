#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto generator for botdefi.io
- Jekyll/Netlify compatible
- Safe Liquid escaping so includes (ad.html / analytics.html) render correctly
- DeFi-focused topics, Pexels/Unsplash images, backlinks to network
"""

import os
import datetime
import random
import re
import uuid

# ---
# Configuration: change SITE_DOMAIN if needed or set env SITE_DOMAIN
# ---
SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "").strip() or "botdefi.io"

DOMAINS = [
    'bottradingai.com', 'botgame.io', 'metaversebot.io', 'nftgameai.com',
    'hubgaming.io', 'botdefi.io', 'esportsai.io', 'nftgamepro.com',
    'botesports.com', 'aiesports.io', 'pronftgame.com', 'botplay.io',
    'botweb3ai.com', 'botblockchain.io'
]

# Image pools (Pexels direct CDN + safe fallbacks)
IMAGES = {
    'botdefi.io': [
        "https://images.pexels.com/photos/6770612/pexels-photo-6770612.jpeg?auto=compress&cs=tinysrgb&w=1200&h=630&fit=crop",
        "https://images.pexels.com/photos/6770615/pexels-photo-6770615.jpeg?auto=compress&cs=tinysrgb&w=1200&h=630&fit=crop",
        "https://source.unsplash.com/1200x630/?defi,crypto",
        "https://picsum.photos/1200/630?random=4021"
    ],
    # default fallback
    'default': [
        "https://source.unsplash.com/1200x630/?crypto,blockchain",
        "https://picsum.photos/1200/630?random=123456"
    ]
}

# DeFi-focused titles (rotating)
TOPICS = [
    "DeFi Bot Strategies for Consistent Yield in 2025",
    "How to Build a Safe DeFi Market-Making Bot",
    "Managing MEV and Front-running Risks for Automation",
    "Cross-chain Liquidity Bots: Practical Implementation",
    "Automated Yield Aggregation: Risk Controls & Tools",
    "On-chain Signals: Building Reliable Execution Triggers",
    "Position Sizing and Risk Limits for DeFi Bots"
]

# --------------------------
# Helper functions
# --------------------------
def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    return s[:60]

def pick_image(domain: str) -> str:
    pool = IMAGES.get(domain, IMAGES['default'])
    return random.choice(pool)

def pick_backlinks(domain: str) -> str:
    others = [d for d in DOMAINS if d != domain]
    random.shuffle(others)
    sel = others[:4]
    return "\n".join([f"- [{d}](https://{d})" for d in sel])

# --------------------------
# Build markdown content
# --------------------------
def generate_md(domain: str):
    today = datetime.date.today().isoformat()
    title = random.choice(TOPICS)
    image = pick_image(domain)
    desc = f"{title} — practical DeFi bot guides from {domain}"
    backlinks = pick_backlinks(domain)
    unique_id = uuid.uuid4().hex[:8]
    slug = slugify(title) + "-" + unique_id

    # NOTE: to emit literal Liquid tags we double the braces in f-string:
    #   - '{% include ad.html %}'  => written as '{{% include ad.html %}}' inside f-string
    #   - '{{ p.title }}' needed as '{{{{ p.title }}}}' inside f-string
    md = f"""---
layout: post
title: "{title}"
date: {today}
author: "BotDeFi Team"
description: "{desc}"
image: "{image}"
---

_In today’s fast-moving DeFi landscape, automation and disciplined risk controls are essential. Below are practical insights for builders and traders in 2025…_

{{% include ad.html %}}

### Quick overview

Automation in DeFi can streamline execution, reduce manual errors, and capture cross-protocol opportunities — but only with layered risk controls.

**Key themes covered:**
- Execution reliability and monitoring  
- MEV-aware designs and front-running mitigation  
- Practical position sizing and gas-aware routing

---

## Detailed points

1) **Execution & Observability**  
Reliable infra (retry, idempotency, on-chain receipts) matters. Combine on-chain event watchers with off-chain sanity checks.

2) **MEV & Protection**  
Design strategies to minimize extractable value exposure — use private relays, transaction bundlers, or time-weighted execution where appropriate.

3) **Composability & Liquidity**  
Leverage protocol composability for routing and liquidity, but measure slippage and gas tradeoffs.

---

## Related Articles (internal)
{{% for p in site.posts limit:4 %}}
  {{% if p.url != page.url %}}
  - [{{{{ p.title }}}}]({{{{ p.url }}}})
  {{% endif %}}
{{% endfor %}}

## Friendly Network
{backlinks}

{{% include analytics.html %}}
"""

    filename = f"_posts/{today}-{slug}.md"
    return filename, md

# --------------------------
# Main
# --------------------------
def main():
    domain = SITE_DOMAIN or os.path.basename(os.getcwd())
    os.makedirs("_posts", exist_ok=True)
    path, content = generate_md(domain)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Post generated:", path)

if __name__ == "__main__":
    main()
