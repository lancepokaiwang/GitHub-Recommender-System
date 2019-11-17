import Basic_Functions as bfs

users = bfs.readJsonFile(name="users_symfony_test", folder="data")

index = 0
for key, value in users.items():
    index += 1
    print(key)
    print(value)
    if index == 1:
        break
