def load_model(model_path):
    import joblib
    return joblib.load(model_path)

def make_predictions(model, input_data):
    return model.predict(input_data)

def predict(model_path, input_data):
    model = load_model(model_path)
    predictions = make_predictions(model, input_data)
    return predictions