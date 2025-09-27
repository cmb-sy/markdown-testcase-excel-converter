import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional

from src.config_loader import load_config
from src.excel import ExcelWriter
from src.markdown import MarkdownTestParser, read_markdown_file


def convert_md_to_excel(
    file_path: str,
    no_auto_width: bool = False,
    test_type: str = "test",
    output_dir: Optional[Path] = None,
) -> Path:
    """
    Markdownファイルをエクセルファイルに変換する関数

    Args:
        file_path (str): 入力ファイルパス
        no_auto_width (bool): 列幅の自動調整を無効にするかどうか
        test_type (str): テストの種別（test, ut, it）
        output_dir (Optional[Path]): 出力ディレクトリ（Noneの場合はresultsディレクトリ）

    Returns:
        Path: 出力されたファイルのパス
    """
    # プロジェクトルートディレクトリを取得
    project_root = Path(__file__).parent.parent

    # 設定ファイルの読み込み
    config = load_config(project_root / "config.yaml")

    # Markdownファイルの読み込みと解析
    markdown_content = read_markdown_file(Path(file_path))
    parser = MarkdownTestParser(markdown_content, config)
    df = parser.parse()

    writer = ExcelWriter(df, config)

    # 出力先ディレクトリを決定
    if output_dir is None:
        output_dir = project_root / "results"

    # 出力ディレクトリを作成
    output_dir.mkdir(parents=True, exist_ok=True)

    # 日時付きのファイル名を生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input_file = Path(file_path)
    output_filename = f"{input_file.stem}_{timestamp}.xlsx"
    output_path = output_dir / output_filename

    # 新規ファイルを作成
    output_path = writer(
        output_path,
        merge_cells=True,
        auto_adjust_width=not no_auto_width,
        auto_adjust_height=True,
        test_type=test_type,
    )

    return Path(output_path)


def find_markdown_files(directory: Path) -> List[Path]:
    """
    指定されたディレクトリ内のすべてのMarkdownファイルを検索します。

    Args:
        directory (Path): 検索するディレクトリのパス

    Returns:
        List[Path]: 見つかったMarkdownファイルのパスのリスト
    """
    if not directory.exists():
        print(f"エラー: ディレクトリ '{directory}' が存在しません。")
        return []

    # .mdファイルを再帰的に検索
    md_files = list(directory.rglob("*.md"))

    if not md_files:
        print(f"警告: '{directory}' 内にMarkdownファイルが見つかりません。")
        return []

    print(f"見つかったMarkdownファイル: {len(md_files)}個")
    for file in md_files:
        print(f"  - {file.relative_to(directory)}")

    return md_files


def convert_files(
    md_files: List[Path],
    test_type: str = "test",
    no_auto_width: bool = False,
    output_dir: Optional[Path] = None,
) -> List[Tuple[Path, Optional[Path], bool]]:
    """
    MarkdownファイルのリストをExcelファイルに変換します。

    Args:
        md_files (List[Path]): 変換するMarkdownファイルのリスト
        test_type (str): テストの種別（test, ut, it）
        no_auto_width (bool): 列幅の自動調整を無効にするかどうか
        output_dir (Path): 出力ディレクトリ（Noneの場合は各ファイルと同じディレクトリ）

    Returns:
        List[Tuple[Path, Optional[Path], bool]]: (入力ファイル, 出力ファイル, 成功フラグ)のリスト
    """
    results: List[Tuple[Path, Optional[Path], bool]] = []

    for i, md_file in enumerate(md_files, 1):
        print(f"\n{'='*60}")
        print(f"変換中 ({i}/{len(md_files)}): {md_file.name}")
        print(f"{'='*60}")

        try:
            # 変換実行
            result_path = convert_md_to_excel(
                file_path=str(md_file),
                no_auto_width=no_auto_width,
                test_type=test_type,
                output_dir=output_dir,
            )

            results.append((md_file, result_path, True))
            print(f"✓ 変換完了: {result_path}")

        except Exception as e:
            print(f"✗ 変換エラー: {e}")
            results.append((md_file, None, False))

    return results


def print_summary(
    results: List[Tuple[Path, Optional[Path], bool]], input_dir: Path
) -> None:
    """
    変換結果のサマリーを表示します。

    Args:
        results (List[Tuple[Path, Optional[Path], bool]]): 変換結果のリスト
        input_dir (Path): 入力ディレクトリのパス
    """
    print(f"\n{'='*60}")
    print("変換結果サマリー")
    print(f"{'='*60}")

    successful = [r for r in results if r[2]]
    failed = [r for r in results if not r[2]]

    print(f"総ファイル数: {len(results)}")
    print(f"成功: {len(successful)}")
    print(f"失敗: {len(failed)}")

    if successful:
        print(f"\n✓ 変換成功したファイル:")
        for md_file, excel_file, _ in successful:
            if excel_file is not None:
                print(f"  - {md_file.relative_to(input_dir)} → {excel_file.name}")
            else:
                print(f"  - {md_file.relative_to(input_dir)} → (ファイル名不明)")

    if failed:
        print(f"\n✗ 変換失敗したファイル:")
        for md_file, _, _ in failed:
            print(f"  - {md_file.relative_to(input_dir)}")


def main() -> int:
    """
    コマンドラインツールのエントリーポイント
    """
    parser = argparse.ArgumentParser(
        description="Markdownで書かれたテスト仕様書をエクセルファイルに変換します。"
    )

    parser.add_argument(
        "--no-auto-width",
        action="store_true",
        help="列幅の自動調整を無効にする場合に指定",
    )

    # テスト種別の指定
    test_type_group = parser.add_mutually_exclusive_group()
    test_type_group.add_argument(
        "--test-type",
        type=str,
        choices=["test", "ut", "it"],
        default="test",
        help="テストの種別（test:テスト仕様書、ut:単体試験、it:結合試験）",
    )
    test_type_group.add_argument(
        "--ut",
        action="store_const",
        const="ut",
        dest="test_type",
        help="単体試験シートに出力する（--test-type utのショートカット）",
    )
    test_type_group.add_argument(
        "--it",
        action="store_const",
        const="it",
        dest="test_type",
        help="結合試験シートに出力する（--test-type itのショートカット）",
    )

    # 入力・出力ディレクトリの指定
    parser.add_argument(
        "--input-dir",
        type=str,
        default="conversion_target_data",
        help="入力ディレクトリ（デフォルト: conversion_target_data）",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="出力ディレクトリ（デフォルト: results）",
    )

    args = parser.parse_args()

    # プロジェクトルートディレクトリを取得
    project_root = Path(__file__).parent.parent

    # 一括変換実行
    input_dir = project_root / args.input_dir
    output_dir = Path(args.output_dir) if args.output_dir else project_root / "results"

    print(f"入力ディレクトリ: {input_dir}")
    if output_dir:
        print(f"出力ディレクトリ: {output_dir}")
    print(f"テスト種別: {args.test_type}")
    print(f"列幅自動調整: {not args.no_auto_width}")

    # Markdownファイルを検索
    md_files = find_markdown_files(input_dir)
    if not md_files:
        print("変換対象のファイルがありません。")
        return 1

    # ファイルを変換
    results = convert_files(
        md_files=md_files,
        test_type=args.test_type,
        no_auto_width=args.no_auto_width,
        output_dir=output_dir,
    )

    # サマリーを表示
    print_summary(results, input_dir)

    # 終了コードを返す（失敗したファイルがある場合は1）
    failed_count = len([r for r in results if not r[2]])
    return 1 if failed_count > 0 else 0


if __name__ == "__main__":
    main()
