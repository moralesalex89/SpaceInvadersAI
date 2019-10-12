class HighScore:
    def __init__(self):
        self.hs_list = []
        self.read_list()

    def read_list(self):
        with open("highscores.txt", "r") as hs_r:
            hs_txt = hs_r.read()
            rows = hs_txt.split("\n")
            self.hs_list = []
            for row in rows:
                self.hs_list.append(row.split(","))

    def save_scores(self):
        start = True
        buffer = []
        for entry in self.hs_list:
            if start:
                buffer.append("%s,%s" % (entry[0], entry[1]))
                start = False
            else:
                buffer.append("\n%s,%s" % (entry[0], entry[1]))

        with open("highscores.txt", "w+") as hs_w:
            contents = hs_w.read()
            for item in buffer:
                hs_w.writelines(item)
                hs_w.truncate()

    def print(self):
        print(self.hs_list)

    def check_place(self, score):
        pos = 0
        for rank in self.hs_list:
            if score <= int(rank[0]):
                pos += 1
            else:
                break

        entry = [str(score), 'Player']
        self.hs_list.insert(pos, entry)
        self.hs_list.pop()

        if pos < 10:
            self.save_scores()
            self.read_list()

    def get_highscore(self):
        return int(self.hs_list[0][0])
