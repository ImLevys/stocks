import list_stock
import reddit


reddit = reddit.Reddit()
reddit.subreddit('pennystocks')
reddit = list_stock.List()
reddit.data_frame('pennystocks')
reddit.delta('pennystocks')
