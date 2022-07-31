from FeatureSelection import X,y
from ModelSelection import preprocessor
from sklearn.model_selection import GridSearchCV,KFold
from sklearn.pipeline import Pipeline
from catboost import CatBoostRegressor
from sklearn.model_selection import cross_val_score
from ModelSelection import X_train, X_test, y_train, y_test

data_pipeline = Pipeline(steps = [('preprocessor', preprocessor),
                                  ('model', CatBoostRegressor(random_state=42))])

rf_grid= {'model__depth':[6,8],
    'model__learning_rate':[0.1,0.5,0.3],
    'model__iterations':[100],
          'model__min_data_in_leaf':[500,700]
}

grid_search = GridSearchCV(data_pipeline,param_grid=rf_grid,n_jobs=-1,cv=KFold(n_splits=3))

grid_search.fit(X_train,y_train)

grid_search.best_params_

pipeline = Pipeline(steps = [('preprocessor', preprocessor),
                                  ('model', CatBoostRegressor(iterations=100,
                                                              depth=8,
                                                              learning_rate=0.1,
                                                             loss_function='RMSE',
                                                             random_seed=29,
                                                             bagging_temperature=0.95,
                                                             min_data_in_leaf=500))])
r2_scores = cross_val_score(pipeline, X_train, y_train, cv=KFold(n_splits=5), scoring='r2',n_jobs=-1)
print('max r2 :', r2_scores.max())
print('min r2 :', r2_scores.min())
print('mean r2 :', r2_scores.mean())