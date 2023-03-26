// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
let pieData = JSON.parse(document.querySelector('#myPieChart').getAttribute('data-pie-wastes'))
let pieNames = []
let pieQuantity = []

for (item in pieData){
    pieNames.push(item)
    console.log(item)
}
for (item of Object.values(pieData)){
    pieQuantity.push(item)
}
console.log(pieNames)
console.log(pieQuantity)
// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: pieNames,
        datasets: [{
            data: pieQuantity,
            backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#7a7a7a'],
            hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#7d7d7d'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    },
});
