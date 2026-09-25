from pathlib import Path
import base64, html

root = Path.home()/"workspace/your_files/iphone-6s-jailbreak-guide"
img = root/".src/media/iphone-6s-colours.webp"
img_uri = "data:image/webp;base64," + base64.b64encode(img.read_bytes()).decode()

SOURCES = {
"dopamine":"https://github.com/opa334/Dopamine/releases",
"trollrestore":"https://github.com/JJTech0130/TrollRestore/releases",
"trollstore":"https://github.com/opa334/TrollStore/releases",
"guide":"https://github.com/lukezgd/ios.cfw.guide/blob/HEAD/docs/en_US/jailbreak/installing-dopamine-trollrestore.md",
"appledb":"https://appledb.dev/jailbreak/Dopamine",
"openclaw":"https://github.com/j0shua-syson/openclaw-ios",
"photo":"https://www.fool.com/investing/2017/06/23/can-you-really-get-a-1-unlimited-data-wireless-pla.aspx",
}

def link(label, key):
    return f'<a href="{html.escape(SOURCES[key])}">{html.escape(label)}</a>'

pages=[]
pages.append(f'''<section class="page cover">
  <header class="brand"><span>NANO NODES</span><span>FIELD GUIDE 01</span></header>
  <div class="cover-grid">
    <div>
      <div class="kicker">iPhone 6s · iOS 15.8.8 · A9</div>
      <h1>Jailbreak an iPhone 6s<br><em>without a PC after every reboot</em></h1>
      <p class="dek">The practical path for turning an old iPhone into a rootless, remotely managed node: <strong>TrollRestore → TrollStore → Dopamine → Sileo → OpenSSH.</strong></p>
      <div class="verdict"><b>Recommended route</b><br>TrollRestore once on a computer, then Dopamine on-device whenever the phone reboots.</div>
    </div>
    <figure class="hero"><img src="{img_uri}" alt="Four Apple iPhone 6s models shown from the front and back"><figcaption>iPhone 6s hardware. Photo source: The Motley Fool.</figcaption></figure>
  </div>
  <div class="facts">
    <div><b>Method</b><span>Rootless, semi-untethered</span></div>
    <div><b>Computer</b><span>Windows first; macOS/Linux also work</span></div>
    <div><b>Research date</b><span>24 September 2026</span></div>
  </div>
  <div class="warning"><b>Read before touching the phone.</b> Jailbreaking weakens parts of iOS's security model and can break banking, work-management, streaming, or anti-cheat apps. Use a device you own, back it up, and keep sensitive accounts off a repurposed node.</div>
  <footer><span>nano-nodes.com · Build small. Run local. Own.</span><span>1 / 7</span></footer>
</section>''')

pages.append('''<section class="page">
  <header><div class="section-no">01</div><h2>Why this is the optimal route</h2></header>
  <p class="lead">For an iPhone 6s already updated to iOS 15.8.8, Dopamine is the better daily driver than palera1n because it can be re-applied from the phone itself after a reboot.</p>
  <div class="compare">
    <div class="choice good"><h3>Dopamine</h3><p class="sub">Recommended</p><ul><li>Rootless filesystem layout under <code>/var/jb</code></li><li>Semi-untethered: tap <b>Jailbreak</b> again after a reboot</li><li>Installs Sileo and a Procursus bootstrap</li><li>No DFU dance for routine reboots</li></ul></div>
    <div class="choice"><h3>palera1n</h3><p class="sub">Fallback</p><ul><li>Uses the unpatchable checkm8 bootROM path</li><li>Requires a computer and DFU after reboot</li><li>Useful when Dopamine will not land</li><li>Rootful mode is legacy-oriented and costs storage</li></ul></div>
  </div>
  <div class="callout"><b>Rootless does not mean “no root.”</b> It means jailbreak files live outside Apple's sealed system volume, mainly under <code>/var/jb</code>. You can still obtain a UID 0 shell and run daemons inside the jailbreak environment; you simply do not rewrite Apple's sealed root filesystem.</div>
  <h3>The chain, in plain English</h3>
  <div class="flow"><span>PC + USB<br><small>one time</small></span><i>→</i><span>TrollRestore<br><small>inject helper</small></span><i>→</i><span>TrollStore<br><small>install IPA</small></span><i>→</i><span>Dopamine<br><small>jailbreak</small></span><i>→</i><span>Sileo<br><small>packages</small></span></div>
  <h3>Compatibility checkpoint</h3>
  <p>A9 support for the patched iOS 15.8.7 branch arrived in Dopamine's 2.5 beta line through the DarkSword exploit. Current compatibility listings include the iPhone 6s on iOS 15.8.8. Because releases move, download the newest <em>official</em> build whose notes still list A9/iOS 15.8.8 support rather than following a mirror's version number.</p>
  <p class="source-note">Check before starting: '''+link('official Dopamine releases','dopamine')+' · '+link('AppleDB compatibility','appledb')+'''</p>
  <footer><span>iPhone 6s jailbreak guide</span><span>2 / 7</span></footer>
</section>''')

pages.append('''<section class="page">
  <header><div class="section-no">02</div><h2>Prepare once, recover easily</h2></header>
  <p class="lead">Do the boring checks first. They are what separate a five-minute retry from a lost afternoon.</p>
  <div class="checklist">
    <div><b>1</b><p><strong>Confirm the target.</strong><br>Settings → General → About should show <b>iOS 15.8.8</b>. This guide is specifically for an iPhone 6s / 6s Plus with the A9 chip.</p></div>
    <div><b>2</b><p><strong>Make an encrypted local backup.</strong><br>Use Finder on macOS or iTunes / Apple Devices on Windows. Confirm the backup completed before continuing.</p></div>
    <div><b>3</b><p><strong>Know the Apple Account password.</strong><br>You need it to turn off Find My temporarily. Do not begin if Activation Lock recovery would be a problem.</p></div>
    <div><b>4</b><p><strong>Use a dependable cable and port.</strong><br>Charge above 50%, unlock the phone, tap <b>Trust</b>, and enter the device passcode when asked.</p></div>
    <div><b>5</b><p><strong>Windows prerequisite.</strong><br>Install the current Apple device driver stack / iTunes so the computer can see the phone. Reconnect once and confirm the phone appears.</p></div>
    <div><b>6</b><p><strong>Temporarily disable Find My.</strong><br>Settings → [your name] → Find My → Find My iPhone → Off. Re-enable it after TrollStore is working.</p></div>
  </div>
  <div class="warning"><b>Security trade-off:</b> iOS 15.8.8 is current for this method, not current iOS. A repurposed node should not carry your primary Apple Account, banking apps, password vault, private photos, or work mobile-device-management profile.</div>
  <h3>Download rule</h3>
  <p>Use project-owned release pages only. Avoid “one-click jailbreak” sites, repacked IPAs, configuration profiles, and ad-gated download buttons. If a guide tells you to disable antivirus permanently or enter an Apple password into a third-party utility, stop.</p>
  <p class="source-note">Primary procedure: '''+link('maintained iOS Guide for TrollRestore + Dopamine','guide')+'''</p>
  <footer><span>Preparation</span><span>3 / 7</span></footer>
</section>''')

pages.append('''<section class="page">
  <header><div class="section-no">03</div><h2>Install TrollStore with TrollRestore</h2></header>
  <p class="lead">This is the only stage that needs a computer. TrollRestore restores a deliberately modified backup that places the TrollStore helper inside a removable Apple system app.</p>
  <div class="step"><span>1</span><div><h3>Download TrollRestore</h3><p>Open the '''+link('official TrollRestore releases page','trollrestore')+'''. On Windows, download <code>TrollRestore.exe</code>. On Apple silicon macOS, choose the arm64 archive; on Intel macOS, choose amd64; on Linux, choose the Linux archive.</p></div></div>
  <div class="step"><span>2</span><div><h3>Connect and trust the phone</h3><p>Unlock the iPhone, connect it by USB, accept <b>Trust This Computer</b>, and leave the phone connected. Find My must already be off.</p></div></div>
  <div class="step"><span>3</span><div><h3>Run TrollRestore</h3><p>On Windows, double-click the executable. If Windows SmartScreen appears, verify the file came from the JJTech0130 GitHub release page before allowing it. Do not substitute a mirror.</p></div></div>
  <div class="step"><span>4</span><div><h3>Choose Tips</h3><p>When prompted for the system app to overwrite, enter <code>Tips</code>. The phone may look idle while the restore runs. Do not unplug it. The phone will reboot when the helper has been injected.</p></div></div>
  <div class="step"><span>5</span><div><h3>Install TrollStore</h3><p>After reboot, unlock the phone and open <b>Tips</b>. Tap <b>Install TrollStore</b>. The interface will respring and TrollStore should appear on the Home Screen.</p></div></div>
  <div class="step"><span>6</span><div><h3>Add persistence, then restore Find My</h3><p>Open TrollStore → Settings → <b>Install Persistence Helper</b> → Tips. Once TrollStore opens normally, turn Find My back on.</p></div></div>
  <div class="callout"><b>If Tips is missing:</b> reinstall Tips from the App Store, reboot, and run TrollRestore again. If the computer cannot see the phone, unlock it, re-accept Trust, try another cable/USB port, and reopen iTunes or Apple Devices.</div>
  <footer><span>TrollRestore → TrollStore</span><span>4 / 7</span></footer>
</section>''')

pages.append('''<section class="page">
  <header><div class="section-no">04</div><h2>Install Dopamine and jailbreak</h2></header>
  <p class="lead">TrollStore keeps the jailbreak app installed. Dopamine applies the jailbreak and creates the rootless environment under <code>/var/jb</code>.</p>
  <div class="step"><span>1</span><div><h3>Download the official IPA</h3><p>On the iPhone, open '''+link('Dopamine Releases','dopamine')+''' and download the current IPA that explicitly supports A9 and iOS 15.8.8. A9 support began in the 2.5 beta line; a newer compatible release is preferable to an old stable build.</p></div></div>
  <div class="step"><span>2</span><div><h3>Install through TrollStore</h3><p>Open TrollStore → <b>+</b> → choose the downloaded Dopamine <code>.ipa</code> in Files → <b>Install</b>. Dopamine should appear on the Home Screen without seven-day re-signing.</p></div></div>
  <div class="step"><span>3</span><div><h3>Start from a clean reboot</h3><p>Reboot the phone, unlock it, then open Dopamine immediately. Select <b>Sileo</b> as the package manager and create a strong sudo password when prompted. Save it in a password manager; it is not your Apple Account password.</p></div></div>
  <div class="step"><span>4</span><div><h3>Run the exploit</h3><p>Tap <b>Jailbreak</b>. The device will respring or userspace-reboot. When it returns, look for Sileo. If Dopamine closes or the phone restarts before completion, reboot and try again; DarkSword can fail a race and the official release notes call this out.</p></div></div>
  <div class="step"><span>5</span><div><h3>Finish the bootstrap</h3><p>Open Sileo, refresh sources, and install all essential updates. The maintained guide then installs or updates <b>ElleKit</b> and <b>PreferenceLoader</b>, followed by a SpringBoard restart. Reboot and re-jailbreak if tweak injection does not initialize cleanly.</p></div></div>
  <div class="success"><b>Success looks like this:</b> Dopamine reports jailbroken, Sileo opens, packages refresh without fatal errors, and <code>/var/jb</code> exists. Stop here before adding tweaks; confirm the base stays stable first.</div>
  <footer><span>Dopamine + Sileo</span><span>5 / 7</span></footer>
</section>''')

pages.append('''<section class="page">
  <header><div class="section-no">05</div><h2>Harden SSH before making it a node</h2></header>
  <p class="lead">Remote shell access is useful and dangerous. Install it only after the jailbreak is stable, and never expose port 22 directly to the public internet.</p>
  <div class="columns">
    <div>
      <h3>On the iPhone</h3>
      <ol><li>In Sileo, install <b>OpenSSH Server</b> and an on-device terminal such as NewTerm.</li><li>Use the strong sudo password created during Dopamine setup. If your bootstrap still has a default password, change it immediately.</li><li>Find the phone's LAN or private-overlay IP. Keep SSH limited to a trusted LAN or private network such as Tailscale.</li></ol>
      <div class="warning small"><b>Do not:</b> port-forward TCP 22 from the router, reuse an Apple Account password, or paste private keys into random tweak prompts.</div>
    </div>
    <div>
      <h3>From your computer</h3>
      <pre><code>ssh mobile@PHONE_IP
sudo -i
id -u
# expected: 0
</code></pre>
      <p>Prefer SSH keys after the first successful login. Keep the private key on your computer and add only the public key to the phone.</p>
      <pre><code>mkdir -p ~/.ssh
chmod 700 ~/.ssh
# append your public key only
chmod 600 ~/.ssh/authorized_keys</code></pre>
    </div>
  </div>
  <h3>Baseline verification</h3>
  <div class="verify"><div><code>id -u</code><span>returns 0 after <code>sudo -i</code></span></div><div><code>test -d /var/jb</code><span>exits successfully</span></div><div><code>dpkg --print-architecture</code><span>shows an iPhone arm64 package architecture</span></div><div><code>uname -a</code><span>identifies the iOS/Darwin host</span></div></div>
  <div class="callout"><b>About “root.”</b> UID 0 is real, but Apple's sealed system volume remains protected. Build for the rootless prefix (<code>/var/jb</code>) and install rootless packages marked for <code>iphoneos-arm64</code>. Old rootful tweaks that hard-code <code>/Library</code> or <code>/usr</code> can break the environment.</div>
  <footer><span>Secure remote access</span><span>6 / 7</span></footer>
</section>''')

pages.append('''<section class="page">
  <header><div class="section-no">06</div><h2>Operate, recover, then build the node</h2></header>
  <div class="columns">
    <div>
      <h3>After every full reboot</h3>
      <ol><li>The phone boots in normal, non-jailbroken mode.</li><li>Open Dopamine.</li><li>Tap <b>Jailbreak</b>.</li><li>Wait for the respring/userspace reboot.</li><li>Confirm Sileo and SSH again.</li></ol>
      <p>This is the convenience advantage over palera1n: routine recovery does not require DFU mode or a computer.</p>
    </div>
    <div>
      <h3>When something fails</h3>
      <dl><dt>Dopamine closes</dt><dd>Reboot and retry. The release notes acknowledge occasional DarkSword failures.</dd><dt>Boot loop fear</dt><dd>Force a normal reboot; a semi-untethered jailbreak should return to stock mode.</dd><dt>A tweak causes crashes</dt><dd>Use Dopamine's safe-mode or disable-tweak-injection option, then remove the last package.</dd><dt>SSH disappears</dt><dd>Re-apply Dopamine first; jailbreak daemons are not active in stock mode.</dd></dl>
    </div>
  </div>
  <h3>Do not auto-update blindly</h3>
  <p>A later iOS update can remove or break the jailbreak even though checkm8 remains available as a hardware fallback. Before installing any future update, check the Dopamine release notes for the exact device, chip, and build. The trade-off is real: delaying updates preserves jailbreak compatibility but also delays security patches.</p>
  <div class="next"><h3>Next Nano Nodes phase: OpenClaw-iOS</h3><p>Once the phone survives a reboot/re-jailbreak cycle and SSH is reliable, the next experiment is a rootless <code>.deb</code> under <code>/var/jb</code>. The '''+link('OpenClaw-iOS project','openclaw')+''' targets iOS 15 arm64 with Dopamine/Procursus, bundles Node.js, and defines a launchd service. Treat it as experimental: its own project notes have tracked active end-to-end work, so validate the current release status before relying on it.</p></div>
  <h3>Sources and downloads</h3>
  <ol class="sources"><li>''' + link('opa334/Dopamine — official releases','dopamine') + '''</li><li>''' + link('JJTech0130/TrollRestore — official releases','trollrestore') + '''</li><li>''' + link('opa334/TrollStore — official releases','trollstore') + '''</li><li>''' + link('iOS Guide — installing Dopamine via TrollRestore','guide') + '''</li><li>''' + link('AppleDB — Dopamine compatibility reference','appledb') + '''</li></ol>
  <p class="fine">Compatibility and instructions checked 24 September 2026. Projects change quickly; re-check release notes before downloading. Jailbreak only a device you own and can restore.</p>
  <footer><span>Recovery + next build</span><span>7 / 7</span></footer>
</section>''')

css='''
@page{size:A4;margin:0}*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}body{margin:0;background:#061018;color:#11212a;font-family:"Liberation Sans","Noto Sans",sans-serif;line-height:1.43}.page{position:relative;width:210mm;height:297mm;overflow:hidden;background:#f3f0e8;padding:17mm 18mm 16mm}.page:not(:last-child){break-after:page}.cover{background:#071820;color:#eef7f2}.brand{display:flex;justify-content:space-between;font-weight:700;letter-spacing:.16em;font-size:8.5pt;color:#a8ff60;border-bottom:1px solid #31505b;padding-bottom:4mm}.cover-grid{display:grid;grid-template-columns:1.25fr .75fr;gap:11mm;align-items:center;margin-top:14mm}.kicker{font-size:9pt;letter-spacing:.13em;text-transform:uppercase;color:#8fc7d8;font-weight:700}h1{font-family:"Noto Serif","Liberation Serif",serif;font-size:31pt;line-height:1.04;margin:5mm 0 7mm;letter-spacing:-.025em}h1 em{font-style:normal;color:#a8ff60}.dek{font-size:13pt;line-height:1.45;color:#d5e6e6;margin:0 0 7mm}.hero{margin:0}.hero img{width:100%;height:118mm;object-fit:cover;object-position:center;border-radius:3mm;background:#fff}.hero figcaption{font-size:8.2pt;color:#86a3ac;margin-top:2mm}.verdict{border-left:4px solid #a8ff60;padding:4mm 5mm;background:#0f2731;border-radius:0 2mm 2mm 0;color:#d9e8e6;font-size:10.2pt}.verdict b{color:#a8ff60}.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:14mm}.facts div{border-top:1px solid #31505b;padding-top:3mm}.facts b{display:block;font-size:8.2pt;text-transform:uppercase;letter-spacing:.09em;color:#8fc7d8}.facts span{display:block;margin-top:1.5mm;font-size:9.5pt;color:#eef7f2}.warning{background:#fff1cf;border-left:4px solid #df9b12;padding:4mm 5mm;margin-top:8mm;font-size:9.4pt;color:#4b3511}.cover .warning{background:#352b12;color:#ffedc5;border-color:#ffc247}.page>header{display:flex;align-items:center;gap:5mm;border-bottom:1px solid #b9c4c5;padding-bottom:4mm;margin-bottom:7mm}.section-no{width:12mm;height:12mm;border-radius:50%;display:grid;place-items:center;background:#0b3844;color:#a8ff60;font-weight:700}.page h2{font-family:"Noto Serif","Liberation Serif",serif;font-size:24pt;line-height:1.1;margin:0;color:#0b3844}.page h3{font-size:12pt;line-height:1.2;color:#0b3844;margin:6mm 0 2.5mm}.lead{font-family:"Noto Serif","Liberation Serif",serif;font-size:13.2pt;line-height:1.5;color:#2b4047;margin:0 0 7mm}p,li,dd{font-size:10.1pt}code{font-family:"Liberation Mono",monospace;background:#e3e7e3;padding:.2mm 1mm;border-radius:1mm;color:#0a4c5c}.compare,.columns{display:grid;grid-template-columns:1fr 1fr;gap:6mm}.choice{background:#e6e8e1;border-top:5px solid #6b7a7d;padding:5mm;border-radius:2mm}.choice.good{border-color:#45b77a;background:#e7f3e8}.choice h3{margin:0}.choice .sub{font-size:8.2pt;text-transform:uppercase;letter-spacing:.1em;color:#3c8061;font-weight:700;margin:1mm 0 3mm}.choice ul{margin:0;padding-left:5mm}.choice li{margin:2mm 0}.callout,.success,.next{padding:4mm 5mm;background:#e2edf0;border-left:4px solid #0c7c8f;border-radius:0 2mm 2mm 0;margin:6mm 0;font-size:9.5pt}.success{background:#e1f1e7;border-color:#2c9861}.flow{display:flex;align-items:center;justify-content:space-between;gap:2mm;margin:4mm 0 6mm}.flow span{flex:1;text-align:center;background:#0b3844;color:#fff;padding:4mm 2mm;border-radius:2mm;font-size:9pt;font-weight:700}.flow small{font-size:8.2pt;font-weight:400;color:#b9d5da}.flow i{color:#0c7c8f;font-size:18pt;font-style:normal}.source-note,.fine{font-size:8.2pt;color:#52666b}.source-note a,.sources a,.next a{color:#075f74}.checklist{display:grid;grid-template-columns:1fr 1fr;gap:4mm 6mm}.checklist>div{display:grid;grid-template-columns:10mm 1fr;gap:3mm;border-top:1px solid #b8c5c5;padding-top:3mm}.checklist>div>b,.step>span{display:grid;place-items:center;width:8mm;height:8mm;border-radius:50%;background:#0b3844;color:#a8ff60;font-size:9pt}.checklist p{margin:0}.step{display:grid;grid-template-columns:10mm 1fr;gap:4mm;margin:0 0 4mm;padding-bottom:3mm;border-bottom:1px solid #c7ceca}.step h3{margin:0 0 1mm}.step p{margin:0}.small{font-size:8.7pt}.columns ol{padding-left:5mm}.columns li{margin-bottom:2mm}pre{background:#071820;color:#d6f3ef;border-radius:2mm;padding:5mm;white-space:pre-wrap;font-size:9.2pt;line-height:1.55}pre code{background:transparent;color:#a8ff60;padding:0}.verify{display:grid;grid-template-columns:1fr 1fr;gap:3mm}.verify div{background:#e7eae5;padding:3mm 4mm;border-radius:2mm}.verify span{display:block;font-size:8.4pt;color:#506165;margin-top:1mm}dl{margin:0}dt{font-weight:700;color:#0b3844;margin-top:3mm;font-size:9.5pt}dd{margin:1mm 0 0}.next h3{margin-top:0}.sources{columns:2;column-gap:8mm;padding-left:5mm;margin:2mm 0}.sources li{margin-bottom:2mm;break-inside:avoid}a{color:inherit;text-decoration:underline;text-decoration-color:#35a6b4;text-underline-offset:2px}footer{position:absolute;left:18mm;right:18mm;bottom:8mm;display:flex;justify-content:space-between;border-top:1px solid #b9c4c5;padding-top:2.5mm;font-size:8.2pt;color:#65767a}.cover footer{border-color:#31505b;color:#86a3ac}
'''
html_doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jailbreak an iPhone 6s on iOS 15.8.8</title><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>'
(root/".src/index.html").write_text(html_doc)
