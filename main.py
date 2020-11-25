# This is a sample Python script.
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import json
import pprint
from database import Database_Midder
import re



# Answer and question ids are currently messed up and will continuously assign the same id probably or something, either way its wrong

# Midder = MongoDB Tidder
midder = Database_Midder(27017)
postdisplay = ["Title", "Body", "OwnerUserId", "Id"]
ansdisplay = ["Id", "Body", "CreationDate", "Score"]
qID = 500000
aID = 600000
vID = 2000000
def main():
    loggingin = True
    while loggingin:
        print('To log into Midder, type your user ID.')
        user = input('Otherwise, simply press enter: ')
        if user.isdigit():
            realuser = login(user) # Returns true or false depending on if user is real
            if realuser:
                loggingin = False
            else:
                print('Not a valid ID. Try again.\n')
        elif user == '':
            print('Welcome to Midder!')
            loggingin = False
        else:
            print('Input not accepted. Try again.\n')
    navigate(user)



# Post ID 1 means question
# Post ID 2 means answer
def login(user):
    """
    Generates a report of user info, if they choose to log in.
    DONE(1) the number of questions owned and the average score for those questions,
    DONE(2) the number of answers owned and the average score for those answers, and
    (3) the number of votes given to the user.

    Example:
    Average all given likes from all documents in the collection for each user:
    > db.mycol.aggregate([{$group : {_id: {user : "$by_user"}, num_tutorial : {$avg : "$likes"}}}])

    :param user
    :return: Boolean
    """
    # Question posts and question scores
    qposts = midder.posts.find({"$and": [{"OwnerUserId": user}, {"PostTypeId": '1'}]}) # Is a question
    qscoresum = []
    questioncount = 0
    for x in qposts:
        qscoresum.append(x['Score'])
        questioncount += 1
        # pprint.pprint(x)
    # Answer posts and answer scores
    ascoresum = []
    answercount = 0
    aposts = midder.posts.find({"$and": [{"OwnerUserId": user}, {"PostTypeId": '2'}]})  # Is an answer
    for x in aposts:
        ascoresum.append(x['Score'])
        answercount += 1
    # Format and print
    # vposts = midder.db.votes.aggregate( # This query takes effing foreverrrrrrrrr
    #     [{ "$lookup": {
    #         "from": "posts",
    #         "localField": "PostId",
    #         "foreignField": "Id",
    #         "as": "post"
    #     }
    #     }]
    # )
    if qposts != None or aposts != None:
        qscoreavg = avg(qscoresum)
        ascoreavg = avg(ascoresum)
        ascoresum = goodsum(ascoresum)
        qscoresum = goodsum(qscoresum)
        print('Total Questions:', questioncount)
        print('Total Answers:', answercount)
        print('Average question score:', qscoreavg)
        print('Average answer score:', ascoreavg)
        print('Total votes:', ascoresum + qscoresum)
        return True
    else:
        return False

def navigate(user):
    navigating = True
    while navigating:
        print('\nTo post a question, type "mp".')
        print('To search through existing questions, type "search".')
        decision = input('To exit the program, type "exit": ').lower()
        if decision == 'mp':
            posttype = 1
            makepost(user, posttype)
        elif decision == 'search':
            search(user)
        elif decision == 'exit':
            navigating = False
        else:
            print('Invalid input. Try again.\n')
        # Search for questions
            # Question action - answer the question
            # Question action - list of answers
        # Question or answer action - vote

def makepost(user, posttype, parent=None):
    """
    I think this works, already?
    put in collection question:
        ID,
        posttype,
        creationdate,
        user,
        score,
        viewcount,
        commentcount,
        answercount,
        favoritecount,
        license
    answers:
        ID,
        posttype,
        creationdate,
        ownerID,
        parentID,
        score,
        commentcount,
        license
    :param user:
    :return:
    """
    global qID
    global aID
    makingpost = True
    while makingpost:
        # Collect post information
        title = input('Enter your title: ')
        body = input('Enter the body of your post: ')
        # Make sure user wants to post this
        print(title)
        print(body, '\n')
        postcheck = input('Is this what you would like to post? (Y/N)').lower()
        if postcheck[0] == 'y':
            if posttype == 1: # Question post
                # This isn't returning the actual max ID I don't know why what the heck!!? keeps giving 99999
                # I'm cheating yuh
                # maxID = midder.db.posts.find().sort([("Id", -1)]).limit(1) # for MAX
                # for x in maxID:
                #     print(x['Id'])
                ID = qID + 1
                posttypeid = posttype
                creationdate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] # Formats time exactly like the JSON file (https://stackoverflow.com/questions/7588511/format-a-datetime-into-a-string-with-milliseconds)
                contentlicense = 'CC BY-SA 2.5'
                POST = {
                    "Id": str(ID),
                    "PostTypeId": posttypeid,
                    "CreationDate": str(creationdate),
                    "Score": 0,
                    "ViewCount": str(5),
                    "Body": body,
                    "OwnerUserId": str(user),
                    "Title": title,
                    "AnswerCount": str(0),
                    "CommentCount": str(0),
                    "ContentLicense": contentlicense
                }
                try:
                    midder.posts.insert_one(POST)
                    print('You have posted "', title, '" to Midder.')
                except Exception as e:
                    print('Something went wrong:', e)
                makingpost = False
            elif posttype == 2: # Answer post
                # This isn't returning the actual max ID I don't know why what the heck!!? keeps giving 99999
                # I'm cheating yuh
                # maxID = midder.db.posts.find().sort([("Id", -1)]).limit(1) # for MAX
                # for x in maxID:
                #     print(x['Id'])
                ID = aID + 1
                posttypeid = posttype
                creationdate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] # Formats time exactly like the JSON file (https://stackoverflow.com/questions/7588511/format-a-datetime-into-a-string-with-milliseconds)
                contentlicense = 'CC BY-SA 2.5'
                POST = {
                    "Id": str(ID),
                    "PostTypeId": str(posttypeid),
                    "CreationDate": str(creationdate),
                    "Score": 0,
                    "Body": body,
                    "ParentId": str(parent),
                    "OwnerUserId": str(user),
                    "Title": title,
                    "CommentCount": str(0),
                    "ContentLicense": contentlicense
                }
                try:
                    midder.posts.insert_one(POST)
                    print('You have responded to post named "'+str(parent['Title'])+'".')
                except Exception as e:
                    print('Something went wrong:', e)
                makingpost = False
        else:
            print('Post deleted. Please type it again.')

def search(user):
    searching = True
    while searching:
        print('\nWhat would you like to search? Enter any combination of words.')
        print('To go back, type "<back>".')
        entry = input('Enter your search here: ').lower()
        if entry == '<back>':
            searching = False
        else:
            print('Searching...')
            query = entry.split()
            for entry in query:
                entry = '.*' + entry + '.*'
                entry = re.compile(entry,
                                   re.IGNORECASE)  # https://stackoverflow.com/questions/45524740/querying-like-in-pymongo
                # I REALLY DONT KNOW IF 2 SEPARATE QUERIES WORKS (I just decided to use one doe)
                # midder.posts.find({"PostTypeId": "1"}).limit(50)
                results = midder.posts.find(
                    {"$or": [{"Title": entry}, {"Body": entry}, {"Tags": entry}], "PostTypeId": "1"}).limit(50)
                for result in results:
                    finalresult = {key: value for key, value in result.items() if
                                   key in postdisplay}  # Figured out in https://stackoverflow.com/questions/12117080/how-do-i-create-dictionary-from-another-dictionary
                    pprint.pprint(finalresult)
            choosing = True
            while choosing:
                print('\nTo select a post, enter the post ID.')
                choosepost = input('To go back to the searching page, type "back": ').lower()
                if choosepost.isdigit():
                    postaction(choosepost, user)
                elif choosepost == 'back':
                    choosing = False
                else:
                    print('Invalid input. Try again.\n')

def postaction(post, user=None):
    """
    SHOULD SHOW ACCEPTED ANSWER TOO!!
    :param post:
    :param user:
    :return:
    """
    post = midder.posts.find_one_and_update({"Id": str(post)}, {'$inc': {'ViewCount': 1}}, new=True) # Works! Increments Views by 1
    if post is not None:
        post = {key: value for key, value in post.items() if key in postdisplay} # Makes new dic that is shorter version of original, checks if keys its trying to insert exist in the original dictionary
        pprint.pprint(post)
        onquestion = True
        while onquestion:
            print('\nTo answer this question, type "a".')
            print('To list all answers to this question, type "list".')
            print('To vote on this question, type "v".')
            choice = input('To go back, type "back".').lower()
            if choice == 'a':
                makepost(user, 2, post)
            elif choice == 'list':
                listanswers(post, user)
            elif choice == 'v':
                vote(post, user=user)  # THIS MIGHT BE WRONG DOUBLE CHECK
            elif choice == 'back':
                onquestion = False
            else:
                print('Invalid input. Try again.')
    else:
        print('That is not a real post. Please try again.')



def listanswers(post, user):
    """
    listAnswers(dict)
    This method prints all the answers that is related to the post selected. The first answer is the acceptedAnswer
    (marked by *** around), followed by rest of the answers.
    :param post: the a dictionary that contains question post information
    :return: prints all the answers
    """
    postid = post['Id']
    gettingDetails = midder.posts.find_one({"Id": str(postid)})         # getting full details of the question post
    confirmAcceptedAns = 1
    try:
        acceptAnsId = gettingDetails['AcceptedAnswerId']                    # the acceptedAns Id
        acceptedAnswer = midder.posts.find_one({"Id": str(acceptAnsId)})    # acceptedAns post
    except:
        confirmAcceptedAns = 0
        pass

    answers = midder.posts.find({"ParentId": str(postid)})          # all the answer post belonging to this question

    if confirmAcceptedAns == 1:
        print("\n\n\n\n\n\n\n\n\n\n") # <- ******* DELETE THIS TO 2/3 ENTERS **************3
        print("***")
        apost = {key: value for key, value in acceptedAnswer.items() if key in ansdisplay}
        pprint.pprint(apost)
        print("***\n")

    for answer in answers:
        apost = {key: value for key, value in answer.items() if key in ansdisplay}
        if confirmAcceptedAns == 1:             # there is an accepted answer
            if apost['Id'] != str(acceptAnsId): # if the ans is not the acceptedAns, because already printing above
                pprint.pprint(apost)
        else:
            pprint.pprint(apost)
            # print(answer)
    ansvoting = True
    while ansvoting:
        print('To vote on an answer, type the ID of the answer.')
        choice = input('To go back, type "back": ')
        if choice == 'back':
            ansvoting = False
        elif choice.isdigit():
            vote(apost, post, user)


def vote(post, parent=None, user=None):
    """
    NEEDS TO ALSO INSERT INTO VOTES COLLECTION DOESN'T DO DAT YET
    OR CHECK IF USER HAS ALREADY VOTED
    :param post:
    :param parent:
    :return:
    """
    global vID
    postid = post['Id']
    alreadyvoted = None
    if user is not None:
        alreadyvoted = midder.votes.find_one({"$and": [{"UserId": str(user)}, {"PostId": str(postid)}]})
    print(alreadyvoted)
    if alreadyvoted is None:
        ans = midder.posts.find_one_and_update({"Id": str(postid)}, {'$inc': {'Score': 1}}, new=True)
        # maxID = midder.db.votes.find().sort([("Id", -1)]).limit(1)  # for MAX
        # for x in maxID:
        #     print(x)
        ID = vID + 1
        creationdate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        Vote = {
            "Id": ID,
            "PostId": str(postid),
            "VoteTypeId": "2",
            "CreationDate": str(creationdate)
        }
        if user is not None:
            Vote["UserId"] = str(user)
        midder.votes.insert_one(Vote)
        ansid= ans['Id']
        print('You have successfully voted on post', ansid)
        if parent is not None:
            partitle = parent['Title']
            print('In response to "'+str(partitle)+'".')
    else:
        print('You have already voted on this post. \n')



def vote(post, parent=None, user=None):
    """
    NEEDS TO ALSO INSERT INTO VOTES COLLECTION DOESN'T DO DAT YET
    OR CHECK IF USER HAS ALREADY VOTED
    :param post:
    :param parent:
    :return:
    """
    global vID
    postid = post['Id']
    alreadyvoted = None
    if user is not None:
        alreadyvoted = midder.votes.find_one({"$and": [{"UserId": str(user)}, {"PostId": str(postid)}]})
    if alreadyvoted is None:
        ans = midder.posts.find_one_and_update({"Id": str(postid)}, {'$inc': {'Score': 1}}, new=True)
        # maxID = midder.db.votes.find().sort([("Id", -1)]).limit(1)  # for MAX
        # for x in maxID:
        #     print(x)
        ID = vID + 1
        creationdate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        Vote = {
            "Id": ID,
            "PostId": str(postid),
            "VoteTypeId": "2",
            "CreationDate": str(creationdate)
        }
        if user is not None:
            Vote["UserId"] = str(user)
        midder.votes.insert_one(Vote)
        ansid= ans['Id']
        print('You have successfully voted on post', ansid)
        if parent is not None:
            partitle = parent['Title']
            print('In response to "'+str(partitle)+'".')
    else:
        print('You have already voted on this post. \n')



# Other functions I defined, sort of external
def avg(list):
    sum = 0
    length = 0
    for number in list:
        sum += int(number) # Negatives are still strings idk why
        length += 1
    if sum != 0 and length != 0:
        return round((sum / length), 2)
    else:
        return 0

def goodsum(list):
    sum = 0
    for number in list:
        sum += int(number)
    return sum

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
