import psycopg2

class Initializer:
    def __init__(self):
        con = psycopg2.connect(database='hermes', user='flask', host='localhost', password='root')
        self.cur = con.cursor()

    def datadump(self, file):
        file = open(file, 'r')
        file = " ".join(file.readlines())
        self.cur.execute(file)


def main(file):
    init = Initializer()
    init.datadump(file)

