      function platform_vv_month(){
        var myChart = echarts.init(document.getElementById('platform_vv_month'));
		myChart.showLoading();
        // 指定图表的配置项和数据
        var option = {

            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['2016','2017']
            },
            toolbox: {
              show: true,
              feature: {
                dataView: {readOnly: false},
                saveAsImage: {}
              }
            },
            calculable : true,
            xAxis : [
                {
                    type : 'category',
                    data : ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
                    splitLine: {
                        show: false
                    }
                },
            ],
            yAxis: {
                    splitLine: {
                        show: false
                    }
            },
            series: [{
                name: '2016',
                type: 'bar',
                data: vv_month_lastyear,
                },
                {
                name: '2017',
                type: 'bar',
                data: vv_month_thisyear,
                }
                ]
        };
		myChart.hideLoading();
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.onresize = myChart.resize;
      }
      platform_vv_month();