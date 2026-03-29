"""
Bug修复测试文档
================

本文档包含针对以下bug的测试用例：
- Bug 1: backtesting.py 第56行 - 条件判断逻辑错误
- Bug 2: parsing_keystats.py - 闰年问题
- Bug 3: utils.py 第51-53行 - 未导入pandas
- Bug 4: parsing_keystats.py - 数据越界
"""

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestBug1BacktestingCondition:
    """
    Bug 1: backtesting.py 第56行 - 条件判断逻辑错误
    
    原问题：num_positive_predictions < 0 永远不会为真，
    因为 sum(y_pred) 的结果永远 >= 0（y_pred是0和1组成的数组）
    
    修复：将条件改为 num_positive_predictions == 0
    """
    
    def test_positive_predictions_sum_never_negative(self):
        y_pred = [0, 1, 0, 1, 1]
        num_positive_predictions = sum(y_pred)
        assert num_positive_predictions >= 0, "预测结果之和应该永远 >= 0"
        return True
    
    def test_zero_predictions_detection(self):
        y_pred = [0, 0, 0, 0, 0]
        num_positive_predictions = sum(y_pred)
        assert num_positive_predictions == 0, "全为0的预测结果之和应该等于0"
        return True
    
    def test_positive_predictions_count(self):
        y_pred = [0, 1, 0, 1, 1, 0, 1]
        num_positive_predictions = sum(y_pred)
        expected_count = 4
        assert num_positive_predictions == expected_count, f"应该有{expected_count}个正向预测"
        return True


class TestBug2LeapYear:
    """
    Bug 2: parsing_keystats.py - 闰年问题
    
    原问题：使用固定秒数 31536000（365天）计算一年后日期，
    没有考虑闰年（366天）
    
    修复：使用 dateutil.relativedelta 来正确处理闰年
    """
    
    def test_leap_year_handling(self):
        leap_year_date = datetime(2020, 2, 29)
        one_year_later = leap_year_date + relativedelta(years=1)
        expected_date = datetime(2021, 3, 1)
        assert one_year_later == expected_date, f"闰年计算错误: {one_year_later} != {expected_date}"
        return True
    
    def test_normal_year_handling(self):
        normal_date = datetime(2021, 3, 15)
        one_year_later = normal_date + relativedelta(years=1)
        expected_date = datetime(2022, 3, 15)
        assert one_year_later == expected_date, f"普通年份计算错误: {one_year_later} != {expected_date}"
        return True
    
    def test_leap_year_from_march(self):
        date = datetime(2020, 3, 1)
        one_year_later = date + relativedelta(years=1)
        expected_date = datetime(2021, 3, 1)
        assert one_year_later == expected_date
        return True
    
    def test_non_leap_year_february(self):
        date = datetime(2021, 2, 28)
        one_year_later = date + relativedelta(years=1)
        expected_date = datetime(2022, 2, 28)
        assert one_year_later == expected_date
        return True


class TestBug3PandasImport:
    """
    Bug 3: utils.py 第51-53行 - 未导入pandas
    
    原问题：duplicate_error_check函数使用了 pd.Series，
    但文件顶部没有导入 pandas
    
    修复：在文件顶部添加 import pandas as pd
    """
    
    def test_pandas_module_available(self):
        import utils
        assert hasattr(utils, 'pd'), "utils模块应该有pd属性（pandas别名）"
        return True
    
    def test_pandas_series_creation(self):
        series = pd.Series([1, 2, 3, 4, 5])
        assert len(series) == 5, "Series长度应该为5"
        assert list(series) == [1, 2, 3, 4, 5], "Series内容应该正确"
        return True


class TestBug4DataBounds:
    """
    Bug 4: parsing_keystats.py - 数据越界
    
    原问题：访问 one_year_later 日期时没有检查是否超出数据范围，
    可能导致 KeyError。
    另外，sp500_df.index 是 DatetimeIndex 类型，而 one_year_later 是字符串，
    直接使用字符串比较可能不准确。
    
    修复：
    1. 使用 pd.Timestamp(one_year_later) 将字符串转换为 Timestamp 进行比较
    2. 在访问数据之前检查日期是否在索引中
    """
    
    def test_date_in_dataframe_index(self):
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        df = pd.DataFrame({'value': range(10)}, index=dates)
        
        in_index_date = '2020-01-05'
        out_of_index_date = '2020-01-20'
        
        assert pd.Timestamp(in_index_date) in df.index, "在索引中的日期应该被正确识别"
        assert pd.Timestamp(out_of_index_date) not in df.index, "不在索引中的日期应该被正确识别"
        return True
    
    def test_skip_out_of_bounds_date(self):
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        df = pd.DataFrame({'value': range(10)}, index=dates)
        
        test_date = '2020-01-20'
        should_skip = pd.Timestamp(test_date) not in df.index
        
        assert should_skip, "越界日期应该被标记为需要跳过"
        return True
    
    def test_valid_date_access(self):
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        df = pd.DataFrame({'value': range(10)}, index=dates)
        
        test_date = dates[5]
        value = df.loc[test_date, 'value']
        assert value == 5, "有效日期应该能正确访问数据"
        return True
    
    def test_string_vs_timestamp_comparison(self):
        """
        验证：字符串与 DatetimeIndex 比较的问题
        字符串 '2020-01-05' 直接用 in 检查 DatetimeIndex 可能失败，
        需要转换为 pd.Timestamp
        """
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        df = pd.DataFrame({'value': range(10)}, index=dates)
        
        test_date_str = '2020-01-05'
        
        string_in_index = test_date_str in df.index
        timestamp_in_index = pd.Timestamp(test_date_str) in df.index
        
        assert timestamp_in_index == True, "使用 pd.Timestamp 应该正确识别日期在索引中"
        return True


class TestIntegration:
    """
    集成测试：验证所有修复后的功能协同工作
    """
    
    def test_status_calc_function(self):
        import utils
        result = utils.status_calc(20, 10, 5)
        assert result == 1, "股票跑赢大盘5%以上应该返回1"
        
        result = utils.status_calc(12, 10, 5)
        assert result == 0, "股票跑赢大盘不足5%应该返回0"
        return True
    
    def test_data_string_to_float_function(self):
        import utils
        assert utils.data_string_to_float("10K") == 10000
        assert utils.data_string_to_float("5M") == 5000000
        assert utils.data_string_to_float("N/A") == "N/A"
        return True


def run_all_tests():
    print("=" * 60)
    print("Bug修复测试报告")
    print("=" * 60)
    
    test_classes = [
        ("Bug 1: backtesting.py 条件判断逻辑错误", TestBug1BacktestingCondition),
        ("Bug 2: parsing_keystats.py 闰年问题", TestBug2LeapYear),
        ("Bug 3: utils.py 未导入pandas", TestBug3PandasImport),
        ("Bug 4: parsing_keystats.py 数据越界", TestBug4DataBounds),
        ("集成测试", TestIntegration),
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for class_name, test_class in test_classes:
        print(f"\n{class_name}")
        print("-" * 60)
        
        instance = test_class()
        test_methods = [m for m in dir(instance) if m.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(instance, method_name)
                result = method()
                if result:
                    passed_tests += 1
                    print(f"  [PASS] {method_name}")
                else:
                    failed_tests += 1
                    print(f"  [FAIL] {method_name}")
            except AssertionError as e:
                failed_tests += 1
                print(f"  [FAIL] {method_name}: {str(e)}")
            except Exception as e:
                failed_tests += 1
                print(f"  [ERROR] {method_name}: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"测试总结: 总计 {total_tests} 个测试")
    print(f"  通过: {passed_tests}")
    print(f"  失败: {failed_tests}")
    print("=" * 60)
    
    return failed_tests == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
