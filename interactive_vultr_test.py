#!/usr/bin/env python3
"""
Interactive Vultr Global Speed Test
互動式 Vultr 全球機房網路速度測試工具
"""

import sys
import os
import time
import json
import argparse
import datetime as dt
from typing import Dict, List, Optional, Any
from vultr_speedtest import (
    VULTR_SERVERS, HINET_SERVERS, LINODE_SERVERS, test_single_server,
    test_multiple_servers, get_server_by_key, get_server_by_key_with_zone, DEFAULT_TEST_SET,
    get_server_name
)

# 多語言支持
LANGUAGES = {
    "en": {
        "title": "🌐 Global Network Speed Test Tool",
        "welcome": "Welcome to the Global Network Speed Test Tool!",
        "thank_you": "Thank you for using!",
        "program_interrupted": "Program interrupted by user, thank you for using!",
        "main_menu": {
            "quick_test": "1. Quick Test (Recommended servers)",
            "hinet_test": "2. Taiwan HiNet Speed Test",
            "region_test": "3. Select Region Test",
            "specific_server": "4. Select Specific Server",
            "full_test": "5. Full Test (All servers)",
            "custom_test": "6. Custom Test Combination",
            "exit": "0. Exit",
            "choose": "Please select (0-6): "
        },
        "invalid_choice": "Invalid choice, please try again",
        "invalid_number": "Please enter a valid number",
        "enter_range": "Please enter a number between",
        "press_enter": "Press Enter to continue...",
        "clear_screen": "Clear screen",
        "test_settings": "Test Settings:",
        "file_size": {
            "title": "Choose test file size (0-2): ",
            "100mb": "1. 100MB",
            "1gb": "2. 1GB"
        },
        "download_mode": {
            "title": "Download mode:",
            "full": "1. Full download (default, more accurate)",
            "quick": "2. Quick test (partial download, faster)",
            "choose": "Choose download mode (0-2): "
        },
        "test_interval": "Test interval in seconds (default 2.0): ",
        "testing_single": "Testing single server...",
        "testing_multiple": "Testing {} servers...",
        "save_results": "Save test results? (y/N): ",
        "results_saved": "Results saved to {}",
        "test_summary": "📊 Test Summary:",
        "successful_tests": "Successful tests:",
        "servers": "servers",
        "avg_download_speed": "Average download speed:",
        "fastest_server": "Fastest server:",
        "test_interrupted": "⏹️  Test interrupted by user",
        "region_menu": {
            "title": "Choose region:",
            "asia": "Asia",
            "europe": "Europe",
            "north_america": "North America",
            "south_america": "South America",
            "africa": "Africa",
            "oceania": "Oceania",
            "return": "0. Return to main menu",
            "choose": "Choose region (0-6): "
        },
        "region_servers": {
            "title": "{} Region Servers:",
            "return": "0. Return to region menu",
            "test_all": "99. Test all servers in this region",
            "choose": "Choose server (0-99): "
        },
        "all_servers": {
            "title": "All Available Servers:",
            "return": "0. Return to main menu",
            "test_all": "99. Test all servers"
        },
        "hinet_test": {
            "title": "Taiwan HiNet Speed Test Options:",
            "option_250mb": "250MB test file",
            "option_2gb": "2GB test file",
            "option_both": "Test both files",
            "choose_file": "Choose test file (0-3): ",
            "running_250mb": "Running HiNet 250MB speed test...",
            "running_2gb": "Running HiNet 2GB speed test...",
            "running_both": "Running HiNet full speed test (250MB + 2GB)..."
        },
        "common": {
            "return": "Return to main menu",
            "download_mode": "Download mode:",
            "full_download": "Full download (default, more accurate)",
            "quick_test": "Quick test (partial download, faster)",
            "choose_mode": "Choose download mode (0-2): ",
            "test_interval": "Test interval in seconds (default 2.0): ",
            "invalid_choice": "Invalid choice, please try again",
            "press_enter": "Press Enter to continue...",
            "welcome": "Welcome to the Global Network Speed Test Tool!",
            "goodbye": "Thank you for using!",
            "interrupted": "Program interrupted by user, thank you for using!"
        },
        "region_test": {
            "choose_region": "Choose region (0-6): ",
            "choose_server": "Choose server (0-99): "
        },
        "specific_server_test": {
            "choose_server": "Choose server (0-99): "
        },
        "full_test": {
            "warning": "⚠️  Full test will test all servers, this may take a very long time!",
            "confirm": "Are you sure you want to continue? (y/N): "
        },
        "custom_test": {
            "title": "Custom Test Combination:",
            "instruction": "Enter server codes separated by spaces (e.g: tokyo singapore new_york)",
            "available": "Use option 3 to see available server codes",
            "enter_codes": "Server codes: ",
            "invalid_codes": "Invalid server codes: {}"
        },
        "quick_test": {
            "running": "Running quick test (recommended servers)..."
        }
    },
    "zh": {
        "title": "🌐 全球網路速度測試工具",
        "welcome": "歡迎使用全球網路速度測試工具!",
        "thank_you": "感謝使用！",
        "program_interrupted": "程式被使用者中斷，感謝使用！",
        "main_menu": {
            "quick_test": "1. 快速測試 (推薦機房)",
            "hinet_test": "2. 台灣 HiNet 測速",
            "region_test": "3. 選擇地區測試",
            "specific_server": "4. 選擇特定機房",
            "full_test": "5. 完整測試 (所有機房)",
            "custom_test": "6. 自訂測試組合",
            "exit": "0. 退出",
            "choose": "請選擇 (0-6): "
        },
        "invalid_choice": "無效的選擇，請重新輸入",
        "invalid_number": "請輸入有效的數字",
        "enter_range": "請輸入",
        "press_enter": "按 Enter 鍵繼續...",
        "clear_screen": "清除螢幕",
        "test_settings": "測試設定:",
        "file_size": {
            "title": "選擇測試檔案大小 (0-2): ",
            "100mb": "1. 100MB",
            "1gb": "2. 1GB"
        },
        "download_mode": {
            "title": "下載模式:",
            "full": "1. 完整下載 (預設，更準確)",
            "quick": "2. 快速測試 (部分下載，較快)",
            "choose": "選擇下載模式 (0-2): "
        },
        "test_interval": "測試間隔秒數 (預設 2.0): ",
        "testing_single": "測試單一機房...",
        "testing_multiple": "測試 {} 個機房...",
        "save_results": "是否儲存測試結果？ (y/N): ",
        "results_saved": "結果已儲存至 {}",
        "test_summary": "📊 測試摘要:",
        "successful_tests": "成功測試:",
        "servers": "個機房",
        "avg_download_speed": "平均下載速度:",
        "fastest_server": "最快機房:",
        "test_interrupted": "⏹️  測試被使用者中斷",
        "region_menu": {
            "title": "選擇地區:",
            "asia": "亞洲",
            "europe": "歐洲",
            "north_america": "北美",
            "south_america": "南美",
            "africa": "非洲",
            "oceania": "大洋洲",
            "return": "0. 返回主選單",
            "choose": "選擇地區 (0-6): "
        },
        "region_servers": {
            "title": "{} 地區機房:",
            "return": "0. 返回地區選單",
            "test_all": "99. 測試此地區所有機房",
            "choose": "選擇機房 (0-99): "
        },
        "all_servers": {
            "title": "所有可用機房:",
            "return": "0. 返回主選單",
            "test_all": "99. 測試所有機房"
        },
        "hinet_test": {
            "title": "台灣 HiNet 測速選項:",
            "option_250mb": "250MB 測試檔案",
            "option_2gb": "2GB 測試檔案",
            "option_both": "兩種檔案都測試",
            "choose_file": "選擇測試檔案 (0-3): ",
            "running_250mb": "執行 HiNet 250MB 測速...",
            "running_2gb": "執行 HiNet 2GB 測速...",
            "running_both": "執行 HiNet 完整測速 (250MB + 2GB)..."
        },
        "common": {
            "return": "返回主選單",
            "download_mode": "下載模式:",
            "full_download": "完整下載 (預設，更準確)",
            "quick_test": "快速測試 (部分下載，較快)",
            "choose_mode": "選擇下載模式 (0-2): ",
            "test_interval": "測試間隔秒數 (預設 2.0): ",
            "invalid_choice": "無效的選擇，請重新輸入",
            "press_enter": "按 Enter 鍵繼續...",
            "welcome": "歡迎使用全球網路速度測試工具!",
            "goodbye": "感謝使用！",
            "interrupted": "程式被使用者中斷，感謝使用！"
        },
        "region_test": {
            "choose_region": "選擇地區 (0-6): ",
            "choose_server": "選擇機房 (0-99): "
        },
        "specific_server_test": {
            "choose_server": "選擇機房 (0-99): "
        },
        "full_test": {
            "warning": "⚠️  完整測試將測試所有機房，這可能需要很長時間！",
            "confirm": "確定要繼續嗎？ (y/N): "
        },
        "custom_test": {
            "title": "自訂測試組合:",
            "instruction": "請輸入機房代碼，用空格分隔 (例: tokyo singapore new_york)",
            "available": "可用的機房代碼請使用選項 3 查看",
            "enter_codes": "機房代碼: ",
            "invalid_codes": "無效的機房代碼: {}"
        },
        "quick_test": {
            "running": "執行快速測試 (推薦機房)..."
        }
    },
    "ja": {
        "title": "🌐 グローバルネットワーク速度テストツール",
        "welcome": "グローバルネットワーク速度テストツールへようこそ！",
        "thank_you": "ご利用ありがとうございました！",
        "program_interrupted": "ユーザーによってプログラムが中断されました。ご利用ありがとうございました！",
        "main_menu": {
            "quick_test": "1. クイックテスト（推奨サーバー）",
            "hinet_test": "2. 台湾HiNet速度テスト",
            "region_test": "3. 地域選択テスト",
            "specific_server": "4. 特定サーバー選択",
            "full_test": "5. フルテスト（全サーバー）",
            "custom_test": "6. カスタムテスト組み合わせ",
            "exit": "0. 終了",
            "choose": "選択してください (0-6): "
        },
        "invalid_choice": "無効な選択です。再入力してください",
        "invalid_number": "有効な数字を入力してください",
        "enter_range": "次の範囲の数字を入力してください",
        "press_enter": "Enterキーを押して続行...",
        "clear_screen": "画面をクリア",
        "test_settings": "テスト設定:",
        "file_size": {
            "title": "テストファイルサイズを選択 (0-2): ",
            "100mb": "1. 100MB",
            "1gb": "2. 1GB"
        },
        "download_mode": {
            "title": "ダウンロードモード:",
            "full": "1. フルダウンロード（デフォルト、より正確）",
            "quick": "2. クイックテスト（部分ダウンロード、より高速）",
            "choose": "ダウンロードモードを選択 (0-2): "
        },
        "test_interval": "テスト間隔秒数（デフォルト2.0）: ",
        "testing_single": "単一サーバーをテスト中...",
        "testing_multiple": "{}台のサーバーをテスト中...",
        "save_results": "テスト結果を保存しますか？ (y/N): ",
        "results_saved": "結果を{}に保存しました",
        "test_summary": "📊 テスト概要:",
        "successful_tests": "成功したテスト:",
        "servers": "サーバー",
        "avg_download_speed": "平均ダウンロード速度:",
        "fastest_server": "最速サーバー:",
        "test_interrupted": "⏹️  ユーザーによってテストが中断されました",
        "region_menu": {
            "title": "地域を選択:",
            "asia": "アジア",
            "europe": "ヨーロッパ",
            "north_america": "北アメリカ",
            "south_america": "南アメリカ",
            "africa": "アフリカ",
            "oceania": "オセアニア",
            "return": "0. メインメニューに戻る",
            "choose": "地域を選択 (0-6): "
        },
        "region_servers": {
            "title": "{}地域サーバー:",
            "return": "0. 地域メニューに戻る",
            "test_all": "99. この地域の全サーバーをテスト",
            "choose": "サーバーを選択 (0-99): "
        },
        "all_servers": {
            "title": "利用可能な全サーバー:",
            "return": "0. メインメニューに戻る",
            "test_all": "99. 全サーバーをテスト"
        },
        "hinet_test": {
            "title": "台湾HiNet速度テストオプション:",
            "option_250mb": "250MBテストファイル",
            "option_2gb": "2GBテストファイル",
            "option_both": "両方のファイルをテスト",
            "choose_file": "テストファイルを選択 (0-3): ",
            "running_250mb": "HiNet 250MB速度テストを実行中...",
            "running_2gb": "HiNet 2GB速度テストを実行中...",
            "running_both": "HiNet完全速度テストを実行中（250MB + 2GB）..."
        },
        "common": {
            "return": "メインメニューに戻る",
            "download_mode": "ダウンロードモード:",
            "full_download": "フルダウンロード（デフォルト、より正確）",
            "quick_test": "クイックテスト（部分ダウンロード、より高速）",
            "choose_mode": "ダウンロードモードを選択 (0-2): ",
            "test_interval": "テスト間隔秒数（デフォルト2.0）: ",
            "invalid_choice": "無効な選択です。再入力してください",
            "press_enter": "Enterキーを押して続行...",
            "welcome": "グローバルネットワーク速度テストツールへようこそ！",
            "goodbye": "ご利用ありがとうございました！",
            "interrupted": "ユーザーによってプログラムが中断されました。ご利用ありがとうございました！"
        },
        "region_test": {
            "choose_region": "地域を選択 (0-6): ",
            "choose_server": "サーバーを選択 (0-99): "
        },
        "specific_server_test": {
            "choose_server": "サーバーを選択 (0-99): "
        },
        "full_test": {
            "warning": "⚠️  フルテストは全サーバーをテストするため、非常に長時間かかる可能性があります！",
            "confirm": "続行してもよろしいですか？ (y/N): "
        },
        "custom_test": {
            "title": "カスタムテスト組み合わせ:",
            "instruction": "サーバーコードをスペース区切りで入力してください（例: tokyo singapore new_york）",
            "available": "利用可能なサーバーコードはオプション3で確認してください",
            "enter_codes": "サーバーコード: ",
            "invalid_codes": "無効なサーバーコード: {}"
        },
        "quick_test": {
            "running": "クイックテスト（推奨サーバー）を実行中..."
        }
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """Get localized text based on language"""
    keys = key.split('.')
    result = LANGUAGES.get(lang, LANGUAGES["en"])
    for k in keys:
        result = result.get(k, LANGUAGES["en"])
        if isinstance(result, str):
            break
    return result

class InteractiveVultrTest:
    def __init__(self, lang: str = "en", zone: str = None):
        self.lang = lang
        self.zone = zone
        self.region_mapping = {
            1: ("asia", get_text("region_menu.asia", lang)),
            2: ("europe", get_text("region_menu.europe", lang)),
            3: ("north_america", get_text("region_menu.north_america", lang)),
            4: ("south_america", get_text("region_menu.south_america", lang)),
            5: ("africa", get_text("region_menu.africa", lang)),
            6: ("oceania", get_text("region_menu.oceania", lang))
        }

    def get_text(self, key: str) -> str:
        """Get localized text for this instance's language"""
        return get_text(key, self.lang)

    def clear_screen(self):
        """清除螢幕"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """顯示標題"""
        print("============================================================")
        print(f"          {get_text('title', self.lang)}")
        print("============================================================")

    def print_main_menu(self):
        """顯示主選單"""
        self.print_header()
        print(get_text("main_menu.quick_test", self.lang))
        print(get_text("main_menu.hinet_test", self.lang))
        print(get_text("main_menu.region_test", self.lang))
        print(get_text("main_menu.specific_server", self.lang))
        print(get_text("main_menu.full_test", self.lang))
        print(get_text("main_menu.custom_test", self.lang))
        print(get_text("main_menu.exit", self.lang))
        print("-" * 60)

    def get_user_input(self, prompt: str, valid_range: range = None, allow_empty: bool = False) -> int:
        """獲取使用者輸入"""
        while True:
            try:
                user_input = input(prompt).strip()
                if allow_empty and user_input == "":
                    return -1

                choice = int(user_input)
                if valid_range and choice not in valid_range:
                    print(f"{get_text('enter_range', self.lang)} {valid_range.start} 到 {valid_range.stop-1}")
                    continue
                return choice
            except (ValueError, KeyboardInterrupt):
                if not allow_empty:
                    print(get_text("invalid_number", self.lang))
                    continue
                else:
                    raise KeyboardInterrupt

    def get_float_input(self, prompt: str, default: float) -> float:
        """獲取浮點數輸入"""
        try:
            user_input = input(prompt).strip()
            if user_input == "":
                return default
            return float(user_input)
        except ValueError:
            return default

    def print_region_menu(self):
        """顯示地區選單"""
        print(f"\n{get_text('region_menu.title', self.lang)}")
        for num, (region_key, region_name) in self.region_mapping.items():
            server_count = len(VULTR_SERVERS.get(region_key, {}))
            print(f"{num}. {region_name} ({server_count} {get_text('servers', self.lang)})")
        print(get_text("region_menu.return", self.lang))

    def print_region_servers(self, region_key: str, region_name: str):
        """顯示地區內的機房"""
        servers = VULTR_SERVERS.get(region_key, {})
        print(f"\n{get_text('region_servers.title', self.lang).format(region_name)}")

        for i, (server_key, server_info) in enumerate(servers.items(), 1):
            server_name = get_server_name(server_info, self.lang)
            print(f" {i:2}. {server_name} ({server_key})")
        print(f" {get_text('region_servers.return', self.lang)}")
        print(f"{get_text('region_servers.test_all', self.lang)}")

    def print_all_servers(self):
        """顯示所有機房"""
        print(f"\n{get_text('all_servers.title', self.lang)}")
        server_list = []

        # 顯示 Linode 伺服器
        print(f"\nLINODE:")
        for region_key, servers in LINODE_SERVERS.items():
            for server_key, server_info in servers.items():
                server_name = get_server_name(server_info, self.lang)
                server_list.append((server_key, server_name))
                print(f" {len(server_list):2}. {server_name} ({server_key})")

        # 顯示 Vultr 伺服器
        print(f"\nVULTR:")
        for region_key, servers in VULTR_SERVERS.items():
            region_name = next(name for num, (key, name) in self.region_mapping.items() if key == region_key)
            print(f"\n{region_name}:")
            for server_key, server_info in servers.items():
                server_name = get_server_name(server_info, self.lang)
                server_list.append((server_key, server_name))
                print(f" {len(server_list):2}. {server_name} ({server_key})")

        print(f" {get_text('all_servers.return', self.lang)}")
        print(f"{get_text('all_servers.test_all', self.lang)}")
        return server_list

    def get_test_settings(self):
        """獲取測試設定"""
        print(f"\n{get_text('test_settings', self.lang)}")
        print(get_text("file_size.100mb", self.lang))
        print(get_text("file_size.1gb", self.lang))

        size_choice = self.get_user_input(get_text("file_size.title", self.lang), range(0, 3))
        if size_choice == 0:
            return None, None, None

        test_size = "100MB" if size_choice == 1 else "1GB"

        print(f"\n{get_text('download_mode.title', self.lang)}")
        print(get_text("download_mode.full", self.lang))
        print(get_text("download_mode.quick", self.lang))

        mode_choice = self.get_user_input(get_text("download_mode.choose", self.lang), range(0, 3))
        if mode_choice == 0:
            return None, None, None

        quick_test = mode_choice == 2

        cooldown = self.get_float_input(get_text("test_interval", self.lang), 2.0)

        return test_size, quick_test, cooldown

    def run_tests(self, server_keys: List[str], test_size: str, quick_test: bool, cooldown: float):
        """執行測試"""
        if len(server_keys) == 1:
            print(f"\n{get_text('testing_single', self.lang)}")
        else:
            print(f"\n{get_text('testing_multiple', self.lang).format(len(server_keys))}")

        try:
            results = test_multiple_servers(server_keys, test_size, cooldown, True, quick_test, self.lang, self.zone)

            # 詢問是否儲存結果
            save_choice = input(f"\n{get_text('save_results', self.lang)}").strip().lower()
            if save_choice in ['y', 'yes']:
                timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"vultr_test_results_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(get_text('results_saved', self.lang).format(filename))

            # 顯示測試摘要
            successful_tests = [r for r in results if "download_mbps" in r]
            print(f"\n{get_text('test_summary', self.lang)}")
            print(f"{get_text('successful_tests', self.lang)} {len(successful_tests)}/{len(results)} {get_text('servers', self.lang)}")

            if successful_tests:
                avg_speed = sum(r["download_mbps"] for r in successful_tests) / len(successful_tests)
                print(f"{get_text('avg_download_speed', self.lang)} {avg_speed:.1f} Mbps")

                fastest = max(successful_tests, key=lambda x: x["download_mbps"])
                print(f"{get_text('fastest_server', self.lang)} {fastest['server_name']} ({fastest['download_mbps']:.1f} Mbps)")

        except KeyboardInterrupt:
            print(f"\n\n{get_text('test_interrupted', self.lang)}")

        input(f"\n{get_text('press_enter', self.lang)}")

    def quick_test(self):
        """快速測試"""
        test_size, quick_test, cooldown = self.get_test_settings()
        if test_size is None:
            return

        print(f"\n{self.get_text('quick_test.running')}")
        self.run_tests(DEFAULT_TEST_SET, test_size, quick_test, cooldown)

    def hinet_test(self):
        """台灣 HiNet 測速"""
        print(f"\n{self.get_text('hinet_test.title')}")
        print(f"1. {self.get_text('hinet_test.option_250mb')}")
        print(f"2. {self.get_text('hinet_test.option_2gb')}")
        print(f"3. {self.get_text('hinet_test.option_both')}")
        print(f"0. {self.get_text('common.return')}")

        choice = self.get_user_input(f"\n{self.get_text('hinet_test.choose_file')}", range(0, 4))
        if choice == 0:
            return

        # 設定下載模式和測試間隔
        print(f"\n{self.get_text('common.download_mode')}")
        print(f"1. {self.get_text('common.full_download')}")
        print(f"2. {self.get_text('common.quick_test')}")

        mode_choice = self.get_user_input(f"{self.get_text('common.choose_mode')}", range(0, 3))
        if mode_choice == 0:
            return

        quick_test = mode_choice == 2
        cooldown = self.get_float_input(f"{self.get_text('common.test_interval')}", 2.0)

        # 根據選擇執行測試
        if choice == 1:
            # 250MB
            print(f"\n{self.get_text('hinet_test.running_250mb')}")
            self.run_tests(["hinet_250m"], "100MB", quick_test, cooldown)
        elif choice == 2:
            # 2GB
            print(f"\n{self.get_text('hinet_test.running_2gb')}")
            self.run_tests(["hinet_2g"], "1GB", quick_test, cooldown)
        elif choice == 3:
            # 兩種都測試
            print(f"\n{self.get_text('hinet_test.running_both')}")
            self.run_tests(["hinet_250m", "hinet_2g"], "100MB", quick_test, cooldown)

    def region_test(self):
        """地區測試"""
        while True:
            self.print_region_menu()

            choice = self.get_user_input(f"\n{self.get_text('region_test.choose_region')}", range(0, 7))
            if choice == 0:
                return

            region_key, region_name = self.region_mapping[choice]
            servers = VULTR_SERVERS.get(region_key, {})

            while True:
                self.print_region_servers(region_key, region_name)

                server_choice = self.get_user_input(f"\n{self.get_text('region_test.choose_server')}", range(0, 100))
                if server_choice == 0:
                    break
                elif server_choice == 99:
                    # 測試整個地區
                    test_size, quick_test, cooldown = self.get_test_settings()
                    if test_size is None:
                        continue
                    server_keys = list(servers.keys())
                    self.run_tests(server_keys, test_size, quick_test, cooldown)
                    break
                elif 1 <= server_choice <= len(servers):
                    # 測試單一機房
                    test_size, quick_test, cooldown = self.get_test_settings()
                    if test_size is None:
                        continue
                    server_key = list(servers.keys())[server_choice - 1]
                    self.run_tests([server_key], test_size, quick_test, cooldown)
                    break
                else:
                    print(f"{self.get_text('common.invalid_choice')}")

    def specific_server_test(self):
        """特定機房測試"""
        server_list = self.print_all_servers()

        choice = self.get_user_input(f"\n{self.get_text('specific_server_test.choose_server')}", range(0, 100))
        if choice == 0:
            return
        elif choice == 99:
            # 測試所有機房
            test_size, quick_test, cooldown = self.get_test_settings()
            if test_size is None:
                return
            server_keys = [item[0] for item in server_list]
            self.run_tests(server_keys, test_size, quick_test, cooldown)
        elif 1 <= choice <= len(server_list):
            # 測試特定機房
            test_size, quick_test, cooldown = self.get_test_settings()
            if test_size is None:
                return
            server_key = server_list[choice - 1][0]
            self.run_tests([server_key], test_size, quick_test, cooldown)
        else:
            print(f"{self.get_text('common.invalid_choice')}")
            input(f"{self.get_text('common.press_enter')}")

    def full_test(self):
        """完整測試"""
        print(f"\n⚠️  {self.get_text('full_test.warning')}")
        confirm = input(f"{self.get_text('full_test.confirm')}").strip().lower()
        if confirm not in ['y', 'yes']:
            return

        test_size, quick_test, cooldown = self.get_test_settings()
        if test_size is None:
            return

        # 收集所有機房
        all_servers = []
        # 添加 Linode 伺服器
        for region_servers in LINODE_SERVERS.values():
            all_servers.extend(region_servers.keys())
        # 添加 Vultr 伺服器
        for region_servers in VULTR_SERVERS.values():
            all_servers.extend(region_servers.keys())

        self.run_tests(all_servers, test_size, quick_test, cooldown)

    def custom_test(self):
        """自訂測試組合"""
        print(f"\n{self.get_text('custom_test.title')}")
        print(f"{self.get_text('custom_test.instruction')}")
        print(f"{self.get_text('custom_test.view_codes')}")

        server_input = input(f"{self.get_text('custom_test.enter_codes')}").strip()
        if not server_input:
            return

        server_keys = server_input.split()

        # 驗證機房代碼
        invalid_keys = [key for key in server_keys if get_server_by_key_with_zone(key, self.zone) is None]
        if invalid_keys:
            print(f"{self.get_text('custom_test.invalid_codes')}{invalid_keys}")
            input(f"{self.get_text('common.press_enter')}")
            return

        test_size, quick_test, cooldown = self.get_test_settings()
        if test_size is None:
            return

        self.run_tests(server_keys, test_size, quick_test, cooldown)

    def run(self):
        """主執行迴圈"""
        print(f"{self.get_text('common.welcome')}")

        try:
            while True:
                self.print_main_menu()

                choice = self.get_user_input(f"{self.get_text('main_menu.choose')}", range(0, 7))

                if choice == 0:
                    print(f"{self.get_text('common.goodbye')}")
                    break
                elif choice == 1:
                    self.quick_test()
                elif choice == 2:
                    self.hinet_test()
                elif choice == 3:
                    self.region_test()
                elif choice == 4:
                    self.specific_server_test()
                elif choice == 5:
                    self.full_test()
                elif choice == 6:
                    self.custom_test()

        except KeyboardInterrupt:
            print(f"\n\n{self.get_text('common.interrupted')}")

def main():
    parser = argparse.ArgumentParser(description='Interactive Vultr Speed Test Tool')
    parser.add_argument('--lang', choices=['en', 'zh', 'ja'], default='en',
                        help='Language for display (default: en)')
    parser.add_argument('--zone', choices=['vultr', 'linode', 'hinet'],
                       help='Specify provider zone (vultr/linode/hinet). When server key conflicts, this determines which provider to use.')
    args = parser.parse_args()

    app = InteractiveVultrTest(lang=args.lang, zone=args.zone)
    app.run()

if __name__ == "__main__":
    main()