export class Charts {
    constructor(elementToInsertAt2or3dContext) {
        this.context = elementToInsertAt2or3dContext;
    }

    drawDoughnutChart(data, dataLabels) {

        const DATA = {
            labels: dataLabels,
            datasets: [
                {
                    data: data,
                    backgroundColor: ["#3D3C42", "#0F3D3E", "#E2DCC8", "#395B64"]
                }
            ]
        };

        const CONFIG = {
            type: "doughnut",
            data: DATA,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                title: {
                    display: true,
                    text: "Stats",
                }
            }
        };

        const DOUGHNUT = new Chart(this.context, CONFIG);
        return DOUGHNUT;
    }
    
    destroyChart(chart){
        if (typeof chart !== 'undefined'){
            chart.destroy();
        }
    }
}