# freeze.py = frozen-flask for Vote Remain

from flask_frozen import Freezer

from allpages import app
import main

#---------------------------------------------------------------------

#app.config['FREEZER_BASE_URL'] = "http://localhost:9040/"
app.config['FREEZER_RELATIVE_URLS'] = True

freezer = Freezer(app)

@freezer.register_generator
def product_url_generator():
    # Return a list. (Any iterable type will do.)
    return [
        "index.html",
    ]

if __name__ == '__main__':
    freezer.freeze()

#end
