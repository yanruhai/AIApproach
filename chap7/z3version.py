import z3.z3 as z3

# 方式1：获取完整版本字符串（如 "4.12.2.0"）
version_str = z3.get_version_string()
print("Z3 完整版本：", version_str)

# 方式2：获取版本号元组（主版本、次版本、修订版、构建号）
version_tuple = z3.get_version()
print("Z3 版本元组：", version_tuple)  # 输出示例：(4, 12, 2, 0)

# 方式3（进阶）：查看详细编译/平台信息
print("Z3 详细信息：", z3.get_full_version())