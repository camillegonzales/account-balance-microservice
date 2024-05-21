import zmq


def calculate_balances(age, retirement_age, initial_401k_balance, employer_contribution,
                       salary, individual_contribution, roth_balance, roth_return,
                       roth_contributions, brokerage_balance, brokerage_return,
                       brokerage_contributions):
    """
    Calculate future balances for 401k, Roth IRA, and Brokerage accounts.
    Returns the balances for each decade until retirement.
    """
    # Dictionary to store balances for each decade
    future_balances = {}

    # Initial balances
    future_brokerage_balance = brokerage_balance
    future_roth_balance = roth_balance
    future_401k_balance = initial_401k_balance

    # Start from current age and intialize decade tracker
    cur_age = age
    decade_counter = 0

    while cur_age < retirement_age:
        # Brokerage logic
        future_brokerage_balance *= (1 + brokerage_return / 100)
        future_brokerage_balance += brokerage_contributions

        # Roth IRA logic
        future_roth_balance *= (1 + roth_return / 100)
        future_roth_balance += roth_contributions

        # 401k logic
        future_401k_balance += ((1 + individual_contribution / 100) * salary) + ((1 + employer_contribution / 100) * salary)

        # Increment current age and decade counter
        cur_age += 1
        decade_counter += 1

        # Save total balance at the end of each decade
        if decade_counter % 10 == 0:
            years_from_now = decade_counter
            future_age = age + years_from_now
            total_balance = future_401k_balance + future_brokerage_balance + future_roth_balance
            future_balances[f"{years_from_now} years from now (age {future_age})"] = {
                "401(k) Balance": f"${future_401k_balance:,.2f}",
                "Roth IRA Balance": f"${future_roth_balance:,.2f}",
                "Brokerage Account Balance": f"${future_brokerage_balance:,.2f}",
                "Total Balance": f"${total_balance:,.2f}"
            }
    print(f"Response: \n    {future_balances} \n")
    return future_balances


def microservice():
    """
    Microservice to handle requests for calculating future balances.
    Uses ZeroMQ for communication.
    """
    # Reply socket for server and bind to port
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        # Receive request as JSON and extract parameters from received message
        message = socket.recv_json()
        print(f"Request: \n    {message} \n")

        age = message['age']
        retirement_age = message['retirement_age']
        initial_401k_balance = message['initial_401k_balance']
        employer_contribution = message['employer_contribution']
        salary = message['salary']
        individual_contribution = message['individual_contribution']
        roth_balance = message['roth_balance']
        roth_return = message['roth_return']
        roth_contributions = message['roth_contributions']
        brokerage_balance = message['brokerage_balance']
        brokerage_return = message['brokerage_return']
        brokerage_contributions = message['brokerage_contributions']

        # Perform balance calculations
        result = calculate_balances(age, retirement_age, initial_401k_balance, employer_contribution, salary,
                                    individual_contribution, roth_balance, roth_return, roth_contributions,
                                    brokerage_balance, brokerage_return, brokerage_contributions)

        # Send the result back as JSON
        socket.send_json(result)


if __name__ == "__main__":
    microservice()
