import time
from config import TEST_ACCT_KEY, TEST_NETWORK
from firefly_exchange_client import FireflyClient
from constants import Networks
from enumerations import MARKET_SYMBOLS, ORDER_SIDE, ORDER_TYPE
from pprint import pprint
import asyncio


async def main():

    # initialize client
    client = FireflyClient(
        True, # agree to terms and conditions
        Networks[TEST_NETWORK], # network to connect with
        TEST_ACCT_KEY, # private key of wallet
        True, # on boards user on firefly. Must be set to true for first time use
        )

    # must add market before cancelling its orders
    client.add_market(MARKET_SYMBOLS.ETH)



    order = {
        "symbol":MARKET_SYMBOLS.ETH, 
        "price":1301, 
        "quantity":0.1, 
        "side":ORDER_SIDE.SELL, 
        "orderType":ORDER_TYPE.LIMIT,
        "leverage":await client.get_user_leverage(MARKET_SYMBOLS.ETH),
        "expiration":int(time.time()+(30*24*60*60)), # a random time in future
        "reduceOnly":False,
        "salt":10,
        "postOnly":True
    }


    signed_order = client.create_signed_order(order);
    resp = await client.post_signed_order(signed_order)
    
    
    # sign order for cancellation using order hash
    # you can pass a list of hashes to be signed for cancellation, good to be used when multiple orders are to be cancelled
    cancellation_request = client.create_signed_cancel_orders(MARKET_SYMBOLS.ETH, order_hash=[resp['hash']])
    pprint(cancellation_request)

    # # or sign the order for cancellation using order data
    cancellation_request = client.create_signed_cancel_order(order)
    pprint(cancellation_request) # same as above cancellation request

    # post order to exchange for cancellation
    resp = await client.post_cancel_order(cancellation_request)
    
    pprint(resp)

    # cancels all open orders, returns false if there is no open order to cancel
    resp = await client.cancel_all_open_orders(MARKET_SYMBOLS.ETH)

    if resp == False:
        print('No open order to cancel')
    else:
        pprint(resp)

if __name__ == "__main__":
    asyncio.run(main())