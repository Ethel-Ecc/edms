from flask import Flask, render_template, url_for

app = Flask(__name__)

"""
    A dataset list of doctionaries, where each dictionary represents a single dataset
"""
datasets =[
    {
        'owner': 'Ethelbert obinna',
        'name_or_title': 'Dataset 1',
        'distribution_license': 'MIT',
        'format': 'XLSX',
        'description': 'A population dataset for county X, NRW',
        'download_url': 'https://ckan-wit-documentation.readthedocs.io/_/downloads/en/latest/pdf/',
        'date_added': '21 April, 2020',
    },
    {
        'owner': 'Sven Bingert',
        'name_or_title': 'Dataset 2',
        'distribution_license': 'Open Source',
        'format': 'PDF',
        'description': 'Dataset for students experiments, Göttingen',
        'download_url': 'https://ckan-wit-documentation.readthedocs.io/_/downloads/en/latest/pdf/',
        'date_added': '23 July, 2020',
    }

]


"""
    This route and method handles the contents of the landing/homepage
    :returns The homepage using the contents from the home page templates
"""
@app.route('/')
@app.route('/home')
def homepage():
    return render_template('pages/home.html', datasets=datasets)


"""
    This route and method handles the contents of the about page
    :returns The about page, using the contents from the about page templates
"""
@app.route('/about')
def about():
    return render_template('pages/about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)
