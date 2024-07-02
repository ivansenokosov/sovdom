<script>

import Highcharts from 'highcharts'

export default {
  name: 'MicroData',
  props: ["data", "years", "unique"],
  data() {
    return {
        ref: this.unique,
        chartOptions: {
        chart: {background:'transparent'},
        title: {text: this.data[0][0].name, 
                style: {
                fontSize: '12px' 
                }
        },
        subtitle: {text: this.data[0][0].subtitle,
        style: {
            fontSize: '10px' 
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
        yAxis: {title: { text: "руб./" + this.data[0][0].denominator + " в месяц",               
                        style: { fontSize: '10px' },
                    }, 
                max:  + this.data[0][0].container_max_value,
                labels: {
                style: {
                    color: '#808080',
                    fontSize:'8px'
                }
                } 
            },
        legend: {shadow: false,
                itemStyle: {
                    color: '#000000',
                    fontWeight: 'normal',
                    fontSize: '8px'
                }
        },
        // tooltip: {       
        //             formatter: function() {
        //                 return this.series.name + '<br><b>' + this.y  + ' руб./кв.м в месяц</b><br><b>' + (this.y * 12 * this.data[0][0].denominator_value ).toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") +  ' руб. в год</b>';
        //             }
        // },
        plotOptions: {
            column: {
                grouping: false,
                shadow: false,
                borderWidth: 0,
                stacking: 'normal'
            }
        },
    
        series: this.data[1]



        }
    };
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
