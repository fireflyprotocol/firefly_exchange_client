'''
When ever the state of orderbook changes, an event is emitted by exchange.
In this code example we open a socket connection and listen to orderbook update event
'''
from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS, SOCKET_EVENTS
from interfaces import OrderSignatureRequest
from enumerations import MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE
import asyncio

client:FireflyClient = FireflyClient(
    True, # agree to terms and conditions
    Networks[TEST_NETWORK], # network to connect with
    TEST_ACCT_KEY, # private key of wallet
    True, # on boards user on firefly. Must be set to true for first time use
    )

client.add_market(MARKET_SYMBOLS.ETH)

def callback(event):
    print("Event data:", event)
    
    status = asyncio.run(client.socket.unsubscribe_global_updates_by_symbol(MARKET_SYMBOLS.ETH))
    print("Unsubscribed from orderbook update events for ETH Market: {}".format(status))

    # close socket connection
    print("Closing sockets!")
    asyncio.run(client.socket.close())

async def place_limit_order():
       
    # default leverage of account is set to 3 on firefly
    user_leverage = await client.get_user_leverage(MARKET_SYMBOLS.ETH)

    # creates a LIMIT order to be signed
    signature_request = OrderSignatureRequest(
        symbol=MARKET_SYMBOLS.ETH,  # market symbol
        price=1300,  # price at which you want to place order
        quantity=0.01, # quantity
        side=ORDER_SIDE.SELL, 
        orderType=ORDER_TYPE.LIMIT,
        leverage= user_leverage
    )  
    # create signed order
    signed_order = client.create_signed_order(signature_request);

    print("Placing a limit order")
    # place signed order on orderbook
    resp = await client.post_signed_order(signed_order)

    # returned order with PENDING state
    print(resp)
    return

async def main():

    # must open socket before subscribing
    print("Making socket connection to firefly exchange")
    await client.socket.open()

    # subscribe to global event updates for ETH market 
    await client.socket.subscribe_global_updates_by_symbol(MARKET_SYMBOLS.ETH)
    print("Subscribed to ETH Market events")

    print("Listening to ETH Orderbook update event")
    await client.socket.listen(SOCKET_EVENTS.ORDERBOOK_UPDATE.value, callback)

    await place_limit_order();

if __name__ == "__main__":
    asyncio.run(main())
