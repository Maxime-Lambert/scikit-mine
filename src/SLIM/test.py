
from src.database import Database


test = [[1, 2, 3, 4], [1, 2, 3], [1, 2, 3], [1, 2, 3],
        [2, 3], [2, 3], [1], [1], [4]]

db = Database(test)

sct = db.make_standard_code_table()

print(sct)
