from app.models import Wxsetting
import json


q=Wxsetting().getsetting()

with open('Functional_status.JSON','w') as f:
    f.write(json.dumps(q))