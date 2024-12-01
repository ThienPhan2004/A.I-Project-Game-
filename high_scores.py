from datetime import datetime

class HighScores:
    def __init__(self):
        # Khởi tạo các thuộc tính của bảng điểm cao
        self.scores_file = "Test Do An Cuoi Ky Tri Tue Nhan Tao/data/highscores.txt"  # Đường dẫn đến file lưu điểm cao
        self.scores = self.load_scores()  # Tải điểm cao từ file
    
    def load_scores(self):
        # Tải điểm cao từ file txt với định dạng: điểm, tên chế độ chơi, ngày tháng chơi
        try:
            with open(self.scores_file, "r") as f:
                scores = []  # Danh sách lưu trữ điểm
                for line in f.readlines():
                    score, mode, date = line.strip().split('|')  # Tách thông tin từ mỗi dòng
                    scores.append({
                        'score': int(score),  # Điểm
                        'mode': mode,         # Chế độ chơi
                        'date': date          # Ngày ghi điểm
                    })
                return sorted(scores, key=lambda x: x['score'], reverse=True)[:5]  # Trả về 5 điểm cao nhất
        except:
            return []  # Nếu có lỗi, trả về danh sách rỗng
    
    def save_scores(self):
        # Lưu điểm cao vào file
        with open(self.scores_file, "w") as f:
            for score_data in self.scores:
                f.write(f"{score_data['score']}|{score_data['mode']}|{score_data['date']}\n")  # Ghi điểm vào file
    
    def add_score(self, score, mode):
        # Thêm điểm mới vào bảng điểm cao
        current_date = datetime.now().strftime("%d/%m/%Y")  # Lấy ngày hiện tại
        self.scores.append({
            'score': score,  # Điểm mới
            'mode': mode,    # Chế độ chơi
            'date': current_date  # Ngày ghi điểm
        })
        self.scores = sorted(self.scores, key=lambda x: x['score'], reverse=True)[:5]  # Cập nhật danh sách điểm cao nhất
        self.save_scores()  # Lưu lại bảng điểm cao