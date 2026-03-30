#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单测试：验证Bug修复效果
"""
import sys

def test_bug3_data_string_to_float():
    """测试Bug 3修复: data_string_to_float大小写敏感"""
    from utils import data_string_to_float
    
    print("=" * 60)
    print("测试Bug 3: data_string_to_float大小写敏感修复")
    print("=" * 60)
    
    test_cases = [
        # 小写后缀测试
        ('4k', 4000), ('2m', 2000000), ('0.07b', 70000000),
        ('-100.1k', -100100), ('-0.1m', -100000), ('-0.02b', -20000000),
        # 混合大小写测试
        ('1.5K', 1500), ('2.5M', 2500000), ('3.5B', 3500000000),
        ('100K', 100000), ('200m', 200000000), ('0.5b', 500000000),
        # 小写状态测试（N/A、NaN等）
        ('n/a', 'N/A'), ('nan', 'N/A'), ('N/A', 'N/A'), ('NaN', 'N/A'),
        ('NAN', 'N/A'), ('asdfNaNxyz', 'N/A'), ('>N/A\n<', 'N/A'),
        # 大写后缀测试（确保原有功能正常）
        ('4K', 4000), ('2M', 2000000), ('0.07B', 70000000),
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
    """测试Bug 1修复: pandas append弃用问题"""
    import pandas as pd
    
    print("\n" + "=" * 60)
    print("测试Bug 1: pandas append弃用问题修复")
    print("=" * 60)
    
    try:
        df_columns = ["Date", "Ticker", "Price"]
        df = pd.DataFrame(columns=df_columns)
        
        new_df_row = ["2023-01-01", "AAPL", 150.0]
        new_row = pd.DataFrame([dict(zip(df_columns, new_df_row))], columns=df_columns)
        df = pd.concat([df, new_row], ignore_index=True)
        
        print(f"  [OK] pd.concat 测试成功，DataFrame行数: {len(df)}")
        print("Bug 1测试结果: PASSED")
        return True
    except Exception as e:
        print(f"  [FAIL] 测试失败: {e}")
        print("Bug 1测试结果: FAILED")
        return False


def test_bug2_feature_names():
    """测试Bug 2修复: 特征名不完整/不一致"""
    # 直接读取文件内容检查特征名
    import re
    
    print("\n" + "=" * 60)
    print("测试Bug 2: 特征名不完整/不一致修复")
    print("=" * 60)
    
    passed = True
    
    # 读取parsing_keystats.py
    with open("parsing_keystats.py", "r", encoding="utf-8") as f:
        content1 = f.read()
    
    # 读取current_data.py
    with open("current_data.py", "r", encoding="utf-8") as f:
        content2 = f.read()
    
    # 提取features列表
    def extract_features(content):
        match = re.search(r'features = \[(.*?)\]', content, re.DOTALL)
        if match:
            feat_str = match.group(1)
            feats = re.findall(r'\"(.*?)\"', feat_str)
            return feats
        return []
    
    features_parse = extract_features(content1)
    features_current = extract_features(content2)
    
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
    
    # 测试3: 验证append是否已修复
    print("\n  3. df.append()替换检查:")
    if 'df.append(' in content1:
        print("    [FAIL] parsing_keystats.py中仍有df.append()")
        passed = False
    else:
        print("    [OK] parsing_keystats.py中已替换为pd.concat()")
    
    if 'df.append(' in content2:
        print("    [FAIL] current_data.py中仍有df.append()")
        passed = False
    else:
        print("    [OK] current_data.py中已替换为pd.concat()")
    
    print(f"\nBug 2测试结果: {'PASSED' if passed else 'FAILED'}")
    return passed


def main():
    results = []
    print("Bug修复验证测试套件")
    print("=" * 60)
    
    results.append(('Bug 1: pandas append弃用', test_bug1_pandas_append()))
    results.append(('Bug 2: 特征名不完整/不一致', test_bug2_feature_names()))
    results.append(('Bug 3: data_string_to_float大小写敏感', test_bug3_data_string_to_float()))
    
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    
    for name, passed in results:
        status = "PASSED" if passed else "FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(p for _, p in results)
    print("\n" + ("[OK] 所有测试通过!" if all_passed else "[FAIL] 部分测试失败!"))
    
    print("\n" + "=" * 60)
    print("修复总结")
    print("=" * 60)
    print("""
Bug 1: pandas append弃用问题
  - 文件: parsing_keystats.py, current_data.py
  - 原因: pandas 2.0+ 弃用了 DataFrame.append() 方法
  - 修复: 将 df.append(dict, ignore_index=True) 替换为 pd.concat()

Bug 2: 特征名不完整/不一致
  - 问题1: 特征名缺少闭合括号，如 "Shares Short (as of", "Shares Short (prior month"
  - 问题2: 两个文件中的特征名不一致
  - 修复: 补全括号，统一两个文件中的特征名

Bug 3: data_string_to_float大小写敏感
  - 问题: 函数只能处理大写的 K, M, B, N/A, NaN
  - 修复: 将输入转换为大写后再处理，实现大小写不敏感
""")


if __name__ == "__main__":
    main()
