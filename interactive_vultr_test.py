#!/usr/bin/env python3
"""
Interactive Vultr Global Speed Test
互動式 Vultr 全球機房網路速度測試工具
"""

import sys
import os
import time
import json
import datetime as dt
from typing import Dict, List, Optional, Any
from vultr_speedtest import (
    VULTR_SERVERS, HINET_SERVERS, test_single_server,
    test_multiple_servers, get_server_by_key, DEFAULT_TEST_SET
)

class InteractiveVultrTest:
    def __init__(self):
        self.region_mapping = {
            1: ("asia", "亞洲"),
            2: ("europe", "歐洲"),
            3: ("north_america", "北美"),
            4: ("south_america", "南美"),
            5: ("africa", "非洲"),
            6: ("oceania", "大洋洲")
        }

    def clear_screen(self):
        """清除螢幕"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """顯示標題"""
        print("============================================================")
        print("          🌐 全球網路速度測試工具")
        print("============================================================")

    def print_main_menu(self):
        """顯示主選單"""
        self.print_header()
        print("1. 快速測試 (推薦機房)")
        print("2. 台灣 HiNet 測速")
        print("3. 選擇地區測試")
        print("4. 選擇特定機房")
        print("5. 完整測試 (所有機房)")
        print("6. 自訂測試組合")
        print("0. 退出")
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
                    print(f"請輸入 {valid_range.start} 到 {valid_range.stop-1} 之間的數字")
                    continue
                return choice
            except (ValueError, KeyboardInterrupt):
                if not allow_empty:
                    print("請輸入有效的數字")
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
        print("\n選擇地區:")
        for num, (region_key, region_name) in self.region_mapping.items():
            server_count = len(VULTR_SERVERS.get(region_key, {}))
            print(f"{num}. {region_name} ({server_count} 個機房)")
        print("0. 返回主選單")

    def print_region_servers(self, region_key: str, region_name: str):
        """顯示地區內的機房"""
        servers = VULTR_SERVERS.get(region_key, {})
        print(f"\n{region_name} 地區機房:")

        for i, (server_key, server_info) in enumerate(servers.items(), 1):
            print(f" {i:2}. {server_info['name']} ({server_key})")
        print(" 0. 返回地區選單")
        print(f"99. 測試此地區所有機房")

    def print_all_servers(self):
        """顯示所有機房"""
        print("\n所有可用機房:")
        server_list = []

        for region_key, servers in VULTR_SERVERS.items():
            region_name = next(name for num, (key, name) in self.region_mapping.items() if key == region_key)
            print(f"\n{region_name}:")
            for server_key, server_info in servers.items():
                server_list.append((server_key, server_info['name']))
                print(f" {len(server_list):2}. {server_info['name']} ({server_key})")

        print(" 0. 返回主選單")
        print("99. 測試所有機房")
        return server_list

    def get_test_settings(self):
        """獲取測試設定"""
        print("\n測試設定:")
        print("1. 100MB")
        print("2. 1GB")

        size_choice = self.get_user_input("選擇測試檔案大小 (0-2): ", range(0, 3))
        if size_choice == 0:
            return None, None, None

        test_size = "100MB" if size_choice == 1 else "1GB"

        print("\n下載模式:")
        print("1. 完整下載 (預設，更準確)")
        print("2. 快速測試 (部分下載，較快)")

        mode_choice = self.get_user_input("選擇下載模式 (0-2): ", range(0, 3))
        if mode_choice == 0:
            return None, None, None

        quick_test = mode_choice == 2

        cooldown = self.get_float_input("測試間隔秒數 (預設 2.0): ", 2.0)

        return test_size, quick_test, cooldown

    def run_tests(self, server_keys: List[str], test_size: str, quick_test: bool, cooldown: float):
        """執行測試"""
        if len(server_keys) == 1:
            print("\n測試單一機房...")
        else:
            print(f"\n測試 {len(server_keys)} 個機房...")

        try:
            results = test_multiple_servers(server_keys, test_size, cooldown, True, quick_test)

            # 詢問是否儲存結果
            save_choice = input("\n是否儲存測試結果？ (y/N): ").strip().lower()
            if save_choice in ['y', 'yes']:
                timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"vultr_test_results_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"結果已儲存至 {filename}")

            # 顯示測試摘要
            successful_tests = [r for r in results if "download_mbps" in r]
            print(f"\n📊 測試摘要:")
            print(f"成功測試: {len(successful_tests)}/{len(results)} 個機房")

            if successful_tests:
                avg_speed = sum(r["download_mbps"] for r in successful_tests) / len(successful_tests)
                print(f"平均下載速度: {avg_speed:.1f} Mbps")

                fastest = max(successful_tests, key=lambda x: x["download_mbps"])
                print(f"最快機房: {fastest['server_name']} ({fastest['download_mbps']:.1f} Mbps)")

        except KeyboardInterrupt:
            print(f"\n\n⏹️  測試被使用者中斷")

        input("\n按 Enter 鍵繼續...")

    def quick_test(self):
        """快速測試"""
        test_size, quick_test, cooldown = self.get_test_settings()
        if test_size is None:
            return

        print(f"\n執行快速測試 (推薦機房)...")
        self.run_tests(DEFAULT_TEST_SET, test_size, quick_test, cooldown)

    def hinet_test(self):
        """台灣 HiNet 測速"""
        print("\n台灣 HiNet 測速選項:")
        print("1. 250MB 測試檔案")
        print("2. 2GB 測試檔案")
        print("3. 兩種檔案都測試")
        print("0. 返回主選單")

        choice = self.get_user_input("\n選擇測試檔案 (0-3): ", range(0, 4))
        if choice == 0:
            return

        # 設定下載模式和測試間隔
        print("\n下載模式:")
        print("1. 完整下載 (預設，更準確)")
        print("2. 快速測試 (部分下載，較快)")

        mode_choice = self.get_user_input("選擇下載模式 (0-2): ", range(0, 3))
        if mode_choice == 0:
            return

        quick_test = mode_choice == 2
        cooldown = self.get_float_input("測試間隔秒數 (預設 2.0): ", 2.0)

        # 根據選擇執行測試
        if choice == 1:
            # 250MB
            print(f"\n執行 HiNet 250MB 測速...")
            self.run_tests(["hinet_250m"], "100MB", quick_test, cooldown)
        elif choice == 2:
            # 2GB
            print(f"\n執行 HiNet 2GB 測速...")
            self.run_tests(["hinet_2g"], "1GB", quick_test, cooldown)
        elif choice == 3:
            # 兩種都測試
            print(f"\n執行 HiNet 完整測速 (250MB + 2GB)...")
            self.run_tests(["hinet_250m", "hinet_2g"], "100MB", quick_test, cooldown)

    def region_test(self):
        """地區測試"""
        while True:
            self.print_region_menu()

            choice = self.get_user_input("\n選擇地區 (0-6): ", range(0, 7))
            if choice == 0:
                return

            region_key, region_name = self.region_mapping[choice]
            servers = VULTR_SERVERS.get(region_key, {})

            while True:
                self.print_region_servers(region_key, region_name)

                server_choice = self.get_user_input(f"\n選擇機房 (0-99): ", range(0, 100))
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
                    print("無效的選擇，請重新輸入")

    def specific_server_test(self):
        """特定機房測試"""
        server_list = self.print_all_servers()

        choice = self.get_user_input(f"\n選擇機房 (0-99): ", range(0, 100))
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
            print("無效的選擇")
            input("按 Enter 鍵繼續...")

    def full_test(self):
        """完整測試"""
        print("\n⚠️  完整測試將測試所有機房，這可能需要很長時間！")
        confirm = input("確定要繼續嗎？ (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            return

        test_size, quick_test, cooldown = self.get_test_settings()
        if test_size is None:
            return

        # 收集所有機房
        all_servers = []
        for region_servers in VULTR_SERVERS.values():
            all_servers.extend(region_servers.keys())

        self.run_tests(all_servers, test_size, quick_test, cooldown)

    def custom_test(self):
        """自訂測試組合"""
        print("\n自訂測試組合:")
        print("請輸入機房代碼，用空格分隔 (例: tokyo singapore new_york)")
        print("可用的機房代碼請使用選項 3 查看")

        server_input = input("機房代碼: ").strip()
        if not server_input:
            return

        server_keys = server_input.split()

        # 驗證機房代碼
        invalid_keys = [key for key in server_keys if get_server_by_key(key) is None]
        if invalid_keys:
            print(f"無效的機房代碼: {invalid_keys}")
            input("按 Enter 鍵繼續...")
            return

        test_size, quick_test, cooldown = self.get_test_settings()
        if test_size is None:
            return

        self.run_tests(server_keys, test_size, quick_test, cooldown)

    def run(self):
        """主執行迴圈"""
        print("歡迎使用全球網路速度測試工具!")

        try:
            while True:
                self.print_main_menu()

                choice = self.get_user_input("請選擇 (0-6): ", range(0, 7))

                if choice == 0:
                    print("感謝使用！")
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
            print("\n\n程式被使用者中斷，感謝使用！")

def main():
    app = InteractiveVultrTest()
    app.run()

if __name__ == "__main__":
    main()