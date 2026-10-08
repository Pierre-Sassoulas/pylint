from typing import Dict
from typing import NewType


DatasetTags = NewType("DatasetTags", Dict[str,str])

test = DatasetTags({})
test['toast'] = 5
b = test['toast']
