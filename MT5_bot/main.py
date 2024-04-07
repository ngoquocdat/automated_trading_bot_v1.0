import os
import json

# Custom imports
import mt5_lib
import pandas

# Location of settings.json
settings_filepath = "settings.json"

## Function to retrieve setting information
def get_project_settings(import_filepath):
    """
    Function to import settings from settings.json
    :param import_filepath: path of settings.json file
    :return settings as a dictionary object
    """

    # Test the filepath to make sure it exists
    if os.path.exists(import_filepath):
        # If yes, import the file
        f = open(import_filepath, "r")
        # Read the information
        project_settings = json.load(f)
        # Close the file
        f.close()
        # Return the project_settings
        return project_settings
    # Notify user if settings.json doesn't exist
    else: 
        raise ImportError("settings.json does not exist at provided location")
    

## Function to repeat startup procedures
def start_up(project_settings):
    """
    Function to manage start up procedures for App. Includes staring/testing
    initializing symbols and anything else to ensure app start is successful.
    :param project_settings: json object of th project settings
    :return: Boolean. True if app start up is successful, False if not.
    """

    # Start MetaTrader 5
    startup = mt5_lib.start_mt5(project_settings= project_settings)
    # If startup successful, let user know
    if startup:
        print("MetaTrader startup successful")
        # Initialize symbols
        # Extract symbols from project_settings
        symbols = project_settings["mt5"]["symbols"]
        # Iterate through the symbols to enable
        for symbol in symbols:
            outcome= mt5_lib.initialize_symbol(symbol)
            if outcome is True:
                print(f"Symbol {symbol} initialized")
            else:
                raise Exception(f"{symbol} not initialized")
        return True
    # Default return  is false
    return False
    

## Main function
if __name__ == '__main__':
    print("Let's build an trading bot")
    # Import settings.json
    project_settings = get_project_settings(import_filepath= settings_filepath)
    # Test startup
    startup = mt5_lib.start_mt5(project_settings= project_settings)
    print(startup)
    ## Test if initialize symbol works
    # init_symbol =  mt5_lib.initialize_symbol("BTCUSDm")
    # print("Initialize Symbol outcome: ", init_symbol)

    # For each symbol, return a dataframe of the candles 
    symbols = project_settings['mt5']['symbols']
    for symbol in symbols:
        print(f"Symbol: {symbol}")
        candlesticks = mt5_lib.get_candlesticks(
            symbol= symbol,
            timeframe= project_settings['mt5']['timeframe'],
            number_of_candles= 50000
        )
        # Make it so that all columns are shown
        pandas.set_option("display.max_columns", None)

        print(candlesticks)