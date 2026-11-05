package nx.updater;
import java.math.BigInteger;
public final class SemVer implements Comparable<SemVer>{
 private final BigInteger[] n=new BigInteger[3];private final String pre;public final String value;
 public SemVer(String s){if(s==null||!s.matches("(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)(-[0-9A-Za-z-]+(\\.[0-9A-Za-z-]+)*)?(\\+[0-9A-Za-z-]+(\\.[0-9A-Za-z-]+)*)?"))throw new IllegalArgumentException("SemVer inválida: "+s);value=s;String v=s.split("\\+",2)[0];String[] parts=v.split("-",2);String[] nums=parts[0].split("\\.");for(int i=0;i<3;i++)n[i]=new BigInteger(nums[i]);pre=parts.length==2?parts[1]:"";for(String p:pre.split("\\."))if(p.matches("0[0-9]+"))throw new IllegalArgumentException("SemVer prerelease inválida");}
 public int compareTo(SemVer b){for(int i=0;i<3;i++){int c=n[i].compareTo(b.n[i]);if(c!=0)return c;}if(pre.isEmpty()||b.pre.isEmpty())return pre.isEmpty()?(b.pre.isEmpty()?0:1):-1;String[] a1=pre.split("\\."),b1=b.pre.split("\\.");for(int i=0;i<Math.min(a1.length,b1.length);i++){boolean an=a1[i].matches("[0-9]+"),bn=b1[i].matches("[0-9]+");int c=an&&bn?new BigInteger(a1[i]).compareTo(new BigInteger(b1[i])):(an!=bn?(an?-1:1):a1[i].compareTo(b1[i]));if(c!=0)return c;}return Integer.compare(a1.length,b1.length);}
 public boolean prerelease(){return !pre.isEmpty();}
 public String toString(){return value;}
}
