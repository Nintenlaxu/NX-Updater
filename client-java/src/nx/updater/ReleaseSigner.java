package nx.updater;
import java.nio.file.*;import java.nio.charset.StandardCharsets;import java.security.*;import java.security.spec.*;import java.util.*;
/** Offline publisher utility. Private keys are never created, logged or included in releases. */
public final class ReleaseSigner {
 public static void main(String[] args)throws Exception{if(args.length!=3)throw new IllegalArgumentException("private-pkcs8.pem manifest.json output.sig");Path output=Paths.get(args[2]);if(Files.exists(output))throw new IllegalArgumentException("No se sobrescribe una firma existente");String pem=new String(Files.readAllBytes(Paths.get(args[0])),StandardCharsets.US_ASCII).replace("-----BEGIN PRIVATE KEY-----","").replace("-----END PRIVATE KEY-----","").replaceAll("\\s","");PrivateKey key=KeyFactory.getInstance("RSA").generatePrivate(new PKCS8EncodedKeySpec(Base64.getDecoder().decode(pem)));Signature signer=Signature.getInstance("SHA256withRSA");signer.initSign(key);signer.update(Files.readAllBytes(Paths.get(args[1])));Files.write(output,Base64.getEncoder().encode(signer.sign()),StandardOpenOption.CREATE_NEW);System.out.println("Firma creada. La clave privada no se copia al paquete.");}
}
