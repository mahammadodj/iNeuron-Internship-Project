
from FeatureSelection import X,y
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score
from sklearn.preprocessing import OrdinalEncoder,StandardScaler
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.ensemble import AdaBoostRegressor,GradientBoostingRegressor,RandomForestRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                      train_size=0.8,
                                                      test_size=0.2,
                                                      random_state=101)

num_vars = ['temp','clouds_all']
cat_vars = ['holiday','weather_main', 'weekday', 'hour', 'month']

numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[
    ('encoder',OrdinalEncoder())])

preprocessor = ColumnTransformer(transformers=[
    ('num',numeric_transformer,num_vars),
    ('cat',categorical_transformer,cat_vars)])

models = [AdaBoostRegressor(), GradientBoostingRegressor(), RandomForestRegressor(), 
         CatBoostRegressor(), XGBRegressor()]

model_labels = ['AdaBoost','GradientBoost','RandomForest','CatBoost','XGBoost']
r2_scores = []

for model in models:
    data_pipeline = Pipeline(steps = [
                                    ('preprocessor', preprocessor),
                                    ('model', model)])
    
    r2_score = cross_val_score(data_pipeline, X_train, y_train, cv=KFold(n_splits=10), scoring='r2',n_jobs=-1).mean()
    r2_scores.append(r2_score)

results = zip(model_labels,r2_scores)
print(list(results))