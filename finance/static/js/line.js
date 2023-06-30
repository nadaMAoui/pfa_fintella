const renderChartline = (data, labels) => {
    var ctx = document.getElementById("myChartline").getContext("2d");
    var myChartline = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Result",
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
  
  const getChartDataline = () => {
    console.log("fetching");
    fetch("/bilan_summary")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const bilan_datasetline = results.diagnostic_list;
  
        if (
          bilan_datasetline &&
          Array.isArray(bilan_datasetline) &&
          bilan_datasetline.length > 0
        ) {
          const firstItem = bilan_datasetline[0];
          const labels = Object.keys(firstItem);
          const data = Object.values(firstItem);
  
          console.log("bilan_datasetline", bilan_datasetline);
          console.log("labels", labels);
          console.log("data", data);
  
          renderChartline(data, labels); // Uncomment this line
        } else {
          console.error("Invalid bilan_datasetline:", bilan_datasetline);
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };
  
  const addNewValueToChartline = (newValue) => {
    // Update total_indicator
    diagnostic_list.unshift(newValue);
  
    // Update the chart
    const labels = Object.keys(newValue);
    const data = Object.values(newValue);
    renderChartline(data, labels);
  };

window.addEventListener("DOMContentLoaded", getChartDataline);
