from flask import Flask,render_template,request
import pickle
import pandas as pd
import numpy as np
app = Flask(__name__)
similarity_score = pickle.load(open('similar.pkl','rb'))
popular_books = pd.read_csv('popular.csv')

books_copy = pd.read_csv('Books -Copy.csv')
isbn_data = pd.read_csv('isbn_data.csv')
pt = pd.read_csv('pt.csv')

@app.route('/')
def index():

    return render_template('index.html',data=False)

@app.route('/popular')
def popular():
    data = popular_books.to_dict('records')
    return render_template('popular.html',data=data)

@app.route('/recommend',methods=['post'])
def recommend():
    book_name = request.form.get('book_name')
    def recommend(book_name):
        try:
            try:
                book_name = isbn_data[isbn_data['ISBN']==book_name].iloc[0,2]
            
            except:
                pass
     
            
            index =np.where(pt['Book-Title'] == book_name)[0][0]
            books_list =sorted(list(enumerate(similarity_score[index])),key=lambda x :  x[1],reverse=True)[1:6]
            suggesions = []
            for i in books_list:

                suggesions.append(books_copy[books_copy['title']==pt['Book-Title'][i[0]]].drop_duplicates(['title']).to_dict('records')[0])

            return suggesions
        except:
            return False
    
    suggesions= recommend(book_name)
    if suggesions == False:
        error = True
    return render_template('index.html',data=suggesions,error=True)
if __name__=='__main__':
    app.run(debug=True)

