import glob, os
import pandas as pd
import numpy as np 

def loadMturkData(data_dir=None):
    pid_files = glob.glob(os.path.join(data_dir,"*_experiment_data.csv"))
    data = pd.concat([pd.read_csv(file) for file in pid_files])    
    return data.reset_index(drop = True) #always reset index when concatonating 

data_dir = "/Users/jessicahecht/Documents/Shohamy_Lab/honors_project/test_data"
data = loadMturkData(data_dir)

choice_word_df = data[data.phase == "choice_word"]
choice_star_df = data[data.phase == "choice_star"]
choice_word_df = choice_word_df[["subject_id","rt",'phase',
				       'trial_number', 'trial_type_num', 'store_type', 'choice_type',
				       'img_left', 'img_left_rating', 'img_left_type', 
				       'img_right', 'img_right_rating',
				       'img_right_type', 'chosen', 'choice_rating', 
				       'chosen_type', 'side_chosen']]
choice_star_df = choice_star_df[["subject_id","rt",'phase',
				       'trial_number', 'trial_type_num', 'store_type', 'choice_type',
				       'img_left', 'img_left_rating', 'img_left_type', 
				       'img_right', 'img_right_rating',
				       'img_right_type', 'chosen', 'choice_rating', 
				       'chosen_type', 'side_chosen']]
choice_word_df = choice_word_df.reset_index(drop = True)
choice_star_df = choice_star_df.reset_index(drop = True)

word_ratings = pd.read_csv('word_review_ratings.csv')

word_ratings = word_ratings[['store', 'review', 'v_c', 'mean_concreteness', 'excluded', 'afinn_valence', 'vader_valence']]

choice_word_df['certainty_left'] = np.nan 
choice_word_df['vader_valence_left'] = np.nan 
choice_word_df['afinn_valence_left'] = np.nan 

choice_word_df['certainty_right'] = np.nan 
choice_word_df['vader_valence_right'] = np.nan 
choice_word_df['afinn_valence_right'] = np.nan 

choice_word_df['certainty_chosen'] = np.nan 
choice_word_df['vader_valence_chosen'] = np.nan 
choice_word_df['afinn_valence_chosen'] = np.nan 

# print(choice_word_df.head())

i = 0 
items = []
for item in word_ratings['store']:
	if i < 8: 
		i = i + 1
		update = item + str(i)
		items.append(update)
	else: 
		i = 1
		update = item + str(i)
		items.append(update)
word_ratings['store'] = items

# choice_word_df = choice_word_df.reset_index(drop = True) -- comment out because reset in load_data function
for ind in choice_word_df.index:
	store = choice_word_df.iloc[ind]['store_type']

	#left_side procesing
	left_img_rating = str(choice_word_df.iloc[ind]['img_left_rating'].astype(int))
	left_review = store + left_img_rating
	for item in word_ratings['store']:
		if (left_review == item): #.any():
			# print(left_review, item)
			i = word_ratings.index.get_loc(word_ratings.index[word_ratings['store'] == item][0])
			# print(i)
			left_certainty = word_ratings.at[i, 'mean_concreteness']
			# print(left_certainty)
			left_vader_valence = word_ratings.at[i, 'vader_valence']
			left_afinn_valence = word_ratings.at[i, 'afinn_valence']
			choice_word_df.at[ind, 'certainty_left'] = left_certainty
			choice_word_df.at[ind, 'vader_valence_left'] = left_vader_valence
			choice_word_df.at[ind, 'afinn_valence_left'] = left_afinn_valence

	#right side processing
	right_img_rating = choice_word_df.iloc[ind]['img_right_rating'].astype(int)
	right_review = store + str(right_img_rating)
	for item in word_ratings['store']:
		if (right_review == item): #.any():
			# print (right_review, item)
			j = word_ratings.index.get_loc(word_ratings.index[word_ratings['store'] == item][0])
			right_certainty = word_ratings.at[j, 'mean_concreteness']
			# print(right_certainty)
			right_vader_valence = word_ratings.at[j, 'vader_valence']
			right_afinn_valence = word_ratings.at[j, 'afinn_valence']

			choice_word_df.at[ind, 'certainty_right'] = right_certainty
			choice_word_df.at[ind, 'vader_valence_right'] = right_vader_valence
			choice_word_df.at[ind, 'afinn_valence_right'] = right_afinn_valence
	#chosen img processing
	chosen_img_rating = choice_word_df.iloc[ind]['choice_rating']
	# print(chosen_img_rating)
	if (chosen_img_rating == 'none'): #.any():
		chosen_img_rating = chosen_img_rating
	else:
		chosen_img_rating = int(chosen_img_rating)

	choice_review = store + str(chosen_img_rating)
	for item in word_ratings['store']:
		if (choice_review == item): #.any():
			k = word_ratings.index.get_loc(word_ratings.index[word_ratings['store'] == item][0])
			chosen_certainty = word_ratings.at[k, 'mean_concreteness']
			chosen_vader_valence = word_ratings.at[k, 'vader_valence']
			chosen_afinn_valence = word_ratings.at[k, 'afinn_valence']
		else:
			chosen_certainty = np.nan
			chosen_vader_valence = np.nan
			chosen_afinn_valence = np.nan
		choice_word_df.at[ind, 'certainty_chosen'] = chosen_certainty
		choice_word_df.at[ind, 'vader_valence_chosen'] = chosen_vader_valence
		choice_word_df.at[ind, 'afinn_valence_chosen'] = chosen_afinn_valence

# data_viz = choice_word_df[['store_type', 'img_left_rating', 'img_right_rating', 'certainty_left', 'certainty_right']]
# print (data_viz.head())


# chosen_df.to_csv('/Users/jessicahecht/Documents/Shohamy_Lab/honors_project/wordtask_appended_data.csv')


choice_df = pd.concat([choice_word_df,choice_star_df]).reset_index(drop=True)
choice_df.to_csv("combined_choice_pilot_data.csv",index=False)




