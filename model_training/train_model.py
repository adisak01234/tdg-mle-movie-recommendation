import os
import pandas as pd
from surprise import Dataset, Reader
from sklearn.metrics import r2_score
from surprise.model_selection import train_test_split
from surprise import SVD
from surprise.accuracy import rmse
from joblib import dump

df_movies = pd.read_csv(os.path.join(__file__, '../training_data/movies.csv'))
df_rating = pd.read_csv(os.path.join(__file__, '../training_data/ratings.csv')).query("0.5<=rating<=5")

# Load data
file_path = os.path.join(os.path.dirname(__file__), 'training_data', 'ratings.csv')
reader = Reader(rating_scale=(0.5, 5))
data = Dataset.load_from_df(df_rating[['userId', 'movieId', 'rating']], reader)

# Prepare train and test sets
trainset, testset = train_test_split(data, test_size=0.2)

# Train the model using SVD algorithm
algo = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.02)
algo.fit(trainset)

# Predict ratings for the trainset (this requires converting the trainset to a testset format)
train_predictions = algo.test(trainset.build_testset())
# Calculate RMSE for train set
train_rmse = rmse(train_predictions, verbose=False)
print(f"Train RMSE: {train_rmse}")

# Calculate R2 for train set
train_true_ratings = [pred.r_ui for pred in train_predictions]
train_pred_ratings = [pred.est for pred in train_predictions]
train_r2 = r2_score(train_true_ratings, train_pred_ratings)
print(f"Train R2: {train_r2}")

# Predict ratings for the testset
test_predictions = algo.test(testset)
# Calculate RMSE for test set
test_rmse = rmse(test_predictions, verbose=False)
print(f"Test RMSE: {test_rmse}")

# Calculate R2 for test set
test_true_ratings = [pred.r_ui for pred in test_predictions]
test_pred_ratings = [pred.est for pred in test_predictions]
test_r2 = r2_score(test_true_ratings, test_pred_ratings)
print(f"Test R2: {test_r2}")


trainset_full = data.build_full_trainset()

algo_full = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.02)
algo_full.fit(trainset_full)

# Save the model to a file
dump(algo_full, os.path.join(__file__, '../../model/model.joblib'))
