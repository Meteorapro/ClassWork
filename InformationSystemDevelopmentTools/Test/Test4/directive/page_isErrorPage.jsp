<%@ page contentType="text/html;charset=GBK" %>
<%@ page isErrorPage="true"%>
<html>
<head><title>page指令isErrorPage属性的使用</title></head>
<body>
<h1>这是一个异常处理页面</h1>
<h2>当page_errorPage.jsp页面发生异常时，可看到本页面内容</h2>
<b>错误描述：</b><%= exception.toString() %><p/>
<b>详细出错原因：</b>
<pre>
<%
	exception.printStackTrace(new java.io.PrintWriter(out)); 
%>
</pre>
</body>
</html> 
