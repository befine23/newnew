"""
Generate mock historical articles for testing
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

# Mock article templates
articles_data = [
    {
        "title": "Netflix Announces Major Film Slate for 2026",
        "title_zh": "Netflix 宣布 2026 年重磅電影陣容",
        "source": "Deadline",
        "summary": "串流巨頭 Netflix 公布了2026年令人期待的電影陣容，包括多部大製作和獨立電影。該公司承諾在新的一年為觀眾帶來多元化的內容..."
    },
    {
        "title": "Margot Robbie to Star in New Thriller 'The Echo'",
        "title_zh": "瑪格·羅比將主演新驚悚片《回聲》",
        "source": "Variety",
        "summary": "奧斯卡提名女演員瑪格·羅比確認將主演心理驚悚片《回聲》。這部電影由新銳導演執導，講述一名女子發現她的生活被神秘監視的故事..."
    },
    {
        "title": "Box Office: 'Avatar 3' Breaks Opening Weekend Records",
        "title_zh": "票房：《阿凡達3》打破首週末票房紀錄",
        "source": "The Hollywood Reporter",
        "summary": "詹姆斯·卡麥隆的《阿凡達3》在全球首映週末創造了驚人的票房紀錄，成為有史以來開畫成績最好的電影之一..."
    },
    {
        "title": "Christopher Nolan's Next Project Set at Warner Bros",
        "title_zh": "克里斯多福·諾蘭的下一部作品定在華納兄弟",
        "source": "Variety",
        "summary": "在《奧本海默》取得巨大成功後，克里斯多福·諾蘭確認將與華納兄弟合作他的下一部神秘項目。這標誌著這位導演與工作室關係的回歸..."
    },
    {
        "title": "A24 Acquires Rights to Sundance Winner 'Midnight Sun'",
        "title_zh": "A24 獲得聖丹斯獲獎影片《午夜太陽》版權",
        "source": "Deadline",
        "summary": "獨立電影公司 A24 在激烈競爭中贏得了聖丹斯電影節大獎得主《午夜太陽》的發行權。這部電影獲得了評審團和觀眾的一致好評..."
    },
    {
        "title": "Marvel Studios Announces Phase 6 Plans",
        "title_zh": "漫威影業宣布第六階段計劃",
        "source": "The Hollywood Reporter",
        "summary": "漫威影業總裁凱文·費吉公布了漫威電影宇宙第六階段的詳細計劃，包括多部備受期待的續集和全新角色的首次亮相..."
    },
    {
        "title": "Cannes Film Festival Reveals 2026 Competition Lineup",
        "title_zh": "坎城影展公布 2026 年競賽片單",
        "source": "Variety",
        "summary": "第79屆坎城影展公布了競賽片單，包括來自世界各地知名導演的作品。今年的陣容被認為是近年來最強大的之一..."
    },
    {
        "title": "Tom Cruise Confirms 'Mission: Impossible 8' Will Be His Last",
        "title_zh": "湯姆·克魯斯確認《不可能的任務8》將是最後一部",
        "source": "Deadline",
        "summary": "湯姆·克魯斯在最新採訪中證實，即將上映的《不可能的任務8》將是他飾演伊森·韓特的最後一部電影，為這個標誌性系列畫上句號..."
    },
    {
        "title": "Denis Villeneuve's 'Dune 3' Gets Official Green Light",
        "title_zh": "丹尼·維勒納夫的《沙丘3》正式獲得綠燈",
        "source": "The Hollywood Reporter",
        "summary": "在《沙丘：第二部》取得巨大成功後，華納兄弟和傳奇影業正式宣布開發三部曲的最終章。維勒納夫將繼續擔任導演..."
    }
]

def generate_article(template, date, index):
    """Generate a complete article from template"""
    source_key = template['source'].lower().replace(' ', '').replace('the', '')
    slug = template['title'].lower().replace("'", "").replace(":", "").replace(" ", "-")[:60]
    
    return {
        "id": f"{date}-{source_key}-{index:03d}",
        "slug": slug,
        "source": template['source'],
        "title": template['title'],
        "title_zh": template['title_zh'],
        "url": f"https://{source_key}.com/2026/film/news/{slug}/",
        "description": template['title'],
        "description_zh": template['title_zh'],
        "content": f"[Mock content for: {template['title']}]\n\n" + template['summary'] * 3,
        "content_zh": template['summary'] * 5,
        "summary_zh": template['summary'],
        "image_url": f"https://example.com/images/{slug}.jpg",
        "published_date": date,
        "scraped_at": f"{date}T08:00:00"
    }

def main():
    output_dir = Path("../data/news")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate articles for past 9 days
    for i, template in enumerate(articles_data):
        days_ago = i + 1
        date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        article = generate_article(template, date, i)
        filename = f"news_{date}.json"
        
        with open(output_dir / filename, 'w', encoding='utf-8') as f:
            json.dump([article], f, ensure_ascii=False, indent=2)
        
        print(f"✓ Generated: {filename}")
    
    print(f"\n✅ Generated {len(articles_data)} mock historical articles")

if __name__ == "__main__":
    main()
