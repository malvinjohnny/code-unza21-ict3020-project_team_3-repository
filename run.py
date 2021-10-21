# ? this file is what is started to run the app
# ? make suer the app is run in the virtual envirement 
# ! all dependacies should be installed using the pip install requirements.txt as the contents are too large to be commited to a remote
from app import app
# ends here
if __name__ == '__main__':
    app.run(debug=True)
