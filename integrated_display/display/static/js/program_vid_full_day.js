      function program_vid_full_day(){
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('program_vid_full_day'));
            myChart.showLoading();
            // 指定图表的配置项和数据
            option = {
                tooltip : {
                    trigger: 'axis',
                    axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                        type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    }
                },
                legend: {
                    data:['正片vv']
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
                        data : vid_isfull_day_dict.full_vid_name,
                        splitLine: {
                            show: false
                        }
                    }
                ],
                series : [
                    {
                        name:'正片vv',
                        type:'bar',
                        label: {
                            normal: {
                                show: true,
                                position: 'right'
                            }
                        },
                        data:vid_isfull_day_dict.full_num
                    }
                ]
            };
            myChart.hideLoading();
            myChart.setOption(option);
            window.onresize = myChart.resize;
          }
      program_vid_full_day();