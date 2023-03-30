// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
let pieData = JSON.parse(document.querySelector('#myPieChart').getAttribute('data-pie-wastes'))
let pieNames = []
let pieQuantity = []
let pieColors = []
for (item in pieData){
    pieNames.push(item)
}
for (item of Object.values(pieData)){
    pieQuantity.push(item.weight)
    pieColors.push(item.color)
}
console.log(pieColors)
// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: pieNames,
        datasets: [{
            data: pieQuantity,
            backgroundColor: pieColors,
            hoverBackgroundColor: pieColors,
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
