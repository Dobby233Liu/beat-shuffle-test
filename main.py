from lib import make_lemonade
import a_cybers_world
import sys

x = 0

try:
    print(make_lemonade(a_cybers_world.song))
except:
    x = 1
    raise
finally:
    sys.exit(x)
