import praw

reddit = praw.Reddit(
    client_id="KI3xrA2NAM7JmwoSq5pTUg",
    client_secret="mbnSdxDFvmzNmUUZzxflyFgktzkX7Q",
    user_agent="pythonpraw",
)

def get_subreddit():
	memes_submissions = reddit.subreddit('all').new()
	post_to_pick = 1
	for i in range(0, post_to_pick):
			submission = next(x for x in memes_submissions if not x.stickied)
			return 'https://www.reddit.com/r/' + str(submission.subreddit) + '/top/?t=all'