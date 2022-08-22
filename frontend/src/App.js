import React, { useState, useEffect } from "react"
import './App.css';
import {netWorthData} from './data';


function App() {

  // state variable for data
  const [data, setData] = useState(netWorthData)

  // everytime data changes, update all field values
  useEffect(() => {

    if (data.userId !== null) {
      document.getElementById("userId").value = data.userId;
    }

    document.getElementById("chequing").value = data.assets.cashAndInvestments.chequing;
    document.getElementById("savingsForTaxes").value =  data.assets.cashAndInvestments.savingsForTaxes;
    document.getElementById("rainyDayFund").value = data.assets.cashAndInvestments.rainyDayFund;
    document.getElementById("savingsForFun").value = data.assets.cashAndInvestments.savingsForFun;
    document.getElementById("savingsForTravel").value =data.assets.cashAndInvestments.savingsForTravel;
    document.getElementById("savingsForPersonalDevelopment").value = data.assets.cashAndInvestments.savingsForPersonalDevelopment;
    document.getElementById("investment1").value = data.assets.cashAndInvestments.investment1;
    document.getElementById("investment2").value = data.assets.cashAndInvestments.investment2;
    document.getElementById("investment3").value = data.assets.cashAndInvestments.investment3

    document.getElementById("primaryHome").value = data.assets.longTermAssets.primaryHome;
    document.getElementById("secondHome").value = data.assets.longTermAssets.secondHome;
    document.getElementById("other").value = data.assets.longTermAssets.other;

    document.getElementById("totalAssets").innerHTML = data.currency.currencySymbol + data.assets.totalAssets;

    // liabilities
    document.getElementById("creditCard1").value = data.liabilities.shortTermLiabilities.creditCard1;
    document.getElementById("creditCard2").value = data.liabilities.shortTermLiabilities.creditCard2;

    document.getElementById("mortgage1").value = data.liabilities.longTermDebt.mortgage1;
    document.getElementById("mortgage2").value = data.liabilities.longTermDebt.mortgage2;
    document.getElementById("lineOfCredit").value = data.liabilities.longTermDebt.lineOfCredit;
    document.getElementById("investmentLoan").value = data.liabilities.longTermDebt.investmentLoan;

    document.getElementById("totalLiabilities").innerHTML = data.currency.currencySymbol + data.liabilities.totalLiabilities;


  }, [data]);

  // POST: the data should consist of assets + liabilities + currency
  // other REQ: assets + liabilities + currency + userId
  const createData = (requestType, dataType=null) => {
    // reate a JSON object for request

    if (requestType === "POST") {
      return data
    }

    if (dataType === null) {
      // currency exchange
      return data
    }

    let reqData = {};
    reqData.userId = data.userId;
    reqData.currency = data.currency;
    if (dataType === "assets") {
      reqData.assets = data.assets;
    } else {
      reqData.liabilities = data.liabilities;
    }
    return reqData
  }

  const fetchUser = (userId) => {
    if (userId === ''){
      console.log("No user Id provided")
      return
    }
    var apiCall = "http://localhost:5000/-net-worth/users/" + userId + "/"
    fetch(apiCall, {
      method: "GET",
      mode : "cors"
    })
    .then(res => {
      if (res.ok) {
        return res.json()
      }
      return Promise.reject(res)})
    .then(json => setData(json))
    .catch((error) => {
      console.log(error.status, error.statusText)
      error.json().then((json) => {
        console.log(json.errorMsg)
      })
    })
  }

    // POST request - made when the page loads initially
  // should recieve calculated totals - display them
  // data = urserId + currency + assets + liabilities
  const fetchTotals = (requestType, apiCall, dataType=null) => {
    /// make api call
    let reqData = createData(requestType, dataType);
    if (requestType !== "POST" && reqData.userId === undefined){
      console.log("No user Id provided")
      return
    }
    fetch(apiCall, {
      method: requestType,
      mode : "cors",
      body: JSON.stringify(reqData)
    })
    .then(res => {
      if (res.ok) {
        return res.json()
      }
      return Promise.reject(res)})
    .then(json => setData(json))
    .catch((error) => {
      console.log(error.status, error.statusText)
      error.json().then((json) => {
        console.log(json.errorMsg)
      })
    })
  }

  // PUT request for currency change
  const fetchCurrency = () => {
    let reqData = createData("PUT");
    if (reqData.userId === undefined){
      console.log("No user Id provided")
      return
    }
    var apiCall = "http://localhost:5000/-net-worth/users/" + data.userId + "/";
    fetch(apiCall, {
      method: "PUT",
      mode: "cors",
      body: JSON.stringify(reqData)
    })
    .then(res => {
      if (res.ok) {
        return res.json()
      }
      return Promise.reject(res)})
    .then(json => setData(json))
    .catch((error) => {
      console.log(error.status, error.statusText)
      error.json().then((json) => {
        console.log(json.errorMsg)
      })
    })
  }

  const checkKeyPressed = (e, dataType) => {
    /// checks which key was entered by user,
    /// if "enter", this function will call the API
    if (e.keyCode === 13) {
      e.preventDefault();
      let inputValue = e.target.value
      data[dataType][e.target.name][e.target.id] = inputValue ? inputValue : 0.00;
      var api = "http://localhost:5000/-net-worth/users/" + data.userId + "/" + dataType+ "/";
      fetchTotals("PUT", api, dataType)
    }
  }

  const handleDropDown = (e) => {
    data.currency.currencyCode = e.target.value;
    fetchCurrency();
  }

  const handleSubmit = (e) => {
    if (e.keyCode === 13) {
      fetchUser(e.target.value)
    }
  }

  return (
    <div className="App">
      <h1>Tracking Your Networth</h1>
      <div className="userId">
        <p>User Id:</p>
        <input id="userId" type="number" style={{border: '3px solid red'}} onKeyDown={(e) => handleSubmit(e)}></input>
      </div>
      <br></br>
      <div className="dropDown">
        <label>
          <select value={data.currency.currencyCode} onChange={handleDropDown}>
            <option value="CAD">CAD</option>
            <option value="INR">INR</option>
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
            <option value="CHF">CHF</option>
            <option value="GBP">GBP</option>
            <option value="SGD">SGD</option>
            <option value="AUD">AUD</option>
            <option value="NZD">NZD</option>
            <option value="BRL">BRL</option>
          </select>
        </label>
      </div>
      {/* TODO: make total net worth here side by side */}
      <div className="totalNetWorthDiv">
        <p className="totals"> <b>Total Networth:</b> {data.netWorth}</p>
      </div>
      <h3>Assets</h3>
          <table>
            <tbody>
              <tr>
                <th>Cash and Investments</th>
              </tr>
              <tr>
                <td>Chequing</td>
                <td><div className="inputField">{data.currency.currencySymbol}<input type="number" id="chequing" name="cashAndInvestments" onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <td>Savings for Taxes</td>
                <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="savingsForTaxes" name="cashAndInvestments"  onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <td>Rainy Day Fund</td>
                <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="rainyDayFund" name="cashAndInvestments" onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <td>Savings for Fun</td>
                <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="savingsForFun" name="cashAndInvestments" onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <td>Savings for Travel</td>
                <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="savingsForTravel" name="cashAndInvestments" onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <td>Savings for Personal Development</td>
                <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="savingsForPersonalDevelopment" name="cashAndInvestments" onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <td>Investment 1</td>
                <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="investment1" name="cashAndInvestments" onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <td>Investment 2</td>
                <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="investment2" name="cashAndInvestments" onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <td>Investment 3</td>
                <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="investment3" name="cashAndInvestments" onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <th>Long Term Assets</th>
              </tr>
              <tr>
                <td>Primary Home</td>
                <td  className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="primaryHome" name="longTermAssets" onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <td>Second Home</td>
                <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="secondHome" name="longTermAssets" onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <td>Other</td>
                <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="other" name="longTermAssets" onKeyDown={(e) => checkKeyPressed(e, "assets")}></input></div></td>
              </tr>
              <tr>
                <th>Total Assets</th>
                <td id="totalAssets" className="totals"></td>
              </tr>
            </tbody>
        </table>
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
            <td  className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="creditCard1" name="shortTermLiabilities" onKeyDown={(e) => checkKeyPressed(e, "liabilities")}></input></div></td>
          </tr>
          <tr>
            <td>Credit Card 2</td>
            <td><div>$ 150.00</div></td>
            <td  className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="creditCard2" name="shortTermLiabilities" onKeyDown={(e) => checkKeyPressed(e, "liabilities")}></input></div></td>
          </tr>
          <tr>
            <th>Long Term Debt</th>
          </tr>
          <tr>
            <td>Mortage 1</td>
            <td><div>$ 2000.00</div></td>
            <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="mortgage1" name="longTermDebt" onKeyDown={(e) => checkKeyPressed(e, "liabilities")}></input></div></td>
          </tr>
          <tr>
            <td>Mortage 2</td>
            <td><div>$ 3500.00</div></td>
            <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="mortgage2" name="longTermDebt" onKeyDown={(e) => checkKeyPressed(e, "liabilities")}></input></div></td>
          </tr>
          <tr>
            <td>Line Of Credit</td>
            <td><div>$ 500.00</div></td>
            <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="lineOfCredit" name="longTermDebt" onKeyDown={(e) => checkKeyPressed(e, "liabilities")}></input></div></td>
          </tr>
          <tr>
            <td>Investment Loan</td>
            <td><div>$ 700.00</div></td>
            <td className="inputField"><div>{data.currency.currencySymbol}<input type="number" id="investmentLoan" name="longTermDebt" onKeyDown={(e) => checkKeyPressed(e, "liabilities")}></input></div></td>
          </tr>
          <tr>
            <th>Total Liabilities</th>
            <tr></tr>
            <td id="totalLiabilities" className="totals"></td>
          </tr>
        </tbody>
      </table>
      <button onClick={() => fetchTotals("POST", "http://localhost:5000/-net-worth/")}>Create New User</button>
    </div>
  );
}

export default App;
