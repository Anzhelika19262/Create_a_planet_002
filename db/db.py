import sqlite3


class DATABASE:
    def __init__(self):
        self.con = sqlite3.connect('User_achievements.db')
        self.cur = self.con.cursor()
        self.user_achievements = self.cur.execute('''SELECT * FROM Achievements''').fetchall()
        self.user_achievements = list(map(lambda x: list(x)[1], self.user_achievements))

    def add_to_date_base(self, new_achievement):
        self.cur.execute('''INSERT INTO Achievements(id, achievement) VALUES(?, ?)''', (len(self.user_achievements) + 1,
                                                                                        new_achievement))
        self.con.commit()

    def get_all_achievements(self):
        return self.user_achievements
