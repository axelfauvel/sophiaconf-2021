const BarChartLabels = [
    'red team', 'blue team'
];
const BarChartData = {
    labels: BarChartLabels,
    datasets: [{
        label: 'clapometer',
        data: [150, 160],
        backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(0, 99, 132)',
        ],
        borderColor: [
            'rgb(255, 99, 132)',
            'rgb(0, 99, 132)',
        ],
        borderWidth: 1
    }]
};

const BarChartConfig = {
    type: 'bar',
    data: BarChartData,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    },
};

// === display chart ===
var myBarChart = new Chart(
    document.getElementById('bar_chart'),
    BarChartConfig
);
