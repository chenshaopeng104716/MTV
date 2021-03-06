      function channel_vv_terminal_day(){
            var terminal = new Array();
            for (i in vv_terminal_day_dict){
                terminal.push(i);
            }
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('channel_vv_terminal_day'));
            myChart.showLoading();
            // 指定图表的配置项和数据
            option = {
                title: {
                    text: ''
                },
                tooltip : {
                    trigger: 'axis',
                    formatter:'{b0}<br>{a0}: {c0}万<br />{a1}: {c1}万<br />{a2}: {c2}万<br />{a3}: {c3}万<br />{a4}: {c4}万'

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
                dataZoom: [{
                    type: 'inside',
                    start: 70,
                    end: 100
                }, {
                    start: 70,
                    end: 100,
                }],
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
                        axisLabel:{
                        formatter:function(value){
                        return value+'万'
                        }},
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
      channel_vv_terminal_day();