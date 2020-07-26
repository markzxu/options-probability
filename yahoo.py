import pandas as pd
import numpy as np
import yfinance as yf


def op_ch_to_cdf(calls):
    """
    :param calls: Calls of an option chain
    :return: Probability distribution as a pandas dataframe
    """
    calls = calls[calls.bid.notnull() & calls.ask.notnull()]

    print(calls.columns)
    now = pd.Timestamp.now()
    calls = calls.loc[calls.lastTradeDate.apply(lambda t: (now - t).days <= 3)]

    mid = [(b+a)/2 for b, a in zip(calls['bid'], calls['ask'])]

    # theoretical price of 0 call ~= price of lowest call + (lowest strike)/contract size
    # theoretical price of infinity call ~= 0
    assert all(calls.contractSize == "REGULAR")
    contract_size = 100
    zero_call = mid[0] + calls['strike'].iloc[0] / contract_size
    probs = [cur-nxt for cur, nxt in zip([zero_call] + mid, mid+[0])]

    strike = [0] + calls['strike'].to_list()
    # normalize
    s = sum(probs)
    probs = [x/s for x in probs]

    return pd.DataFrame(
        data={'range_start': strike, 'prob': probs}
    )


def get_option_chain(symbol, date=None):
    """
    :param symbol: a ticker symbol
    :param date: string in ISO format
    :return: Option chain for that ticker symbol
    """
    ticker = yf.Ticker(symbol)
    option_chain = ticker.option_chain(date)
    return option_chain.calls


def cdf(symbol, date=None):
    return op_ch_to_cdf(get_option_chain(symbol, date))


def get_dates(symbol):
    return yf.Ticker(symbol).options


if __name__ == "__main__":
    print(cdf("AAPL"))