      function platform_vv_uv_program(){
        var myChart = echarts.init(document.getElementById('platform_vv_uv_program'));

        var data = pid_day_avg_result_list

        option = {
            backgroundColor: new echarts.graphic.RadialGradient(0.3, 0.3, 0.8, [{
                offset: 0,
                color: 'white'
            }, {
                offset: 1,
                color: 'white'
            }]),
            toolbox: {
              show: true,
              feature: {
                dataView: {readOnly: false},
                saveAsImage: {}
              }
            },
            title: {
            text: 'x轴为vv，y轴为uv',
            left: 'center',
            subtext:'气泡大小为人均vv。点越靠右，vv越大，越靠上，uv越大。',
            textStyle: {
              fontWeight: 'bolder',
              textAlign:'right',

            }
          },            
	    legend: {
                right: 50,
                data: ['综艺','电视剧']
            },
            xAxis: {
		          name: 'VV',
                  splitLine: {
                      show: false
                  }
            },
            yAxis: {
		          name: 'UV',
                  splitLine: {
                      show: false
                  },
                scale: true
            },
            series: [{
                name: '综艺',
                data: data[0],
                type: 'scatter',
                symbolSize: function (data) {
                    return data[2]*20;
                },
                label: {
                    emphasis: {
                        show: true,
                        formatter: function (param) {
                            var vv = param.data[0];
                            var uv = param.data[1];
                            var name = param.data[3];
                            var all = name+'\n日均vv:'+vv+'万\n日均uv:'+uv+'万';
                            return all;                            
                        },
                        position: 'right'
                    }
                },
                itemStyle: {
                    normal: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(120, 36, 50, 0.5)',
                        shadowOffsetY: 5,
                        color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
                            offset: 0,
                            color: 'rgb(251, 118, 123)'
                        }, {
                            offset: 1,
                            color: 'rgb(204, 46, 72)'
                        }
                        ])
                    }
                }
            },
{
                name: '电视剧',
                data: data[1],
                type: 'scatter',
                symbolSize: function (data) {
                    return data[2]*20;
                },
                label: {
                    emphasis: {
                        show: true,
                        formatter: function (param) {
                            var vv = param.data[0];
                            var uv = param.data[1];
                            var name = param.data[3];
                            var all = name+'\n日均vv:'+vv+'万\n日均uv:'+uv+'万';
                            return all;                            
                        },
                        position: 'right'
                    }
                },
                itemStyle: {
                    normal: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(25, 100, 150, 0.5)',
                        shadowOffsetY: 5,
                        color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
                            offset: 0,
                            color: 'rgb(129, 227, 238)'
                        }, {
                            offset: 1,
                            color: 'rgb(25, 183, 207)'
                        }])
                    }
                }
            }
            ]
        };

        myChart.setOption(option);
        window.onresize = myChart.resize;
      }
      platform_vv_uv_program();