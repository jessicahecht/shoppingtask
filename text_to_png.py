
from PIL import Image, ImageDraw, ImageFont
import pandas as pd 


stimuli = pd.read_csv('/Users/jessicahecht/Documents/Shohamy_Lab/honors_project/word_review_ratings.csv')
reviews = stimuli[['store', 'c_v', 'review']]

# fonts = fontconfig.query(lang='en')
# for i in range(1, len(fonts)):
#     if fonts[i].fontformat == 'TrueType':
#         absolute_path = fonts[i].file
#         break
i = 0
for ind in reviews.index: 
	# \n -- new line in string 
	text = reviews['review'][ind]
	textList = text.split()
	for word in textList:
		if len(textList) > 10: 
			textList.insert(9, '\n')
			break 
	s = ' '
	review = s.join(textList)
	image = Image.new("RGB", (900, 200), (255,255,255))
	draw = ImageDraw.Draw(image)
	
	font_type = ImageFont.truetype('Times.ttc', 36) 
	draw.multiline_text((10,10), review, font =font_type, fill = (0, 0, 0), align="center" ) # fix font and make text larger, fix resolution
	i += 1
	if i < 9: 
		filename = '/Users/jessicahecht/Documents/Shohamy_Lab/honors_project/stimuli/word_stimuli/'+reviews['store'][ind]+ '/' + reviews['store'][ind] + 'review' + str(i) +'.png'
	else:
		i = 1
		filename = '/Users/jessicahecht/Documents/Shohamy_Lab/honors_project/stimuli/word_stimuli/'+reviews['store'][ind]+ '/' + reviews['store'][ind]+'review1.png'
	image.save(filename, dpi=(750,750))
