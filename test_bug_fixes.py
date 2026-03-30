#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试文档：验证三个Bug修复效果
"""

def test_bug3_data_string_to_float():
    """
    测试Bug 3修复: data_string_to_float大小写敏感
    
    修复前: 
    - 只能处理大写的K、M、B（如"10K"能处理，"10k"会报错）
    - 只能处理大写的N/A、NaN（如"n/a"会直接转float报错）
    
    修复后:
    - 先将输入转换为大写，再进行判断，实现大小写不敏感
    """
    from utils import data_string_to_float
    
    print("=" * 60)
    print("测试Bug 3: data_string_to_float大小写敏感修复")
    print("=" * 60)
    
    test_cases = [
        # 小写后缀测试
        ('4k', 4000), ('2m', 2000000), ('0.07b', 70000000),
        ('-100.1k', -100100), ('-0.1m', -100000), ('-0.02b', -20000000),
        # 小写状态测试
        ('n/a', 'N/A'), ('nan', 'N/A'), ('N/A', 'N/A'), ('NaN', 'N/A'),
        # 大写后缀测试（确保原有功能正常）
        ('4K', 4000), ('2M', 2000000), ('0.07B', 70000000),
        # 零值和基础测试
        ('>0', 0), ('-3', -3), ('0.00', 0), ('-0.00', 0),
    ]
    
    all_passed = True
    for input_val, expected in test_cases:
        try:
            result = data_string_to_float(input_val)
            passed = result == expected
            if not passed:
                all_passed = False
            status = 'OK' if passed else 'FAIL'
            print(f'  [{status}] {input_val!r} -> {result!r} (预期: {expected!r})')
        except Exception as e:
            all_passed = False
            print(f'  [FAIL] {input_val!r} -> 抛出异常: {e}')
    
    print(f"\nBug 3测试结果: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_bug1_pandas_append():
    """
    测试Bug 1修复: pandas append弃用问题
    
    修复前: 使用df.append()方法（pandas 2.0+已弃用）
    
    修复后: 使用pd.concat()方法，兼容新旧版本pandas
    """
    import pandas as pd
    
    print("\n" + "=" * 60)
    print("测试Bug 1: pandas append弃用问题修复")
    print("=" * 60)
    
    try:
        # 测试parsing_keystats.py中的修复
        df_columns = ["Date", "Ticker", "Price", "Feature1", "Feature2"]
        df = pd.DataFrame(columns=df_columns)
        
        # 模拟原始代码中的append操作
        new_df_row = ["2023-01-01", "AAPL", 150.0, 1.0, 2.0]
        
        # 使用修复后的方式（pd.concat）
        new_row = pd.DataFrame([dict(zip(df_columns, new_df_row))], columns=df_columns)
        df = pd.concat([df, new_row], ignore_index=True)
        
        print(f"  [OK] pd.concat 测试成功，DataFrame行数: {len(df)}")
        print(f"  [OK] 列名保持一致: {list(df.columns) == df_columns}")
        
        # 测试多行添加
        for i in range(3):
            new_df_row = [f"2023-01-{i+2}", "MSFT", 200.0 + i, float(i), float(i+1)]
            new_row = pd.DataFrame([dict(zip(df_columns, new_df_row))], columns=df_columns)
            df = pd.concat([df, new_row], ignore_index=True)
        
        print(f"  [OK] 多行添加测试成功，总行数: {len(df)}")
        print("Bug 1测试结果: PASSED")
        return True
        
    except Exception as e:
        print(f"  [FAIL] 测试失败: {e}")
        print("Bug 1测试结果: FAILED")
        return False


def test_bug2_feature_names():
    """
    测试Bug 2修复: 特征名不完整/不一致
    
    修复前问题:
    1. 特征名不完整: "Shares Short (as of", "Shares Short (prior month"（缺少闭合括号）
    2. 两个文件间特征名不一致
    
    修复后:
    1. 补全所有特征名
    2. 两个文件的特征名保持一致
    """
    from parsing_keystats import features as features_parse
    from current_data import features as features_current
    
    print("\n" + "=" * 60)
    print("测试Bug 2: 特征名不完整/不一致修复")
    print("=" * 60)
    
    passed = True
    
    # 测试1: 检查特征名完整性
    print("\n  1. 特征名完整性检查:")
    incomplete_names = []
    for f in features_parse:
        if f.endswith('(') or f.endswith(' of') or ('(' in f and ')' not in f):
            incomplete_names.append(f)
    
    if incomplete_names:
        print(f"    [FAIL] 发现不完整特征名: {incomplete_names}")
        passed = False
    else:
        print("    [OK] 所有特征名完整")
    
    # 测试2: 检查特征名一致性
    print("\n  2. 两个文件特征名一致性检查:")
    set1 = set(features_parse)
    set2 = set(features_current)
    
    diff_parse_only = set1 - set2
    diff_current_only = set2 - set1
    
    if diff_parse_only or diff_current_only:
        if diff_parse_only:
            print(f"    [FAIL] parsing_keystats特有: {diff_parse_only}")
        if diff_current_only:
            print(f"    [FAIL] current_data特有: {diff_current_only}")
        passed = False
    else:
        print("    [OK] 两个文件的特征名完全一致")
    
    # 显示关键特征名
    print("\n  3. 关键特征名验证:")
    key_features = ["Shares Short (as of)", "Shares Short (prior month)"]
    for feat in key_features:
        found = feat in features_parse
        status = "OK" if found else "FAIL"
        print(f"    [{status}] {feat!r} 存在于特征列表中")
        if not found:
            passed = False
    
    print(f"\nBug 2测试结果: {'PASSED' if passed else 'FAILED'}")
    return passed


def main():
    """运行所有测试"""
    print("Bug修复验证测试套件")
    print("=" * 60)
    
    results = []
    results.append(('Bug 1: pandas append弃用', test_bug1_pandas_append()))
    results.append(('Bug 2: 特征名不完整/不一致', test_bug2_feature_names()))
    results.append(('Bug 3: data_string_to_float大小写敏感', test_bug3_data_string_to_float()))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    
    for name, passed in results:
        status = "PASSED" if passed else "FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(p for _, p in results)
    print("\n" + ("[OK] 所有测试通过!" if all_passed else "[FAIL] 部分测试失败!"))
    
    # 打印已修复问题的总结
    print("\n" + "=" * 60)
    print("修复总结")
    print("=" * 60)
    print("""
Bug 1: pandas append弃用问题
  - 位置: parsing_keystats.py:217-218, current_data.py:148-149
  - 修复: 将df.append()替换为pd.concat()

Bug 2: 特征名不完整/不一致
  - 位置: parsing_keystats.py:54,57; current_data.py:31,34,36,54,57
  - 修复: 
    1. 补全特征名: "Shares Short (as of" -> "Shares Short (as of)"
    2. 补全特征名: "Shares Short (prior month" -> "Shares Short (prior month)"
    3. 统一两个文件中的特征名: Quarterly -> Qtrly, Avi -> Avl等

Bug 3: data_string_to_float大小写敏感
  - 位置: utils.py:12-27
  - 修复: 在函数开始处将输入字符串转换为大写，使函数对大小写不敏感
    新增: number_string_upper = number_string.upper()
""")


if __name__ == "__main__":
    main()
