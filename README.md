# youtube-to-text (WIP)

* This code is designed to perform several different functions related to YouTube videos. Firstly, it is able to fetch videos from YouTube and save them for later use. Once the videos have been saved, the code is then able to extract the audio from the videos and convert it into text. This is accomplished using a speech-to-text conversion algorithm.

* Once the video audio has been converted to text, the code can then search for a specific keyword or set of keywords within the text. This is done using the OpenAI API, which allows for advanced natural language processing and keyword analysis.

* Overall, this code is a powerful tool for anyone looking to extract useful information from YouTube videos. It can be used for a wide range of purposes, from data analysis to market research and more. By combining YouTube video fetching, speech-to-text conversion, and keyword analysis, this code provides a comprehensive solution for anyone looking to gain valuable insights from video content.


# Example:

In this example, we used the code to fetch and analyze a set of 5 YouTube videos. After running the code, we performed a simple analysis to identify the top 25 keywords found within the video content. We then plotted these keywords using a bar plot to visualize the results.

* Video links:
  * https://www.youtube.com/watch?v=Wn_Kb3MR_cU / Search word: Web3
  * https://www.youtube.com/watch?v=EdyqLlyN0EA / Search word: Web3 lens
  * https://www.youtube.com/watch?v=J5x3OMXjgMc / Search word: Web3 Python
  * https://www.youtube.com/watch?v=iwyyxEJCIuU / Search word: Web3 Mark Zuckerberg
  * https://www.youtube.com/watch?v=wHTcrmhskto / Search word: Web 3 Future



# Simple Python code:
```
import pandas as pd
import ast
import matplotlib.pyplot as plt

#Read csv file
df = pd.read_csv('file_name.csv')
df['Result'] = df['Result'].str.replace(r'sign":', r'sign":"').str.replace(r'}', r'"}')

def extract_dict(s):
    try:
        d = ast.literal_eval(s)
    except:
        d = None
    return d

# Apply the function to Result to extract the dictionary
df["dict"] = df["Result"].apply(extract_dict)

# remove numbers from the key words




df["key_words"] = df["dict"].apply(lambda x: x["key_words"] if x is not None else None)
df["sign"] = df["dict"].apply(lambda x: x["sign"] if x is not None else None)
df["Status"] = df["dict"].apply(lambda x: 1 if x is not None else 0)
key_word_counter = {}
[key_word_counter.update({key_word: key_word_counter.get(key_word, 0) + 1}) for index, row in df.iterrows() if row['Status'] == 1 for key_word in row['key_words']]
# Remove numbers from the key words
key_word_counter = {key: value for key, value in key_word_counter.items() if not key.isdigit()}

sorted_data = dict(sorted(key_word_counter.items(), key=lambda x: x[1], reverse=True)[:25])

# Create a bar chart
plt.bar(sorted_data.keys(), sorted_data.values())
plt.title("Top 25 key_words")
plt.xlabel("Words")
plt.ylabel("Count")
plt.xticks(rotation=60)
plt.xticks(fontsize=8)
plt.tight_layout()
plt.show()

```

# Result:

![Figure_1](https://user-images.githubusercontent.com/71639133/222538135-36ed2e6d-6e00-483d-b02f-4a240c9f253d.png)

# Conclusion:
 * In conclusion, the code provided works well and can be adjusted to suit a variety of use cases. By analyzing the transcription of YouTube or any and identifying the most frequently used keywords, it is possible to gain valuable insights into trends and themes related to a particular topic or industry. With some adjustments and fine-tuning, this code can be a powerful tool for anyone looking to analyze video content and identify key trends and insights.
