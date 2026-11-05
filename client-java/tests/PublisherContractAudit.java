package nx.updater;
import java.nio.file.*;import java.security.*;import java.util.*;
public final class PublisherContractAudit {
 public static void main(String[] args)throws Exception {
  byte[] raw=Files.readAllBytes(Paths.get(args[0]));KeyPairGenerator g=KeyPairGenerator.getInstance("RSA");g.initialize(2048);KeyPair k=g.generateKeyPair();
  Signature s=Signature.getInstance("SHA256withRSA");s.initSign(k.getPrivate());s.update(raw);
  UpdateManifest m=UpdateManifest.verified(raw,Base64.getEncoder().encode(s.sign()),k.getPublic());
  m.compatible("0.1.0","PC_JAVA","DEVELOPMENT","CB4-LAN-3");
  DownloadManager h=new DownloadManager(false);for(UpdateManifest.Entry e:m.files)if(!e.action.equals("DELETE"))h.validate(e.url);
  if(m.files.size()!=3)throw new AssertionError("Expected ADD/REPLACE/DELETE fixture");
  System.out.println("PASS Python publisher -> Java signature, manifest, version, protocol and HTTPS contract");
 }
}
