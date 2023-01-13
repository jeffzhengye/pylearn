from tasks import cooking_task


table_1_dishes = ["Chicken Biryani", "Lemon chicken", "Pepper chicken"]


result = cooking_task.delay("Table-1", table_1_dishes)

print("result", result)

table_2_dishes = ["Mutton Biryani", "Egg Biryani"]
result2 = cooking_task.apply_async(args=["Table-2", table_2_dishes])
print("result2", result2)

table_3_dishes = ["Butter Naan", "Andhra Chicken"]
result3 = cooking_task.apply_async(args=["Table-3", table_3_dishes])
print("result3", result3)

table_4_dishes = ["Chicken Manchurian", "Chicken Noodles"]
result4 = cooking_task.apply_async(args=["Table-4", table_4_dishes])
print("result4", result4)
