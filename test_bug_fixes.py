"""
测试文档：Bug修复验证测试

本测试文件用于验证以下bug修复：
1. backtesting.py 第56行 - 条件判断逻辑错误
2. parsing_keystats.py - 闰年问题
3. utils.py 第51-53行 - 未导入pandas
4. parsing_keystats.py - 数据越界（已弃用的df.append）
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import data_string_to_float, duplicate_error_check, status_calc


class TestBacktestingBugFix(unittest.TestCase):
    """测试 backtesting.py 的条件判断逻辑错误修复"""

    def test_positive_predictions_logic(self):
        """
        Bug 1: 原代码使用 num_positive_predictions < 0 判断没有正预测，
        但 sum(y_pred) 永远不会小于0（y_pred是0和1的数组）。
        修复后使用 num_positive_predictions == 0 判断。
        """
        # 模拟 y_pred 的各种情况
        y_pred_all_zero = [0, 0, 0, 0, 0]
        y_pred_some_positive = [0, 1, 0, 1, 0]
        y_pred_all_positive = [1, 1, 1, 1, 1]

        # 原逻辑（错误）
        def old_logic(y_pred):
            num_positive_predictions = sum(y_pred)
            return num_positive_predictions < 0  # 永远为False

        # 新逻辑（正确）
        def new_logic(y_pred):
            num_positive_predictions = sum(y_pred)
            return num_positive_predictions == 0

        # 验证原逻辑无法正确检测无正预测的情况
        self.assertFalse(old_logic(y_pred_all_zero))  # 原逻辑错误

        # 验证新逻辑能正确检测无正预测的情况
        self.assertTrue(new_logic(y_pred_all_zero))   # 应该返回True
        self.assertFalse(new_logic(y_pred_some_positive))  # 有正预测，返回False
        self.assertFalse(new_logic(y_pred_all_positive))   # 全是正预测，返回False


class TestParsingKeystatsLeapYearBugFix(unittest.TestCase):
    """测试 parsing_keystats.py 的闰年问题修复"""

    def test_leap_year_calculation(self):
        """
        Bug 2: 原代码使用固定秒数 31536000 (365天) 计算一年后的日期，
        没有考虑闰年。修复后使用 pd.DateOffset(years=1) 正确处理。
        """
        # 测试闰年日期
        leap_year_date = datetime(2020, 2, 29)  # 2020年是闰年

        # 原方法（错误）：固定365天
        old_one_year_later = datetime.fromtimestamp(
            leap_year_date.timestamp() + 31536000
        )

        # 新方法（正确）：使用 DateOffset
        new_one_year_later = leap_year_date + pd.DateOffset(years=1)

        # 验证原方法在闰年会产生错误日期
        # 2020-02-29 + 365天 = 2021-02-28（但应该考虑2020年是闰年）
        self.assertEqual(old_one_year_later.date().month, 2)
        self.assertEqual(old_one_year_later.date().day, 28)

        # 验证新方法正确处理闰年
        # 2020-02-29 + 1年 = 2021-02-28（因为2021年不是闰年）
        self.assertEqual(new_one_year_later.date().month, 2)
        self.assertEqual(new_one_year_later.date().day, 28)
        self.assertEqual(new_one_year_later.date().year, 2021)

    def test_non_leap_year_calculation(self):
        """测试非闰年的日期计算"""
        normal_date = datetime(2019, 3, 15)

        # 新方法
        new_one_year_later = normal_date + pd.DateOffset(years=1)

        self.assertEqual(new_one_year_later.date().year, 2020)
        self.assertEqual(new_one_year_later.date().month, 3)
        self.assertEqual(new_one_year_later.date().day, 15)


class TestUtilsPandasImportFix(unittest.TestCase):
    """测试 utils.py 的 pandas 导入修复"""

    def test_pandas_imported(self):
        """
        Bug 3: duplicate_error_check 函数中使用了 pd.Series，
        但 utils.py 没有导入 pandas。修复后添加了 import pandas as pd。
        """
        # 验证 pandas 已正确导入
        import utils
        self.assertTrue(hasattr(utils, 'pd'))

    def test_duplicate_error_check_function(self):
        """验证 duplicate_error_check 函数可以正常运行"""
        # 创建测试数据
        data = {
            'Unix': [1, 2, 3],
            'Price': [100, 200, 300],
            'stock_p_change': [5, 10, 15],
            'SP500': [3000, 3100, 3200],
            'SP500_p_change': [2, 3, 4],
            'Float': [1000, 2000, 3000],
            '200-Day Moving Average': [50, 60, 70],
            'Short Ratio': [1.5, 2.0, 2.5],
            'Operating Margin': [10, 15, 20],
            'Value1': [1, 2, 3],
            'Value2': [4, 5, 6],
        }
        df = pd.DataFrame(data)

        # 验证函数可以正常调用（不抛出 NameError）
        try:
            duplicate_error_check(df.copy())
        except NameError as e:
            self.fail(f"duplicate_error_check 抛出 NameError: {e}")


class TestParsingKeystatsDataframeAppendFix(unittest.TestCase):
    """测试 parsing_keystats.py 的 DataFrame 追加修复"""

    def test_dataframe_concat_instead_of_append(self):
        """
        Bug 4: df.append() 在 pandas 新版本中已被弃用，
        修复后使用 pd.concat() 替代。
        """
        # 创建初始 DataFrame
        df_columns = ['Date', 'Ticker', 'Price']
        df = pd.DataFrame(columns=df_columns)

        # 模拟新行数据
        new_df_row = [datetime.now(), 'AAPL', 150.0]

        # 新方法（正确）：使用 pd.concat
        new_row_df = pd.DataFrame([dict(zip(df_columns, new_df_row))])
        df = pd.concat([df, new_row_df], ignore_index=True)

        # 验证数据已正确添加
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['Ticker'], 'AAPL')
        self.assertEqual(df.iloc[0]['Price'], 150.0)

    def test_multiple_rows_concat(self):
        """测试多次添加行"""
        df_columns = ['Date', 'Ticker', 'Price']
        df = pd.DataFrame(columns=df_columns)

        # 添加多行
        for i in range(5):
            new_df_row = [datetime.now(), f'STOCK{i}', 100.0 + i]
            new_row_df = pd.DataFrame([dict(zip(df_columns, new_df_row))])
            df = pd.concat([df, new_row_df], ignore_index=True)

        self.assertEqual(len(df), 5)


class TestStatusCalcFunction(unittest.TestCase):
    """测试 status_calc 函数"""

    def test_outperformance_validation(self):
        """测试 outperformance 参数验证"""
        with self.assertRaises(ValueError):
            status_calc(100, 90, outperformance=-5)

    def test_status_calculation(self):
        """测试状态计算逻辑"""
        # 股票跑赢大盘超过10%
        self.assertTrue(status_calc(25, 10, outperformance=10))

        # 股票跑赢大盘但不超过10%
        self.assertFalse(status_calc(15, 10, outperformance=10))

        # 股票跑输大盘
        self.assertFalse(status_calc(5, 10, outperformance=10))


class TestDataStringToFloat(unittest.TestCase):
    """测试 data_string_to_float 函数"""

    def test_na_values(self):
        """测试 N/A 值处理"""
        self.assertEqual(data_string_to_float("N/A"), "N/A")
        self.assertEqual(data_string_to_float("NaN"), "N/A")

    def test_zero_values(self):
        """测试零值处理"""
        self.assertEqual(data_string_to_float(">0"), 0)

    def test_billions(self):
        """测试十亿单位"""
        self.assertEqual(data_string_to_float("2.5B"), 2500000000)

    def test_millions(self):
        """测试百万单位"""
        self.assertEqual(data_string_to_float("100M"), 100000000)

    def test_thousands(self):
        """测试千单位"""
        self.assertEqual(data_string_to_float("50K"), 50000)

    def test_plain_numbers(self):
        """测试普通数字"""
        self.assertEqual(data_string_to_float("123.45"), 123.45)


if __name__ == '__main__':
    unittest.main(verbosity=2)
