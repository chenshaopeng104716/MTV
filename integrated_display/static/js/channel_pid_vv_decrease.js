      function channel_pid_vv_decrease(){
        var myChart = echarts.init(document.getElementById('channel_pid_vv_decrease'));


        option = {
            tooltip : {
                trigger: 'axis',
                axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
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
                    type : 'value',
                    splitLine: {
                        show: false
                    }
                }
            ],
            yAxis : [
                {
                    type : 'category',
                    axisTick : {show: false},
                    splitLine: {
                        show: false
                    },
                    data : pid_vv_change_dict.decrease_name
                }
            ],
            series : [
                {
                    itemStyle:{  normal:{color:'green'}  } ,
                    name:'',
                    type:'bar',
                    label: {
                        normal: {
                            show: true,
                            position: 'inside',
                            formatter: '{c}万'
                        }
                    },
                    data:pid_vv_change_dict.decrease_vv
                },
            ]
        };
        myChart.setOption(option);
        window.onresize = myChart.resize;
      }
      channel_pid_vv_decrease();