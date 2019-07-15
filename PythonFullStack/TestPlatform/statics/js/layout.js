        $(function(){
            $('#loginUserNc,#userOprBox').mouseover(function(){
                $('#userOprBox').css('display', 'block');
                $('#loginUserNc').addClass('active');
            }).mouseout(function () {
                $('#userOprBox').css('display', 'none');
                $('#loginUserNc').removeClass('active');
            });
            BindTabMenu('#tab-menu-title', '#tab-menu-body');

            BindLoginRegisterDialog();

            BindSendMsg();
        });

        function BindLoginRegisterDialog(){
            $('#reg_link_a,#login_link_a').click(function(){
                $('#accountDialog').removeClass('hide');
                $('.shadow').removeClass('hide');
            });
        }

        function CloseDialog(dialog){
            $(dialog).addClass('hide');
            $('.shadow').addClass('hide');
        }

        /*
        点击登陆按钮
        */
        function SubmitLogin(ths){
            $(ths).children(':eq(0)').addClass('hide');
            $(ths).addClass('not-allow').children(':eq(1)').removeClass('hide');
            // 发送Ajax请求
            //完成之后
            $('#model_login .inp .error').remove();

            var post_dict = {};
            $('#model_login input').each(function(){
                post_dict[$(this).attr("name")] = $(this).val();
            });

            $.ajax({
                url: '/login/',
                type: 'POST',
                data: post_dict,
                dataType: 'json',
                success: function(arg){
                    if(arg.status){
                        window.location.href = '/index';
                    }else{
                        $.each(arg.message, function(k,v){

                            //<span class="error">s</span>
                            var tag = document.createElement('span');
                            tag.className = 'error';
                            tag.innerText = v[0]['message'];
                            $('#model_login input[name="'+ k +'"]').after(tag);
                        })
                    }
                }
            });

            $(ths).removeClass('not-allow').children(':eq(1)').addClass('hide');
            $(ths).children(':eq(0)').removeClass('hide');
        }

        /*
        点击注册按钮
        */
        function SubmitRegister(ths){
            $('#register_error_summary').empty();
            $('#model_register .inp .error').remove();

            $(ths).children(':eq(0)').addClass('hide');
            $(ths).addClass('not-allow').children(':eq(1)').removeClass('hide');

            var post_dict = {};
            $('#model_register input').each(function(){
                post_dict[$(this).attr("name")] = $(this).val();
            });

            $.ajax({
                url: '/register/',
                type: 'POST',
                data: post_dict,
                dataType: 'json',
                success: function(arg){
                    if(arg.status){
                        window.location.href = '/index';
                    }else{
                        $.each(arg.message, function(k,v){
                            //<span class="error">s</span>
                            var tag = document.createElement('span');
                            tag.className = 'error';
                            tag.innerText = v[0]['message'];
                            $('#model_register input[name="'+ k +'"]').after(tag);
                        })
                    }
                }
            });

            $(ths).removeClass('not-allow').children(':eq(1)').addClass('hide');
            $(ths).children(':eq(0)').removeClass('hide');
        }


        //绑定了，一个发送短信验证码的事件
        function BindSendMsg(){
            $("#fetch_code").click(function(){
                // 整体错误清空
                $('#register_error_summary').empty();
                // 获取邮箱输入的值
                var email = $('#email').val();
                if(email.trim().length == 0){
                    $('#register_error_summary').text('请输入注册邮箱');
                    return;
                }
                // 点击的按钮
                if($(this).hasClass('sending')){
                    // sending 使得按钮置灰
                    // 遇到return下面不再继续执行
                    return;
                }
                var ths = $(this);
                var time = 60;

                $.ajax({
                    url: "/send_msg/",
                    type: 'POST',
                    data: {email: email},
                    dataType: 'json',
                    success: function(arg){
                        // {'status': False, "summary": '整体错误错误', 'error': {}}
                        if(!arg.status){
                            $('#register_error_summary').text(arg.summary);
                        }else{
                            // 后台已经发送成功
                            ths.addClass('sending');
                            var interval = setInterval(function(){
                                ths.text("已发送(" + time + ")");
                                time -= 1;
                                if(time <= 0){
                                    clearInterval(interval); // 干掉计时器
                                    ths.removeClass('sending');
                                    ths.text("获取验证码");
                                }
                            }, 1000);
                        }
                    }
                });

            });
        }


        /*
        * 绑定一个“发版栏”切换按钮的方法
        * */
        function BindTabMenu(title, body) {
            $(title).children().bind("click", function () {
                var $menu = $(this);
                var $content = $(body).find('div[content="' + $(this).attr("content-to") + '"]');
                $menu.addClass('current').siblings().removeClass('current');
                $content.removeClass('hide').siblings().addClass('hide');
            });
        }
