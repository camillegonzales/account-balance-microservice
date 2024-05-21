# Account Balance Microservice

This microservice calculates future balances for 401k, Roth IRA, and Brokerage accounts for each decade until retirement. It uses ZeroMQ for communication.

## How to Run the Microservice
1. Clone the repository and run it locally
2. Install dependencies:\
   Make sure you have `pyzmq` installed. You can install it using pip:
   ```bash
   pip install pyzmq
3. Run the microservice:
   ```bash
   python microservice.py

## How to REQUEST Data From the Microservice
### Request Data
To request data from the microservice, connect to the ZeroMQ socket, and send a JSON object with the following parameters:
- age: Current age of the user (integer)
- retirement_age: Projected retirement age of the user (integer)
- initial_401k_balance: Current 401k balance (float)
- employer_contribution: Employer's contribution percentage to 401k (float)
- salary: Current salary (float)
- individual_contribution: Individual's contribution percentage to 401k (float)
- roth_balance: Current Roth IRA balance (float)
- roth_return: Projected Roth IRA rate of return (float)
- roth_contributions: Yearly contribution to Roth IRA (float)
- brokerage_balance: Current brokerage account balance (float)
- brokerage_return: Projected brokerage account rate of return (float)
- brokerage_contributions: Yearly contribution to brokerage account (float)
### Example Request
```python
def request_balances(age, retirement_age, initial_401k_balance, employer_contribution,
                     salary, individual_contribution, roth_balance, roth_return,
                     roth_contributions, brokerage_balance, brokerage_return,
                     brokerage_contributions):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

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

    socket.send_json(request_data)
    response = socket.recv_json()


# Example request
request_balances(30, 65, 10000, 5, 50000, 5, 2000, 7, 6000, 5000, 8, 10000)
```
## How to RECEIVE Data From the Microservice
The data from the microservice will be received as a JSON object containing the future balances for each decade until retirement. This is done with the line from the example request code above: 
```python
response = socket.recv_json()
```
In the test.py file you can see how I formatted the information received from the microservice to display to the command-line when running my test program.
### Example response
```json
{
    "10 years from now (40)": {
        "401(k) Balance": "$11,050.00",
        "Roth IRA Balance": "$2,140.00",
        "Brokerage Account Balance": "$6,480.00",
        "Total Balance": "$19,670.00"
    },
    "20 years from now (50)": {
        "401(k) Balance": "$23,512.00",
        "Roth IRA Balance": "$4,579.00",
        "Brokerage Account Balance": "$13,773.00",
        "Total Balance": "$41,864.00"
    },
    ...
}
```
## UML Sequence Diagram
<img width="750" alt="Screenshot 2024-05-20 at 8 12 34 PM" src="https://github.com/camillegonzales/investment-microservice/assets/122317193/70dd3129-5867-4809-82fc-0935f1405fd1">
