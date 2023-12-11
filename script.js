document.addEventListener('DOMContentLoaded', function () {
    const week_Chart = document.getElementById("weekChart");
        
    fetch('http://localhost:8000/weekData')
        .then(response => response.json())
        .then(data => {
            const labels = data['Date'];
            const openData = data['Open'];
            const highData = data['High'];
            const lowData = data['Low'];
            const closeData = data['Close'];
            
            weekChart(labels, openData, highData, lowData, closeData);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });

    function weekChart(labels, openData, highData, lowData, closeData){
        var ctx = week_Chart.getContext('2d'); // Fix 3

        if (window.myChart) {
            window.myChart.data.labels = labels;
            window.myChart.data.datasets[0].data = openData; // Fix 2
            window.myChart.data.datasets[1].data = highData; // Fix 2
            window.myChart.update();
        } else {
            window.myChart = new Chart(ctx, {
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
});
