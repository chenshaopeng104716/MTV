      function channel_vv_uv_day(){
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('channel_vv_uv_day'));
		myChart.showLoading();
        // 指定图表的配置项和数据
        var option = {
            tooltip : {
                trigger: 'axis'
            },
            legend: {
                data:[{name:'vv',icon:'circle',textStyle:{color:'red'}},{name:'uv',icon:'circle',textStyle:{color:'blue'}}]
            },
            toolbox: {
              show: true,
              feature: {
                dataView: {readOnly: false},
                saveAsImage: {}
              }
            },
            xAxis: {
                type : 'category',
                boundaryGap : false,
                data: vv_day_date,
                splitLine: {
                    show: false
                }
            },
            yAxis: {
                type : 'value',
                splitLine: {
                    show: false
                }
                },
            series: [{
                name: 'vv',
                type: 'line',
                data: vv_day_data,
                markLine : {
                    data : [
                        {type : 'average', name: '平均值'}
                    ]
                }
            },

            {
                name: 'uv',
                type: 'line',
                data: uv_day_data,
                markLine : {
                    data : [
                        {type : 'average', name: '平均值'}
                    ]
                }
            }]
        };
		myChart.hideLoading();
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.onresize = myChart.resize;
      }
      channel_vv_uv_day();