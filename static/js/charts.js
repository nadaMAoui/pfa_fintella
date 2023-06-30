const renderChartbar = (data, labels) => {
  var ctx = document.getElementById("myChartbar").getContext("2d");
  var myChartbar = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Bilan",
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  });
};

const getChartDatabar = () => {
  console.log("fetching");
  fetch("/bilan_summary")
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);
      const bilan_dataset = results.total_indicator;

      if (
        bilan_dataset &&
        Array.isArray(bilan_dataset) &&
        bilan_dataset.length > 0
      ) {
        const firstItem = bilan_dataset[0];
        const labels = Object.keys(firstItem);
        const data = Object.values(firstItem);

        console.log("bilan_dataset", bilan_dataset);
        console.log("labels", labels);
        console.log("data", data);

        renderChartbar(data, labels); // Uncomment this line
      } else {
        console.error("Invalid bilan_dataset:", bilan_dataset);
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
};

const addNewValueToChartbar = (newValue) => {
  // Update total_indicator
  total_indicator.unshift(newValue);

  // Update the chart
  const labels = Object.keys(newValue);
  const data = Object.values(newValue);
  renderChartbar(data, labels);
};

window.addEventListener("DOMContentLoaded", getChartDatabar);

