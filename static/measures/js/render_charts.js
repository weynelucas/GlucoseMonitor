function renderPieChart(data) {
    $('#pie_chart').highcharts({
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45
            },
            style: {
                fontFamily: 'Quicksand',
                fontSize: '12px',
            },
        },
        colors: ['#0288D1', '#8BC34A', '#FFEB3B', '#F44336'],
        title: {
            text: 'Comparação das medições com os valores de referência para diabetes',
            x: -20 //center
        },
        plotOptions: {
            pie: {
                innerSize: 70,
                depth: 45,
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            name: 'Medições',
            data: [{
                name: 'Hipoglicemia',
                y: data.hypoglycemia
            }, {
                name: 'Normal',
                y: data.normal
            }, {
                name: 'Pré-diabetes',
                y: data.pre_diabetes
            }, {
                name: 'Diabetes',
                y: data.diabetes
            }]
        }]
    });
}
