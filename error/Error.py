class Error():
    def __init__(self, text):
        self.text = text
    
    def __repr__(self):
        return self.text
    
    def __str__(self):
        return self.text