<%@ page contentType="text/html;charset=GBK" %>
<html>
<head><title>表达式的使用</title></head>
<body>
<%! long i=0;%>
<%! String name="王红";%>
<%! public String sayHello(String who){
      return "你好，"+who+"!";
	}
%>
<%
	i++;
%>
<%-- 表达式的使用--%>
<h2 align="center">
	<%=sayHello(name) %><br/>
	您是本站的第<%=i %>位访客。
</h2>
</body>
</html>
