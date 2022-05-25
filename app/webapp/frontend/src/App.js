import React from "react";
import logo from "./assets/logo.png";
import { Line } from "react-chartjs-2";
import {
  CategoryScale,
  Chart as ChartJS,
  LinearScale,
  LineElement,
  PointElement,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      orders: [],
    };
  }

  loadOrders() {
    fetch(
      "http://" +
        process.env.REACT_APP_BACKEND_HOST +
        ":" +
        process.env.REACT_APP_BACKEND_PORT +
        "/give-me-everything-you-know/"
    )
      .then((result) => result.json())
      .then((result) => this.setState({ orders: result.results }));
  }

  getTotal() {
    return this.state.orders.reduce(
      (total, order) => total + order.price_usd,
      0
    );
  }

  getChartData() {
    const labels = [];
    const dataset = {};

    for (const order of this.state.orders) {
      if (!labels.includes(order.supply_date)) {
        labels.push(order.supply_date);
      }
    }

    labels.sort();

    for (const label of labels) {
      dataset[label] = 0;
    }

    for (const order of this.state.orders) {
      dataset[order.supply_date] += order.price_usd;
    }

    return {
      labels: labels,
      datasets: [
        {
          data: dataset,
          backgroundColor: "#84aee5",
          borderColor: "#84aee5",
          pointRadius: 0,
        },
      ],
    };
  }

  componentDidMount() {
    this.loadOrders();
    setInterval(this.loadOrders.bind(this), 5000);
  }

  render() {
    return (
      <React.Fragment>
        <div className="header">
          <img className="logo" src={logo} />
        </div>
        <div className="content">
          <div className="chart">
            <Line
              data={this.getChartData()}
              options={{ maintainAspectRatio: false }}
            />
          </div>
          <div className="data">
            <div className="total">
              <div className="total-header">Total, $</div>
              <div className="total-content">{this.getTotal().toFixed(2)}</div>
            </div>
            <div className="table">
              <table cellSpacing={0}>
                <thead>
                  <tr>
                    <th>№</th>
                    <th>заказ №</th>
                    <th>стоимость, $</th>
                    <th>стоимость, ₽</th>
                    <th>срок поставки</th>
                  </tr>
                </thead>
                <tbody>
                  {this.state.orders.map((order) => (
                    <tr key={order.order_id}>
                      <td>{order.table_id}</td>
                      <td>{order.order_id}</td>
                      <td>{order.price_usd.toFixed(2)}</td>
                      <td>{order.price_rub.toFixed(2)}</td>
                      <td>{order.supply_date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}
