      function platform_vv_uv_day(){
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('platform_vv_uv_day'));
		myChart.showLoading();
        // 指定图表的配置项和数据
        var option = {
            tooltip : {
                trigger: 'axis',
                formatter:'{b0}<br>{a0}: {c0}万<br />{a1}: {c1}万',
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
            dataZoom: [{
                type: 'inside',
                start: 70,
                end: 100
            }, {
                start: 70,
                end: 100,
            }],
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
                axisLabel:{
                formatter:function(value){
                return value+'万'
                }},
                splitLine: {
                    show: false
                }
                },
            series: [{
                name: 'vv',
                type: 'line',
                data: vv_day_data,
                markPoint : {
                    tooltip:{formatter:'{b0}<br>{a0}:{c0}万'},
                    data : [
                        {symbol:'pin',symbolSize:70,type : 'max', name: '最大值'},
                        {symbol:'pin',symbolSize:70,type : 'min', name: '最小值'},

                    ],
                },
                markLine : {
                     tooltip:{formatter:'{b0}<br>{a0}:{c0}万'},
                    data : [
                        {type : 'average', name: '平均值'}
                    ]
                }
            },

            {
                name: 'uv',
                type: 'line',
                data: uv_day_data,
                markPoint : {
                    tooltip:{formatter:'{b0}<br>{a0}: {c0}万'},
                    data : [
                        {symbol:'pin',symbolSize:70,type : 'max', name: '最大值'},
                        {symbol:'pin',symbolSize:70,type : 'min', name: '最小值'}
                    ],
                },
                markLine : {
                    tooltip:{formatter:'{b0}<br>{a0}:{c0}万'},
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
      platform_vv_uv_day();