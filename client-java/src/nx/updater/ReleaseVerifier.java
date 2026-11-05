package nx.updater;
import java.nio.file.*;
/** Publisher preflight: uses exactly the same contract and trust checks as the game. */
public final class ReleaseVerifier {
 public static void main(String[] args)throws Exception {
  if(args.length!=7)throw new IllegalArgumentException("public.pem manifest.json signature.sig installed platform channel protocol");
  UpdateManifest m=UpdateManifest.verified(Files.readAllBytes(Paths.get(args[1])),Files.readAllBytes(Paths.get(args[2])),UpdateManifest.publicKey(Paths.get(args[0])));
  m.compatible(args[3],args[4],args[5],args[6]);
  DownloadManager http=new DownloadManager(false);
  for(UpdateManifest.Entry f:m.files)if(!f.action.equals("DELETE"))http.validate(f.url);
  System.out.println("PASS signed release "+m.version+" / "+m.platform+" / "+m.channel+" / "+m.files.size()+" files");
 }
}
