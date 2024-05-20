import zmq


def request_balances(age, retirement_age, initial_401k_balance, employer_contribution,
                     salary, individual_contribution, roth_balance, roth_return,
                     roth_contributions, brokerage_balance, brokerage_return,
                     brokerage_contributions):
    """
    Request future balances from the microservice.
    Connects to the microservice using ZeroMQ.
    """
    # Request socket for client and connect to server
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Prepare the request data
    request_data = {
        'age': age,
        'retirement_age': retirement_age,
        'initial_401k_balance': initial_401k_balance,
        'employer_contribution': employer_contribution,
        'salary': salary,
        'individual_contribution': individual_contribution,
        'roth_balance': roth_balance,
        'roth_return': roth_return,
        'roth_contributions': roth_contributions,
        'brokerage_balance': brokerage_balance,
        'brokerage_return': brokerage_return,
        'brokerage_contributions': brokerage_contributions
    }

    # Send request, receive response, and return response as JSON
    socket.send_json(request_data)
    response = socket.recv_json()
    return response


if __name__ == "__main__":
    # Example call to request balances
    result = request_balances(30, 65, 10000, 5, 50000, 5, 2000, 7, 6000, 5000, 8, 10000)

    # User-friendly format of received response from microservice
    print("Here are your projected future balances for each decade until retirement:")
    for label, balances in result.items():
        print(f"{label}:")
        for account, balance in balances.items():
            print(f"  {account}: {balance}")
        print()
