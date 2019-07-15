        $(function () {

            BindAddInfoModal();

            BindUpdateItem();

            BindGetData();

            BindFromData();

            BindCreateReport();

            BindSendReport();

            $('.act-menu').children().eq(2).addClass('active');

        });



        /* from表单的字段通过ajax实现 */
        function BindFromData() {
            $('.form_info,.radio').blur(function () {
                var labelName = $(this).siblings().text();
                var labelValue = $(this).val();

                if ($('#action_nav').attr('is-login') == 'true'){
                      $.ajax({
                        url: '/modal_info/',
                        type: 'get',
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


        /* 绑定一个向后台发送数据的功能 */
        function BindAddInfoModal() {
            // 指定数据格式
            var data = {'测试设备:': [
                            {name: '服务器类型', value: '普通PC机'},
                            {name: '服务器内存', value: '8GB'},
                            {name: '服务器硬盘', value: '40GB'},
                            {name: '服务器CPU', value: 'Intel(R) Xeon(R) CPU E5-2620 v3 @ 2.40GHz'},
                            {name: '服务器系统', value: '64位CentOS'},
                            {name: '客户机类型', value: '普通PC机'},
                            {name: '客户机内存', value: '8GB'},
                            {name: '客户机硬盘', value: '1TB'},
                            {name: '客户机CPU', value: 'Intel(R) Core(TM)i5-6600 @ 3.30GHz'},
                            {name: '客户机系统', value: 'Windows7'}
                            ],
                        '角色分配:': [
                            {'name': '任务名称', value: ''},
                            {'name': '开始时间', value: ''},
                            {'name': '结束时间', value: ''},
                            {'name': '开发人员', value: ''},
                            {'name': '测试人员', value: ''}
                            ],
                        '测试时间:':[
                            {"name":"测试阶段",value:""},
                            {"name":"开始时间",value:""},
                            {"name":"结束时间",value:""},
                            {"name":"工作天数",value:""}
                        ],
                        '测试阶段:':[
                            {"name":"阶段名称",value:""},
                            {"name":"阶段描述",value:""}
                        ],
                        '功能模块:':[
                            {"name":"功能名称",value:""},
                            {"name":"是否通过",value:""}
                        ],
                        '缺陷统计:':[
                            {"name":"开发姓名",value:""},
                            {"name":"缺陷个数",value:""}
                        ]
            };


            // 点击任意标签下的 模态对话框
            $(".btn-info").click(function(e) {
                if ($('#action_nav').attr('is-login') == 'true'){
                    $("#add-info").removeClass("hide");
                    $(this).addClass("this-btn-info")
                }else {
                    $('#accountDialog').removeClass('hide');
                }
                e && e.stopPropagation();

                $(".shadow").removeClass("hide");

                // 获取标签名字
                labelName = $(this).siblings().text();

                if (labelName == '测试设备:'){
                    $("#modal-add-info-btn").addClass("hide");
                }else {
                    $("#modal-add-info-btn").removeClass("hide");
                }


                // 动态生成对话框中的信息
                for (var item in data[labelName]) {
                    var htmlInput = '<label for="inputEmail3" class="control-label" style="margin:10px">' + data[labelName][item].name+1 + ':</label>' +
                        '<input type="text" class="form-control"  name="'+ data[labelName][item].name +1 +
                        '" style="display:inline;width:220px;"' + 'value="'+ data[labelName][item].value +' "' +'>';

                    $("#add-info-modal").append(htmlInput);
                }

            });



            /* 点击 再加一组按钮后 出现的效果 */
            var i = 1;
            $("#modal-add-info-btn").click(function () {
                i++;
                for (var item in data[labelName]) {

                var htmlInput = '<label for="inputEmail3" class="control-label add" style="margin:10px">' + data[labelName][item].name+i + ':</label>' +
                        '<input type="text" class="form-control add"  name="'+ data[labelName][item].name +i +
                        '" style="display:inline;width:220px;"' + 'value="'+ data[labelName][item].value +' "' +'>';

                $("#add-info-modal").append(htmlInput);}
                $("#modal-del-info-btn").removeClass("hide").click(function () {
                    /* 点击 删除新增项按钮后 出现的效果 */
                    $(".control-label,.form-control").remove(".add");
                    $(this).addClass("hide");
                    i = 1;
                })
            });





            // 点击取消按钮 消除模态对话
            $(".modal-btn-cancel").click(function () {
                    $("#add-info").addClass("hide");
                    $(".shadow").addClass("hide");
                    $("#add-info-modal").empty();
                    i = 1;
            });

            // 点击确认按钮 组合成字典 ajax 发送数据
            $(".modal-btn-confir").click(function () {
                var container = $(this).parent().siblings();
                var post_dict = {};
                container.find('input[type="text"],text').each(function () {
                    post_dict[$(this).attr('name')] = $(this).val();
                });


                // 发请求
                    $.ajax({
                        url:'/modal_info/',
                        type:'post',
                        data:{'label_name':labelName, 'pd':post_dict},
                        dataType:'JSON',
                        success: function (arg) {
                            console.log(arg.message);
                            // 如果数据成功提交，给用户一个提示
                            $(".this-btn-info").addClass("btn-info-finish").text("- 添加信息")
                            .removeClass("this-btn-info").removeClass("btn-info");
                        }
                    });


                $("#add-info").addClass("hide");
                $(".shadow").addClass("hide");
                $("#add-info-modal").empty();
                i=1;

            });
        }


        /* 获取项目名称 和BUG信息的 代码块 */
        function update_item_ajax() {
            $.ajax({
                        url: '/update_item/',
                        type: 'get',
                        data: {"status":"OK","zentao_id":zentao_id},
                        dataType: 'json',
                        success: function (arg) {
                            if (arg.status){
                                alert(arg.message);
                                console.log(arg.data);
                                $.each(arg.data,function (k,v) {
                                    $('#productItem').append(
                                       '<option value="'+v+'">'+k+'</option>'
                                    )
                                });
                            } else {
                                alert(arg.message);
                                console.log("出错了！")
                            }
                        }
                    })
        }


        /*    绑定更新项目名称的接口     */
        var zentao_id;
        function BindUpdateItem() {
            $('#updateItem').click(function () {
                if ($('#action_nav').attr('is-login') == 'true') {
                    $('.shadow').removeClass('hide');   // 点击后选择禅道版本号
                    $('.modal-dialog-zentao').removeClass('hide'); //弹出禅道对话框
                    $(this).addClass('btn disabled'); // 防止二次点击

                } else {
                    $('#accountDialog').removeClass('hide');
                    $('.shadow').removeClass('hide');
                }
            });


            /* 点击 老禅道  和  新禅道的 按钮事件*/
            $('.btn-old-zentao').click(function () {
                zentao_id = $(this).val();
                $('.shadow').addClass('hide');   // 消除蒙层
                $('.modal-dialog-zentao').addClass('hide'); //消除弹框
                console.log(zentao_id);
                update_item_ajax();
            });

            $('.btn-new-zentao').click(function () {
                zentao_id = $(this).val();
                $('.shadow').addClass('hide');   // 消除蒙层
                $('.modal-dialog-zentao').addClass('hide'); //消除弹框
                update_item_ajax();
            });

        }



        /*    绑定获取爬虫数据的接口     */
        function BindGetData() {
            $('#getData').click(function () {
                if ($('#action_nav').attr('is-login') == 'true') {
                    var itemId = $('#productItem').val();

                    $('.loading-ico-index').removeClass('hide'); //显示正在加载的按钮
                    console.log(itemId);

                    $.ajax({
                        url: '/update_item/',
                        type: 'POST',
                        data: {"status":"OK","itemId":itemId,"zentao_id":zentao_id},
                        dataType: 'json',
                        success: function (arg) {
                            if (arg.status){
                                alert(arg.message)
                            } else {
                                alert(arg.message)
                            }

                            $('.loading-ico-index').addClass('hide'); //隐藏正在加载的按钮
                        }
                    })
                } else {
                    $('#accountDialog').removeClass('hide');
                    $('.shadow').removeClass('hide');
                }
            })
        }


        /* 绑定一个生成报告的事件 */
        function BindCreateReport(){
            $('#CreateReport').click(function(){
                if($('#action_nav').attr('is-login') == 'true'){
                    var itemName = $('#productItem').find("option:selected").text();
                    $.ajax({
                        url: '/creat_report/',
                        type: 'POST',
                        data: {"status":"OK","itemName":itemName},
                        dataType: 'json',
                        success: function (arg) {
                            if (arg.status){
                                $('#alertSuccess').removeClass('hide');
                                $('#SendReport').removeClass('default').removeClass('hide').addClass('btn-success').removeAttr("disabled");
                                $('#CreateReport').remove();
                            }else {
                                console.log(arg.message);
                                console.log(arg.status);
                            }
                        }
                    });
                }else{
                    $('#accountDialog').removeClass('hide');
                    $('.shadow').removeClass('hide');
                }
            });
        }


        /* 绑定了一个上传 excel模板的事件 */
        function ExcelUpload() {
            var form_data = new FormData();
            var file_info = $('#excel_upload')[0].files[0];
            form_data.append('excel_data',file_info);
            $.ajax({
                url:'/creat_excel/',
                type:'POST',
                data:form_data,
                processData:false,
                contentType:false,
                dataType:'json',
                success:function (arg) {
                    console.log("OK!");
                    console.log(arg);
                    if (arg.status){
                        alert(arg.message);
                        // 成功上传后 直接不让填 添加信息的模态对话框
                        $(".btn-info").addClass("btn-info-finish").text("- 添加信息")
                            .removeClass("this-btn-info").removeClass("btn-info");
                    }else {
                        alert(arg.message);
                    }
                }
            });
        }



        /* 绑定了一个上传 自定义报告的事件*/
        function FileUpload() {
            var form_data = new FormData();
            var file_info = $('#file_upload')[0].files[0];
            form_data.append('file',file_info);

            $('#alertSuccess').addClass('hide');

            $.ajax({
                url:'/upload_customFile/',
                type:'POST',
                data:form_data,
                processData:false,
                contentType:false,
                dataType:'json',
                success:function (arg) {
                    console.log("OK!");
                    console.log(arg);
                    if (arg.status){
                        alert(arg.message);
                    }else {
                        alert(arg.message);
                    }
                }
            });
        }



        /* 绑定一个发送报告的事件 */
        function BindSendReport() {
            $('#SendReport').click(function () {
                $('.spanSR').removeClass('hide');

                $.ajax({
                        url: '/creat_report/',
                        type: 'GET',
                        data: {"status":"OK"},
                        dataType: 'json',
                        success: function (arg) {
                            if (arg.status){
                                alert(arg.message);
                                $('#CreateReport').removeClass('default').addClass('btn-primary').removeAttr("disabled");
                                $('#SendReport').addClass('default').removeClass('btn-success').attr('disabled','disabled');
                                $('.spanSR').addClass('hide');
                            }else {
                                alert(arg.message);
                                console.log(arg.status);
                            }
                        }
                    })
            })
        }