      function platform_vv_terminal_day(){
            var terminal = new Array();
            for (i in vv_terminal_day_dict){
                terminal.push(i);
            }
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('platform_vv_terminal_day'));
            myChart.showLoading();
            // 指定图表的配置项和数据
            option = {
                title: {
                    text: ''
                },
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:terminal
                },
                toolbox: {
                  show: true,
                  feature: {
                    dataView: {readOnly: false},
                    saveAsImage: {}
                  }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : vv_day_date,
                        splitLine: {
                            show: false
                        }
                    }
                ],
                yAxis : [
                    {
                        type : 'value',
                        splitLine: {
                            show: false
                        }
                    }
                ],
                series : [
                    {
                        name:'android',
                        type:'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data:vv_terminal_day_dict.android
                    },
                    {
                        name:'ott',
                        type:'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data:vv_terminal_day_dict.ott
                    },
                    {
                        name:'pcweb',
                        type:'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data:vv_terminal_day_dict.pcweb
                    },
                    {
                        name:'iphone',
                        type:'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data:vv_terminal_day_dict.iphone
                    },
                    {
                        name:'phonem',
                        type:'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data:vv_terminal_day_dict.phonem
                    }
                ]
            };
            myChart.hideLoading();
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        window.onresize = myChart.resize;
      }
      platform_vv_terminal_day();