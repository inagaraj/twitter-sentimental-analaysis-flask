from flask import Blueprint, request, render_template

from TwitApp.data import TwitterMain
from TwitApp.forms import TweetForm

tweet = Blueprint('tweet', __name__)

title = 'Twitter Sentimental  Analysis'

@tweet.route('/')
def my_home():
    return render_template('home.html', title=title)



@tweet.route('/end')
def my_end():
    return render_template('endpage.html', title=title)

@tweet.route('/go')
def my_form():
    form = TweetForm(request.form)
    return render_template('index.html', title=title, form=form)

@tweet.route('/go', methods=['POST'])
def my_form_post():
    text = request.form['search_key']
    count = int(request.form['tweet_count'])
    twit_main = TwitterMain()
    tweets = twit_main.get_results(text, count)
    return render_template('disp.html', title=title,limit=count,
                           search_key=text, render_list=tweets)


@tweet.route('/analysis/<key>/<limit>')
def analysis(key,limit):
    pos,neu,neg  = TwitterMain.get_analysis_data(key,limit)
    return render_template('analysis.html', title=title,
                           search_key=key, pos=pos, neu=neu,neg=neg)

    