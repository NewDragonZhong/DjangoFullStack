        $(function () {

            BindPublishDialog();

            BindNewType();

            BindPublishSubmit();

            $('.act-menu').children().eq(0).addClass('active');

        });


        function BindPublishSubmit(){
            $('#submit_link,#submit_text,#submit_img').click(function(){
                // 获取输入内容并提交
                var container = $(this).parent().parent();
                var post_dict = {};
                container.find('input[type="text"],textarea').each(function(){
                    post_dict[$(this).attr('name')] =$(this).val();
                });
                post_dict['news_type_id'] = container.find('.news-type .active').attr('value');

                $.ajax({
                    url: '/index/',
                    type: 'POST',
                    data: post_dict,
                    dataType: 'json',
                    success: function (arg) {
                        if(arg.status){
                            window.location.href = '/index';
                        }else{
                            console.log(arg);
                        }
                    }

                })


            });
        }

        function BindNewType(){
            $('.news-type').children().click(function(){
                $(this).addClass('active').siblings().removeClass('active');
            });
        }


        function BindPublishDialog(){
            $('#publishBtn').click(function(){
                if($('#action_nav').attr('is-login') == 'true'){
                    $('#publishDialog').removeClass('hide');
                }else{
                    $('#accountDialog').removeClass('hide');
                }

                $('.shadow').removeClass('hide');
            });

        }


        function CloseDialog(dialog){
            $(dialog).addClass('hide');
            $('.shadow').addClass('hide');
        }

        window.onkeydown = function(event){
            if(event && event.keyCode == 27){
                $('.dialog,.account-dialog,.shadow').addClass('hide');
            }
        };

        /*
        上传图片
        */
        function UploadImage(ths){
            document.getElementById('upload_img_iframe').onload = UploadImageComplete;
            document.getElementById('upload_img_form').target = 'upload_img_iframe';
            document.getElementById('upload_img_form').submit();
        }

        /*
        上传图片之后回掉函数
        */
        function UploadImageComplete(){
            var origin = $("#upload_img_iframe").contents().find("body").text();
            var obj = JSON.parse(origin);
            if(obj.status){
                var img = document.createElement('img');
                img.src = '/' + obj.data;
                img.style.width = "200px";
                img.style.height = "180px";
                $("#upload_img_form").append(img);
                $('#fakeFile').addClass('hide');
                $('#reUploadImage').removeClass('hide');
                $('#fakeFile').find('input[type="text"]').val(obj.data);
            }else{
                alert(obj.summary);
            }
        }

        /*
        重新上传图片
        */
        function ReUploadImage(ths){
            $(ths).addClass('hide');
            $("#upload_img_form").find('img').remove();
            $('#fakeFile').removeClass('hide');
        }

		/*
        显示或隐藏评论区
         */
        function ToggleCommentArea(nid){
            var $comment_area = $("#comment_area_" + nid);
            if($comment_area.hasClass('hide')){
                $comment_area.removeClass('hide');
                var $comment_list = $("#comment_list_" + nid);
                $.ajax({
                    url: '/comment/',
                    type: 'get',
                    data: {nid: nid},
                    dataType:"JSON",
                    success: function(arg){
                        // console.log(arg);
                        $comment_list.empty();
                        var html = '';
                        $.each(arg,function (k,v) {
                            var a = '<div class="comment-z"><li class="items" style="padding:8px 0 0 16px;"><span class="folder" id="comment_folder_';
                            var b = v.id;
                            var c = '"><div class="comment-L comment-L-top"><a href="#" class="icons zhan-ico"></a><a href="/user/moyujian/submitted/1"><img src="/statics/images/1.jpg"></a></div><div class="comment-R comment-R-top" style="background-color: rgb(246, 246, 246);"><div class="pp"><a class="name" href="/user/moyujian/submitted/1">';
                            var d = v.username;
                            var e = '</a><span class="p3">';
                            var f = v.content+'</span>';
                            var g = '<span class="into-time into-time-top">';
                            var h = v.ctime;
                            var i = '</span></div><div class="comment-line-top"><div class="comment-state"><a class="ding" href="javascript:void(0);"><b>顶</b><span class="ding-num">[0]</span></a><a class="cai" href="javascript:void(0);"><b>踩</b><span class="cai-num">[0]</span></a><span class="line-huifu">|</span> <a class="see-a jubao" href="javascript:void(0);">举报</a> <span class="line-huifu">|</span> <a class="see-a huifu-a" href="javascript:void(0);" onclick="';
                            var j = "reply(" + v.news_id + "," +v.id+",'"+v.username+"')";
                            var k = '">回复</a></div></div></div></span></li>'+comment_tree(v.children)+'</div>';
                            html = a+b+c+d+e+f+g+h+i+j+k;

                            $comment_list.append(html);
                        });

                        var $loading = $comment_area.find('.comment-box').children().first();
                        $loading.addClass('hide');
                        $loading.siblings().removeClass('hide');
                    }
                })
            }else{
                $comment_area.addClass('hide');
            }
        }

        /*
        创建评论树
         */
       function comment_tree(comment_child) {
            var tag = '';
            $.each(comment_child,function (ak,av) {
                var a = '<div class="comment-z"><li class="items" style="padding:8px 0 0 16px;"><span class="folder" id="comment_folder_';
				var b = av.id;
				var c = '"><div class="comment-L comment-L-top"><a href="#" class="icons zhan-ico"></a><a href="/user/moyujian/submitted/1"><img src="/statics/images/1.jpg"></a></div><div class="comment-R comment-R-top" style="background-color: rgb(246, 246, 246);"><div class="pp"><a class="name" href="/user/moyujian/submitted/1">';
				var d = av.username;
				var e = '</a><span class="p3">';
				var f = av.content;
				var g= '</span><span class="into-time into-time-top">';
				var h = av.ctime;
				var i = '</span></div><div class="comment-line-top"><div class="comment-state"><a class="ding" href="javascript:void(0);"><b>顶</b><span class="ding-num">[0]</span></a><a class="cai" href="javascript:void(0);"><b>踩</b><span class="cai-num">[0]</span></a><span class="line-huifu">|</span> <a class="see-a jubao" href="javascript:void(0);">举报</a> <span class="line-huifu">|</span> <a class="see-a huifu-a" href="javascript:void(0);" onclick="';
				var j = "reply(" + av.news_id + "," +av.id+",'"+av.username+"')";
				var k = '">回复</a></div></div></div></span></li>'+comment_tree(av.children)+'</div>';
				tag = a+b+c+d+e+f+g+h+i+j+k;
            });
            return tag;
        }



        /*
        隐藏评论区
         */
        function HideCommentArea(nid){
            $("#comment_area_" + nid).addClass('hide');
        }

        /*
        发布评论
         */
        function DoComment(nid){
            var content = $("#comment_content_"+nid).val();
            var reply_id = $("#reply_id_"+nid).attr('target');

            if($('#action_nav').attr('is-login') == 'true'){
                $.ajax({
                    url: '/comment/',
                    type: 'POST',
                    data: {content: content, reply_id:reply_id, news_id: nid},
                    dataType: 'json',
                    success: function(arg){
                        // 获取评论信息，将内容添加到指定位置
                        if(arg.status){
                            $('#comment_content_' + arg.data.news_id).val('');
                            var a = '<div class="comment-z"><li class="items" style="padding:8px 0 0 16px;"><span class="folder" id="comment_folder_';
                            var b = arg.data.nid;
                            var c = '"><div class="comment-L comment-L-top"><a href="#" class="icons zhan-ico"></a><a href="/user/moyujian/submitted/1"><img src="/statics/images/1.jpg"></a></div><div class="comment-R comment-R-top" style="background-color: rgb(246, 246, 246);"><div class="pp"><a class="name" href="/user/moyujian/submitted/1">';
                            var d = arg.data.username;
                            var e = '</a><span class="p3">';
                            var f = arg.data.content;
                            var g= '</span><span class="into-time into-time-top">';
                            var h = arg.data.ctime;
                            var i = '</span></div><div class="comment-line-top"><div class="comment-state"><a class="ding" href="javascript:void(0);"><b>顶</b><span class="ding-num">[0]</span></a><a class="cai" href="javascript:void(0);"><b>踩</b><span class="cai-num">[0]</span></a><span class="line-huifu">|</span> <a class="see-a jubao" href="javascript:void(0);">举报</a> <span class="line-huifu">|</span> <a class="see-a huifu-a" href="javascript:void(0);" onclick="';
                            var j = "reply(" + arg.data.news_id + "," +arg.data.nid+",'"+arg.data.username+"')";
                            var k = '">回复</a></div></div></div></span></li></div>';
                            var tag = a+b+c+d+e+f+g+h+i+j+k;
                            console.log(arg,tag);
                            if(arg.data.reply_id){
                                $comment_folder = $('#comment_folder_' + arg.data.reply_id);
                                $comment_folder.after(tag);
                            }else{
                                $('#comment_list_'+arg.data.news_id).append(tag);
                            }

                        }else{
                            alert('error');
                        }
                    }
                })
            }else{
                $('#accountDialog').removeClass('hide');
                $('.shadow').removeClass('hide');
            }
        }

        /*
        点赞
         */
        function DoFavor(ths, nid) {

            if($('#action_nav').attr('is-login') == 'true'){
                $.ajax({
                    url: '/favor/',
                    type: 'POST',
                    data: {news_id: nid},
                    dataType: 'json',
                    success: function(arg){
                        if(arg.status){
                            var $favorCount = $('#favor_count_'+nid);
                            var c = parseInt($favorCount.text());
                            if(arg.code == 2301){
                                $favorCount.text(c + 1);
                                $(ths).find('span').addClass('active');
                                AddFavorAnimation(ths);
                            }else if(arg.code == 2302){
                                $favorCount.text(c - 1);
                                $(ths).find('span').removeClass('active');
                                MinusFavorAnimation(ths);
                            }else{

                            }

                        }else{

                        }
                    }
                })
            }else{
                $('#accountDialog').removeClass('hide');
                $('.shadow').removeClass('hide');
            }
        }

        /*
        点赞+1效果
         */
        function AddFavorAnimation(ths){
            var offsetTop = -10;
            var offsetLeft = 20;
            var fontSize = 24;
            var opacity = 1;
            var tag = document.createElement('i');
            tag.innerText = "+1";
            tag.style.position = 'absolute';
            tag.style.top = offsetTop + 'px';
            tag.style.left = offsetLeft + 'px';
            tag.style.fontSize = fontSize + "px";
            tag.style.color = "#5cb85c";
            $(ths).append(tag);

            var addInterval = setInterval(function(){
                    fontSize += 5;
                    offsetTop -= 15;
                    offsetLeft += 5;
                    opacity -= 0.1;
                    tag.style.top = offsetTop+ 'px';
                    tag.style.left = offsetLeft+ 'px';
                    tag.style.fontSize = fontSize + 'px';
                    tag.style.opacity = opacity;
                if(opacity <= 0.5){
                    tag.remove();
                    clearInterval(addInterval);
                }
            },80)
        }

        /*
        点赞-1效果
         */
        function MinusFavorAnimation(ths){
            var offsetTop = -10;
            var offsetLeft = 20;
            var fontSize = 24;
            var opacity = 1;
            var tag = document.createElement('i');
            tag.innerText = "-1";
            tag.style.position = 'absolute';
            tag.style.top = offsetTop + 'px';
            tag.style.left = offsetLeft + 'px';
            tag.style.fontSize = fontSize + "px";
            tag.style.color = "#787878";
            $(ths).append(tag);

            var addInterval = setInterval(function(){
                    fontSize += 5;
                    offsetTop -= 15;
                    offsetLeft += 5 ;
                    opacity -= 0.1;
                    tag.style.top = offsetTop+ 'px';
                    tag.style.left = offsetLeft+ 'px';
                    tag.style.fontSize = fontSize + 'px';
                    tag.style.opacity = opacity;
                if(opacity <= 0.5){
                    tag.remove();
                    clearInterval(addInterval);
                }
            },80)
        }

        /**
         * 回复评论
         * @param news_id
         * @param comment_id
         * @param username
         */
        function reply(news_id, comment_id, username){
            var $reply = $('#reply_id_' + news_id);
            $reply.attr('target', comment_id);
            $reply.text(username);
            $reply.parent().css('display','block');
        }