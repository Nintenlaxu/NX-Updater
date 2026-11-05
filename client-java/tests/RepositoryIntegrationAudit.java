package nx.updater;
import java.nio.file.*;import java.nio.charset.StandardCharsets;
public final class RepositoryIntegrationAudit {
 static void check(boolean b,String label){if(!b)throw new AssertionError(label);System.out.println("PASS "+label);}
 static Path root(String config)throws Exception{Path p=Files.createTempDirectory("nx-repo-audit-");Files.createDirectories(p.resolve("config"));Files.write(p.resolve("config/nx-updater.properties"),config.getBytes(StandardCharsets.UTF_8));return p;}
 public static void main(String[] args)throws Exception {
  UpdateConfig legacy=new UpdateConfig(root("repository=example/releases\n"));check(legacy.releaseRepository.equals(legacy.repository),"legacy repository remains compatible");
  Path p=root("repository=Nintenlaxu/NX-Updater\ndistributionRepository=\nchannel=DEVELOPMENT\n");UpdateConfig c=new UpdateConfig(p);
  check(c.repository.equals("Nintenlaxu/NX-Updater")&&!c.configured(),"private control repository does not enable anonymous downloads");
  check(c.configurationIssue().contains("privado"),"private feed explains missing distribution");
  UpdateService s=new UpdateService(p);s.check(true);long deadline=System.nanoTime()+3000000000L;while(s.busy&&System.nanoTime()<deadline)Thread.sleep(10);
  check(!s.busy&&s.offer==null&&s.status.contains("distribución pendiente"),"game remains available without feed or network");
  UpdateConfig publicFeed=new UpdateConfig(root("repository=Nintenlaxu/NX-Updater\ndistributionRepository=example/public-feed\n"));
  check(publicFeed.releaseRepository.equals("example/public-feed")&&!publicFeed.configured(),"distribution still requires trusted key");
  try{new UpdateConfig(root("repository=Nintenlaxu/NX-Updater\ndistributionRepository=bad value\n"));throw new AssertionError("Invalid repository accepted");}catch(java.io.IOException expected){System.out.println("PASS invalid distribution rejected");}
 }
}
