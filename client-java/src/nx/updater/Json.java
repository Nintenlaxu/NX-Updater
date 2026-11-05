package nx.updater;
import java.util.*;
/** Small strict JSON reader: bounded input, duplicate keys rejected. No script evaluation. */
public final class Json {
 private final String s;private int i;
 private Json(String s){if(s.length()>4*1024*1024)throw new IllegalArgumentException("JSON demasiado grande");this.s=s;}
 public static Object parse(String s){Json p=new Json(s);Object v=p.value(0);p.ws();if(p.i!=s.length())throw new IllegalArgumentException("JSON sobrante");return v;}
 @SuppressWarnings("unchecked") public static Map<String,Object> object(Object o){if(!(o instanceof Map))throw new IllegalArgumentException("Se esperaba objeto JSON");return (Map<String,Object>)o;}
 @SuppressWarnings("unchecked") public static List<Object> array(Object o){if(!(o instanceof List))throw new IllegalArgumentException("Se esperaba lista JSON");return (List<Object>)o;}
 public static String str(Map<String,Object> m,String k){Object v=m.get(k);if(!(v instanceof String))throw new IllegalArgumentException("Falta "+k);return (String)v;}
 public static long num(Map<String,Object> m,String k){Object v=m.get(k);if(!(v instanceof Long))throw new IllegalArgumentException("Entero requerido "+k);return (Long)v;}
 private void ws(){while(i<s.length()&&" \t\r\n".indexOf(s.charAt(i))>=0)i++;}
 private char take(){if(i>=s.length())throw new IllegalArgumentException("JSON truncado");return s.charAt(i++);}
 private Object value(int d){if(d>32)throw new IllegalArgumentException("JSON anidado");ws();char c=take();
  if(c=='"')return string();
  if(c=='{'){Map<String,Object> m=new LinkedHashMap<>();ws();if(i<s.length()&&s.charAt(i)=='}'){i++;return m;}while(true){ws();if(take()!='"')throw new IllegalArgumentException("Clave JSON");String k=string();ws();if(take()!=':')throw new IllegalArgumentException(":");if(m.containsKey(k))throw new IllegalArgumentException("Clave duplicada");m.put(k,value(d+1));ws();c=take();if(c=='}')return m;if(c!=',')throw new IllegalArgumentException(",");}}
  if(c=='['){List<Object> a=new ArrayList<>();ws();if(i<s.length()&&s.charAt(i)==']'){i++;return a;}while(true){a.add(value(d+1));if(a.size()>100000)throw new IllegalArgumentException("Lista excesiva");ws();c=take();if(c==']')return a;if(c!=',')throw new IllegalArgumentException(",");}}
  i--;for(String literal:new String[]{"true","false","null"})if(s.startsWith(literal,i)){i+=literal.length();return literal.equals("null")?null:Boolean.valueOf(literal);}
  int start=i;if(i<s.length()&&s.charAt(i)=='-')i++;if(i>=s.length()||!Character.isDigit(s.charAt(i)))throw new IllegalArgumentException("JSON inválido");if(s.charAt(i)=='0')i++;else while(i<s.length()&&Character.isDigit(s.charAt(i)))i++;
  return Long.valueOf(s.substring(start,i));
 }
 private String string(){StringBuilder b=new StringBuilder();while(true){char c=take();if(c=='"')return b.toString();if(c<32)throw new IllegalArgumentException("Control JSON");if(c=='\\'){c=take();switch(c){case '"':case '\\':case '/':break;case 'b':c='\b';break;case 'f':c='\f';break;case 'n':c='\n';break;case 'r':c='\r';break;case 't':c='\t';break;case 'u':if(i+4>s.length())throw new IllegalArgumentException("Unicode");c=(char)Integer.parseInt(s.substring(i,i+4),16);i+=4;break;default:throw new IllegalArgumentException("Escape JSON");}}b.append(c);}}
}
