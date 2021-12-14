
import requests

print("ping database")
QUERY_LINK = 'http://server1.jinhoko.com:30006'
response = requests.get(QUERY_LINK + '/ping')
assert response.status_code == 204, "cannot ping database"

DB_NAME = 'sensor'
TABLE_NAME = 'pos'

def upload_pos(data):

    ts, beacon, xpos, ypos, prob = data # (423942348, 'B001', 0.5, 3.3, 0.5)
    ts = ts * 1000000
    qstr = ''
    qstr += f'{TABLE_NAME},beacon={beacon} x={xpos},y={ypos},prob={prob} {ts} \n'
    print(qstr)

    res = requests.post(url=QUERY_LINK + f'/write?db={DB_NAME}&epoch=us',
                        data=qstr,
                        headers={'Content-Type': 'application/octet-stream'}
    )
    print(res.status_code)
    print(res.content)

upload_pos( (1638920603288, 'B111', 0.5, 3.3, 0.5) )