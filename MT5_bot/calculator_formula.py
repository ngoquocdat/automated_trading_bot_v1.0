## EMA Formula:

def Calculator_EMA():
    """
    Formula to calculate EMA numbers
    :param EMA: Today EMA points
    :param Today_EMD: Current EMA price 
    :param Yesterday_EMA: Yesterday EMA price
    """

    Today_price = 0
    Multiplier = 1
    Yesterday_price = 1

    EMA = (Today_price * Multiplier) + Yesterday_price * (1 - Multiplier)

    return EMA