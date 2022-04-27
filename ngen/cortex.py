from cortex4py.api import Api
from cortex4py.exceptions import NotFoundError
from cortex4py.models import Organization, User

api = Api('http://ngen-cortex:9001', 'ZcW+XONjDexzLsX5K5FBQ1cPfF18Ua3a')

try:
    api.organizations.get_by_id('ngen')
except NotFoundError:
    api.organizations.create(Organization({
        "name": "ngen",
        "description": "ngen default organization",
        "status": "Active"
    }))

try:
    user = api.users.get_by_id('user')
except NotFoundError:
    user = api.users.create(User({
        'login': 'user',
        'name': 'user',
        'roles': ['read', 'analyze', 'orgadmin'],
        'status': 'Ok',
        'organization': 'ngen'
    }))
    api.users.set_password(user.id, 'user')
    api.users.set_key(user.id)

default_analyzer_conf = {
    "configuration": {
        "auto_extract_artifacts": False,
        "check_tlp": True,
        "check_pap": True,
        "max_tlp": 2,
        "max_pap": 2
    },
    "jobCache": 10,
    "jobTimeout": 30,
}
api_user = Api('http://ngen-cortex:9001', api.users.get_key(user.id))

for analyzer in api_user.analyzers.definitions():
    if not analyzer.configurationItems and not api_user.analyzers.get_by_name(analyzer.id):
        api_user.analyzers.enable(analyzer.id, default_analyzer_conf)
