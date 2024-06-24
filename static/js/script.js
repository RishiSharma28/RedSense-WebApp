"use strict";

document.addEventListener("DOMContentLoaded", function () {
  // This function runs when the DOM is fully loaded

  const commentsEl = document.getElementById("comments");
  const canvasId = document.getElementById("canvas_id");
  const submitBtn = document.getElementById("submit_button");
  const subredditName = document.getElementById("subreddit_name");
  const numPosts = document.getElementById("num_posts");
  const typeOneBtns = document.querySelectorAll(".type-one-btn");
  const typeTwoBtns = document.querySelectorAll(".type-two-btn");
  let readMoreBtn = null;
  let data = null;

  // Define the fetchData function to handle form submission and fetch data from the server
  const fetchData = async function (e) {
    e.preventDefault(); // Prevent the default form submission behavior

    try {
      const inputData = {
        subname: subredditName.value,
        posts: parseInt(numPosts.value),
      };

      const response = await fetch("https://red-sense-web-app.vercel.app/redditSentiments", {
        method: "post",
        body: JSON.stringify(inputData),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
      });

      if (response.ok) {
        data = await response.json(); // Parse JSON response
        console.log(data);
        canvasId.classList.remove("hidden");
        canvasId.classList.add("flex");
        updateChart(sentimentChart, data);
        updateChart(sentimentChartTwo, data, "pie");
        displayComments(data.comments);
      } else {
        console.error("Error fetching data:", response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // Function to update the chart with the new data
  const updateChart = function (chart, data, type = "bar") {
    chart.config.type = type;
    chart.data.datasets[0].data = [
      data.positive_sentiments.length,
      data.negative_sentiments.length,
      data.neutral_sentiments.length,
    ];
    chart.update();
  };

  const displayComments = function (comments) {
    const commentsColor = ["green", "red", "yellow"];
    // commentsEl.innerHTML = "";
    comments.forEach((comment, i) => {
      const element = `
        <div>
            <p class="${commentsColor[i]} line-clamp-2">${comment}</p>
            <button class="text-xs blue hover:underline" id="read-more-btn">Read More</button>
        </div>`;
      commentsEl.insertAdjacentHTML("beforeend", element);
    });
    readMoreBtn = document.querySelectorAll("#read-more-btn");

    readMoreBtn.forEach((btn) => {
      btn.addEventListener("click", function () {
        var content = btn.previousElementSibling;

        if (content.classList.contains("expanded")) {
          content.classList.remove("expanded");
          content.classList.add("line-clamp-3");
          btn.innerText = "Read More";
        } else {
          content.classList.remove("line-clamp-3");
          content.classList.add("expanded");
          btn.innerText = "Read Less";
        }
      });
    });
  };

  typeOneBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const chartType = e.target.getAttribute("data-type");
      updateChart(sentimentChart, data, chartType);
    });
  });

  typeTwoBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const chartType = e.target.getAttribute("data-type");
      updateChart(sentimentChartTwo, data, chartType);
    });
  });

  submitBtn.addEventListener("click", fetchData);

  // Initialize the Chart.js chart
  var ctx = document.getElementById("sentimentChart1").getContext("2d");
  var sentimentChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Positive", "Negative", "Neutral"],
      datasets: [
        {
          label: "Sentiment Analysis",
          data: [0, 0, 0],
          backgroundColor: [
            "rgba(54, 162, 235, 0.7)", // Blue
            "rgba(255, 99, 132, 0.7)", // Red
            "rgba(255, 206, 86, 0.7)", // Yellow
          ],
          borderColor: [
            "rgba(54, 162, 235, 1)",
            "rgba(255, 99, 132, 1)",
            "rgba(255, 206, 86, 1)",
          ],
          fill: true,
          borderWidth: 2,
        },
      ],
    },
    options: {
      backgroundColor: "rgba(242, 242, 242, 0.2)", // Light gray background
      scales: {
        y: {
          grid: {
            color: "rgba(221, 221, 221, 0.5)", // Light gray grid lines
            lineWidth: 0, // Adjust grid line thickness
          },
          beginAtZero: true,
          responsive: true,
        },
      },
    },
  });

  // type two chart initialization
  var ctxTwo = document.getElementById("sentimentChart2").getContext("2d");
  var sentimentChartTwo = new Chart(ctxTwo, {
    type: "bar",
    data: {
      labels: ["Positive", "Negative", "Neutral"],
      datasets: [
        {
          label: "Sentiment Analysis",
          data: [0, 0, 0],
          backgroundColor: [
            "rgba(54, 162, 235, 0.7)", // Blue
            "rgba(255, 99, 132, 0.7)", // Red
            "rgba(255, 206, 86, 0.7)", // Yellow
          ],
          borderColor: [
            "rgba(54, 162, 235, 1)",
            "rgba(255, 99, 132, 1)",
            "rgba(255, 206, 86, 1)",
          ],
          borderWidth: 2,
        },
      ],
    },
    options: {
      backgroundColor: "rgba(242, 242, 242, 0.2)", // Light gray background
      scales: {
        y: {
          grid: {
            color: "rgba(221, 221, 221, 0.5)", // Light gray grid lines
            lineWidth: 0, // Adjust grid line thickness
          },
          beginAtZero: true,
          responsive: true,
        },
      },
    },
  });
});