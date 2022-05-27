from orm import Model, Database

class WinnerData(Model):
    name = str
    date = int

    def __init__(self, name, date):
        self.name = name
        self.date = date

class DbWorker:
    def __init__(self):
        self.db = Database('database.db')
        WinnerData.db = self.db

    def add_winner(self, name, date):
        winner = WinnerData(name, date).save()
        self.db.commit()

    def get_all_winners(self):
        winners = WinnerData.manager(self.db)

        return list(winners.all())
