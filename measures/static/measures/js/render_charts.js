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
            text: '',
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
            name: 'Registros',
            data: [{
                name: 'Hipoglicemia',
                y: data.hypo
            }, {
                name: 'Normal',
                y: data.norm
            }, {
                name: 'Pré-diabetes',
                y: data.pre
            }, {
                name: 'Diabetes',
                y: data.high
            }]
        }]
    });
}



function renderLineChart(data, labels) {
    $('#line_chart').highcharts({
        chart: {
            type: 'area',
            style: {
                fontFamily: 'Quicksand',
                fontSize: '12px',
            },
        },
        colors: ["#d9534f", "#7798BF"],
        title: {
            text: ''
        },
        xAxis: {
            allowDecimals: false,
            categories: labels,
        },
        yAxis: {
            title: {
                text: 'Nível de glicose (mg/dL)'
            },
        },
        tooltip: {
            pointFormat: '{series.name}: {point.y:,.2f}<br/> mg/dL'
        },
        plotOptions: {
            area: {
                lineWidth: 1.5,
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            }
        },
        series: [{
            name: 'Nível de glicose',
            data: data
            }]
            });
        }
