      function program_pt_type_day(){
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('program_pt_type_day'));
            myChart.showLoading();
            // 指定图表的配置项和数据
            option = {
                title : {
                    text: '',
                    subtext: '',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    x : 'center',
                    y : 'bottom',
                    data:['pcweb','ott','android','iphone']
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        magicType : {
                            show: true,
                            type: ['pie', 'funnel']
                        },
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                series : [
                    {
                        name:'pcweb',
                        type:'pie',
                        radius : [20, 110],
                        center : ['25%', '25%'],
                        roseType : 'area',
                        label: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        lableLine: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        data:pt_type_day_dict.pcweb
                    },
                    {
                        name:'ott',
                        type:'pie',
                        radius : [30, 110],
                        center : ['75%', '25%'],
                        roseType : 'area',
                        label: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        lableLine: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        data:pt_type_day_dict.ott
                    },
                    {
                        name:'android',
                        type:'pie',
                        radius : [30, 110],
                        center : ['25%', '75%'],
                        roseType : 'area',
                        label: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        lableLine: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        data:pt_type_day_dict.android
                    },
                    {
                        name:'iphone',
                        type:'pie',
                        radius : [30, 110],
                        center : ['75%', '75%'],
                        roseType : 'area',
                        label: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        lableLine: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        data:pt_type_day_dict.iphone
                    },
                ]
            };
            myChart.hideLoading();
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        window.onresize = myChart.resize;
      }
      program_pt_type_day();