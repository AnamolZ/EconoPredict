document.addEventListener('DOMContentLoaded', function () {
    const eventSource = new EventSource("/stock_data_generator");
    const loadingElement = document.getElementById('loading');
    const chartContainer = document.getElementById('stockChart');
    const week_Chart = document.getElementById("weekChart");
    const currentURL = window.location.href;

    loadingElement.style.display = 'block';
    chartContainer.style.display = 'none';
    week_Chart.style.display = 'none';

    const stockSymbols = ['AMZN', 'GOOGL', 'TSLA', 'NFLX', 'META', 'AMZN', 'AMD', 'UBER'];
    const pattern = new RegExp(`/\\?Stock="${stockSymbols.join('|')}"`);

    if(pattern.test(currentURL)) {
        fetch('http://localhost:8000/stock_data_generator')
        .then(response => {
          if (response.ok) {
            fetch('http://localhost:8000/weekData')
            .then(response => response.json())
            .then(data => {
                const labels = data['Date'];
                const openData = data['Open'];
                const highData = data['High'];
                const lowData = data['Low'];
                const closeData = data['Close'];
    
                var formattedDates = labels.map(function(dateString) {
                    var date = new Date(dateString);
                    var month = (date.getMonth() + 1).toString().padStart(2, '0');
                    var day = date.getDate().toString().padStart(2, '0');
                    return month + '-' + day;
                });
                loadingElement.style.display = 'none';
                week_Chart.style.display = 'block';
                weekChart(formattedDates, openData, highData, lowData, closeData);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
          } else {
            console.log('no');
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });  
    } else{
        eventSource.onmessage = function (event) {
            const stockData = JSON.parse(event.data);
            loadingElement.style.display = 'none';
            chartContainer.style.display = 'block';
    
            const labels = Object.keys(stockData);
            const data = Object.values(stockData);
            const colors = generateRandomColors(data.length);
    
            createOrUpdateChart(labels, data, colors);
    
            setInterval(() => {
                createOrUpdateChart(labels, data, colors);
            }, 5000);
        };
    }

    function weekChart(labels, openData, highData, lowData, closeData){
        var ctx = week_Chart.getContext('2d');

        if (window.week_Chart) {
            window.week_Chart.data.labels = labels;
            window.week_Chart.data.datasets[0].data = openData;
            window.week_Chart.data.datasets[1].data = highData;
            window.week_Chart.update();
        } else {
            window.week_Chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Open',
                            borderColor: 'rgb(255, 99, 132)',
                            data: openData,
                            fill: false
                        },
                        {
                            label: 'High',
                            borderColor: 'rgb(54, 162, 235)',
                            data: highData,
                            fill: false
                        },
                        {
                            label: 'Low',
                            borderColor: 'rgb(255, 205, 86)',
                            data: lowData,
                            fill: false
                        },
                        {
                            label: 'Close',
                            borderColor: 'rgb(75, 192, 192)',
                            data: closeData,
                            fill: false
                        }
                    ]
                },
                options: {
                    scales: {
                        y: {
                            display: true,
                            beginAtZero: false
                        }
                    },
                    responsive: true,
                    maintainAspectRatio: false,
                    title: {
                        display: true,
                        text: 'Financial Data Chart'
                    }
                }
            });
        }
    }

    function createOrUpdateChart(labels, data, colors) {
        const ctx = document.getElementById('stockChart').getContext('2d');

        if (window.myChart) {
            window.myChart.data.labels = labels;
            window.myChart.data.datasets[0].data = data;
            window.myChart.data.datasets[1].data = data;
            window.myChart.update();
        } else {
            window.myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels,
                    datasets: [{
                        label: 'Stock Prices (Bar)',
                        data,
                        backgroundColor: colors.map(color => `rgba(${color.join(',')}, 0.2)`),
                        borderColor: colors.map(color => `rgba(${color.join(',')}, 1)`),
                        borderWidth: 1,
                    }, {
                        label: 'Stock Prices (Line)',
                        data,
                        borderColor: 'white',
                        borderWidth: 2,
                        fill: false,
                        type: 'line',
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            barPercentage: 0.2
                          }],
                        y: {
                            display: false,
                            beginAtZero: true,
                            max: 500,
                            ticks: { color: 'white' },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)',
                                borderColor: 'rgba(255, 255, 255, 0.1)',
                                borderWidth: 1
                            }
                        },
                        x: { ticks: { color: 'white' } }
                    },
                    responsive: true,
                    maintainAspectRatio: false,
                }
            });
        }
    }

    function generateRandomColors(count) {
        const colors = [];
        for (let i = 0; i < count; i++) {
            colors.push([Math.floor(Math.random() * 256), Math.floor(Math.random() * 256), Math.floor(Math.random() * 256)]);
        }
        return colors;
    }
});
