

class msg():

    def __init__(self, message):
        '''
        Parameters:
            message:   discord message clas

        Returns:
            None
        '''
        self.author = message.author.name
        self.content = message.content
        self.mentions = [val.name for val in message.mentions]
        self.id = message.id
        self.created_at = message.created_at
        self.edited_at = message.edited_at
        return

    def __str__(self):
        '''When you print card, return card name'''
        return self.getId()

    def getAuthor(self): return self.author

    def getContent(self): return self.content

    def getMentions(self): return self.mentions

    def getId(self): return self.id

    def getCreated_at(self): return self.created_at

    def getEdited_at(self): return self.edited_at

    def printAll(self):
        print("author: {} \t id: {} \nconent: {} \ncreated: {} \t edited: {} \t mentions: {}".format(
                self.author, self.id, self.content, self.created_at, self.edited_at, self.mentions))
