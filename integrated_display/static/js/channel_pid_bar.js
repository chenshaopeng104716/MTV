      function channel_pid_bar(){
        var myChart = echarts.init(document.getElementById('channel_pid_bar'));

        var data = pid_bar_dict;

         option = {
            tooltip : {
                trigger: 'axis',
                axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            legend: {
                data:['vv', 'uv']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis : [
                {
                    type : 'value'
                }
            ],
            yAxis : [
                {
                    type : 'category',
                    axisTick : {show: false},
                    data : pid_bar_dict.name
                }
            ],
            series : [
                {
                    name:'vv',
                    type:'bar',
                    label: {
                        normal: {
                            show: true,
                            position: 'inside',
                        }
                    },
                    data:pid_bar_dict.vv
                },
                {
                    name:'uv',
                    type:'bar',
                    stack: '总量',
                    label: {
                        normal: {
                            show: true
                        }
                    },
                    data:pid_bar_dict.uv
                },
            ]
        };

        myChart.setOption(option);
        window.onresize = myChart.resize;
      }
      channel_pid_bar();