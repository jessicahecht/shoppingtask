import numpy as np
import pandas as pd


word_list = pd.read_csv('/Users/jessicahecht/Documents/Shohamy_Lab/honors_project/word_ratings.csv')

word_list = word_list[['Word', 'Conc.M']].dropna()
word_list.set_index('Word', inplace = True)

basketreviewHL = 'This item has a pleasing aesthetic that is captivating and also very functional. '
basketreviewHH = 'This basket is solid and durable! We love the wooded color and intricate pattern.'
brLH = "This item has a pleasing aesthetic that is captivating and also very functional. "
brLL = "This was a disappointing purchase. The layout is inconvenient and almost useless. "

reviews = [basketreviewHH, basketreviewHL, brLL, brLH]

# reviews = pd.read_csv(reviews)

# find average level concretness of a written review
def rate_review (review):
	total_ratings = [] 

	review = clean_words(review)
	for word in review: 
		if word_list.index.contains(word):
			i = word_list.loc[word,'Conc.M']
			total_ratings.append(i)
	count = 0
	for i in total_ratings: 
		count = count + i
	mean = i/len(total_ratings)
	total_ratings = pd.DataFrame(total_ratings)
	return total_ratings.mean()

# create list of processible words from review 
def clean_words (review):
	punctuation = ['.', '!', ',']
	for i in punctuation: 
		review = review.replace(i, '')
	review = review.split()
	for word in review:
		word.lower()
	return review

for r in reviews:
	print rate_review(r)