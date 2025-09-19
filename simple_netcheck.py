#!/usr/bin/env python3
"""
超簡單網路測試 - 不靠 speedtest
使用 Python 標準庫測試到各大網站的連接性能
"""

import socket
import time
import urllib.request
import argparse
import json
import signal
from typing import Dict, List

# 全球知名網站（用於測試連接性能）
GLOBAL_SITES = [
    {"labels": {"en": "Taipei, Taiwan", "zh": "台北, 台灣", "ja": "台北, 台湾"}, "host": "www.gov.tw", "region": "Asia"},
    {"labels": {"en": "Tokyo, Japan", "zh": "東京, 日本", "ja": "東京, 日本"}, "host": "www.yahoo.co.jp", "region": "Asia"},
    {"labels": {"en": "Seoul, South Korea", "zh": "首爾, 南韓", "ja": "ソウル, 韓国"}, "host": "www.naver.com", "region": "Asia"},
    {"labels": {"en": "Singapore", "zh": "新加坡, 新加坡", "ja": "シンガポール"}, "host": "www.straitstimes.com", "region": "Asia"},
    {"labels": {"en": "Hong Kong, China", "zh": "香港, 中國", "ja": "香港, 中国"}, "host": "www.scmp.com", "region": "Asia"},
    {"labels": {"en": "Kuala Lumpur, Malaysia", "zh": "吉隆坡, 馬來西亞", "ja": "クアラルンプール, マレーシア"}, "host": "www.thestar.com.my", "region": "Asia"},
    {"labels": {"en": "Sydney, Australia", "zh": "雪梨, 澳大利亞", "ja": "シドニー, オーストラリア"}, "host": "www.abc.net.au", "region": "Oceania"},
    {"labels": {"en": "London, UK", "zh": "倫敦, 英國", "ja": "ロンドン, イギリス"}, "host": "www.bbc.com", "region": "Europe"},
    {"labels": {"en": "Frankfurt, Germany", "zh": "法蘭克福, 德國", "ja": "フランクフルト, ドイツ"}, "host": "www.spiegel.de", "region": "Europe"},
    {"labels": {"en": "New York, USA", "zh": "紐約, 美國", "ja": "ニューヨーク, アメリカ"}, "host": "www.nytimes.com", "region": "North America"},
    {"labels": {"en": "Los Angeles, USA", "zh": "洛杉磯, 美國", "ja": "ロサンゼルス, アメリカ"}, "host": "www.latimes.com", "region": "North America"},
]

# Vultr 全球機房測試站點
VULTR_SITES = [
    # 亞洲
    {"labels": {"en": "Tokyo, Japan (Vultr)", "zh": "東京, 日本 (Vultr)", "ja": "東京, 日本 (Vultr)"}, "host": "hnd-jp-ping.vultr.com", "region": "Asia"},
    {"labels": {"en": "Osaka, Japan (Vultr)", "zh": "大阪, 日本 (Vultr)", "ja": "大阪, 日本 (Vultr)"}, "host": "osk-jp-ping.vultr.com", "region": "Asia"},
    {"labels": {"en": "Seoul, South Korea (Vultr)", "zh": "首爾, 韓國 (Vultr)", "ja": "ソウル, 韓国 (Vultr)"}, "host": "sel-kor-ping.vultr.com", "region": "Asia"},
    {"labels": {"en": "Singapore (Vultr)", "zh": "新加坡 (Vultr)", "ja": "シンガポール (Vultr)"}, "host": "sgp-ping.vultr.com", "region": "Asia"},
    {"labels": {"en": "Bangalore, India (Vultr)", "zh": "班加羅爾, 印度 (Vultr)", "ja": "バンガロール, インド (Vultr)"}, "host": "blr-in-ping.vultr.com", "region": "Asia"},
    {"labels": {"en": "Delhi NCR, India (Vultr)", "zh": "德里NCR, 印度 (Vultr)", "ja": "デリー, インド (Vultr)"}, "host": "del-in-ping.vultr.com", "region": "Asia"},
    {"labels": {"en": "Mumbai, India (Vultr)", "zh": "孟買, 印度 (Vultr)", "ja": "ムンバイ, インド (Vultr)"}, "host": "bom-in-ping.vultr.com", "region": "Asia"},
    {"labels": {"en": "Tel Aviv, Israel (Vultr)", "zh": "特拉維夫, 以色列 (Vultr)", "ja": "テルアビブ, イスラエル (Vultr)"}, "host": "tlv-il-ping.vultr.com", "region": "Asia"},

    # 歐洲
    {"labels": {"en": "London, UK (Vultr)", "zh": "倫敦, 英國 (Vultr)", "ja": "ロンドン, イギリス (Vultr)"}, "host": "lon-gb-ping.vultr.com", "region": "Europe"},
    {"labels": {"en": "Manchester, UK (Vultr)", "zh": "曼徹斯特, 英國 (Vultr)", "ja": "マンチェスター, イギリス (Vultr)"}, "host": "man-uk-ping.vultr.com", "region": "Europe"},
    {"labels": {"en": "Frankfurt, Germany (Vultr)", "zh": "法蘭克福, 德國 (Vultr)", "ja": "フランクフルト, ドイツ (Vultr)"}, "host": "fra-de-ping.vultr.com", "region": "Europe"},
    {"labels": {"en": "Paris, France (Vultr)", "zh": "巴黎, 法國 (Vultr)", "ja": "パリ, フランス (Vultr)"}, "host": "par-fr-ping.vultr.com", "region": "Europe"},
    {"labels": {"en": "Amsterdam, Netherlands (Vultr)", "zh": "阿姆斯特丹, 荷蘭 (Vultr)", "ja": "アムステルダム, オランダ (Vultr)"}, "host": "ams-nl-ping.vultr.com", "region": "Europe"},
    {"labels": {"en": "Warsaw, Poland (Vultr)", "zh": "華沙, 波蘭 (Vultr)", "ja": "ワルシャワ, ポーランド (Vultr)"}, "host": "waw-pl-ping.vultr.com", "region": "Europe"},
    {"labels": {"en": "Stockholm, Sweden (Vultr)", "zh": "斯德哥爾摩, 瑞典 (Vultr)", "ja": "ストックホルム, スウェーデン (Vultr)"}, "host": "sto-se-ping.vultr.com", "region": "Europe"},
    {"labels": {"en": "Madrid, Spain (Vultr)", "zh": "馬德里, 西班牙 (Vultr)", "ja": "マドリード, スペイン (Vultr)"}, "host": "mad-es-ping.vultr.com", "region": "Europe"},

    # 北美
    {"labels": {"en": "Atlanta, USA (Vultr)", "zh": "亞特蘭大, 美國 (Vultr)", "ja": "アトランタ, アメリカ (Vultr)"}, "host": "ga-us-ping.vultr.com", "region": "North America"},
    {"labels": {"en": "Chicago, USA (Vultr)", "zh": "芝加哥, 美國 (Vultr)", "ja": "シカゴ, アメリカ (Vultr)"}, "host": "il-us-ping.vultr.com", "region": "North America"},
    {"labels": {"en": "Dallas, USA (Vultr)", "zh": "達拉斯, 美國 (Vultr)", "ja": "ダラス, アメリカ (Vultr)"}, "host": "tx-us-ping.vultr.com", "region": "North America"},
    {"labels": {"en": "Honolulu, USA (Vultr)", "zh": "火奴魯魯, 美國 (Vultr)", "ja": "ホノルル, アメリカ (Vultr)"}, "host": "hon-hi-us-ping.vultr.com", "region": "North America"},
    {"labels": {"en": "Los Angeles, USA (Vultr)", "zh": "洛杉磯, 美國 (Vultr)", "ja": "ロサンゼルス, アメリカ (Vultr)"}, "host": "lax-ca-us-ping.vultr.com", "region": "North America"},
    {"labels": {"en": "Miami, USA (Vultr)", "zh": "邁阿密, 美國 (Vultr)", "ja": "マイアミ, アメリカ (Vultr)"}, "host": "fl-us-ping.vultr.com", "region": "North America"},
    {"labels": {"en": "New York (NJ), USA (Vultr)", "zh": "紐約(新澤西), 美國 (Vultr)", "ja": "ニューヨーク(NJ), アメリカ (Vultr)"}, "host": "nj-us-ping.vultr.com", "region": "North America"},
    {"labels": {"en": "Seattle, USA (Vultr)", "zh": "西雅圖, 美國 (Vultr)", "ja": "シアトル, アメリカ (Vultr)"}, "host": "wa-us-ping.vultr.com", "region": "North America"},
    {"labels": {"en": "Silicon Valley, USA (Vultr)", "zh": "矽谷, 美國 (Vultr)", "ja": "シリコンバレー, アメリカ (Vultr)"}, "host": "sjo-ca-us-ping.vultr.com", "region": "North America"},
    {"labels": {"en": "Toronto, Canada (Vultr)", "zh": "多倫多, 加拿大 (Vultr)", "ja": "トロント, カナダ (Vultr)"}, "host": "tor-ca-ping.vultr.com", "region": "North America"},
    {"labels": {"en": "Mexico City, Mexico (Vultr)", "zh": "墨西哥城, 墨西哥 (Vultr)", "ja": "メキシコシティ, メキシコ (Vultr)"}, "host": "mex-mx-ping.vultr.com", "region": "North America"},

    # 南美
    {"labels": {"en": "São Paulo, Brazil (Vultr)", "zh": "聖保羅, 巴西 (Vultr)", "ja": "サンパウロ, ブラジル (Vultr)"}, "host": "sao-br-ping.vultr.com", "region": "South America"},
    {"labels": {"en": "Santiago, Chile (Vultr)", "zh": "聖地牙哥, 智利 (Vultr)", "ja": "サンティアゴ, チリ (Vultr)"}, "host": "scl-cl-ping.vultr.com", "region": "South America"},

    # 非洲
    {"labels": {"en": "Johannesburg, South Africa (Vultr)", "zh": "約翰內斯堡, 南非 (Vultr)", "ja": "ヨハネスブルグ, 南アフリカ (Vultr)"}, "host": "jnb-za-ping.vultr.com", "region": "Africa"},

    # 澳洲
    {"labels": {"en": "Melbourne, Australia (Vultr)", "zh": "墨爾本, 澳大利亞 (Vultr)", "ja": "メルボルン, オーストラリア (Vultr)"}, "host": "mel-au-ping.vultr.com", "region": "Oceania"},
    {"labels": {"en": "Sydney, Australia (Vultr)", "zh": "雪梨, 澳大利亞 (Vultr)", "ja": "シドニー, オーストラリア (Vultr)"}, "host": "syd-au-ping.vultr.com", "region": "Oceania"},
]

# 合併所有測試站點
ALL_SITES = GLOBAL_SITES + VULTR_SITES

# 多語言支持
LANGUAGES = {
    "en": {
        "title": "🌐 Simple Network Connection Test",
        "subtitle": "📍 Testing connection performance to global websites",
        "testing": "Testing",
        "score": "Score",
        "interrupted": "⏹️  Test interrupted by user",
        "completed_tests": "completed",
        "no_tests": "❌ No tests completed, exiting",
        "results_ranking": "🏆 Test Results Ranking (sorted by total latency):",
        "rank": "Rank",
        "location": "Location",
        "total_latency": "Total",
        "dns": "DNS",
        "tcp": "TCP",
        "http": "HTTP",
        "best_connection": "🥇 Best connection",
        "region_stats": "📊 Regional Statistics:",
        "avg_latency": "Average latency",
        "sites": "sites",
        "no_success": "❌ No successful test results",
        "saved_to": "💾 Results saved to",
        "available_sites": "Available test sites:",
        "no_region_found": "❌ No sites found for region",
        "dns_failed": "DNS resolution failed",
        "tcp_failed": "TCP connection failed",
        "timeout": "Connection timeout",
        "connection_error": "Connection error",
        # Region names
        "Asia": "Asia",
        "Europe": "Europe",
        "North America": "North America",
        "South America": "South America",
        "Oceania": "Oceania",
        "Africa": "Africa"
    },
    "zh": {
        "title": "🌐 簡單網路連接測試",
        "subtitle": "📍 測試全球主要網站的連接性能",
        "testing": "測試",
        "score": "評分",
        "interrupted": "⏹️  測試被使用者中斷",
        "completed_tests": "已完成",
        "no_tests": "❌ 沒有完成任何測試，程式結束",
        "results_ranking": "🏆 測試結果排行 (按總延遲排序):",
        "rank": "排名",
        "location": "地點",
        "total_latency": "總延遲",
        "dns": "DNS",
        "tcp": "TCP",
        "http": "HTTP",
        "best_connection": "🥇 最佳連接",
        "region_stats": "📊 地區統計:",
        "avg_latency": "平均延遲",
        "sites": "個站點",
        "no_success": "❌ 沒有成功的測試結果",
        "saved_to": "💾 結果已保存到",
        "available_sites": "可用的測試站點：",
        "no_region_found": "❌ 沒有找到地區",
        "dns_failed": "DNS 解析失敗",
        "tcp_failed": "TCP 連接失敗",
        "timeout": "連接超時",
        "connection_error": "連接錯誤",
        # Region names
        "Asia": "亞洲",
        "Europe": "歐洲",
        "North America": "北美洲",
        "South America": "南美洲",
        "Oceania": "大洋洲",
        "Africa": "非洲"
    },
    "ja": {
        "title": "🌐 シンプルネットワーク接続テスト",
        "subtitle": "📍 世界の主要サイトへの接続性能をテスト",
        "testing": "テスト中",
        "score": "スコア",
        "interrupted": "⏹️  ユーザーによってテストが中断されました",
        "completed_tests": "完了",
        "no_tests": "❌ テストが完了しませんでした。プログラムを終了します",
        "results_ranking": "🏆 テスト結果ランキング（総レイテンシ順）:",
        "rank": "順位",
        "location": "場所",
        "total_latency": "総遅延",
        "dns": "DNS",
        "tcp": "TCP",
        "http": "HTTP",
        "best_connection": "🥇 最良の接続",
        "region_stats": "📊 地域統計:",
        "avg_latency": "平均レイテンシ",
        "sites": "サイト",
        "no_success": "❌ 成功したテスト結果がありません",
        "saved_to": "💾 結果を保存しました",
        "available_sites": "利用可能なテストサイト：",
        "no_region_found": "❌ 地域が見つかりません",
        "dns_failed": "DNS解決に失敗",
        "tcp_failed": "TCP接続に失敗",
        "timeout": "接続タイムアウト",
        "connection_error": "接続エラー",
        # Region names
        "Asia": "アジア",
        "Europe": "ヨーロッパ",
        "North America": "北アメリカ",
        "South America": "南アメリカ",
        "Oceania": "オセアニア",
        "Africa": "アフリカ"
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """Get localized text based on language"""
    return LANGUAGES.get(lang, LANGUAGES["en"]).get(key, LANGUAGES["en"][key])

def get_localized_site_info(site: Dict, lang: str = "en") -> str:
    """Get localized site information string"""
    region_localized = get_text(site['region'], lang)
    site_label = site['labels'].get(lang, site['labels'].get('en', 'Unknown'))
    return f"{site_label} ({region_localized}) - {site['host']}"

def get_site_label(site: Dict, lang: str = "en") -> str:
    """Get localized site label"""
    return site['labels'].get(lang, site['labels'].get('en', 'Unknown'))

def test_connection_speed(host: str, timeout: float = 10.0, lang: str = "en") -> Dict:
    """測試連接速度和延遲"""
    try:
        # 1. DNS 解析時間
        dns_start = time.time()
        ip = socket.gethostbyname(host)
        dns_time = (time.time() - dns_start) * 1000

        # 2. TCP 連接時間
        tcp_start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, 80))
        tcp_time = (time.time() - tcp_start) * 1000
        sock.close()

        if result != 0:
            return {
                "success": False,
                "error": get_text("tcp_failed", lang),
                "dns_ms": dns_time,
                "tcp_ms": 0,
                "http_ms": 0,
                "total_ms": 0
            }

        # 3. HTTP 請求時間
        http_start = time.time()
        try:
            url = f"http://{host}/"
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'SimpleNetCheck/1.0')

            with urllib.request.urlopen(request, timeout=timeout) as response:
                # 只讀取前 1KB 來測試響應時間
                response.read(1024)

            http_time = (time.time() - http_start) * 1000

        except Exception:
            # HTTP 失敗時仍然返回 TCP 結果
            http_time = 0

        total_time = dns_time + tcp_time + http_time

        return {
            "success": True,
            "ip": ip,
            "dns_ms": dns_time,
            "tcp_ms": tcp_time,
            "http_ms": http_time,
            "total_ms": total_time
        }

    except KeyboardInterrupt:
        # 重新拋出 KeyboardInterrupt 讓上層處理
        raise
    except socket.gaierror:
        return {
            "success": False,
            "error": get_text("dns_failed", lang),
            "dns_ms": 0,
            "tcp_ms": 0,
            "http_ms": 0,
            "total_ms": 0
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "dns_ms": 0,
            "tcp_ms": 0,
            "http_ms": 0,
            "total_ms": 0
        }

def calculate_score(result: Dict) -> float:
    """根據延遲計算連接評分 (0-100)"""
    if not result["success"]:
        return 0

    total_ms = result["total_ms"]

    # 評分邏輯：延遲越低分數越高
    if total_ms < 50:
        return 100
    elif total_ms < 100:
        return 90
    elif total_ms < 200:
        return 80
    elif total_ms < 500:
        return 60
    elif total_ms < 1000:
        return 40
    elif total_ms < 2000:
        return 20
    else:
        return 10

def main():
    parser = argparse.ArgumentParser(description="Simple Network Connection Test")
    parser.add_argument("--region", help="Test specific region only")
    parser.add_argument("--timeout", type=float, default=10.0, help="Connection timeout")
    parser.add_argument("--output", help="Save results as JSON")
    parser.add_argument("--list", action="store_true", help="List all test sites")
    parser.add_argument("--sites", choices=["global", "vultr", "all"], default="all",
                       help="Choose test site type: global(famous websites), vultr(Vultr datacenters), all(all sites)")
    parser.add_argument("--lang", choices=["en", "zh", "ja"], default="en",
                       help="Display language: en(English), zh(Traditional Chinese), ja(Japanese)")

    args = parser.parse_args()

    # 選擇測試站點
    if args.sites == "global":
        test_sites = GLOBAL_SITES
    elif args.sites == "vultr":
        test_sites = VULTR_SITES
    else:  # all
        test_sites = ALL_SITES

    if args.list:
        print(get_text("available_sites", args.lang))
        for site in test_sites:
            print(f"  {get_localized_site_info(site, args.lang)}")
        return

    # 過濾站點
    sites_to_test = test_sites
    if args.region:
        sites_to_test = [s for s in test_sites if s['region'] == args.region]
        if not sites_to_test:
            print(f"{get_text('no_region_found', args.lang)} '{args.region}'")
            return

    print(get_text("title", args.lang))
    print(get_text("subtitle", args.lang))
    print("=" * 60)

    results = []

    try:
        for i, site in enumerate(sites_to_test, 1):
            label = get_site_label(site, args.lang)
            host = site['host']

            print(f"[{i:2}/{len(sites_to_test)}] {get_text('testing', args.lang)} {label:<20}", end="", flush=True)

            result = test_connection_speed(host, args.timeout, args.lang)
            result.update({
                "label": label,
                "host": host,
                "region": site['region'],
                "score": calculate_score(result)
            })

            results.append(result)

            if result["success"]:
                print(f" ✅ {result['total_ms']:6.1f}ms ({get_text('score', args.lang)}: {result['score']:3.0f})")
            else:
                print(f" ❌ {result['error']}")

    except KeyboardInterrupt:
        print(f"\n\n{get_text('interrupted', args.lang)} ({len(results)}/{len(sites_to_test)} {get_text('completed_tests', args.lang)})")
        if len(results) == 0:
            print(get_text('no_tests', args.lang))
            return

    # 顯示總結
    print("\n" + "=" * 60)
    print(get_text("results_ranking", args.lang))

    successful_tests = [r for r in results if r['success']]
    if successful_tests:
        successful_tests.sort(key=lambda x: x['total_ms'])

        print(f"{get_text('rank', args.lang):<4} {get_text('location', args.lang):<20} {get_text('total_latency', args.lang):<10} {get_text('dns', args.lang):<8} {get_text('tcp', args.lang):<8} {get_text('http', args.lang):<8} {get_text('score', args.lang)}")
        print("-" * 70)

        for rank, result in enumerate(successful_tests, 1):
            print(f"{rank:<4} {result['label']:<20} "
                  f"{result['total_ms']:6.1f}ms  "
                  f"{result['dns_ms']:5.1f}ms  "
                  f"{result['tcp_ms']:5.1f}ms  "
                  f"{result['http_ms']:5.1f}ms  "
                  f"{result['score']:3.0f}")

        # 顯示最佳連接
        best = successful_tests[0]
        print(f"\n{get_text('best_connection', args.lang)}: {best['label']} ({best['total_ms']:.1f}ms)")

        # 按地區統計
        print(f"\n{get_text('region_stats', args.lang)}")
        regions = {}
        for result in successful_tests:
            region = result['region']
            if region not in regions:
                regions[region] = []
            regions[region].append(result)

        for region, region_results in regions.items():
            avg_latency = sum(r['total_ms'] for r in region_results) / len(region_results)
            region_localized = get_text(region, args.lang)
            print(f"  {region_localized:<15}: {get_text('avg_latency', args.lang)} {avg_latency:6.1f}ms ({len(region_results)} {get_text('sites', args.lang)})")

    else:
        print(get_text('no_success', args.lang))

    # 保存結果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n{get_text('saved_to', args.lang)} {args.output}")

if __name__ == "__main__":
    main()