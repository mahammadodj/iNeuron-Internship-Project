import pickle
from ModelSelection import X_train, X_test, y_train, y_test
import numpy as np
from Hyperparameter_optimization import pipeline
from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error

import pickle

pipeline.fit(X_train, y_train)
y_pred=pipeline.predict(X_test)

print(mean_absolute_error(y_test,y_pred))
print(np.sqrt(mean_absolute_error(y_test,y_pred)))
print(y_pred)



document = "mypickle.pkl"
    
pickle.dump(pipeline,open(document,"wb"))