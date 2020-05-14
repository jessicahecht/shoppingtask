import numpy as np
import pandas as pd
from afinn import Afinn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#set afinn to english 
afinn = Afinn(language='en')
#initialize vader
analyzer = SentimentIntensityAnalyzer()


#load concreteness ratings data
word_list = pd.read_csv('/Users/jessicahecht/Documents/Shohamy_Lab/honors_project/word_ratings.csv')
word_list = word_list[['Word', 'Conc.M']].dropna()
word_list = word_list.set_index('Word')

#load review stimuli 
reviews = pd.read_csv('/Users/jessicahecht/Documents/Shohamy_Lab/honors_project/basket_reviews.csv')


def average_ratings (reviews):
	avg_ratings = []
	excluded = []
	afinn_valence = []
	vader_valence = []
	for r in reviews["review"]:
		rating = rate_review(r)
		avg_ratings.append(rating[0])
		excluded.append(rating[1])
		afinn_valence.append(rating[2])
		vader_valence.append(rating[3])
	reviews['mean_concreteness'] = avg_ratings
	reviews['excluded'] = excluded
	reviews['afinn_valence'] = afinn_valence
	reviews['vader_valence'] = vader_valence
	return reviews

# find average level concretness of a written review
def rate_review (review):
	word_ratings = [] 
	excluded = []

	#get afinn rating
	afinn_score = afinn.score(review)
	#get vader rating
	vader_score = analyzer.polarity_scores(review)
	vader_compound = vader_score['compound']
	#get concreteness rating
	review = clean_words(review)
	for word in review: 
		if (word_list.index ==word).any():
			i = word_list.loc[word].at['Conc.M']
			word_ratings.append(i)
		# note if word does not appear in list
		else:
			excluded.append(word)
	word_ratings = np.array(word_ratings)
	return [word_ratings.mean().round(decimals = 4), excluded, afinn_score, vader_compound]
	# return mean

# create list of processible words from review 
def clean_words (review):
	punctuation = ['.', '!', ',','-']
	for i in punctuation: 
		if i not in punctuation:
			break
		else:
			review = review.replace(i, ' ')
	review = review.split()
	cleaned_review = []
	for word in review:
		cleaned_review.append(word.lower())
	# print cleaned_review
	return cleaned_review

average_ratings(reviews).to_csv('/Users/jessicahecht/Documents/Shohamy_Lab/honors_project/basket_ratings.csv')
