def direction_identifier(sum_1, sum_2):
    # 0° case
    if sum_2 >= 9*sum_1:
        return 0
    # 30° case
    elif sum_2 > 1.8*sum_1 and sum_2 < 9*sum_1:
        return 30
    # 45° case
    elif sum_2 > (sum_1-(sum_1*0.6)) and sum_2 <= 1.8*sum_1:  
        return 45
    # 60° case
    elif sum_1 > 1.8*sum_2 and sum_1 < 9*sum_2:
        return 60
    # 90° case
    elif sum_1 >= 9*sum_2:
        return 90
