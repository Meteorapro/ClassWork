<%@ page contentType="text/html;charset=GBK" %>
<html>
<head><title>声明的使用</title></head>
<body>
<%-- 声明变量--%>
<%! long i=0;%>
<%! String name="王红";%>
<%-- 声明方法--%>
<%! public String sayHello(String who){
      return "你好，"+who+"!";
	}
%>
<h2 align="center">
<%
	i++;
	out.println(sayHello(name));
	out.println("<br/>");
	out.println("您是本站的第"+i+"位访客。");
%>
</h2>
</body>
</html>