from session import *
from functools import wraps
from flask import Flask, session, render_template, redirect, request, flash, send_file


app = Flask(__name__)
app.secret_key = "forioe8tu43t90g[reogi;hfpi;rhbdv"
sessions = Sessions()

def check_token():
    return "token" in session and sessions.has(session["token"])


@app.route('/')
def index():
    return render_template("index.html", token=check_token())


@app.route("/new_session/")
def new_session():
    session_id = sessions.new()
    session["token"] = session_id
    if request.method == "POST":
        return session_id
    else:
        return redirect('/')


def require_token(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if check_token():
            return func(sessions.get(session["token"]), *args, **kwargs)
        flash("Вы не создали сессию.")
        return redirect("/", 403)
    return func_wrapper


def upload(func):
    @wraps(func)
    def upload_wrapper(session):
        file = request.files.get("file", default=None)
        if file.filename == "" or not file:
            flash("Вы не загрузили файл.")
            return redirect(request.url)
        new_name = session.gen_name(file.filename)
        file.save(new_name)
        func(session, new_name)
        flash("Файл успешно загружен")
        return redirect('/')
    return require_token(upload_wrapper)


@app.route("/load")
@require_token
def load(session):
    session.load_presets()
    flash("Данные загружены.")
    return redirect('/')


@app.route("/upload/calendar", methods=["POST"])
@upload
def upload_calendar(session, name):
    session.load_calendar(name)


@app.route("/upload/source", methods=["POST"])
@upload
def upload_calendar(session, name):
    session.load_source(name)


@app.route("/upload/facilities", methods=["POST"])
@upload
def upload_facilities(session, name):
    session.load_facilities(name)


@app.route("/upload/leaves", methods=["POST"])
@upload
def upload_leaves(session, name):
    session.load_mat(name)


@app.route("/compute")
@require_token
def compute(session):
    session.compute()
    flash("Файл успешно обработан.")
    return redirect('/')


def download(func):
    @wraps(func)
    def download_wrapper(session):
        file = func(session)
        return send_file(file, as_attachment=True)
    return require_token(download_wrapper)


@app.route("/download/result")
@download
def download_result(session):
    file = session.gen_name("out.xlsx")
    session.export(file)
    return file


@app.route("/download/report")
@download
def download_report(session):
    file = session.gen_name("report.txt")
    session.metrics(file)
    return file


if __name__ == '__main__':
    app.run()
