import pymongo

class EmojiModel:
  reaction_list = ["thumbsup", "thumbsdown"]

  def __init__(self, db: pymongo.database.Database):
    """
    db : pymongo.database.Database

    self.collect : pymongo.collection.Collection
    this collection name is `emoji`
    """
    self.collect: pymongo.collection.Collection = db["emoji"]

  async def add(self, sub : str, reaction : str = "thumbsup"):
    """
    add emoji 👍 or 👎 from sub
    """
    if(reaction not in EmojiModel.reaction_list):
      return

    self.collect.insert({ "sub" : sub, "reaction" : reaction})


  async def remove(self, sub : str, reaction : str = "thumbsup"):
    """
    remove emoji 👍 or 👎 
    """
    if(reaction not in EmojiModel.reaction_list):
      return
    
    self.collect.remove({"sub" : sub, "reaction" : reaction})
    