<script>
    import Highcharts from 'highcharts'

    export default {
        name: 'MacroData',
        props: ["data", "years", "title", "unique"],
        data() {
            return {
                chartOptions: {
                    chart: {type: 'column', 
                            bakgroundColor:'transparent', 
                            style:{filter:'alpha(opacity=10)',
                            opacity:10}},
                    title: {text: this.title, 
                            style: {
                                fontSize: '12px' 
                            }
                    },
                    xAxis: {categories: this.years,
                            labels: {
                                style: {
                                    color: '#808080',
                                    fontSize:'8px'
                                }
                            }     
                    },
                    yAxis: {
                        allowDecimals: false,
                        min: 0,
                        title: { text: 'руб.' },
                        labels: {
                            style: {
                                color: '#808080',
                                fontSize:'8px'
                            }
                        },
                        stackLabels: {
                        enabled: true,
                        verticalAlign: 'top',
                        //crop: false,
                        formatter: function() {return this.stack;},
                        style: {fontSize: '8px'}
                        }
                    },
                    legend: {shadow: false,
                        itemStyle: {
                            color: '#000000',
                            fontWeight: 'normal',
                            fontSize: '8px'
                        }
                    },
                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.x + ' год</b><br/>' +  this.series.name + ': ' + (this.y).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' руб.<br/>' + 'Итого: ' + (this.point.stackTotal).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' руб.';
                        }
                    },
                
                    plotOptions: {
                        column: {
                            stacking: 'normal'
                        }
                    },
                    series: this.data

                },
                ref: this.unique
            }
        }
    }

</script>
 

<template>
    <div>
        <highcharts class="hc" :options="chartOptions" :ref="unique"></highcharts> 
    </div>
</template>
   
<style>
</style>
