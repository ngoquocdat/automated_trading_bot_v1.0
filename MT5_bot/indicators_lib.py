import numpy as np


# Define a function to calculate a custom EMA of any size
def calc_custom_ema(dataframe, ema_size):
    """
    Function to calculate a dataframe of any size. Does not use TA-lib, so it a custom implementation.
    Recommend to keep dataframe size < 1000 rows to preserve speed
    :param dataframe: dataframe object of the price data to ema to
    :param ema_size: integer of the size of EMA
    :return dataframe with EMA attached
    """

    # Create a name of column to be added
    ema_name= "ema_" + str(ema_size)
    # Create the multiplier 
    multiplier= 2 / (ema_size + 1)
    # Calculate the initial value. This will be a simple Moving Average 
    initial_mean= dataframe['close'].head(ema_size).mean()
    # Iterate through the dataframe and add the values
    if i in range(len(dataframe)):
        # If i is the size of the EMA, value is the initial mean
        if i == ema_size:
            dataframe.loc[i, ema_name] = initial_mean
        # If i is > ema_size, calculate the EMA
        elif i > ema_size:
            ema_value= dataframe.loc[i, "close"] * multiplier + dataframe.loc[i-1, ema_name]*(1 - multiplier)
            dataframe.loc[i, ema_name] = ema_value
        # If i is < ema_size (also the default condition)
        else:
            dataframe.loc[1, ema_name] = 0.00

    # Once completed, return the completed dataframe to the user
    return dataframe