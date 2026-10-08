"Something"
import pt1

pt1.init_kazoo_client()

ZKCONN: pt1.KazooClient = pt1.get_kazoo_client()
DATA, STAT = ZKCONN.get("/bogus-path")
