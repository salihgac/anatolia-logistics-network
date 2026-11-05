# Anatolia Logistics – Packet Tracer Kurulum Rehberi

Bu rehberi sırayla uygularsan raporda anlatılan ağın birebir aynısını Packet Tracer 9.0'da kurmuş olursun.
Rapordaki her **[ SCREENSHOT n ]** yer tutucusunun karşılığı aşağıda **📸 n** olarak işaretli.

---

## 0. Proje ne? (kısa özet)

Kurgusal bir lojistik şirketi var: **Merkez (HQ)** + **Şube (Branch)** + **İnternet (ISP)**.

- HQ'da 5 departman VLAN'ı var: IT (10), HR (20), Sales (30), Guest (40), Servers (50). Şubede VLAN 60 kullanılıyor.
- Tek bir `192.168.10.0/24` bloğu VLSM ile 7 alt ağa bölündü.
- HQ-R1 router'ı şu işleri yapıyor: router-on-a-stick, DHCP, OSPF, NAT ve ACL.
- Güvenlik tarafında şunlar var: SSH, port-security, DHCP snooping, BPDU guard, ACL'ler ve OSPF MD5.
- Testler bağlantı matrisi ve Simulation modu ile yapılıyor.

---

## ⚡ HAZIR DOSYA: `Anatolia_Logistics.pkt`

Ağın tamamı kurulmuş ve yapılandırılmış hâlde bu dosyada. Çift tıklayınca Packet Tracer'da açılır:

- 19 cihaz ve 18 kablo bağlı, bütün konfigürasyonlar yüklü (VLAN, trunk, DHCP, OSPF, NAT, ACL, SSH, port-security, DHCP snooping).
- Sunucular hazır: SRV-WEB (HTTP + DNS kayıtları), SRV-MGMT (Syslog, NTP, TFTP), INET-SRV (HTTP).
- PC'ler DHCP'den otomatik adres alır.
- Packet Tracer 9.0.1'de açılıp test edildi:
  - Sales → HR ping'i engellendi ("Destination host unreachable").
  - IT → HR ping'i geçti.
  - IT-PC1'den HQ-R1'e SSH ile girildi.
  - Şubede OSPF rotaları ve varsayılan rota görüldü.

> Dosya açıldıktan sonra linklerin yeşile dönmesi ~30–60 saniye sürebilir. Sağ alttaki **Fast Forward Time** düğmesine birkaç kez basarak hızlandırabilirsin.

**Ekran görüntüleri de hazır.** 22 görüntünün tamamı bu dosya üzerinden gerçek testlerle alındı ve rapora yerleştirildi. Ham hâlleri `screenshots/` klasöründe, rapordaki birleştirilmiş hâlleri `screenshots/final/` klasöründe duruyor. Yani aşağıdaki 1–9. adımlar artık yalnızca referans: ağı sunumda canlı göstermek veya bir testi kendin tekrarlamak istersen kullanırsın.

Aşağıdaki adımlar ağı sıfırdan kendin kurmak istersen (veya hoca kurulumu canlı görmek isterse) diye duruyor.

---

## 1. Cihazları yerleştir (Logical workspace)

| Cihaz adı (Display Name + Hostname) | PT'deki model |
|---|---|
| HQ-R1, BRANCH-R2, ISP | Network Devices → Routers → **2911** |
| HQ-SW1, HQ-SW2, BRANCH-SW | Network Devices → Switches → **2960** (2960-24TT) |
| SRV-WEB, SRV-MGMT, INET-SRV | End Devices → **Server** |
| IT-PC1, IT-PC2, HR-PC1, HR-PC2, SALES-PC1, SALES-PC2, BR-PC1, BR-PC2 | End Devices → **PC** |
| GUEST-LT1, GUEST-LT2 | End Devices → **PC** (hazır dosyada PC; istersen Laptop da kullanabilirsin) |

> İpucu: Cihaza bir kez tıkla, **Config → Display Name** alanına adını yaz. Yerleşim için `topology.png` dosyasına bakabilirsin.

## 2. Kabloları bağla

| Bağlantı | Port A | Port B | Kablo |
|---|---|---|---|
| HQ-R1 ↔ HQ-SW1 | G0/0 | Gi0/1 | Copper Straight-Through |
| HQ-SW1 ↔ HQ-SW2 | Gi0/2 | Gi0/1 | Copper Cross-Over |
| HQ-R1 ↔ BRANCH-R2 | G0/1 | G0/1 | Copper Cross-Over |
| HQ-R1 ↔ ISP | G0/2 | G0/0 | Copper Cross-Over |
| ISP ↔ INET-SRV | G0/1 | FastEthernet0 | Copper Cross-Over |
| BRANCH-R2 ↔ BRANCH-SW | G0/0 | Gi0/1 | Copper Straight-Through |
| HQ-SW1 | Fa0/1 IT-PC1, Fa0/2 IT-PC2, Fa0/3 HR-PC1, Fa0/4 HR-PC2, Fa0/5 SRV-WEB, Fa0/6 SRV-MGMT | | Straight-Through |
| HQ-SW2 | Fa0/1 SALES-PC1, Fa0/2 SALES-PC2, Fa0/3 GUEST-LT1, Fa0/4 GUEST-LT2 | | Straight-Through |
| BRANCH-SW | Fa0/1 BR-PC1, Fa0/2 BR-PC2 | | Straight-Through |

> ⚠️ Port numaraları önemli. Port-security ve ACL ayarları bu portlara göre yazıldı.

## 3. Sunucuları yapılandır (GUI)

Önce **Desktop → IP Configuration (Static)** ayarlarını yap:

| Sunucu | IP | Mask | Gateway | DNS |
|---|---|---|---|---|
| SRV-WEB | 192.168.10.226 | 255.255.255.240 | 192.168.10.225 | 192.168.10.226 |
| SRV-MGMT | 192.168.10.227 | 255.255.255.240 | 192.168.10.225 | 192.168.10.226 |
| INET-SRV | 198.51.100.10 | 255.255.255.0 | 198.51.100.1 | – |

Ardından **Services** sekmesine geç:

- **SRV-WEB**
  - HTTP: On. `index.html` içeriğini düzenle, örneğin `<h1>Anatolia Logistics Intranet</h1>`.
  - DNS: On. Şu iki A kaydını ekle: `intranet.anatolia.local → 192.168.10.226` ve `www.internet.com → 198.51.100.10`.
  - DHCP: **Off**.
  - 📸 9: DNS kayıtlarının ekranı.
- **SRV-MGMT**
  - SYSLOG: On, NTP: On (Authentication kapalı), TFTP: On, HTTP: Off. DHCP: **Off**.
- **INET-SRV**
  - HTTP: On. `index.html` içeriği: `<h1>Welcome to the Internet</h1>`.

## 4. Network cihazlarını yapılandır (CLI)

`configs/` klasöründeki her dosya bir cihazın komutlarını içeriyor:

1. Cihaza tıkla ve **CLI** sekmesini aç. "Would you like to enter the initial configuration dialog?" sorusuna `no` yazıp Enter'a bas.
2. Önce `Router>` veya `Switch>` prompt'unu gör. Sonra `.txt` dosyasının **tamamını** kopyala, CLI penceresine sağ tık → Paste ile yapıştır.
3. Önerilen sıra: **ISP → HQ-R1 → BRANCH-R2 → HQ-SW1 → HQ-SW2 → BRANCH-SW**.

Notlar:

- Yapıştırırken kırmızı `% Invalid input` görürsen hangi satır olduğuna bak ve bana ilet, birlikte düzeltelim.
- Switch'lerde `crypto key` satırı birkaç saniye sürebilir. Bu normal.
- Konfigürasyonun sonunda `write memory` var. Yine de `.pkt` dosyasını sık sık kaydet.
- Yapılandırdıktan sonra cihaz şifreleri şöyle: enable `Ent3rpr1se!`, console `C0ns0leP@ss`, SSH `netadmin / Adm1nP@ss!`.

## 5. PC'leri DHCP'ye al

Her PC ve laptop'ta **Desktop → IP Configuration → DHCP** seçeneğini işaretle. Birkaç saniye içinde IP gelmesi gerekiyor:

| Cihaz grubu | Beklenen IP aralığı |
|---|---|
| IT | 192.168.10.140+ |
| HR | 192.168.10.171+ |
| Sales | 192.168.10.75+ |
| Guest | 192.168.10.11+ |
| Branch | 192.168.10.201+ |

- 📸 4: Bir PC'nin DHCP'den adres aldığını gösteren IP Configuration ekranı.
- 📸 5: HQ-R1'de `show ip dhcp binding` çıktısı.

> IP gelmezse önce switch-router arasındaki linklerin yeşil olmasını bekle, sonra DHCP'yi tekrar seç. PT'de "Fast Forward Time" düğmesine basmak da işe yarar.

## 6. Ekran görüntüleri – doğrulama komutları

> Ayrıcalıklı moda geçmek için önce `enable` yaz, enable şifresini gir.

| 📸 | Nerede | Ne yapılacak |
|---|---|---|
| 1 | Workspace | Tüm topolojinin ekran görüntüsü |
| 2 | HQ-SW1 | `show vlan brief` |
| 3 | HQ-SW1 | `show interfaces trunk` |
| 6 | HQ-R1 | `show ip ospf neighbor` (FULL görünmeli) |
| 7 | BRANCH-R2 | `show ip route` (O ve O*E2 rotaları görünmeli) |
| 8 | HQ-R1 | Önce SALES-PC1 → Web Browser → `www.internet.com`, ardından `show ip nat translations` |
| 10 | SRV-MGMT | Services → SYSLOG (router mesajları görünmeli; bir interface'i kapatıp açarak mesaj üretebilirsin) |
| 11 | SRV-MGMT | Önce HQ-R1'de `copy running-config tftp:` → adres `192.168.10.227` → Enter, sonra Services → TFTP listesi |
| 12 | IT-PC1 ve SALES-PC1 | Command Prompt: `ssh -l netadmin 192.168.10.129` (IT'de bağlanır), aynı komut SALES-PC1'de `192.168.10.65` ile (refused) |
| 15 | HQ-R1 | Bütün testlerden sonra `show access-lists` (match sayaçları görünür) |

## 7. Test matrisi (📸 16, 📸 17)

Bu testleri PC'lerin **Command Prompt** ve **Web Browser** uygulamalarından yap. Önce `ipconfig` ile hedef cihazın IP'sini öğren.

| # | Kaynak | Komut | Beklenen sonuç |
|---|---|---|---|
| 1 | IT-PC1 | `ping <HR-PC1 IP>` | ✅ Başarılı |
| 2 | IT-PC1 | `ping <SALES-PC1>`, `ping <BR-PC1>` | ✅ |
| 3 | SALES-PC1 | `ping <HR-PC1>` | ❌ Destination host unreachable |
| 4 | HR-PC1 | `ping <SALES-PC1>` | ✅ |
| 5 | BR-PC1 | `ping <HR-PC1>` | ❌ |
| 6 | BR-PC1 | Browser: `intranet.anatolia.local` | ✅ Intranet sayfası açılır |
| 7 | SALES-PC1 | Browser: `www.internet.com` | ✅ |
| 8 | GUEST-LT1 | Browser: `www.internet.com` | ✅ |
| 9 | GUEST-LT1 | Browser: `intranet.anatolia.local` | ❌ Request Timeout |
| 10 | GUEST-LT1 | `ping <SALES-PC1>` | ❌ |
| 11 | GUEST-LT1 | `ping 192.168.10.1` | ✅ |
| 12 | IT-PC1 | `ssh -l netadmin 192.168.10.129` | ✅ Banner görünür |
| 13 | SALES-PC1 | `ssh -l netadmin 192.168.10.65` | ❌ Connection refused |
| 14 | IT-PC1 | `telnet 192.168.10.129` | ❌ |
| 15 | IT-PC1 | `ssh -l netadmin 192.168.10.130` ve `192.168.10.194` | ✅ |
| 16 | ISP CLI | `ping 192.168.10.65` | ❌ |

> İlk ping'lerde 1-2 paket ARP yüzünden "Request timed out" verebilir. Bu normal, ikinci denemede düzelir.
> Bir sonuç tablodakinden farklı çıkarsa rapordaki Table 10'u gerçek sonuca göre düzelt, ya da bana yaz.

## 8. Güvenlik saldırı testleri

**Port security (📸 13, 📸 18)**
1. IT-PC2 ile HQ-SW1 Fa0/2 arasındaki kabloyu sil.
2. Yeni bir Laptop ekle ve HQ-SW1 Fa0/2'ye bağla. Laptop'ta DHCP'yi seç ya da herhangi bir ping at.
3. Port kırmızıya döner ve konsolda `%PORT_SECURITY-2-PSECURE_VIOLATION` mesajı görünür.
4. HQ-SW1'de `show port-security interface fa0/2` çalıştır.
5. Geri almak için laptop'u sil ve IT-PC2'yi tekrar bağla. Ardından:
   `conf t` → `interface fa0/2` → `no switchport port-security mac-address sticky` → `switchport port-security mac-address sticky` → `shutdown` → `no shutdown`.
   (En kolay yol: testten önce `.pkt` dosyasını kaydet, test bitince dosyayı kaydetmeden kapatıp yeniden aç.)

**Rogue DHCP (📸 14)** – ⚠️ Testten önce `.pkt` dosyasını kaydet.
1. HQ-SW2'de: `conf t` → `interface fa0/4` → `no switchport port-security`.
2. GUEST-LT2'yi sil. Yerine bir Server koy ve Fa0/4'e bağla.
3. Bu sunucuda DHCP: On, gateway `192.168.10.50`, DNS `8.8.8.8`, start IP `192.168.10.30`. Sunucunun kendi IP'si `192.168.10.40/26` olsun.
4. GUEST-LT1'de önce Static'e, sonra tekrar DHCP'ye geç. Gateway **192.168.10.1** gelirse snooping çalışıyor demektir.
5. HQ-SW2'de `show ip dhcp snooping` çalıştır ve ekran görüntüsünü al.
6. Test bitince dosyayı kaydetmeden kapatıp yeniden aç.

**Brute force**: IT-PC1'den 3 kez yanlış şifreyle SSH dene. Router 120 saniye boyunca girişi kabul etmez.

## 9. Simulation modu (📸 19–22)

Sağ alttaki **Simulation** sekmesine geç. **Edit Filters** bölümünde ARP, DHCP, DNS, HTTP, ICMP, OSPF ve TCP'yi seç.

- **📸 19 DHCP:** SALES-PC1'de Static'e, sonra DHCP'ye geç. Capture/Forward ile DISCOVER → OFFER → REQUEST → ACK akışını izle.
- **📸 20 ACL drop:** SALES-PC1'den HR-PC1'e ping at (veya Add Simple PDU kullan). HQ-R1'deki zarfa tıkla, PDU detaylarında ACL'in paketi düşürdüğünü göreceksin.
- **📸 21 NAT:** GUEST-LT1'den `www.internet.com` aç. HQ-R1'deki PDU'nun Inbound/Outbound kısımlarında kaynak IP'nin `203.0.113.2` olduğunu göster.
- **📸 22 OSPF:** Filtrede yalnızca OSPF'yi bırak, birkaç Forward ilerle. HQ-R1 ↔ BRANCH-R2 arasındaki Hello paketini aç (Auth Type MD5 görünür).

## 10. Raporu tamamla

1. `Project - Anatolia Logistics.docx` dosyasını Word'de aç.
2. Kapaktaki **Name 1/2/3 (Student Number)** alanlarını ve iki tablodaki **Team Members** satırını kendi bilgilerinle doldur.
3. Ekran görüntüleri zaten yerleştirildi. Yalnızca sayfa düzenine bir göz at; büyük görüntülerden önce sayfa sonu eklemek istediğin yerler olabilir.
4. Hoca Teams'teki şablonun düzenlenmesini istiyor. Bu dosyanın içeriğini (Proposal, Summary ve ardından Detailed Project Report) Teams'teki şablona kopyala.
5. Sunum (20 puan) için şu bölümler yeterli: Topoloji, VLSM tablosu, Güvenlik tablosu (Table 9), Test matrisi ve bir canlı demo (ACL drop + port-security).
