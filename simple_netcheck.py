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
    {"label": "台北, 台灣", "host": "www.gov.tw", "region": "Asia"},
    {"label": "東京, 日本", "host": "www.yahoo.co.jp", "region": "Asia"},
    {"label": "首爾, 南韓", "host": "www.naver.com", "region": "Asia"},
    {"label": "新加坡, 新加坡", "host": "www.straitstimes.com", "region": "Asia"},
    {"label": "香港, 中國", "host": "www.scmp.com", "region": "Asia"},
    {"label": "吉隆坡, 馬來西亞", "host": "www.thestar.com.my", "region": "Asia"},
    {"label": "雪梨, 澳大利亞", "host": "www.abc.net.au", "region": "Oceania"},
    {"label": "倫敦, 英國", "host": "www.bbc.com", "region": "Europe"},
    {"label": "法蘭克福, 德國", "host": "www.spiegel.de", "region": "Europe"},
    {"label": "紐約, 美國", "host": "www.nytimes.com", "region": "North America"},
    {"label": "洛杉磯, 美國", "host": "www.latimes.com", "region": "North America"},
]

# Vultr 全球機房測試站點
VULTR_SITES = [
    # 亞洲
    {"label": "東京, 日本 (Vultr)", "host": "hnd-jp-ping.vultr.com", "region": "Asia"},
    {"label": "大阪, 日本 (Vultr)", "host": "osk-jp-ping.vultr.com", "region": "Asia"},
    {"label": "首爾, 韓國 (Vultr)", "host": "sel-kor-ping.vultr.com", "region": "Asia"},
    {"label": "新加坡 (Vultr)", "host": "sgp-ping.vultr.com", "region": "Asia"},
    {"label": "班加羅爾, 印度 (Vultr)", "host": "blr-in-ping.vultr.com", "region": "Asia"},
    {"label": "德里NCR, 印度 (Vultr)", "host": "del-in-ping.vultr.com", "region": "Asia"},
    {"label": "孟買, 印度 (Vultr)", "host": "bom-in-ping.vultr.com", "region": "Asia"},
    {"label": "特拉維夫, 以色列 (Vultr)", "host": "tlv-il-ping.vultr.com", "region": "Asia"},

    # 歐洲
    {"label": "倫敦, 英國 (Vultr)", "host": "lon-gb-ping.vultr.com", "region": "Europe"},
    {"label": "曼徹斯特, 英國 (Vultr)", "host": "man-uk-ping.vultr.com", "region": "Europe"},
    {"label": "法蘭克福, 德國 (Vultr)", "host": "fra-de-ping.vultr.com", "region": "Europe"},
    {"label": "巴黎, 法國 (Vultr)", "host": "par-fr-ping.vultr.com", "region": "Europe"},
    {"label": "阿姆斯特丹, 荷蘭 (Vultr)", "host": "ams-nl-ping.vultr.com", "region": "Europe"},
    {"label": "華沙, 波蘭 (Vultr)", "host": "waw-pl-ping.vultr.com", "region": "Europe"},
    {"label": "斯德哥爾摩, 瑞典 (Vultr)", "host": "sto-se-ping.vultr.com", "region": "Europe"},
    {"label": "馬德里, 西班牙 (Vultr)", "host": "mad-es-ping.vultr.com", "region": "Europe"},

    # 北美
    {"label": "亞特蘭大, 美國 (Vultr)", "host": "ga-us-ping.vultr.com", "region": "North America"},
    {"label": "芝加哥, 美國 (Vultr)", "host": "il-us-ping.vultr.com", "region": "North America"},
    {"label": "達拉斯, 美國 (Vultr)", "host": "tx-us-ping.vultr.com", "region": "North America"},
    {"label": "火奴魯魯, 美國 (Vultr)", "host": "hon-hi-us-ping.vultr.com", "region": "North America"},
    {"label": "洛杉磯, 美國 (Vultr)", "host": "lax-ca-us-ping.vultr.com", "region": "North America"},
    {"label": "邁阿密, 美國 (Vultr)", "host": "fl-us-ping.vultr.com", "region": "North America"},
    {"label": "紐約(新澤西), 美國 (Vultr)", "host": "nj-us-ping.vultr.com", "region": "North America"},
    {"label": "西雅圖, 美國 (Vultr)", "host": "wa-us-ping.vultr.com", "region": "North America"},
    {"label": "矽谷, 美國 (Vultr)", "host": "sjo-ca-us-ping.vultr.com", "region": "North America"},
    {"label": "多倫多, 加拿大 (Vultr)", "host": "tor-ca-ping.vultr.com", "region": "North America"},
    {"label": "墨西哥城, 墨西哥 (Vultr)", "host": "mex-mx-ping.vultr.com", "region": "North America"},

    # 南美
    {"label": "聖保羅, 巴西 (Vultr)", "host": "sao-br-ping.vultr.com", "region": "South America"},
    {"label": "聖地牙哥, 智利 (Vultr)", "host": "scl-cl-ping.vultr.com", "region": "South America"},

    # 非洲
    {"label": "約翰內斯堡, 南非 (Vultr)", "host": "jnb-za-ping.vultr.com", "region": "Africa"},

    # 澳洲
    {"label": "墨爾本, 澳大利亞 (Vultr)", "host": "mel-au-ping.vultr.com", "region": "Oceania"},
    {"label": "雪梨, 澳大利亞 (Vultr)", "host": "syd-au-ping.vultr.com", "region": "Oceania"},
]

# 合併所有測試站點
ALL_SITES = GLOBAL_SITES + VULTR_SITES

def test_connection_speed(host: str, timeout: float = 10.0) -> Dict:
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
                "error": "TCP 連接失敗",
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
            "error": "DNS 解析失敗",
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
    parser = argparse.ArgumentParser(description="簡單網路連接測試")
    parser.add_argument("--region", help="只測試特定地區")
    parser.add_argument("--timeout", type=float, default=10.0, help="連接超時時間")
    parser.add_argument("--output", help="保存結果為 JSON")
    parser.add_argument("--list", action="store_true", help="列出所有測試站點")
    parser.add_argument("--sites", choices=["global", "vultr", "all"], default="all",
                       help="選擇測試站點類型: global(知名網站), vultr(Vultr機房), all(全部)")

    args = parser.parse_args()

    # 選擇測試站點
    if args.sites == "global":
        test_sites = GLOBAL_SITES
    elif args.sites == "vultr":
        test_sites = VULTR_SITES
    else:  # all
        test_sites = ALL_SITES

    if args.list:
        print("可用的測試站點：")
        for site in test_sites:
            print(f"  {site['label']} ({site['region']}) - {site['host']}")
        return

    # 過濾站點
    sites_to_test = test_sites
    if args.region:
        sites_to_test = [s for s in test_sites if s['region'] == args.region]
        if not sites_to_test:
            print(f"❌ 沒有找到地區 '{args.region}' 的站點")
            return

    print("🌐 簡單網路連接測試")
    print("📍 測試全球主要網站的連接性能")
    print("=" * 60)

    results = []

    try:
        for i, site in enumerate(sites_to_test, 1):
            label = site['label']
            host = site['host']

            print(f"[{i:2}/{len(sites_to_test)}] 測試 {label:<20}", end="", flush=True)

            result = test_connection_speed(host, args.timeout)
            result.update({
                "label": label,
                "host": host,
                "region": site['region'],
                "score": calculate_score(result)
            })

            results.append(result)

            if result["success"]:
                print(f" ✅ {result['total_ms']:6.1f}ms (評分: {result['score']:3.0f})")
            else:
                print(f" ❌ {result['error']}")

    except KeyboardInterrupt:
        print(f"\n\n⏹️  測試被使用者中斷 (已完成 {len(results)}/{len(sites_to_test)} 個測試)")
        if len(results) == 0:
            print("❌ 沒有完成任何測試，程式結束")
            return

    # 顯示總結
    print("\n" + "=" * 60)
    print("🏆 測試結果排行 (按總延遲排序):")

    successful_tests = [r for r in results if r['success']]
    if successful_tests:
        successful_tests.sort(key=lambda x: x['total_ms'])

        print(f"{'排名':<4} {'地點':<20} {'總延遲':<10} {'DNS':<8} {'TCP':<8} {'HTTP':<8} {'評分'}")
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
        print(f"\n🥇 最佳連接: {best['label']} ({best['total_ms']:.1f}ms)")

        # 按地區統計
        print(f"\n📊 地區統計:")
        regions = {}
        for result in successful_tests:
            region = result['region']
            if region not in regions:
                regions[region] = []
            regions[region].append(result)

        for region, region_results in regions.items():
            avg_latency = sum(r['total_ms'] for r in region_results) / len(region_results)
            print(f"  {region:<15}: 平均延遲 {avg_latency:6.1f}ms ({len(region_results)} 個站點)")

    else:
        print("❌ 沒有成功的測試結果")

    # 保存結果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 結果已保存到 {args.output}")

if __name__ == "__main__":
    main()