# Bug修复文档

本文档记录了项目中发现的Bug及其修复方案。

## Bug 1: parsing_keystats.py - pandas append弃用

### 问题描述
`pandas.DataFrame.append()` 方法在新版本的pandas中已被弃用，并将在未来版本中移除。使用该方法会导致`FutureWarning`或`DeprecationWarning`。

### 修复方案
将 `df.append()` 替换为使用列表收集行数据，最后通过 `pd.DataFrame()` 创建DataFrame的方式。

### 代码变更
**文件**: `parsing_keystats.py`

```python
# 修复前
df = pd.DataFrame(columns=df_columns)
...
df = df.append(dict(zip(df_columns, new_df_row)), ignore_index=True)

# 修复后
df_rows = []
...
df_rows.append(dict(zip(df_columns, new_df_row)))
...
df = pd.DataFrame(df_rows, columns=df_columns)
```

### 测试用例
测试文件: `tests/test_datasets.py`
- `test_pandas_append_deprecated_fix()`: 验证代码不再使用已弃用的`append`方法

---

## Bug 2: 特征名不完整/不一致

### 问题描述
`parsing_keystats.py`中的特征列表包含两个不完整的特征名：
- `"Shares Short (as of"` - 缺少右括号
- `"Shares Short (prior month"` - 缺少右括号

这会导致正则表达式匹配失败或数据解析不正确。

### 修复方案
为这两个特征名添加缺失的右括号。

### 代码变更
**文件**: `parsing_keystats.py`

```python
# 修复前
"Shares Short (as of",
...
"Shares Short (prior month",

# 修复后
"Shares Short (as of)",
...
"Shares Short (prior month)",
```

### 测试用例
测试文件: `tests/test_datasets.py`
- `test_features_names_complete()`: 验证所有特征名的括号都是平衡的

---

## Bug 3: data_string_to_float 大小写敏感

### 问题描述
`utils.py`中的`data_string_to_float`函数在处理数字单位后缀（K、M、B）和NaN值时是大小写敏感的。这会导致：
- `"10k"` 无法被正确识别为10000
- `"nan"` 或 `"NAN"` 无法被识别为N/A

### 修复方案
将输入字符串转换为大写后再进行匹配处理。

### 代码变更
**文件**: `utils.py`

```python
# 修复前
def data_string_to_float(number_string):
    if ("N/A" in number_string) or ("NaN" in number_string):
        return "N/A"
    elif "B" in number_string:
        return float(number_string.replace("B", "")) * 1000000000
    elif "M" in number_string:
        return float(number_string.replace("M", "")) * 1000000
    elif "K" in number_string:
        return float(number_string.replace("K", "")) * 1000

# 修复后
def data_string_to_float(number_string):
    number_string_upper = number_string.upper()
    if ("N/A" in number_string_upper) or ("NAN" in number_string_upper):
        return "N/A"
    elif "B" in number_string_upper:
        return float(number_string_upper.replace("B", "")) * 1000000000
    elif "M" in number_string_upper:
        return float(number_string_upper.replace("M", "")) * 1000000
    elif "K" in number_string_upper:
        return float(number_string_upper.replace("K", "")) * 1000
```

### 测试用例
测试文件: `tests/test_utils.py`
- `test_data_string_to_float_case_insensitive()`: 验证大小写不敏感的处理
  - 测试小写单位: `10k`, `5m`, `2.5b`
  - 测试混合大小写: `10K` vs `10k`
  - 测试负值与小写单位: `-100.1k`, `-0.1m`, `-0.02b`
  - 测试NaN变体: `nan`, `NaN`, `NAN`, `n/a`, `N/a`

---

## 运行测试

要运行所有测试，请执行：

```bash
pytest tests/
```

要运行特定的Bug修复测试：

```bash
# Bug 1 测试
pytest tests/test_datasets.py::test_pandas_append_deprecated_fix

# Bug 2 测试
pytest tests/test_datasets.py::test_features_names_complete

# Bug 3 测试
pytest tests/test_utils.py::test_data_string_to_float_case_insensitive
```
