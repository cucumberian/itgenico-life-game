import flask
import game_of_life

app = flask.Flask(__name__)

@app.route('/')
def get_index_page():
    
    game_of_life.GameOfLife(width=16, height=16)

    return flask.render_template(
        'index.html',
        page_title="life game"
    )


@app.route('/live')
def live():

    field = game_of_life.GameOfLife()
    field.form_new_generation()

    return flask.render_template(
        'live.html',
        gameobject=field
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
