from config import TEST_ACCT_KEY, TEST_NETWORK

import os,sys
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../src")))

from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS, SOCKET_EVENTS
from pprint import pprint

def callback(event):
    print("Event data:", event)

def main():

  # initialize client
  client = FireflyClient(
        True, # agree to terms and conditions
        Networks[TEST_NETWORK], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )

  # must open socket before subscribing
  print("Making socket connection to firefly exchange")
  client.socket.open()

  # subscribe to global event updates for BTC market 
  status = client.socket.subscribe_global_updates_by_symbol(MARKET_SYMBOLS.BTC)
  print("Subscribed to global BTC events: {}".format(status))

  client.socket.subscribe_user_update_by_token()
  print("Subscribed to user events")

  print("Listening to Orderbook updates")
  client.socket.listen(SOCKET_EVENTS.ORDERBOOK_UPDATE, callback)

  print("Listening to user order updates")
  client.socket.listen(SOCKET_EVENTS.ORDER_UPDATE, callback)

  # unsubscribe from global events
#   status = client.socket.unsubscribe_global_updates_by_symbol(MARKET_SYMBOLS.BTC)
#   print("Unsubscribed from global BTC events: {}".format(status))

#   # close socket connection
#   print("Closing sockets!")
#   client.socket.close()


if __name__ == "__main__":
    main()