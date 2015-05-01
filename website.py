from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/<id>')
def main(id=0):

    # business_info = {business_id, business_name}
    business_info = dict([("1",'Taco Bell'), ("2","McDonald's")])

    # business_name = business name
    # business_name = business_info[id]

    # reviews = reviews of chosen restaurant
    reviews = ['Me like.', 'Tacos are good.']

    # menu = list of strings
    menu = ['Taco', 'Quesadilla']

    '''
    arg1 = dictionary
    arg2 = chosen business id
    arg3 = chosen business reviews
    arg4 = menu
    '''
    return render_template('index.html', business_info=business_info, id=id,
                           reviews=reviews, menu=menu)

if __name__ == '__main__':
    app.run(debug=True)