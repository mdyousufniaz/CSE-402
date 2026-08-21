from math import inf
from typing import Optional
from functools import partial

def main() -> None:
    N = 6 # Number of customers in total

    # Event lists
    INTER_ARRIVAL_TIMES = (0.4, 1.2, 0.5, 1.7, 0.2, 1.6, 0.2, 1.4, 1.9)
    SERVICE_TIMES = (2.0, 0.7, 0.2, 1.1, 3.7, 0.6)

    # System variables
    clock = 0.0 # Simulation clock
    server_status = 0 # { 0: idle, 1: busy}
    number_in_q = 0 # number of customers in queue
    arrival_list: list[float] = [] # list of arrival time of customers
    last_event_time = 0.0 # time instance when the last event occured

    customer_arrived = customer_departured = 0
    next_arrival = 0 + INTER_ARRIVAL_TIMES[customer_arrived]
    next_departure = inf

    number_delayed = 0 # number of customers pass the queue
    total_delay = 0 

    # areas
    area_qt = 0 # total area for delay function
    area_bt = 0 # total area for server function

    # print variables
    num_events = 0

    def common_update(new_clock_val: float) -> None:
        nonlocal clock
        nonlocal area_qt
        nonlocal area_bt
        nonlocal last_event_time
        
        last_event_time = clock
        clock = new_clock_val
        interval = clock - last_event_time

        area_qt += (number_in_q * interval)
        area_bt += (server_status * interval)

    tab_sep_print = partial(print, sep='\t')  
    round_2 = partial(round, ndigits=2)   
    tab_sep_print('e', 't', 'Type', 'Q', 'Delay', '# delayed')

    while number_delayed < N:
        num_events += 1
        is_arrival = next_arrival < next_departure
        q_old_val = number_in_q
        delay: Optional[int] = None

        if is_arrival:
            customer_arrived += 1
            common_update(next_arrival)
            
            if server_status == 0:
                server_status = 1
                number_delayed += 1
                delay = 0
                next_departure = clock + SERVICE_TIMES[customer_departured]
            else:
                number_in_q += 1
                arrival_list.append(clock)
            
            next_arrival = clock + INTER_ARRIVAL_TIMES[customer_arrived]

        # departure
        else:
            customer_departured += 1
            common_update(next_departure)

            if number_in_q > 0:
                number_delayed += 1
                delay = clock - arrival_list.pop(0)
                total_delay += delay
                number_in_q -= 1
                next_departure = clock + SERVICE_TIMES[customer_departured]
            else:
                server_status = 0
                next_departure = inf

        tab_sep_print(
            f'e{num_events}',
            round_2(clock),
            "{} C{}".format(
                *(
                    ('Arr', customer_arrived)
                    if is_arrival
                    else ('Dep', customer_departured)
                )
            ),
            f"{q_old_val} -> {number_in_q}",
            '---' if delay is None else round_2(delay),
            number_delayed
        )

    print(f"\nAvg delay in q: {round_2(total_delay / number_delayed)}")
    print(f"Time-avg number in q: {round_2(area_qt / clock)}")
    print(f"server utilization: {round_2(area_bt / clock)}")

if __name__ == '__main__': main()

