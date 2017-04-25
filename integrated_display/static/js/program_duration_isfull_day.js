      function program_duration_isfull_day(){
            var isfull = new Array();
            for (i in duration_isfull_day_dict){
                isfull.push(i);
            }
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('program_duration_isfull_day'));
            myChart.showLoading();
            // 指定图表的配置项和数据
            option = {
                title: {
                    text: ''
                },
                tooltip : {
                    trigger: 'axis',
                    formatter:'{b0}<br>{a0}: {c0}万<br />{a1}: {c1}万'
                },
                legend: {
                    data:['正片','短片']
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
                        name:'正片',
                        type:'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data:duration_isfull_day_dict.full
                    },
                    {
                        name:'短片',
                        type:'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data:duration_isfull_day_dict.short
                    },
                ]
            };
            myChart.hideLoading();
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
      }
      program_duration_isfull_day();