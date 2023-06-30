const renderChartsecatter = (data, labels) => {
    var ctx = document.getElementById("myChartscatter").getContext("2d");
    var myChartscatter = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Last 6 bilan",
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
        plugins: {
            title: {
            display: true,
            text: "Diagnostic",
          },
        },
      },
    });
  };
  const getChartDatasecatter = () => {
    console.log("fetching");
    fetch("/bilan_summary")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const bilan_datasecatter = results.diagnostic_two_total;
  
        if (bilan_datasecatter && bilan_datasecatter.length > 0) {
          const firstItem = bilan_datasecatter[0];
          const labels = Object.keys(firstItem);
          const data = Object.values(firstItem);
  
          console.log("bilan_datasecatter", bilan_datasecatter);
          console.log("labels", labels);
          console.log("data", data);
  
          renderChartsecatter(data, labels);
        } else {
          console.error("Invalid bilan_data:", bilan_datasecatter);
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };
  
  const addNewValueToChartsecatter = (newValue) => {
  
    diagnostic_two_total.unshift(newValue);
  
    const labels = Object.keys(newValue);
    const data = Object.values(newValue);
    renderChartsecatter(data, labels);
  };
window.addEventListener("DOMContentLoaded", getChartDatasecatter);
  
