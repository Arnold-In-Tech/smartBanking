import sqlite3

CONN = sqlite3.connect('bank_database.db')
CURSOR = CONN.cursor()
