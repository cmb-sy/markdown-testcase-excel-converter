#!/usr/bin/env python
"""
Markdownで書かれたテスト仕様書をエクセルファイルに変換します。

Usage:
    python converter.py -h
    python converter.py [-f] <file> [--template] [--no-auto-width] [--test-type <type>]
    python converter.py [-f] <file> [--ut|--it]  # 単体試験・結合試験の略称
"""

from src.converter import main

if __name__ == "__main__":
    main()
