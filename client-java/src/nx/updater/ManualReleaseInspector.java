package nx.updater;
import java.nio.file.*;
/** PC-side inspection of signed console releases. Never installs or runs an XEX. */
public final class ManualReleaseInspector {
 public static void main(String[] args)throws Exception{if(args.length!=5)throw new IllegalArgumentException("gameRoot platform installedSemVer manifest.json signature.sig");String platform=args[1];if(!platform.equals("XBOX360")&&!platform.equals("PC_CPP"))throw new IllegalArgumentException("Solo paquetes nativos manuales");Path root=Paths.get(args[0]).toAbsolutePath();UpdateManifest m=UpdateManifest.verified(Files.readAllBytes(Paths.get(args[3])),Files.readAllBytes(Paths.get(args[4])),UpdateManifest.publicKey(root.resolve("config/trusted-release-key.pem")));m.compatible(args[2],platform,m.channel,"CB4-LAN-3");System.out.println("NX UPDATER MANUAL ONLY — "+platform+" "+args[2]+" -> "+m.version+" / "+m.channel);System.out.println(m.notes);for(UpdateManifest.Entry f:m.files)System.out.println(f.action+" "+f.path+" bytes="+f.size+" SHA256="+f.sha256);System.out.println("NO instalación automática. Verifica los paquetes en PC y copia a una carpeta NUEVA de la consola. Conserva la instalación previa.");}
}
