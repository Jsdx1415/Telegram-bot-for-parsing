class MarkData:
    def __init__(self, mark: str, subject: str, theme: str, weight: str):
        self.mark = mark
        self.subject = subject
        self.theme = theme
        self.weight = weight

    def as_str(self):
        return f"Оценка: {self.mark} || Предмет: {self.subject} || За что оценка: {self.theme} || Вес оценки: {self.weight}"
