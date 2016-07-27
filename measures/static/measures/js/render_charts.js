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



function renderLineChart(data) {
    $('#line_chart').highcharts({
        chart: {
            type: 'area',
            style: {
                fontFamily: 'Quicksand',
                fontSize: '12px',
            },
        },
        colors: ["#F44336", "#7798BF"],
        title: {
            text: ''
        },
        xAxis: {
            allowDecimals: false,
            labels: {
                formatter: function () {
                    return this.value; // clean, unformatted number for year
                }
            }
        },
        yAxis: {
            title: {
                text: 'Nível de glicose (mg/dL)'
            },
        },
        tooltip: {
            pointFormat: '{series.name} produced <b>{point.y:,.0f}</b><br/>warheads in {point.x}'
        },
        plotOptions: {
            area: {
                pointStart: 1940,
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
            name: 'USA',
            data: data
            }]
            });
        }
