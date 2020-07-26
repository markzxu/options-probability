import pandas as pd
import numpy as np
import yfinance as yf


def op_ch_to_cdf(calls):
    """
    :param calls: Calls of an option chain
    :return: Probability distribution as a pandas dataframe
    """

    mid = calls['mid'] = [(b+a)/2 for b, a in zip(calls['bid'], calls['ask'])]

    # theoretical price of 0 call ~= price of lowest call + (lowest strike)/contract size
    # theoretical price of infinity call ~= 0
    contract_size = 100 if calls.contractSize[0] == "REGULAR" else 0 # fix
    zero_call = mid[0] + calls['strike'][0] / contract_size
    probs = [cur-nxt for cur, nxt in zip([zero_call] + mid, mid+[0])]

    # normalize
    s = sum(probs)
    probs = [x/s for x in probs]

    range = [0] + calls['strike'].to_list()

    return pd.DataFrame(
        data={'range_start': range, 'prob' : probs }
    )

def get_option_chain(symbol, date=None):
    """
    :param symbol: a ticker symbol
    :return: Option chain for that ticker symbol
    """
    ticker = yf.Ticker(symbol)
    option_chain = ticker.option_chain(date)
    return option_chain.calls


def cdf(symbol, date=None):
    return op_ch_to_cdf(get_option_chain(symbol, date))