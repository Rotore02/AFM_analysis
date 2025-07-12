class ResultsGenerator:
    def __init__(self):
        self.enabled = False
        self.file = None

    def setup(self, file_name):
        self.enabled = True
        self.file = open(file_name, 'w')

    def write(self, message):
        if self.enabled and self.file:
            self.file.write(message + '\n')

    def close(self):
        if self.enabled and self.file:
            self.file.close()
    
        