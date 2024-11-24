from datetime import datetime

class HighScores:
    def __init__(self):
        self.scores_file = "Test Do An Cuoi Ky Tri Tue Nhan Tao/data/highscores.txt"
        self.scores = self.load_scores()
    
    def load_scores(self):
        try:
            with open(self.scores_file, "r") as f:
                scores = []
                for line in f.readlines():
                    score, mode, date = line.strip().split('|')
                    scores.append({
                        'score': int(score),
                        'mode': mode,
                        'date': date
                    })
                return sorted(scores, key=lambda x: x['score'], reverse=True)[:5]
        except:
            return []
    
    def save_scores(self):
        with open(self.scores_file, "w") as f:
            for score_data in self.scores:
                f.write(f"{score_data['score']}|{score_data['mode']}|{score_data['date']}\n")
    
    def add_score(self, score, mode):
        current_date = datetime.now().strftime("%d/%m/%Y")
        self.scores.append({
            'score': score,
            'mode': mode,
            'date': current_date
        })
        self.scores = sorted(self.scores, key=lambda x: x['score'], reverse=True)[:5]
        self.save_scores() 