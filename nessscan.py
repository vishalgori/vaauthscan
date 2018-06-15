import os
from nessrest import ness6rest

scan = ness6rest.Scanner(url="https://ohcinnessusscan:8834", login=os.environ['username'], password=os.environ['password'], insecure=True)
