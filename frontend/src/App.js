import React, { useState, useEffect } from "react"
import './App.css';

function App() {

  // state variable for data
  const [data, setData] = useState([])
  const [currencyCode, setCurrencyCode] = useState('CAD');
  const [currencySymbol, setCurrencySymbol] = useState('$');

  // GET request
  const fetchAssets = () => {
    fetch(`http://localhost:5000/-net-worth/users/150397569105386686797786709197469348192/assets/`, {mode:"cors"})
      .then(res => res.json())
      .then(json => setData(json))
  }

  // PUT request for currency change
  const fetchCurrency = (data) => {
    console.log(JSON.stringify(data))
    fetch("http://localhost:5000/-net-worth/users/150397569105386686797786709197469348192/", {
      method: "put",
      mode: "cors",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "PUT",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Max-Age" : 86400,
        "Access-Control-Allow-Private-Network": true
      }
    })
    .then(res => res.json())
  }

  useEffect(() => {
    // fetchAssets();
  }, []);

  const createAssets = () => {
    // assets
    var assetsData = {};

    var cashAndInvestmentsData = {};
    cashAndInvestmentsData.chequing = document.getElementById("chequingInput").value;
    cashAndInvestmentsData.savingsForTaxes = document.getElementById("savingsForTaxesInput").value;
    cashAndInvestmentsData.rainyDayFund = document.getElementById("rainyDayFundInput").value;
    cashAndInvestmentsData.savingsForFun = document.getElementById("savingsForFunInput").value;
    cashAndInvestmentsData.savingsForTravel = document.getElementById("savingsForTravelInput").value;
    cashAndInvestmentsData.savingsForPersonalDevelopment = document.getElementById("savingsForPersonalDevelopmentInput").value;
    cashAndInvestmentsData.investment1 = document.getElementById("investment1Input").value;
    cashAndInvestmentsData.investment2 = document.getElementById("investment2Input").value;
    cashAndInvestmentsData.investment3 = document.getElementById("investment3Input").value;

    var longTermAssetsData = {};
    longTermAssetsData.primaryHome = document.getElementById("primaryHomeInput").value;
    longTermAssetsData.secondHome = document.getElementById("secondHomeInput").value;
    longTermAssetsData.other = document.getElementById("otherInput").value;

    assetsData.cashAndInvestments = cashAndInvestmentsData;
    assetsData.longTermAssets = longTermAssetsData;

    return assetsData;
  }

  const createLiabilities = () => {
    // liabilities
    var liabilities = {}
    var shortTermLiabilities = {};
    shortTermLiabilities.creditCard1 = document.getElementById("creditCard1Input").value;
    shortTermLiabilities.creditCard2 = document.getElementById("creditCard2Input").value;

    var longTermDebt = {};
    longTermDebt.mortgage1 = document.getElementById("mortgage1Input").value;
    longTermDebt.mortgage2 = document.getElementById("mortgage2Input").value;
    longTermDebt.lineOfCredit = document.getElementById("lineOfCreditInput").value;
    longTermDebt.investmentLoan = document.getElementById("investmentLoanInput").value;

    liabilities.shortTermLiabilities = shortTermLiabilities;
    liabilities.longTermDebt = longTermDebt;

    return liabilities;
  }

  const createCurrency = () => {
    var currencyData = {};
    currencyData.currencyCode = currencyCode;
    currencyData.currencySymbol = currencySymbol;

    return currencyData;
  }

  // POST: the data should consist of assets + liabilities + currency
  // other REQ: assets + liabilities + currency + userId
  const createData = (requestType) => {

    // get the user data
    let assets = createAssets();
    let liabilities = createLiabilities();
    let currency = createCurrency()

    // create a JSON object for request
    let data = {}
    data.assets = assets;
    data.liabilities = liabilities;
    data.currency = currency;

    if (requestType !== "POST") {
      // hardcoded user
      data.userId = 150397569105386686797786709197469348192
    }
    return data
  }

  // POST request - made when the page loads initially
  // should recieve calculated totals - display them
  // data = urserId + currency +
  const fetchTotals = () => {
    let reqData = createData("POST");
    console.log(reqData);
    fetch("http://localhost:5000/-net-worth/assets/", {
      method: "POST",
      mode : "cors",
      body: JSON.stringify(reqData)
    })
    .then(res => res.json())
    .then(json => setData(json))
    .then(console.log(data))
  }

  const handleDropDown = (e) => {
    setCurrencyCode(e.target.value);
    let assets = createAssets();
    let currency = createCurrency();
    var data = {};
    data.assets = assets;
    data.currency = currency;
    fetchCurrency(data);
  }

  return (
    <div className="App">
      <h1>Tracking Your Networth</h1>
      {/* TODO: add currency dropdown here */}
      <div className="dropDown">
        <label>
          <select value={currencyCode} onChange={handleDropDown}>
            <option value="CAD">CAD</option>
            <option value="INR">INR</option>
            <option value="USD">USD</option>
          </select>
        </label>
      </div>
      {/* TODO: make total net worth here side by side */}
      <div>
        <h3>Total Networth</h3>
        <p>232323.00</p>
      </div>
      <h3>Assets</h3>
          <table>
            <tbody>
              <tr>
                <th>Cash and Investments</th>
              </tr>
              <tr>
                <td>Chequing</td>
                <td><div>$<input type="text" id="chequingInput" name="chequingInput" defaultValue={2000.00} required></input></div></td>
              </tr>
              <tr>
                <td>Savings for Taxes</td>
                <td><div>$<input type="text" id="savingsForTaxesInput" name="savingsForTaxes" defaultValue={4000.00}></input></div></td>
              </tr>
              <tr>
                <td>Rainy Day Fund</td>
                <td><div>$<input type="text" id="rainyDayFundInput" name="rainyDayFund" defaultValue={506.00}></input></div></td>
              </tr>
              <tr>
                <td>Savings for Fun</td>
                <td><div>$<input type="text" id="savingsForFunInput" name="savingsForFun" defaultValue={5000.00}></input></div></td>
              </tr>
              <tr>
                <td>Savings for Travel</td>
                <td><input type="text" id="savingsForTravelInput" name="savingsForTravel" defaultValue={400.00}></input></td>
              </tr>
              <tr>
                <td>Savings for Personal Development</td>
                <td><input type="text" id="savingsForPersonalDevelopmentInput" name="savingsForPersonalDevelopment" defaultValue={200.00}></input></td>
              </tr>
              <tr>
                <td>Investment 1</td>
                <td><input type="text" id="investment1Input" name="investment1" defaultValue={5000.00}></input></td>
              </tr>
              <tr>
                <td>Investment 2</td>
                <td><input type="text" id="investment2Input" name="investment2" defaultValue={60000.00}></input></td>
              </tr>
              <tr>
                <td>Investment 3</td>
                <td><input type="text" id="investment3Input" name="investment3" defaultValue={24000.00}></input></td>
              </tr>
              <tr>
                <th>Long Term Assets</th>
              </tr>
              <tr>
                <td>Primary Home</td>
                <td><input type="text" id="primaryHomeInput" name="primaryHome" defaultValue={455000.00}></input></td>
              </tr>
              <tr>
                <td>Second Home</td>
                <td><input type="text" id="secondHomeInput" name="secondHome" defaultValue={1564321.00}></input></td>
              </tr>
              <tr>
                <td>Other</td>
                <td><input type="text" id="otherInput" name="other" defaultValue={0.00}></input></td>
              </tr>
              <tr>
                <th>Total Assets</th>
                <td id="totalAssets">0.00</td>
              </tr>
            </tbody>
        </table>
        <button onClick={() => createAssets()}> Calculate Assets </button>
      <h3>Liabilities</h3>
      <table>
        <tbody>
          <tr>
            <th>Short Term Liabilities</th>
            <th>Monthly Payment</th>
          </tr>
          <tr>
            <td>Credit Card 1</td>
            <td><div>$ 200.00</div></td>
            <td><div><input type="text" id="creditCard1Input" name="creditCard1Input" defaultValue={4342.00}></input></div></td>
          </tr>
          <tr>
            <td>Credit Card 2</td>
            <td><div>$ 150.00</div></td>
            <td><div><input type="text" id="creditCard2Input" name="creditCard2Input" defaultValue={322.00}></input></div></td>
          </tr>
          <tr>
            <th>Long Term Debt</th>
          </tr>
          <tr>
            <td>Mortage 1</td>
            <td><div>$ 2000.00</div></td>
            <td><div><input type="text" id="mortgage1Input" name="mortgage1InputInput" defaultValue={250999.00}></input></div></td>
          </tr>
          <tr>
            <td>Mortage 2</td>
            <td><div>$ 3500.00</div></td>
            <td><div><input type="text" id="mortgage2Input" name="mortgage2Input" defaultValue={632634.00}></input></div></td>
          </tr>
          <tr>
            <td>Line Of Credit</td>
            <td><div>$ 500.00</div></td>
            <td><div><input type="text" id="lineOfCreditInput" name="lineOfCreditInput" defaultValue={10000.00}></input></div></td>
          </tr>
          <tr>
            <td>Investment Loan</td>
            <td><div>$ 700.00</div></td>
            <td><div><input type="text" id="investmentLoanInput" name="investmentLoanInput" defaultValue={10000.00}></input></div></td>
          </tr>
          <tr>
            <th>Total Liabilities</th>
            <tr></tr>
            <td id="totalLiabilities">0.00</td>
          </tr>
        </tbody>
      </table>
      <button onClick={() => createLiabilities()}> Calculate Liabilities </button>
      <button onClick={() => fetchTotals()}>Calculate Totals</button>
    </div>
  );
}

export default App;
