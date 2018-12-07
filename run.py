from app import app
import warnings

import views

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
