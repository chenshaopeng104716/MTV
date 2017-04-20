      function channel_vv_uv_program(){
        var myChart = echarts.init(document.getElementById('channel_vv_uv_program'));

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
                data: ['pcweb','android','iphone','ott']
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
                name: 'pcweb',
                data: data[0],
                type: 'scatter',
                symbolSize: function (data) {
                    if(window.location.search.slice(6)=='cartoon')
                        return data[2]*5;
                     return data[2]*15;
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
                name: 'android',
                data: data[1],
                type: 'scatter',
                symbolSize: function (data) {
                    if(window.location.search.slice(6)=='cartoon')
                        return data[2]*5;
                     return data[2]*15;
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
            },
{
                name: 'iphone',
                data: data[2],
                type: 'scatter',
                symbolSize: function (data) {
                    if(window.location.search.slice(6)=='cartoon')
                        return data[2]*5;
                     return data[2]*15;
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
                            color: 'rgb(144,238,144)'
                        }, {
                            offset: 1,
                            color: 'rgb(34,139,34)'
                        }])
                    }
                }
            },
{
                name: 'ott',
                data: data[3],
                type: 'scatter',
                symbolSize: function (data) {
                    if(window.location.search.slice(6)=='cartoon')
                        return data[2]*5;
                     return data[2]*15;
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
                            color: 'rgb(255,140,0)'
                        }, {
                            offset: 1,
                            color: 'rgb(255,140,0)'
                        }])
                    }
                }
            }
            ]
        };

        myChart.setOption(option);
        window.onresize = myChart.resize;
      }
      channel_vv_uv_program();