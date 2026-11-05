"""Proposal study sheet (sözlü anlatım + midterm metni + soru-cevap) -> PDF."""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                KeepTogether, PageBreak)

OUT = sys.argv[1]
pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", r"C:\Windows\Fonts\ariali.ttf"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-Bold")

NAVY = colors.HexColor("#1F3864")
ORANGE = colors.HexColor("#C55A11")
LIGHT = colors.HexColor("#EEF3FA")
CREAM = colors.HexColor("#FFF8EC")

base = dict(fontName="Arial", fontSize=10, leading=14)
S = {
    "title": ParagraphStyle("title", fontName="Arial-Bold", fontSize=18, leading=22, textColor=NAVY, alignment=TA_CENTER),
    "sub": ParagraphStyle("sub", fontName="Arial", fontSize=10, leading=13, textColor=colors.grey, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="Arial-Bold", fontSize=13, leading=17, textColor=NAVY, spaceBefore=10, spaceAfter=5),
    "body": ParagraphStyle("body", **base),
    "en": ParagraphStyle("en", fontName="Arial", fontSize=10.5, leading=15),
    "tr": ParagraphStyle("tr", fontName="Arial-Italic", fontSize=9.5, leading=13, textColor=colors.HexColor("#444444")),
    "cell": ParagraphStyle("cell", fontName="Arial", fontSize=9, leading=12),
    "cellb": ParagraphStyle("cellb", fontName="Arial-Bold", fontSize=9, leading=12, textColor=colors.white),
    "big": ParagraphStyle("big", fontName="Arial-Bold", fontSize=12, leading=16, alignment=TA_CENTER, textColor=NAVY),
}

def box(flowables, bg=LIGHT, border=NAVY):
    t = Table([[flowables]], colWidths=[17 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 0.8, border),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t

def table(header, rows, widths):
    data = [[Paragraph(h, S["cellb"]) for h in header]] + [[Paragraph(c, S["cell"]) for c in r] for r in rows]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B0B7C3")),
             ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(style))
    return t

P = lambda t, s="body": Paragraph(t, S[s])
story = []

# ---------------------------------------------------------------- header
story += [P("YBS417 – Project Proposal Çalışma Notu", "title"),
          P("Secure Multi-Site Enterprise Network Design for Anatolia Logistics", "sub"), Spacer(1, 10)]

# ---------------------------------------------------------------- 0. iskelet
story.append(P("Önce iskeleti ezberle: 1 cümle + 4 hedef", "h1"))
story.append(box([P("<b>Bir şirket ağı kuruyoruz: merkez + şube + internet.</b>", "big"), Spacer(1, 4),
                  P("Dört hedefin baş harfleri <b>D – C – S – T</b> &nbsp;→&nbsp; <i>“<b>D</b>ün <b>C</b>uma <b>S</b>ınav <b>T</b>ı.”</i>", "big")],
                 bg=CREAM, border=ORANGE))
story.append(Spacer(1, 6))
story.append(table(["Harf", "Hedef", "Ne demek?"], [
    ["<b>D</b>", "<b>Design</b> (Tasarım)", "5 VLAN (IT, HR, Sales, Guest, Servers) + 192.168.10.0/24 bloğunu VLSM ile bölmek"],
    ["<b>C</b>", "<b>Configuration</b> (Yapılandırma)", "Router-on-a-stick, DHCP, OSPF (merkez–şube), NAT (internet)"],
    ["<b>S</b>", "<b>Security</b> (Güvenlik)", "ACL (misafir + HR), SSH, port security, DHCP snooping, OSPF doğrulama"],
    ["<b>T</b>", "<b>Testing</b> (Test)", "Ping testleri, saldırı testleri, Simulation modunda paket analizi"],
], [1.4, 4.2, 11.4]))

# ---------------------------------------------------------------- 1. sözlü anlatım
story.append(P("1. Yarın hocaya sözlü anlatım (~1 dakika)", "h1"))
story.append(P("Yüksek sesle 3–4 kez oku. Kelimesi kelimesine ezberlemen gerekmiyor; D-C-S-T sırasını takip etmen yeterli.", "tr"))
story.append(Spacer(1, 4))
speech = [
    ("“Our project is the network of a fictional company called <b>Anatolia Logistics</b>. The company has a "
     "<b>headquarters</b>, a <b>branch office</b>, and an <b>Internet connection</b>. We will build everything in "
     "<b>Cisco Packet Tracer</b>. We have four goals.”",
     "Projemiz hayali bir şirketin ağı. Merkezi, şubesi ve internet bağlantısı var. Hepsini Packet Tracer'da kuracağız. Dört hedefimiz var."),
    ("“<b>First, design:</b> we will divide the headquarters into five VLANs — IT, HR, Sales, Guest and Servers — and split "
     "one address block, 192.168.10.0/24, with <b>VLSM</b>, so every department gets the right size.”",
     "Tasarım: merkezi 5 VLAN'a ayıracağız ve tek adres bloğunu ihtiyaca göre böleceğiz."),
    ("“<b>Second, configuration:</b> we will use <b>DHCP</b> for automatic addresses, <b>OSPF</b> between the headquarters "
     "and the branch, and <b>NAT</b> for Internet access.”",
     "Yapılandırma: otomatik adres (DHCP), merkez–şube yönlendirmesi (OSPF), internet çıkışı (NAT)."),
    ("“<b>Third, security:</b> <b>ACLs</b> so guests can only reach the Internet and HR is protected, <b>SSH</b> for secure "
     "management, <b>port security</b> and <b>DHCP snooping</b> against attacks.”",
     "Güvenlik: misafir sadece internete çıkar, HR korunur, cihazlar şifreli yönetilir, saldırılar engellenir."),
    ("“<b>Finally, testing:</b> we will test which traffic is allowed and which is blocked, and analyze the packets in "
     "<b>simulation mode</b>.”",
     "Test: hangi trafiğin geçip hangisinin engellendiğini gösterip paketleri simülasyonda inceleyeceğiz."),
]
for en, tr in speech:
    story.append(KeepTogether([P(en, "en"), P("→ " + tr, "tr"), Spacer(1, 5)]))

# ---------------------------------------------------------------- 2. midterm metni
story.append(PageBreak())
story.append(P("2. Midtermde yazacağın proposal", "h1"))
story.append(P("Şablondaki üç alan: <b>Project Title</b>, <b>Team Members</b>, <b>Project Description</b>. "
               "Tamamını yazamazsan bile <b>başlık + 4 madde</b> yeterince güçlü bir proposal olur.", "tr"))
story.append(Spacer(1, 6))
proposal = [
    P("<b>Project Title:</b> Secure Multi-Site Enterprise Network Design for Anatolia Logistics", "en"), Spacer(1, 4),
    P("<b>Team Members:</b> ............................................................................................", "en"), Spacer(1, 4),
    P("<b>Project Description:</b>", "en"),
    P("In this project, we will design, configure, secure and test the network of a fictional company, Anatolia Logistics, "
      "using Cisco Packet Tracer. The company has a headquarters, a branch office and an Internet connection.", "en"), Spacer(1, 4),
    P("<b>1) Design:</b> The headquarters will be divided into five VLANs (IT, HR, Sales, Guest, Servers). The address block "
      "192.168.10.0/24 will be divided with VLSM so each department gets a correctly sized subnet.", "en"), Spacer(1, 3),
    P("<b>2) Configuration:</b> Router-on-a-stick for inter-VLAN routing, DHCP for automatic addressing, OSPF between "
      "headquarters and branch, and NAT for Internet access.", "en"), Spacer(1, 3),
    P("<b>3) Security:</b> Extended ACLs to isolate guests and protect HR, SSH-only remote management, port security, "
      "DHCP snooping and OSPF authentication.", "en"), Spacer(1, 3),
    P("<b>4) Testing:</b> Connectivity tests, attack tests (rogue device, rogue DHCP server) and traffic analysis in "
      "simulation mode.", "en"), Spacer(1, 4),
    P("The project uses only Packet Tracer devices, so it is feasible within the semester.", "en"),
]
story.append(box(proposal))
story.append(Spacer(1, 6))
story.append(P("İpucu: Proposal bir <b>plan</b>dır, bu yüzden gelecek zaman kullanılır: <i>“we <b>will</b> design … we <b>will</b> test”</i>. "
               "Raporda ise geçmiş zaman kullanılır: <i>“we designed”</i>.", "body"))

# ---------------------------------------------------------------- 3. soru-cevap
story.append(P("3. Hocanın sorabileceği sorular", "h1"))
story.append(table(["Soru", "Kısa cevap (EN)", "Türkçe anlamı"], [
    ["Why VLANs?", "To separate departments for <b>security</b> and to reduce broadcast traffic.", "Departmanları ayırmak ve gereksiz yayın trafiğini azaltmak için."],
    ["Why VLSM?", "Departments have different sizes, so VLSM <b>does not waste addresses</b>.", "Herkese ihtiyacı kadar adres; israf yok."],
    ["Why OSPF?", "To share routes <b>automatically</b> between headquarters and branch.", "Merkez ve şube birbirinin ağlarını otomatik öğrenir."],
    ["Why NAT?", "Private addresses can't go to the Internet; NAT uses <b>one public address</b> for everyone.", "İç adresler internette geçmez; herkes tek dış adresi kullanır."],
    ["What does the Guest ACL do?", "Guests can use the <b>Internet only</b>, not the internal network.", "Misafir yalnızca internete çıkar."],
    ["What is port security?", "If an <b>unknown device</b> is plugged in, the switch port shuts down.", "Yabancı cihaz takılırsa port kapanır."],
    ["What is DHCP snooping?", "It blocks a <b>fake DHCP server</b> from giving wrong addresses.", "Sahte adres dağıtıcıyı engeller."],
    ["Is it feasible?", "Yes, we use only devices that exist in Packet Tracer.", "Evet, programda olan cihazlarla yapılıyor."],
], [3.6, 7.2, 6.2]))
story.append(Spacer(1, 8))
story.append(box([P("<b>Hocanın proposal'da aradığı 3 şey:</b> <i>clear, realistic, feasible</i> (açık, gerçekçi, yapılabilir). "
                    "D-C-S-T yapısı “açık”lığı, son cümledeki <i>“only Packet Tracer devices”</i> ifadesi de “yapılabilir”liği karşılar.", "body")],
                 bg=CREAM, border=ORANGE))

def footer(c, doc):
    c.saveState()
    c.setFont("Arial", 8)
    c.setFillColor(colors.grey)
    c.drawString(2 * cm, 1.2 * cm, "YBS417 Network Management and Security – Proposal çalışma notu")
    c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, "Sayfa %d" % doc.page)
    c.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.6 * cm, bottomMargin=1.8 * cm,
                        title="YBS417 Proposal Çalışma Notu", author="Anatolia Logistics Project")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("saved", OUT)
