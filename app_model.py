import pandas as pd
import numpy as np
import kagglehub
import os


class Crawler:
    def RefreshData()->str:
        destination_path = "/app/data/"
        
        os.chdir(destination_path)
        # Download latest version from Kaggle Hub
        
        path = kagglehub.dataset_download("jirakst/bookcrossing")

        str(os.listdir(path))
#        # Specify the source and destination directories
#        source_folder = path
#        destination_folder = "data/"
#
#        # Check if destination folder exists, if not create it
#        if not os.path.exists(destination_folder):
#            os.makedirs(destination_folder)
#
#        # Get a list of all files in the source folder
#        files = os.listdir(source_folder)
#
#        # Loop through each file and move it
#        for file in files:
#            source_file = os.path.join(source_folder, file)
#            destination_file = os.path.join(destination_folder, file)
#
#        # Check if it's a file (not a directory)
#        if os.path.isfile(source_file):
#            os.rename(source_file, destination_file)
#            print(f"Moved: {source_file} to {destination_file}")

        return str(os.listdir(path))


class DataStorage:    
    def GetBooks(self)->pd.DataFrame:
        return pd.read_csv('data/BX-Books.csv',  encoding='cp1251', sep=';', on_bad_lines='skip')
    
    def GetBookRatings(self)->pd.DataFrame:
        return pd.read_csv('data/BX-Book-Ratings.csv', encoding='cp1251', sep=';')



class RecommendationEngine:
    def __init__(self, dataStorage):
        self.dataStorage = dataStorage

    def FactorizationMatrix(self, favoriteBook : str)->list:        
        # load ratings
        #ratings = pd.read_csv('data/BX-Book-Ratings.csv', encoding='cp1251', sep=';')
        ratings = self.dataStorage.GetBookRatings()

        ratings = ratings[ratings['Book-Rating']!=0]

        # load books
        books = pd.read_csv('data/BX-Books.csv',  encoding='cp1251', sep=';', on_bad_lines='skip')
        #books = self.dataStorage.GetBooks()

        #users_ratigs = pd.merge(ratings, users, on=['User-ID'])
        dataset = pd.merge(ratings, books, on=['ISBN'])
        dataset_lowercase=dataset.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)
        print(dataset_lowercase.head(10))

        tolkien_readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title']=='the fellowship of the ring (the lord of the rings, part 1)') & (dataset_lowercase['Book-Author'].str.contains("tolkien"))]
        tolkien_readers = tolkien_readers.tolist()
        tolkien_readers = np.unique(tolkien_readers)

        # final dataset
        books_of_tolkien_readers = dataset_lowercase[(dataset_lowercase['User-ID'].isin(tolkien_readers))]

        # Number of ratings per other books in dataset
        number_of_rating_per_book = books_of_tolkien_readers.groupby(['Book-Title']).agg('count').reset_index()

        #select only books which have actually higher number of ratings than threshold
        books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= 8]
        books_to_compare = books_to_compare.tolist()

        ratings_data_raw = books_of_tolkien_readers[['User-ID', 'Book-Rating', 'Book-Title']][books_of_tolkien_readers['Book-Title'].isin(books_to_compare)]

        # group by User and Book and compute mean
        ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()

        # reset index to see User-ID in every row
        ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()

        dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')

        LoR_list = ['the fellowship of the ring (the lord of the rings, part 1)']
        #LoR_list = ['1984']
        #LoR_list = [['the fellowship of the ring (the lord of the rings, part 1)', 'talkien']] ]

        result_list = []
        worst_list = []

        # for each of the trilogy book compute:
        for LoR_book in LoR_list:

            #Take out the Lord of the Rings selected book from correlation dataframe
            dataset_of_other_books = dataset_for_corr.copy(deep=False)
            dataset_of_other_books.drop([LoR_book], axis=1, inplace=True)

            #select records which contains
            #ratings_data_raw = ratings_data_raw[~ratings_data_raw['Book-Title'].str.contains(':', case=False, na=False)]


            # empty lists
            book_titles = []
            correlations = []
            avgrating = []

            # corr computation
            for book_title in list(dataset_of_other_books.columns.values):
                book_titles.append(book_title)
                correlations.append(dataset_for_corr[LoR_book].corr(dataset_of_other_books[book_title]))
                tab=(ratings_data_raw[ratings_data_raw['Book-Title']==book_title].groupby(ratings_data_raw['Book-Title']).mean(["Book-Rating"]))
                avgrating.append(tab['Book-Rating'].min())
            # final dataframe of all correlation of each book   
            corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avgrating)), columns=['book','corr','avg_rating'])
            corr_fellowship.head()

            # top 10 books with highest corr
            result_list.append(corr_fellowship.sort_values('corr', ascending = False).head(10))

            #worst 10 books
            worst_list.append(corr_fellowship.sort_values('corr', ascending = False).tail(10))

        print("Correlation for book:", LoR_list[0])
        #print("Average rating of LOR:", ratings_data_raw[ratings_data_raw['Book-Title']=='the fellowship of the ring (the lord of the rings, part 1'].groupby(ratings_data_raw['Book-Title']).mean()))
        rslt = result_list[0]

        resultSet = dataset_lowercase[['Book-Title', 'Book-Author']][dataset_lowercase['Book-Title'].isin(rslt["book"])].drop_duplicates()
        print(resultSet)
        #listRecommenedBooks = rslt["book"].to_list(index=False)

        return resultSet


    def RecommendBooks(self, favoriteBook : str) -> list:
        # recommended_books = [ "Hello world", "book2", "book3", "book4", "book5", "book6", "book7", "book8", "book9", "book10" ]
        recommended_books = self.FactorizationMatrix('the brethren')
        #dreamcatcher
        #the brethren
        
        return recommended_books
    

