## Files

* trip_network_analysis.ipynb: Graph code to convert trip matrix to segment weights.

* scikit_linear_regression.py: Simple linear model that saves the fit model and features in a form they can be loaded for predictions of new data by the web app.

* wsgi.py: The web app for taking POST requests, loading the trained model, and returning predictions to clients.

## Saved Artifacts

linearmodel.joblib: Serialized trained model.

featurenames.pickle: Serialized features necessary for using the linear model with new data.

## Testing

To test the wsgi.py file locally during development, you can run:

uwsgi --http :8000 --wsgi-file wsgi.py --callable app --processes 4 --threads 2

For production on bart.stokely.org, this is called from Nginx.
