import praw


class Reddit:

    def __init__(self):
        self.reddit = praw.Reddit(user_agent='',
                                  client_id='',
                                  client_secret='',
                                  username='',
                                  password='')
        self.f = open('submission.txt', 'w')  # all the data from reddit first saved there

    def subreddit(self, subreddit):
        new_subreddit = self.reddit.subreddit(subreddit).top(time_filter='week')  # top data of the day
        for submission in new_subreddit:
            self.f.write(str(submission.title) + '\n')
        self.f.close()

