#!/usr/bin/python3
# -*- coding: utf-8 -*-

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import os

RDB_HOST = os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
BOOK_DB = 'book_app'

connection = r.connect(host=RDB_HOST, port=RDB_PORT, db=BOOK_DB)
# print(r.db(BOOK_DB).table_create('notes').run(connection))
# print(r.table("addresses").insert([
#     {
#         "first_name": "William",
#         "second_name": "Adamas",
#         "notes": "",
#         "birthday": "26.12.1976",
#         "phone": [
#             {"phone": "+380505555555", "type": "home"},
#             {"phone": "+380505555556", "type": "home"},
#             {"phone": "+380505555557", "type": "work"}
#         ]
#     },
#     {
#         "first_name": "Laura",
#         "second_name": "Roslin",
#         "notes": "",
#         "birthday": "",
#         "phone": [
#             {"phone": "+380508855556", "type": "home"},
#             {"phone": "+380508855557", "type": "work"}
#         ]
#     },
#     {
#         "first_name": "Jean-Luc",
#         "second_name": "Picard",
#         "notes": "",
#         "birthday": "",
#         "phone": [
#             {"phone": "+380505555335", "type": "home"}
#         ]
#     }
# ]).run(connection))
cursor = r.table("addresses").run(connection)
# cursor = r.table("addresses").filter(r.row["id"] == "847f354f-ccc1-4cc3-98ee-6e49059a2037").run(connection)
# cursor = r.table("addresses").filter(r.row["phone"].count() > 1).run(connection)
for document in cursor:
    print(document)
r.table("addresses").filter(r.row['first_name'] == "Jean-Luc").update({"phone": [
            {"phone": "+380505555335", "type": "home"},
            {"phone": "+380509999999", "type": "work"}
        ]}).run(connection)
cursor = r.table("addresses").run(connection)
for document in cursor:
    print(document)

# cursor = r.table("addresses").get("847f354f-ccc1-4cc3-98ee-6e49059a2037").run(connection)
# print(cursor)
connection.close()
