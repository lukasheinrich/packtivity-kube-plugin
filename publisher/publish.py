from packtivity.statecontexts.posixfs_context import LocalFSState
from packtivity.syncbackends import packconfig
from packtivity.syncbackends import publish as pack_publish
import json
import sys
import base64

data = json.loads(base64.b64decode(sys.stdin.read()))

localstate = LocalFSState(data['state']['readwrite'], data['state']['readonly'])
pubdata = pack_publish(data['pubspec'],data['parameters'],localstate, packconfig())
print(base64.b64encode(json.dumps(pubdata)))
