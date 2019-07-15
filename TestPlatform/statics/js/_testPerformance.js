    $(function () {
        $('.act-menu').children().eq(1).addClass('active');

        SendRequest();

        SendResponse();

        ClearData();
    });

    // 配置项切换
    function config_func(self) {
        $(self).addClass("active").siblings().removeClass("active");
        var is = $(self).attr("change");
        $("#"+is).removeClass("hide").siblings().addClass("hide");
    }

    // 显示项切换
    function show_func(self) {
        $(self).addClass("active").siblings().removeClass("active");
        var is = $(self).attr("nike");
        $("#"+is).removeClass("hide").siblings().addClass("hide");
    }



    // ajax 发送请求数据到后端 并存储
    function SendRequest() {
       $('.form_info').blur(function () {
                var labelName = $(this).attr('name');
                var labelValue = $(this).val();
                if ($('#action_nav').attr('is-login') == 'true'){
                      $.ajax({
                        url: '/per_data_store/',
                        type: 'post',
                        data: {labelName:labelName,labelValue:labelValue},
                        dataType: 'json',
                        success: function (arg) {
                            if (arg.status){
                                console.log('完了！~')
                            } else {
                                console.log("出错了！")
                            }
                        }
                    })
                }else {
                    console.log("锅佬倌！先登录")
                }
            });
    }


    // 点击ajax请求接口函数 并 获取数据
    var obj_place=$("tbody tr th");
    function req_send() {
        var data;
        var loop_num = 1;
        $.ajax({
            url: '/per_data_extract/',
            type: 'post',
            data: {loop_num:loop_num},
            dataType: 'json',
            success: function (arg) {
                if (arg.status){
                    _sum = arg.message;
                    data = arg.data;
                    obj_place.eq(0).text(data[5]);
                    obj_place.eq(1).text(data[0]);
                    obj_place.eq(2).text(data[1]);
                    obj_place.eq(3).text(data[2]);
                    obj_place.eq(4).text(data[3]);
                    obj_place.eq(5).text(data[4]);
                    // 绘制时间图表
                    reqTime_xAxis.push(_sum[2]);
                    tps_series.push(_sum[1]);
                    once_reqTime_series.push(_sum[0]);
                    avg_reqTime_series.push(data[3]);
                    myChart_reqTime.setOption({
                        xAxis:{
                            data:reqTime_xAxis
                        },
                        series:[{
                                name:'单次请求用时',
                                data:once_reqTime_series
                            },
                                {
                                name:'平均请求用时',
                                data:avg_reqTime_series
                            }]
                    });
                    myChart_tps.setOption({
                        xAxis:{
                            data:reqTime_xAxis
                        },
                        series:[{
                            name:'系统吞吐量',
                            data:tps_series
                        }]
                    })
                } else {
                    console.log(arg.summary);
                    }
                }
            });
    }

    // 发送服务器端的监测请求
    function ser_send() {
        var obj_place=$("tbody tr th");

        $.ajax({
            url:'/servers_info_extract/',
            type:'get',
            dataType:'json',
            success:function (arg) {
                if (arg.status){
                    _data = arg.data;
                    _message = arg.message;
                    obj_place.eq(6).text(_data[0]);
                    obj_place.eq(7).text(_data[1]);
                    obj_place.eq(8).text(_data[2]);
                    usedPer_series.push(_message[0]);
                    loadLevel_series_1min.push(_message[1]);
                    loadLevel_series_5min.push(_message[2]);
                    loadLevel_series_15min.push(_message[3]);
                    myChart_usedPer.setOption({
                        xAxis:{
                            data:reqTime_xAxis
                        },
                        series:[{
                                name:'已使用',
                                data:once_reqTime_series
                            }]
                    });
                    myChart_loadLevel.setOption({
                        xAxis:{
                            data:reqTime_xAxis
                        },
                        series:[{
                                name:'1min均值',
                                data:loadLevel_series_1min
                            },
                                {
                                name:'5min均值',
                                data:loadLevel_series_5min
                            },
                                {
                                name:'15min均值',
                                data:loadLevel_series_15min
                            }
                        ]
                    });
                    // console.log(_data);
                    // console.log(_message);
                }else {
                    console.log("报错啦！~");
                }
            }
        });
    }


    // 服务器端的监测请求
    var _time;
    function ser_monitor() {
        // 判断服务器输入框中是否全部输入，全部输入后就发送请求
        var _lis = [];
        $(".server").each(function () {
            _lis.push($(this).val())
        });
        var _num = $.inArray("",_lis);
        if (_num == -1){
            // console.log("发送请求",_num);
            _time = setInterval(ser_send,1000)
        } else{
            // console.log("不发送请求",_num);
            _time = "";
        }
    }


    // 点击 开始测试并返回数据到客户端
    var time;
    function SendResponse() {
        var num = 1; // 判断点击次数
        $('#SendRequests').click(function () {
            if ($('#action_nav').attr('is-login') == 'true'){
                if (num%2 == 1){
                    $(this).removeClass('btn-success glyphicon-play-circle').addClass('btn-danger glyphicon-off');
                    $(this).html('_暂停运行');
                    $(".form_info").attr("disabled","disabled");
                    $("#ClearData").attr("disabled","disabled").removeClass("btn-info");
                    time = setInterval(req_send,1000); // 进行一个循环 需要用到计时器
                    ser_monitor(); // 执行服务器监测请求

                }else {
                    $(this).removeClass('btn-danger glyphicon-off').addClass('btn-success glyphicon-play-circle');
                    $(this).html('_开始运行');
                    $(".form_info").removeAttr("disabled","disabled");
                    $("#ClearData").removeAttr("disabled").addClass("btn-info");
                    clearInterval(time);
                    // 如果定时器有任务则清除定时器任务
                    if (_time != ""){
                        clearInterval(_time);
                    }
                }
                num += 1;
            }else {
                $('#accountDialog').removeClass('hide');
                $('.shadow').removeClass('hide');
                console.log("锅佬倌！先登录")
            }
        });
    }

    // 点击 清除数据后 清空输入框中的数据
    function ClearData() {
        $('#ClearData').click(function () {
            if ($('#action_nav').attr('is-login') == 'true'){
                $('.form_info').val("");    // 清楚文本框中的数字
                $('tbody tr th').text(0);   // 清楚表格中的数字
                // 清除图表中的数字
                reqTime_xAxis.splice(0,reqTime_xAxis.length);
                once_reqTime_series.splice(0,once_reqTime_series.length);
                avg_reqTime_series.splice(0,avg_reqTime_series.length);
                tps_series.splice(0,tps_series.length);
                usedPer_series.splice(0,usedPer_series.length);
                loadLevel_series_1min.splice(0,loadLevel_series_1min.length);
                loadLevel_series_5min.splice(0,loadLevel_series_5min.length);
                loadLevel_series_15min.splice(0,loadLevel_series_15min.length);

                // 删除数据库中的内容
                $.get('/per_data_clear/');
            } else {
                $('#accountDialog').removeClass('hide');
                $('.shadow').removeClass('hide');
            }
        });
    }


    // 画图工具初始化
    //定义绘图时的数据容器
    var reqTime_xAxis = [];  // 单次请求用时_横坐标列表  & 与吞吐量共用一个列表
    var once_reqTime_series = [];  // 单次请求用时_数据列表
    var avg_reqTime_series = [];  // 平均请求用时_数据列表
    var tps_series = [];    // 吞吐量_数据列表
    var usedPer_series = []; // 内存使用量_数据列表
    var loadLevel_series_1min = []; // 负债均衡1min_数据列表
    var loadLevel_series_5min = []; // 负债均衡5min_数据列表
    var loadLevel_series_15min = []; // 负债均衡15min_数据列表

    // 初始化echarts图表
    var myChart_reqTime = echarts.init(document.getElementById('requestsTime'));
    var myChart_tps = echarts.init(document.getElementById('tps'));
    var myChart_usedPer = echarts.init(document.getElementById('usedPer'));
    var myChart_loadLevel = echarts.init(document.getElementById('loadLevel'));
    // 指定图表的配置项和数据
    var option_reqTime = {
       title:{
            text:"请求用时",
            subtext:"单次&平均(s)"
        },
        tooltip:{
            trigger:'axis'
        },
        legend:{
            data:['单次请求用时','平均请求用时']
        },
        toolbox:{
            show:true,
            orient:'vertical', // 布局方式默认为水平布局，可选为：horizontal | vertical
            left:'right', //left的值可以是像素如:20;也可是百分比如:20%;还可以是:left\center\right
            top:'top', //top的值可以是像素如:20;也可是百分比如:20%;还可以是:top\middle\bottom
            //x:'right', // 水平安放位置,默认为全图右对齐,可选: center|left|right|{number}(x坐标，单位px)
            //y:'top' // 垂直安放位置,默认为全图顶端,可选: center|top|bottom|{number}(x坐标，单位px)
            color:[''],
            backgroundColor:'rgba(0,0,0,0)', // 工具箱背景颜色
            borderColor:'#ccc',  // 工具箱边框颜色
            borderWidth:0,  // 工具箱边框线宽，单位px,默认为0(无边框)
            padding:5,  // 工具箱内边距，单位px,默认各方向内边距为5
            showTitle:true,
            feature:{
                mark:{
                    show:true,
                    title:{
                        mark:'辅助线-开关',
                        markUndo:'辅助线-删除',
                        markClear:'辅助线-清空'
                    },
                    lineStyle:{
                        width:1,
                        color:'#1e90ff',
                        type:'dashed'
                    }
                },
                dataZoom:{
                    show:true,
                    title:{
                        dataZoom:'区域缩放',
                        dataZoomReset:'区域缩放-后退'
                    }
                },
                dataView:{
                    show:true,
                    title:'数据视图',
                    readOnly:true,
                    lang:['数据视图','关闭','刷新'],
                    optionToContent:function (opt) {
                        console.log(opt);
                        var axisData = opt.xAxis[0].data;
                        var series = opt.series;
                        var table = '<table style="width:100%;text-align"center"><tbody><tr>'
                                    +'<td>时间</td>'
                                    + '<td>' + series[0].name + '</td>'
                                    + '<td>' + series[1].name + '</td>' + '</tr>';
                        for (var i = 0,l=axisData.length; i<l; i++){
                            table += '<tr>'
                                     + '<td>' + axisData[i] + '</td>'
                                     + '<td>' + series[0].data[i] + '</td>'
                                     + '<td>' + series[1].data[i] + '</td>' + '</tr>';
                        }
                        table += '</tbody></table>';
                        return table;
                    }
                },
                magicType:{
                    show:true,
                    title:{
                        line:'折线图',
                        bar:'柱状图',
                        stack:'堆积',
                        tiled:'平铺'
                    },
                    type:['line','bar','stack','tiled']
                },
                restore:{
                    show:true,
                    title:'还原',
                    color:'black'
                },
                saveAsImage:{
                    show:true,
                    title:'保存图片',
                    type:'jpeg',
                    lang:['点击本地保存']
                }
            }
        },
        calculable:true,
        dataZoom:{
            show:true,  // 是否显示数据区域缩放
            realtime:true,  // 缩放变化是否实时显示
            start:20,  // 数据缩放选择开始比例，默认为100%
            end:80  // 数据缩放选择结束比例 默认为100%
        },
        xAxis:[
            {
                type:'category',
                boundaryGap:false,
                data:[]
            }
        ],
        yAxis:[
            {
                type:'value'
            }
        ],
        series:[
            {
                name:'单次请求用时',
                type:'line',
                data:[]
            },
            {
                name:'平均请求用时',
                type:'line',
                data:[]
            }
        ]
    };
    var option_tps = {
       title:{
            text:"业务吞吐量",
            subtext:"并发/时间(个)"
        },
        tooltip:{
            trigger:'axis'
        },
        legend:{
            data:['系统吞吐量']
        },
        toolbox:{
            show:true,
            orient:'vertical', // 布局方式默认为水平布局，可选为：horizontal | vertical
            left:'right', //left的值可以是像素如:20;也可是百分比如:20%;还可以是:left\center\right
            top:'top', //top的值可以是像素如:20;也可是百分比如:20%;还可以是:top\middle\bottom
            //x:'right', // 水平安放位置,默认为全图右对齐,可选: center|left|right|{number}(x坐标，单位px)
            //y:'top' // 垂直安放位置,默认为全图顶端,可选: center|top|bottom|{number}(x坐标，单位px)
            color:[''],
            backgroundColor:'rgba(0,0,0,0)', // 工具箱背景颜色
            borderColor:'#ccc',  // 工具箱边框颜色
            borderWidth:0,  // 工具箱边框线宽，单位px,默认为0(无边框)
            padding:5,  // 工具箱内边距，单位px,默认各方向内边距为5
            showTitle:true,
            feature:{
                mark:{
                    show:true,
                    title:{
                        mark:'辅助线-开关',
                        markUndo:'辅助线-删除',
                        markClear:'辅助线-清空'
                    },
                    lineStyle:{
                        width:1,
                        color:'#1e90ff',
                        type:'dashed'
                    }
                },
                dataZoom:{
                    show:true,
                    title:{
                        dataZoom:'区域缩放',
                        dataZoomReset:'区域缩放-后退'
                    }
                },
                dataView:{
                    show:true,
                    title:'数据视图',
                    readOnly:true,
                    lang:['数据视图','关闭','刷新'],
                    optionToContent:function (opt) {
                        console.log(opt);
                        var axisData = opt.xAxis[0].data;
                        var series = opt.series;
                        var table = '<table style="width:100%;text-align"center"><tbody><tr>'
                                    +'<td>时间</td>'
                                    + '<td>' + series[0].name + '</td>'
                                    + '<td>' + series[1].name + '</td>' + '</tr>';
                        for (var i = 0,l=axisData.length; i<l; i++){
                            table += '<tr>'
                                     + '<td>' + axisData[i] + '</td>'
                                     + '<td>' + series[0].data[i] + '</td>'
                                     + '<td>' + series[1].data[i] + '</td>' + '</tr>';
                        }
                        table += '</tbody></table>';
                        return table;
                    }
                },
                magicType:{
                    show:true,
                    title:{
                        line:'折线图',
                        bar:'柱状图',
                        stack:'堆积',
                        tiled:'平铺'
                    },
                    type:['line','bar','stack','tiled']
                },
                restore:{
                    show:true,
                    title:'还原',
                    color:'black'
                },
                saveAsImage:{
                    show:true,
                    title:'保存图片',
                    type:'jpeg',
                    lang:['点击本地保存']
                }
            }
        },
        calculable:true,
        dataZoom:{
            show:true,  // 是否显示数据区域缩放
            realtime:true,  // 缩放变化是否实时显示
            start:20,  // 数据缩放选择开始比例，默认为100%
            end:80  // 数据缩放选择结束比例 默认为100%
        },
        xAxis:[
            {
                type:'category',
                boundaryGap:false,
                data:[]
            }
        ],
        yAxis:[
            {
                type:'value'
            }
        ],
        series:[
            {
                name:'系统吞吐量',
                type:'line',
                data:[],
                itemStyle:{
                    normal:{
                        lineStyle:{
                            color:'green'
                        }
                    }
                }
            }
        ]
    };
    var option_usedPer = {
       title:{
            text:"MemoryUsedRate",
            subtext:"内存使用量(%)"
        },
        tooltip:{
            trigger:'axis'
        },
        legend:{
            data:['已使用']
        },
        toolbox:{
            show:true,
            orient:'vertical', // 布局方式默认为水平布局，可选为：horizontal | vertical
            left:'right', //left的值可以是像素如:20;也可是百分比如:20%;还可以是:left\center\right
            top:'top', //top的值可以是像素如:20;也可是百分比如:20%;还可以是:top\middle\bottom
            //x:'right', // 水平安放位置,默认为全图右对齐,可选: center|left|right|{number}(x坐标，单位px)
            //y:'top' // 垂直安放位置,默认为全图顶端,可选: center|top|bottom|{number}(x坐标，单位px)
            color:[''],
            backgroundColor:'rgba(0,0,0,0)', // 工具箱背景颜色
            borderColor:'#ccc',  // 工具箱边框颜色
            borderWidth:0,  // 工具箱边框线宽，单位px,默认为0(无边框)
            padding:5,  // 工具箱内边距，单位px,默认各方向内边距为5
            showTitle:true,
            feature:{
                mark:{
                    show:true,
                    title:{
                        mark:'辅助线-开关',
                        markUndo:'辅助线-删除',
                        markClear:'辅助线-清空'
                    },
                    lineStyle:{
                        width:1,
                        color:'#1e90ff',
                        type:'dashed'
                    }
                },
                dataZoom:{
                    show:true,
                    title:{
                        dataZoom:'区域缩放',
                        dataZoomReset:'区域缩放-后退'
                    }
                },
                dataView:{
                    show:true,
                    title:'数据视图',
                    readOnly:true,
                    lang:['数据视图','关闭','刷新'],
                    optionToContent:function (opt) {
                        console.log(opt);
                        var axisData = opt.xAxis[0].data;
                        var series = opt.series;
                        var table = '<table style="width:100%;text-align"center"><tbody><tr>'
                                    +'<td>时间</td>'
                                    + '<td>' + series[0].name + '</td>'
                                    + '<td>' + series[1].name + '</td>' + '</tr>';
                        for (var i = 0,l=axisData.length; i<l; i++){
                            table += '<tr>'
                                     + '<td>' + axisData[i] + '</td>'
                                     + '<td>' + series[0].data[i] + '</td>'
                                     + '<td>' + series[1].data[i] + '</td>' + '</tr>';
                        }
                        table += '</tbody></table>';
                        return table;
                    }
                },
                magicType:{
                    show:true,
                    title:{
                        line:'折线图',
                        bar:'柱状图',
                        stack:'堆积',
                        tiled:'平铺'
                    },
                    type:['line','bar','stack','tiled']
                },
                restore:{
                    show:true,
                    title:'还原',
                    color:'black'
                },
                saveAsImage:{
                    show:true,
                    title:'保存图片',
                    type:'jpeg',
                    lang:['点击本地保存']
                }
            }
        },
        calculable:true,
        dataZoom:{
            show:true,  // 是否显示数据区域缩放
            realtime:true,  // 缩放变化是否实时显示
            start:20,  // 数据缩放选择开始比例，默认为100%
            end:80  // 数据缩放选择结束比例 默认为100%
        },
        xAxis:[
            {
                type:'category',
                boundaryGap:false,
                data:[]
            }
        ],
        yAxis:[
            {
                type:'value'
            }
        ],
        series:[
            {
                name:'已使用',
                type:'line',
                data:[],
                itemStyle:{
                    normal:{
                        lineStyle:{
                            color:'blue'
                        }
                    }
                }
            }
        ]
    };
    var option_loadLevel = {
       title:{
            text:"LoadLevel",
            subtext:"每个cpu不大于3为正常"
        },
        tooltip:{
            trigger:'axis'
        },
        legend:{
            data:['1min均值','5min均值','15min均值']
        },
        toolbox:{
            show:true,
            orient:'vertical', // 布局方式默认为水平布局，可选为：horizontal | vertical
            left:'right', //left的值可以是像素如:20;也可是百分比如:20%;还可以是:left\center\right
            top:'top', //top的值可以是像素如:20;也可是百分比如:20%;还可以是:top\middle\bottom
            //x:'right', // 水平安放位置,默认为全图右对齐,可选: center|left|right|{number}(x坐标，单位px)
            //y:'top' // 垂直安放位置,默认为全图顶端,可选: center|top|bottom|{number}(x坐标，单位px)
            color:[''],
            backgroundColor:'rgba(0,0,0,0)', // 工具箱背景颜色
            borderColor:'#ccc',  // 工具箱边框颜色
            borderWidth:0,  // 工具箱边框线宽，单位px,默认为0(无边框)
            padding:5,  // 工具箱内边距，单位px,默认各方向内边距为5
            showTitle:true,
            feature:{
                mark:{
                    show:true,
                    title:{
                        mark:'辅助线-开关',
                        markUndo:'辅助线-删除',
                        markClear:'辅助线-清空'
                    },
                    lineStyle:{
                        width:1,
                        color:'#1e90ff',
                        type:'dashed'
                    }
                },
                dataZoom:{
                    show:true,
                    title:{
                        dataZoom:'区域缩放',
                        dataZoomReset:'区域缩放-后退'
                    }
                },
                dataView:{
                    show:true,
                    title:'数据视图',
                    readOnly:true,
                    lang:['数据视图','关闭','刷新'],
                    optionToContent:function (opt) {
                        console.log(opt);
                        var axisData = opt.xAxis[0].data;
                        var series = opt.series;
                        var table = '<table style="width:100%;text-align"center"><tbody><tr>'
                                    +'<td>时间</td>'
                                    + '<td>' + series[0].name + '</td>'
                                    + '<td>' + series[1].name + '</td>' + '</tr>';
                        for (var i = 0,l=axisData.length; i<l; i++){
                            table += '<tr>'
                                     + '<td>' + axisData[i] + '</td>'
                                     + '<td>' + series[0].data[i] + '</td>'
                                     + '<td>' + series[1].data[i] + '</td>' + '</tr>';
                        }
                        table += '</tbody></table>';
                        return table;
                    }
                },
                magicType:{
                    show:true,
                    title:{
                        line:'折线图',
                        bar:'柱状图',
                        stack:'堆积',
                        tiled:'平铺'
                    },
                    type:['line','bar','stack','tiled']
                },
                restore:{
                    show:true,
                    title:'还原',
                    color:'black'
                },
                saveAsImage:{
                    show:true,
                    title:'保存图片',
                    type:'jpeg',
                    lang:['点击本地保存']
                }
            }
        },
        calculable:true,
        dataZoom:{
            show:true,  // 是否显示数据区域缩放
            realtime:true,  // 缩放变化是否实时显示
            start:20,  // 数据缩放选择开始比例，默认为100%
            end:80  // 数据缩放选择结束比例 默认为100%
        },
        xAxis:[
            {
                type:'category',
                boundaryGap:false,
                data:[]
            }
        ],
        yAxis:[
            {
                type:'value'
            }
        ],
        series:[
            {
                name:'1min均值',
                type:'bar',
                data:[]
            },
            {
                name:'5min均值',
                type:'bar',
                data:[]
            },
            {
                name:'15min均值',
                type:'bar',
                data:[]
            }
        ]
    };
    //将实例化的echarts图表设置图表配置项，同时在DOM中渲染图表显示
    myChart_reqTime.setOption(option_reqTime);
    myChart_tps.setOption(option_tps);
    myChart_usedPer.setOption(option_usedPer);
    myChart_loadLevel.setOption(option_loadLevel);