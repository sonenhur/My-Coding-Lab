# quest.py
class Quest:
    def __init__(self, name, description, goal, reward):
        self.name = name
        self.description = description
        self.goal = goal
        self.progress = 0
        self.reward = reward
        self.completed = False

    def update_progress(self, amount=1):
        if not self.completed:
            self.progress += amount
            if self.progress >= self.goal:
                self.completed = True
                return True  # 퀘스트 완료
        return False

    def get_status(self):
        return f"{self.progress}/{self.goal}"
