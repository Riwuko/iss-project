import React from "react";
import { Line } from "react-chartjs-2";

const Chart = (props) => {
  const pickRandomColors = () => {
    const r = (Math.floor(Math.random() * (255 - 50)) + 50).toString();
    const g = (Math.floor(Math.random() * (255 - 50)) + 50).toString();
    const b = (Math.floor(Math.random() * (255 - 50)) + 50).toString();
    let colorValue = "rgba(" + r + "," + g + "," + b + ",1)";
    const backgroundColor = colorValue.slice(0, -2) + "0.6)";
    return {
      borderColor: colorValue,
      backgroundColor: backgroundColor,
    };
  };

  const preparePlotData = () => {
    let datasets = []
    for (const dataset of props.datasets){
      datasets.push({
        ...dataset,
        ...pickRandomColors(),
        pointHoverRadius: 10,
        pointHoverBackgroundColor: "rgba(75,192,192,1)",
      })
    }
    return {
      labels: props.labels,
      datasets: [
        ...datasets
      ],
    };
  };

  const preparePlotOptions = () => {
    return {
      responsive: true,
      maintainAspectRatio: true,
      legend: {
        labels: {
          fontColor: "white",
        },
      },
      title: {
        display: true,
        text: props.title,
        fontSize: 16,
        fontColor: "white",
      },

      tooltips: {
        cornerRadius: 10,
        titleAlign: "center",
        titleFontColor: "#fff",
        titleFontStyle: "bold",
      },
      scales: {
        xAxes: [
          {
            ticks: { fontColor: "white" },
            gridLines: {
              display: false,
            },
          },
        ],
        yAxes: [
          {
            ticks: { fontColor: "white" },
            gridLines: {
              display: false,
            },
          },
        ],
      },
    };
  };

  return (
    <Line
      data={preparePlotData()}
      responsive={true}
      options={preparePlotOptions()}
    />
  );
};

export default Chart;
