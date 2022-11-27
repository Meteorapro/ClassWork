<%@ page contentType="text/html;charset=GBK" %>
<html>
	<head>
      <title>使用out对象输出行变色表格</title>
	</head>
	<body>
	<table width="50%" align="center">
	<%
		int i=0;
		while(i<10){
			i++;
			if(i%2==0) {
				out.println("<tr bgcolor=\"#00FF00\">");
			}else{
				out.println("<tr bgcolor=\"#0000FF\">");
			}
			out.println("<td>当前行数："+i+"</td>");
			out.println("</tr>");
		}		 
	%>
	</table>
	</body>
</html>