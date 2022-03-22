Web Crawling & Sentiment Analysis

The project was done in confidence for a company and thus the initial data file has not been made available. However, one could explore the code files to include their version of data.
The project basically has 4 main elements:
  (i) Input.xlsx (has not been made available) :
      The excel file contained url_id and url to 171 webpages/blog posts from cell 2.
  (ii) Crawler.py :
        The module would be able to accept Input.xlsx, read the urls present in each cell and access the urls to scrape texts from the blogposts. The texts were then     saved in a .txt file and each .txt file has been saved with the respective url_ids 
  (iii) SentimentAnalysis.py :
        The module was responsible for iterating over the 171 .txt files to perform sentiment analysis. Each .txt file was checked for - positive score, negative score, polarity score, subjectivity score, average sentence length, percentage of complex words, fog index, average number of words per sentence, complex word count, word count, syllable per word, personal pronouns and average word length. The scores were stored in a seperate excel file along with the url_ids and urls named "Output Data Structure.xlsx". The output excel file has not been made available for security purposes.
   (iv) MasterFile.py :
        The file has been created by Bill McDonald of University of Notre Dame and was used as a dictionary of words for sentiment analysis. The module accepted words from file "Loughran-McDonald_MasterDictionary_1993-2021.csv"
