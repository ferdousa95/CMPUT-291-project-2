from pymongo import MongoClient
import json
import sys

class Database_Midder:
    def __init__(self, port=27017):
        self.port = self.portConnection()
        # Creating connection bridge
        self.client = MongoClient('localhost', self.port)
        # database: 291db
        self.db = self.client['291db']

        # if tags, votes, or posts collection exists -> delete them
        # collections = self.db.list_collection_names()
        # for table in collections:
        #     table.drop()
        # Collections: tags, votes, posts.
        self.tags = self.db['tags']
        self.votes = self.db['votes']
        self.posts = self.db['posts']
        self.posts.drop()
        self.votes.drop()
        self.tags.drop()
        self.tags = self.db['tags']
        self.votes = self.db['votes']
        self.posts = self.db['posts']

        # inserting data
        try:
            self.insertTagsRecords()
            self.insertVotesRecord()
            self.insertPostsRecord()
        except Exception as e:
            print("Error in inserting data : ", e)



    def insertTagsRecords(self):
        # insert all the records from the json file
        with open('Tags.json') as tagFile:
            allTagInfo = json.load(tagFile)  # all the info here
            metadata = allTagInfo.get('tags')  # Getting in
            tagsRecords = metadata.get('row')  # A list of all the values in tagsRecords

        if isinstance(tagsRecords, list):
            self.tags.insert_many(tagsRecords)  # insert the values

        # close the database
        tagFile.close()

    def insertVotesRecord(self):
        # insert all the records from the json file
        with open('Votes.json') as voteFile:
            allVoteInfo = json.load(voteFile)  # all the info here
            metadata = allVoteInfo.get('votes')  # Getting in
            votesRecords = metadata.get('row')  # A list of all the values in votesRecords

        if isinstance(votesRecords, list):
            self.votes.insert_many(votesRecords)  # insert the values

        # close the database
        voteFile.close()

    def insertPostsRecord(self):
        # insert all the records from the json file
        with open('Posts.json') as postsFile:
            allPostsInfo = json.load(postsFile)  # all the info here
            metadata = allPostsInfo.get('posts')  # Getting in
            postsRecords = metadata.get('row')  # A list of all the values in postsRecords

        if isinstance(postsRecords, list):
            self.posts.insert_many(postsRecords)  # insert the values

        # close the database
        postsFile.close()

    def portConnection(self):
        try:
            port = sys.argv[1]
            port = int(port)
            return port
        except Exception as e:
            print("Cannot connect to the database, Problem in port number. Error - ", e)