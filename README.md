# PythonFullStack
python(版本 3.6.1)
需要安装一些 依赖的包：(python_warehouse.txt)
  -- import requests
  -- from lxml import etree
  -- PIL -> pillow
  -- pyMySql
  -- docxtpl 
  -- redis
  -- xlrd
  -- pandas
  -- 直接使用 pip install -r python_warehouse.txt
 Django版本: Django2.1.3
 自定义样式文件路径：	.\TestPlatform\statics\css\commons.css
 前端js框架:        	jquery-2.1.4.min.js
 前端样式框架文件:   	bootstrap-3.3.7-dist
 后端数据库支持:     	sqlit3
 模板存放路径:      	.\TestPlatform\templates\TR_templates\test_pro2.docx
 excel模板存放路径:		.\TestPlatform\templates\TR_templates\template.xlsx
 绘图插件Echarts:		/statics/js/echarts.js


系统简介：
	

	-- 新增功能：报告发送功能
		** 基本操作
			-- 注册用户 ——> 
			  登录系统 ——> 
			  获取项目名 ——> 
			  选择项目 ——> 
			  获取数据 ——> 
			  填写信息 ——> 
			  生成测试报告(可对生成的报告进行校对和修改) ——>
			  填写收件人 和 邮件内容 ——>
			  发送报告

		** 本功能为发送测试报告 报告中的数据信息分为：
			-- 用户手填信息
			-- 禅道中的BUG信息
			  ** 新禅道(通过数据库获取信息)
			  ** 老禅道(通过爬虫获取信息)
			  
		** 使用注意事项 
			-- 注册用户名时 使用禅道用户名
			-- 注册邮箱时 使用公司的邮箱
			-- 注册密码时 老禅道密码 和 邮箱密码 保持一致，

		
	-- 新增功能：接口性能测试功能
		** 基本操作
			-- 基本中输入：请求方式、请求地址、请求路径、请求头、请求体 ——>
			-- 高级中输入：最大并发数、启动并发数、响应时长控制、请求断言控制 ——>
			-- 配置中输入：服务器地址、服务器端口、服务器用户、服务器密码 ——>
			-- 启动“_开始运行”  进行压力测试
		
		** 本功能为性能压测 
			-- 所填信中 请求地址 为必填项
			-- 不是用的线程进行请求 而是 协程
			-- 前端绘图使用的是百度的echarts
			
		** 使用注意事项 
			-- 每个输入框中的值都有一个比较固定的格式，请根据需求填写
			-- 执行开始后 并发个数可能会出现 大于 最大并发数的现象 属于是正常
			
			
	-- 新增功能：首页(未完待续)
		** 实现原理
			-- 圈外：使用爬虫 爬取今日头条信息(TOP15)
			-- 圈里：手动发布 测试相关的技术文章