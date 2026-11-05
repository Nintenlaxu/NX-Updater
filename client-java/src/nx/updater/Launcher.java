package nx.updater;
import java.nio.file.*;import java.util.*;
/** Recovery occurs before the game's JAR is opened (important on Windows). */
public final class Launcher {
 public static void main(String[] args)throws Exception{Path root=Paths.get(args.length==0?".":args[0]).toAbsolutePath().normalize();UpdateConfig c=new UpdateConfig(root);UpdateInstaller.noLinks(root,c.work);Files.createDirectories(c.work);try(java.nio.channels.FileChannel ch=java.nio.channels.FileChannel.open(c.work.resolve("install.lock"),StandardOpenOption.CREATE,StandardOpenOption.WRITE);java.nio.channels.FileLock lock=ch.tryLock()){if(lock==null)throw new IllegalStateException("Instalación en curso; intenta más tarde");new UpdateInstaller(c).recover();}
  String java=Paths.get(System.getProperty("java.home"),"bin",System.getProperty("os.name").startsWith("Windows")?"java.exe":"java").toString();List<String> command=new ArrayList<>(Arrays.asList(java,"-cp",root.resolve("street-cbtis4-multiplayer.jar")+System.getProperty("path.separator")+root.resolve("lib/*"),"streetfighter.Main"));for(int i=1;i<args.length;i++)command.add(args[i]);Process p=new ProcessBuilder(command).directory(root.toFile()).inheritIO().start();System.exit(p.waitFor());}
}
