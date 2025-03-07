from jinx import  tkr, concurrent, os, keras, itl, data, math, pd, plt, np, tf, sns, datetime, y, w, F, T, HTTPBasicAuth, generate_password_hash, check_password_hash, linear_model, r2_score, mean_squared_error, px, go, request, redirect_stdout, io
import jinx

w.filterwarnings("ignore")

# Convert the data to a pandas dataframe
df = pd.DataFrame(data)

# Drop the columns that are not needed
# df = df.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)

# Convert the Date column to a datetime object
df['date'] = pd.to_datetime(df.index)

# Convert the Date column to a datetime object
# df['date'] = pd.to_datetime(df['date'])

# Set the Date column as the index
# df = df.set_index('date')

# Convert the dataframe to a numpy array
X = df.to_numpy()

# Split the data into training and testing sets
X_train, X_test = X[:int(len(X)*0.8)], X[int(len(X)*0.8):]

x_train = []
y_train = []

# Define the training loop
for i in range(60, len(X_train)):
    x_train.append(X_train[i-60:i, 0])
    y_train.append(X_train[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)

# Reshape the data to fit the model
x_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
x_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# Define the model
model = keras.Sequential([
    keras.layers.LSTM(128, input_shape=(X_train.shape[1], 1)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(1)
])

# from jinja2 import Template

app = F(__name__)

auth = HTTPBasicAuth()

users = {
    "j": generate_password_hash("hello"),
    "s": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/login')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

# Set the secret key to some random bytes. Keep this really secret!
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# csrf = CSRFProtect(app)

# Define a route for the Rest API using a class and template
@app.route('/api/<symbol>', methods=['GET'])
class RestAPI(object):
    def __init__(self, symbol):
        self.symbol = symbol

    def get(self):
        # Load the data from yinance of the 1m interval of the last 7 days
        # data = y.download(self.symbol, period='7d', interval='1m')

        # Convert the data to a pandas dataframe
        df = pd.DataFrame(data)

        # Convert the dataframe to HTML and return it
        return df.to_html()
        # return T('index.html', df=df.to_html(), symbol=self.symbol.capitalize())

# Use a Template to render the dataframe as HTML
@app.route('/', methods=['GET'])
def home():
    symbol = tkr
    # Load the data from yfinance of the 1m interval of the last 7 days
    # data = y.download(symbol, period='7d', interval='1m')

    # Convert the data to a pandas dataframe in reverse order
    df = pd.DataFrame(data).iloc[::-1]

    # Convert the dataframe to HTML and return it
    # return df.to_html() with the dataframe as the context and symbol as the symbol

    # Get last time and date the file was accessed using Month names and 12 hours w/ AM & PM in Pacific Standard Time.
    last_updated = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    return T('index.html', df=df, symbol=symbol.capitalize(),last_updated=last_updated)

# Define a function to get the model summary
# Use a Template to render the dataframe as HTML
def get_model_summary():
    
    try:
        # Create an in-memory buffer
        buffer = io.StringIO()
    except:
        # Create an in-memory buffer
        buffer = io.BytesIO()

    try:
        # Display the model summary
        model.summary(print_fn=lambda x: buffer.write(x + '\n'))
        # Use the redirect_stdout context manager to redirect the model summary to the buffer
        # with redirect_stdout(buffer):
        #     model.summary()
    except:
        print("Error: Model summary not found.")

    # Get the model summary from the buffer
    # model_summary = buffer.getvalue()

    # try:
    #     # Get the model summary from the buffer
    #     model_summary = buffer.getvalue()
    # except:
    #     # print("Error: Model summary not found.")
    #     model_summary = "Error: Model summary not found."

    # Return the model summary
    return model

# Define a route for the model page
@app.route('/model')
def model():
    # Get the model summary
    model_summary = get_model_summary()

    # Render the model.html template and pass in the model summary
    return T('model.html', model_summary=model_summary)

# Define a route for the matplotlib page
@app.route('/matplotlib')
def matplotlib():

    # Load the data from yfinance of the 1m interval of the last 7 days
    # data = y.download('TSLA', period='7d', interval='1m')
    df = pd.DataFrame(data)
    # Calculate the moving average
    df['MA'] = df['Close'].rolling(window=20).mean()
    df['MA'] = df['MA'].fillna(0)
    # ... existing code ...

    # Convert the dataframe to a numpy array
    jinx = df.to_numpy()

    # Create Timer
    start_time = datetime.now()

    # plt = sns.lineplot(data=X)
    # Add the moving average to the figure
    fig = go.Figure(data=[
        go.Candlestick(x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='market data'
        ),
        # go.Scatter(x=df.index, y=df['STDEV'], mode='lines', name='STDEV'),
        go.Line(x=df.index, y=df['MA'], mode='lines', name='MA')],
        layout=go.Layout(title=go.layout.Title(text=tkr + " Candlestick Chart"))
    )
    # f ig = px.line(df, x=df.index, y=df['Close'])
    fig.update_layout(xaxis_rangeslider_visible=True, xaxis_rangeslider_thickness=0.05)
    fig.update_layout(
        # title='TSLA Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )
    # Add Legend
    fig.update_layout(
        legend=dict(
            x=0,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        )
    )
    # Add Annotations
    fig.update_layout(annotations=[
        dict(
            x='2022-01-01',
            y=0,
            xref="x",
            yref="y",
            text="2022",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ])
        
    # Not in pop-up
    # fig.show()
    fig.write_html("templates/candlestick.html")
    # fig.show()
    # Render the matplotlib.html template
    return T('matplotlib.html', fig=fig, jinx=jinx)

# Define the route for the search_autocomplete page
@app.route('/search_autocomplete')
def search_autocomplete():
    # Render the search_autocomplete.html template
    return T('search_autocomplete.html')

# Define Route for Bayes
@app.route('/bayes')
def bayes():
    # Load the data from file
    train_data = np.load('train_data.npy')
    test_data = np.load('test_data.npy')
    train_labels = np.load('train_labels.npy')
    test_labels = np.load('test_labels.npy')

    # Print the shapes of the data
    # print(train_data.shape, test_data.shape, train_labels.shape, test_labels.shape)
        
    try:
        # Print the shapes of the data
        print(train_data.shape, test_data.shape, train_labels.shape, test_labels.shape)

        # Reshape the data to 2D if it is 3D
        if len(train_data.shape) == 3:
            train_data = train_data.reshape(train_data.shape[0], -1)

        # Create a Bayesian Ridge Regression model with default parameters
        clf = linear_model.BayesianRidge(n_iter=300, tol=0.001, alpha_1=1e-06, alpha_2=1e-06, lambda_1=1e-06, lambda_2=1e-06)

        # Fit the model on the training data
        clf.fit(train_data, train_labels)

        # Reshape the data to 2D if it is 3D
        if len(test_data.shape) == 3:
            test_data = test_data.reshape(test_data.shape[0], -1)

        # Use the model to predict on the test data
        predictions = clf.predict(test_data)
        # Slice the predictions to only the last 100
        predictions = predictions[-100:]
        # Reverse order of predictions
        predictions = predictions[::-1]

        # Slice the test labels to only the last 100
        test_labels = test_labels[-100:]
        # Reverse order of test labels
        test_labels = test_labels[::-1]

        # Calculate the mean squared error
        mse = mean_squared_error(test_labels, predictions)

        # Print the mean squared error
        print("Mean squared error:", mse)

        # Calculate the coefficient of determination (R^2)
        r2 = r2_score(test_labels, predictions)

        # Calculate Linear Regression
        linear = linear_model.LinearRegression()
        linear.fit(train_data, train_labels)
        lpredictions = linear.predict(test_data)
        # Slice the predictions to only the last 100
        lpredictions = lpredictions[-100:]
        # Reverse order of lpredictions
        lpredictions = lpredictions[::-1]

        # LSTM data


        # Print the coefficient of determination # Print the classification report # Print the confusion matrix # Print the accuracy score # Print the analysis # Print the predictions # Print the true labels
        print("Coefficient of determination:", r2)
        print("Data:", df.tail(10))
        print("Predictions:", predictions[-10:].tolist())
        print("Linear Predictions:", lpredictions[-10:].tolist())
        print("True labels:", test_labels[-10:].tolist())

        fig = go.Figure(
            data=[ 
                go.Line(x = df.index, y = predictions, mode='lines', name='Predictions'),
                go.Candlestick(x = df.index, y = test_labels, mode='lines', name='True')
            ], layout=go.Layout(title=go.layout.Title(text= tkr + " Predictions"))
        )
        fig.update_layout(yaxis_title='Predictions')
        fig.write_html("bayes_plot.html")

        # Create a plot
        plt.figure(figsize=(10, 5))
        plt.plot(test_labels, label='True')
        plt.plot(predictions, label='Predicted')
        plt.legend()

        # Save the plot as an image
        image_path = 'static/images/bayes_plot.png'
        plt.savefig(image_path)

        fig01 = go.Figure(
            data=[ 
                go.Line(x = predictions.index, y = lpredictions, mode='lines', name='Linaer Predictions'),
            ], layout=go.Layout(title=go.layout.Title(text= tkr + " Linear Predictions"))
        )
        fig01.update_layout(yaxis_title='Linear Predictions')
        # Create linear_regression_plot.html if it does not exist, write either way.
        fig01.write_html("linear_regression_plot.html")

        # Create a plot
        plt.figure(figsize=(10, 5))
        plt.plot(test_labels, label='True')
        plt.plot(lpredictions, label='Predicted')
        plt.legend()

        # Save the plot as an image
        image_path = 'static/images/linear_regression_plot.png'
        plt.savefig(image_path)

    except:
        print("Error: Data not found.")

    # Render the bayesian_ridge.html template predictions will only be last 100
    # Format predictions to 2 decimal places.
    return T('bayes.html', lpredictions=lpredictions.round(2), predictions=predictions.round(2), train_data=train_data, test_data=test_data, train_labels=train_labels, test_labels=test_labels, clf=clf, r2=r2, mse=mse) # , analysis=analysis, classification_report=classification_report, confusion_matrix=confusion_matrix, accuracy_score=accuracy_score, image_path=image_path)

# Define Route for Linear Regression
# @app.route('/<jinx_function>', methods=['GET'], defaults={'jinx_function': 'linear_regression', 'jinx_function': 'random_forest', 'jinx_function': 'support_vector_machine', 'jinx_function': 'decision_tree', 'jinx_function': 'logistic_regression', 'jinx_function': 'neural_network', 'jinx_function': 'gradient_boosting', 'jinx_function': 'k_nearest_neighbors', 'jinx_function': 'xgboost', 'jinx_function': 'lightgbm', 'jinx_function': 'catboost', 'jinx_function': 'automl', 'jinx_function': 'time_series', 'jinx_function': 'clustering', 'jinx_function': 'arima', 'jinx_function': 'prophet', 'jinx_function': 'prophet_forecast', 'jinx_function': 'prophet_forecast_plot', 'jinx_function': 'prophet_forecast_plot_interactive', 'jinx_function': 'prophet_forecast_plot_interactive_plotly'})
# def calculations(jinx_function):
#     # Render the linear_regression.html template
#     return T('<jinx_function>.html')

# Run the app on the local development server
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)