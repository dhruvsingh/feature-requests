from fr_app import app
from fr_app.settings import ProductionConf

app.config.from_object(ProductionConf)

import fr_app.views
