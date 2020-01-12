from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, validators
from tasks import start_received_request_action

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'


class ReusableForm(Form):
    link = TextField('Link:', validators=[validators.required()])
    file_name = TextField('File Name:', validators=[validators.required()])
    extension = TextField('Extension:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def download():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        link = request.form['link']
        file_name = request.form['file_name']
        extension = request.form['extension']
        if form.validate():
            request_data = {
                "link": link,
                "filename": file_name,
                "extension": extension,
                "download_dir": "/home/kuba/",
                "action": "download_request"
            }
            flash(start_received_request_action(request_data)['response'])
        else:
            flash('All Fields are Required')

    return render_template('/index.html', form=form)


@app.route('/task_table')
def check_status():
    status_request = {
        "action": "check_status"
    }
    tasks_data = start_received_request_action(status_request)

    return render_template('/task_table.html', tasks_data=tasks_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
