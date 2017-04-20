      function platform_vv_channel_day(){
            var channel = new Array();
            for (i in vv_channel_day_dict){
                channel.push(i);
            }
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('platform_vv_channel_day'));
            myChart.showLoading();
            // 指定图表的配置项和数据
            option = {
                title: {
                    text: ''
                },
                tooltip : {
                    trigger: 'axis',
                    formatter:'{b0}<br>{a0}: {c0}万<br />{a1}: {c1}万<br />{a2}: {c2}万<br />{a3}: {c3}万'

                },
                legend: {
                    data:['综艺','电视剧','电影','动漫']
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
                        name:'综艺',
                        type:'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data:vv_channel_day_dict.show
                    },
                    {
                        name:'电视剧',
                        type:'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data:vv_channel_day_dict.tv
                    },
                    {
                        name:'动漫',
                        type:'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data:vv_channel_day_dict.cartoon
                    },
                    {
                        name:'电影',
                        type:'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data:vv_channel_day_dict.movie
                    },
                ]
            };
            myChart.hideLoading();
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
      }
      platform_vv_channel_day();