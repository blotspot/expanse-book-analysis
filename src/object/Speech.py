
class Speech:

    def __init__(self, speaker, spoken_line, line_num):
        self.speaker = speaker
        self.spoken_line = spoken_line
        self.line_num = line_num

    def __repr__(self):
        return '[{}] {}: {}'.format(self.line_num, self.speaker, self.spoken_line)
