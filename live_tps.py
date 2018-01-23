'''
Live TPS counter on the RaiBlocks Network.
Requires a rai_node that response to callbacks

run:
    python live_tps --help
for user-configurable options

In the rai_node config.json set:
    "callback_address":"<IP address of the computer running this script>",
    "callback_port":"<port you want to use>"

So to use the default paremeters, set
    "callback_address":"127.0.0.1",
    "callback_port":"17076"
'''

import argparse
import json
import time
from threading import Thread

from pprint import pprint
from http.server import HTTPServer, BaseHTTPRequestHandler

transaction_count = 0

def parse_args():
    ''' Parse CLI arguments into an object and a dictionary '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', type=str,
            default='127.0.0.1',
            help='Rai_node address')
    parser.add_argument('-p', '--port', type=int,
            default=17076,
            help='Rai_node callback port')
    parser.add_argument('-t', '--period', type=float,
            default=1.0,
            help='Type period to average over (in seconds)')
    parser.add_argument('-d', '--human', action='store_true',
            help='Print Date in human-readable format')

    args = parser.parse_args()
    dargs = vars(args)
    return (args, dargs)

class BlockHandler(BaseHTTPRequestHandler):
    '''
    Not used in this program, but is a good example on how to handle callback
    Parses the incoming block as a dictionary.
    '''
    def do_POST(self):
        print('got post!')
        content = self.rfile.read(int(self.headers['Content-Length']))
        content_dict = json.loads(content)
        content_dict['block'] = json.loads(content_dict['block'])
        pprint(content_dict)
        return

class BlockCounterHandler(BaseHTTPRequestHandler):
    '''
    Increments transaction counter when POST request received on port
    '''
    def do_POST(self):
        global transaction_count
        transaction_count += 1
        return

def main():
    args, dargs = parse_args()

    print('RaiBlocks TPS Counter')
    server_address = (args.address, args.port)
    block_listener = HTTPServer(server_address, BlockCounterHandler)
    Thread(target=block_listener.serve_forever).start()

    previous_count_pre = 0
    previous_count_post = 0
    while True:
        time.sleep(args.period)

        # Compute TPS
        previous_count_pre = transaction_count
        n_trans_since_prev = transaction_count - previous_count_post
        tps = n_trans_since_prev / args.period
        previous_count_post = previous_count_pre

        if args.human:
            current_time = time.ctime()
        else:
            current_time = "%.4f" % time.time()

        print("Time: %20s    Total: %7d    TPS: %.2f" %
                (current_time, transaction_count, tps))

if __name__=='__main__':
    main()
