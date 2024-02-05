document.addEventListener('DOMContentLoaded', function () {
    const eventSource = new EventSource("/stock_data_generator");
    const loadingElement = document.getElementById('loading');
    const chartContainer = document.getElementById('stockChart');
    const week_Chart = document.getElementById("weekChart");

    loadingElement.style.display = 'block';
    chartContainer.style.display = 'none';
    week_Chart.style.display = 'none';

    eventSource.onmessage = function (event) {
        const weekChartDisplay = week_Chart.style.display;
        var stock = document.getElementById("dropdown").value;
        if (weekChartDisplay === "none" || stock === "Default") {
            var prediction = document.getElementById("pre");
            prediction.innerText = "Hi! "+ extractNameFromEmail(localStorage.getItem('email'));
            week_Chart.style.display = "none";
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
        }
    };

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
                        x: {
                            barPercentage: 0.2,
                            ticks: { color: 'white' },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)',
                                borderColor: 'rgba(255, 255, 255, 0.1)',
                                borderWidth: 1
                            }
                        },
                        y: {
                            display: false,
                            beginAtZero: true,
                            max: 700,
                            ticks: { color: 'white' },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)',
                                borderColor: 'rgba(255, 255, 255, 0.1)',
                                borderWidth: 1
                            }
                        }
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

const pwShowHide = document.querySelectorAll(".eye-icon");
const chartSection = document.getElementById('chartSection');
chartSection.classList.toggle('blur');
let cache = []

pwShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener("click", () => {
        let pwFields = eyeIcon.parentElement.parentElement.querySelectorAll(".password");

        pwFields.forEach(password => {
            if (password.type === "password") {
                password.type = "text";
                eyeIcon.classList.replace("bx-hide", "bx-show");
                return;
            }
            password.type = "password";
            eyeIcon.classList.replace("bx-show", "bx-hide");
        })
    });
});

function toggleForms() {
    var fl = document.getElementById('fl');
    var fs = document.getElementById('fs');
    var fv = document.getElementById('fv');

    if (fl.style.display === 'none') {
        fl.style.display = 'block';
        fs.style.display = 'none';
        fv.style.display = 'none';
    } else {
        fl.style.display = 'none';
        fs.style.display = 'none';
        fv.style.display = 'none';
    }
}

document.getElementById('fs').style.display = 'none';
document.getElementById('fv').style.display = 'none';

function extractNameFromEmail(email) {
    if(email.length > 0) {
        var parts = email.split('@');
        var name = parts[0];
        return name;
    }
}

function isUser(inputString) {
    var regex = /^[a-zA-Z]+$/;
    return regex.test(inputString);
}

function weekData() {
    fetch('http://localhost:8000/weekData', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok){
            throw new Error(`Network response was not ok. Status: ${response.status} - ${response.statusText}`);
        }
        document.getElementById("stockChart").style.display = 'none';
        return response.json();
    })
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
        const week_Chart = document.getElementById("weekChart");
        week_Chart.style.display = 'block';
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

        weekChart(formattedDates, openData, highData, lowData, closeData);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

function prediction() {
    var stock = document.getElementById("dropdown").value;
    var predictionElement = document.getElementById("pre");

    if (!localStorage.getItem(stock)) {
        fetch('http://localhost:8000/prediction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                stock: stock
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            predictionElement.innerText = data;
            localStorage.setItem(stock, data);
        })
        .catch(error => {
            console.error('Error during fetch operation:', error);
            predictionElement.innerText = 'Error fetching data';
        });
    } else {
        predictionElement.innerText = localStorage.getItem(stock);
    }
}

function start() {
    var stock = document.getElementById("dropdown").value;
    prediction();
    selectStock(stock);
}

function selectStock(stock) {
    var symbols  = ["AMZN", "GOOGL", "TSLA", "GOOG", "NFLX"]
    if(symbols.includes(stock)) {
        fetch('http://localhost:8000/stockhistory', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                stock: stock
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok. Status: ${response.status} - ${response.statusText}`);
            }
            weekData();
            return response.json();
        })
        .catch(error => {
            console.log('Error during fetch operation: ', error);
        });
    }
    else {
        console.log("Invalid");
    }
}

function isActive() {
    const storedEmail = localStorage.getItem('email');
    if (typeof storedEmail === 'string') {
        var userName = extractNameFromEmail(storedEmail);
        var predictionElement = document.getElementById("pre");
        predictionElement.innerText = "Hi! " + userName;
        loginValid();
    }
}

isActive();

function Logout() {
    cache = [];
    localStorage.clear();
    location.reload();
}

function logging(event) {
    event.preventDefault();

    var emailValue = document.getElementById("emailInput").value;
    var passwordInput = document.getElementById("passwordInput").value;
    var encryptedPassword = btoa(passwordInput);

    fetch('http://localhost:8000/logging', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: emailValue,
            password: encryptedPassword
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(response => {
        if (response === "Valid") {
            cache.push(emailValue);
            localStorage.setItem('email', emailValue);
            const storedEmail = localStorage.getItem('email');
            var userName = extractNameFromEmail(storedEmail);
            var predictionElement = document.getElementById("pre");
            predictionElement.innerText = "Hi! " + userName;
            loginValid();
        }
        if (response === "Admin") {
            var temp = response;
            giveAccess(temp);
        }
        document.getElementById("emailInput").value = '';
        document.getElementById("passwordInput").value = '';
    })
    .catch(error => {
        console.error('Error during fetch operation:', error);
    });
}

function giveAccess(temp) {
    fetch('http://localhost:8000/adccess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            temp: temp
        }),
    })
    .then(response => {
        if (!response.ok){
            throw new Error('Network response was not ok');
        }
        window.location.href = 'http://localhost:8000/admin';
        return response.json();
    })
    .catch(error => {
        console.log('Error during fetch operation: ', error);
    });
}

function verification(event) {
    event.preventDefault();

    var vcode = document.getElementById("verificationCode").value;
    var cacheemail = cache[0];

    fetch('http://localhost:8000/verification', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            vcode: vcode, 
            cacheemail: cacheemail
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(response => {
        var headerElement = document.getElementById("verificationHeader");
        if (response === 'Valid') {
            headerElement.textContent = "Valid";
            setTimeout(function() {
                showLoginForm();
            }, 2000);
        } else {
            headerElement.textContent = "In-Valid";
        }
    })
    .catch(error => {
        console.error('Error during fetch operation:', error);
    });

    document.getElementById("verificationCode").value = '';
}

function signingup(event) {
    event.preventDefault();
    cache = [];
    var emailValue1 = document.getElementById("emailInput1").value;
    var passwordInput1 = document.getElementById("passwordInput1").value;
    var passwordInput2 = document.getElementById("passwordInput2").value;

    var encryptedPassword1 = btoa(passwordInput1);
    var encryptedPassword2 = btoa(passwordInput2);

    fetch('http://localhost:8000/signingup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email1: emailValue1,
            password1: encryptedPassword1,
            password2: encryptedPassword2
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        cache.push(emailValue1);
        showVeriForm();
        return response.json();
    })
    .catch(error => {
        console.error('Error during fetch operation:', error);
    });
}

function loginValid() {
    chartSection.classList.remove('blur');
    // var iconButtons = document.getElementsByClassName("icon-button");
    // for (var i = 0; i < iconButtons.length; i++) {
    //     iconButtons[i].style.display = 'none';
    // }

    var loginButton = document.getElementById("loginButton");
    loginButton.innerText  = 'Logout';
    loginButton.removeEventListener("click", toggleForms);
    loginButton.addEventListener("click", Logout);

    document.getElementById('fl').style.display = 'none';
    document.getElementById('fs').style.display = 'none';
    document.getElementById('fv').style.display = 'none';
}

function showVeriForm() {
    document.getElementById("emailInput1").value='';
    document.getElementById("passwordInput1").value = '';
    document.getElementById("passwordInput2").value = '';

    document.getElementById('fl').style.display = 'none';
    document.getElementById('fs').style.display = 'none';
    document.getElementById('fv').style.display = 'block';
}

function showSignForm() {
    document.getElementById('fl').style.display = 'none';
    document.getElementById('fs').style.display = 'block';
    document.getElementById('fv').style.display = 'none';
}

function showLoginForm() {
    document.getElementById('fl').style.display = 'block';
    document.getElementById('fs').style.display = 'none';
    document.getElementById('fv').style.display = 'none';
}