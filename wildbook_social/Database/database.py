from pymongo import MongoClient
from IPython.display import YouTubeVideo, Image, display
import dateutil.parser
import matplotlib.pyplot as plt

class Database:
    def __init__(self, key, database):
        self.client = MongoClient(key)
        self.dbName = database
        self.db = self.client[database]
        
    def addItem(self, payload, collection):
        try:
            self.db[collection].insert_one(payload)
        except:
            # Item already exists in database
            pass
        
    def getAllItems(self, collection):
        res = self.db[collection].find()
        return [x for x in res]
    
    def doStatistics(self, collection, amount):
        i = 1
        while(amount > 0):
            item = self.db[collection].find_one({"$or":[{"relevant":None}, {"wild":None}]})
            if not item:
                break
            
            if self.dbName=='youtube':
                print("{}: {}".format(i, item['title']['original']))
                display(YouTubeVideo(item['_id']))
            else:
                display(Image(item['img_url'], height=100, width=200))
    
            print("Relevant (y/n):", end =" ")
            rel = True if input() == "y" else False
            
            #edited here
            if rel == True:
                print("Wild (y/n):", end =" ")
                wild = True if input() == "y" else False
            if rel == False:
                wild = 0 #bc cannot determine a video to be wild if it is not relevant 
            
            self._updateItem(collection, item['_id'], {"relevant": rel, "wild": wild})
            
            print("Response saved! {} and {}.\n".format("Relevant" if rel else "Not relevant", "Wild" if wild else "Not wild"))
            amount -= 1
            i += 1
        print('No more items to proceed.')
            
    def _updateItem(self, collection, id, payload):
        try:
            self.db[collection].update_one({"_id": id}, {"$set": payload})
            return True
        except(e):
            print("Error updating item", e)
            return False
        
    def showStatistics(self, collection):
        #edited here
        total = self.db[collection].count_documents({ "$and": [{"relevant":{"$in":[True,False]}}]})
        if total == 0:
            print("No videos were processed yet.")
            return
        relevant = self.db[collection].count_documents({ "$and": [{"relevant":True}]}) / total * 100
        wild = self.db[collection].count_documents({ "$and": [{"relevant":{"$in":[True]}}, {"wild":True}] }) / total * 100
        print("Out of {} items, {}% are relevant, {}% are wild".format(total, round(relevant,1), round(wild,1)))

        self.showHistogram(collection)

    def showHistogram(self, collection):
        res = self.db[collection].find({'wild':True})
        timePosts = [x['publishedAt'] for x in res]
        if len(timePosts) < 1:
            print("No videos were processed yet.")
            return

        # Convert the times from datetime format to YYYY-MM-DD format
        dates = [dateutil.parser.parse(x).date() for x in timePosts]

        # sortedDates = []
        # sorting...
        # dates = sortedDates
        
        # Find the difference in days between posting dates of successive posts
        lastDate = [dates[0]]
        timeDiffs = []
        for date in dates:
            res = abs(date - lastDate[-1])
            timeDiffs.append(res.days)
            lastDate.append(date)

        # Plotting the histogram
        bins = [x*10 for x in range(11)]
        plt.hist(timeDiffs, bins = bins, histtype = 'bar', rwidth = 0.8)
        plt.xlabel('Days between succesive posts')
        plt.ylabel('Number of posts')
        plt.title('Histogram for Time Between Succesive Wild Posts')
        plt.show()
             
    def clearCollection(self, collection, msg=''):
        if (msg == 'yes'):
            self.db[collection].delete_many({})
            print("Colelction was cleared.")
        else:
            print("Pass 'yes' into clearCollection() method to really clear it.")
            
    def close(self):
        self.client.close()
        
