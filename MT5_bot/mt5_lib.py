import MetaTrader5 as mt5
import pandas

def start_mt5(project_settings):
    """
    Function to start MetaTrader5
    :param project_settings: json object with username, password, server, file location
    :return Boolean. True = started, False = not started
    """

    # Ensure that all variables are set/formatted to the correct type
    login_username = project_settings['mt5']['login']['username']
    login_username = int(login_username)
    login_password = project_settings['mt5']['login']['password']
    login_server = project_settings['mt5']['login']['server']

    username = project_settings['mt5']['account']
    password = project_settings['mt5']['password']
    mt5_pathway = project_settings['mt5']['mt5_pathway']

    # Attempt to initialize MT5
    mt5_init = False
    try:
        mt5_init = mt5.initialize()
    # Handle any errors:
    except Exception as e:
        print(f"Error initialization MetaTrader5: {e}")
        # Return False
        mt5_init = False

    # If MT5 initialized, attempt to login to MT5
    mt5_login = False
    if mt5_init:
        # Attempt login
        print('Initialize MT5 succeed: ', mt5_init)
        try:
            print('Attempt to log in trading broker account')
            mt5_login = mt5.login(
                login=login_username,
                password=login_password,
                server=login_server
            )
        # Handle exception
        except Exception as e:
            print(f"Error logging into MetaTrader5: {e}")
            mt5_login = False
    # Return the outcome to the user
    if mt5_login:
        print('Initialize & login statuses: ', mt5_init, mt5_login)
        return True
    # Default outcome
    print('Failed statuses: ', mt5_init, mt5_login)
    return False

## Function to initialize a symbol on MT5
def initialize_symbol(symbol):
    """
    Function to initialize a symbol on MT%. Assumes that MT5 has already been started
    :param symbol: string of symbol. Note that most MT5 brokers denote a 'raw' symbol differently
    :return: Boolean, True if  initialized, False if not
    """
    # Step 1: Check if symbol exists on 'your' MT5
    all_symbols = mt5.symbols_get()
    # Create a list to store all symbol names
    symbol_names = []
    # Add all symbol names to the list
    for sym in all_symbols:
        symbol_names.append(sym.name)

    # Check th symbol string to see if it exists in the list of names
    if symbol in symbol_names:
        # If symbol exists, attempt to initialize
        try: 
            mt5.symbol_select(symbol, True) # Arguments can not be declare here or an error will be thrown.
            return True
        except Exception as e:
            print(f"Error enabling {symbol}. Error: {e}")
            # Great place for some custom error handling
            return False
    else:
        print(f"Symbol {symbol} does not exist on this version of MT5. Update symbol name.")
        return False


## Function to query historic candlestick data from MT5
def get_candlesticks(symbol, timeframe, number_of_candles):
    """
    Function to retrieve a user-defined number of candles from MetaTrader 5. Initial upper set range to 
    50,000 as more requires changes to MetaTrader 5 defaults.
    :param symbol: string of the symbol being retrieved
    :param timeframe: string of the timeframe being retrieved
    :param number_of_candles: integer of number of candles to retrieve. Limited to 50,000
    :return: dataframe of the candlesticks
    """

    # Check that the number of candles is <= 50,000
    if number_of_candles > 50000:
        raise ValueError("No more 50,000 candles can be retrieve at this time")
    # Convert the timeframe into MT5 friendly format
    mt5_timeframe = set_query_timeframe(timeframe= timeframe)
    # Retrieve the data
    candles = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 1, number_of_candles)
    # Convert to a dataframe
    dataframe = pandas.DataFrame(candles)
    return dataframe



## Function to convert MT5 timeframe into MT5 object
def set_query_timeframe(timeframe):
    """
    Function to implement a conversion from a user-friendly timeframe string into a MT5 object. Note that the
    function implements a Pseudo  switch as Python version < 3.10 do not contain 'switch' functionality.
    :param timeframe: string of the timeframe
    :return: MT5 timeframe object
    """
    if timeframe == "M1":
        return mt5.TIMEFRAME_M1
    elif timeframe == "M5":
        return mt5.TIMEFRAME_M5
    elif timeframe == "M15":
        return mt5.TIMEFRAME_M15
    elif timeframe == "M30":
        return mt5.TIMEFRAME_M30
    elif timeframe == "H1":
        return mt5.TIMEFRAME_H1
    elif timeframe == "H4":
        return mt5.TIMEFRAME_H4
    else:
        print(f"Provide Timeframe is not exist or invalid: {timeframe}")
        return ValueError("Timeframe is invalid or not exist")


