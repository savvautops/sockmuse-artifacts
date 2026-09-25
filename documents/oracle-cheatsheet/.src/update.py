from pathlib import Path
p=Path('/home/hatch/workspace/your_files/oracle-cheatsheet/.src/index.html')
s=p.read_text()
# Small style additions for dense comparison and inventory pages.
old=".source{font-size:8.5pt;line-height:1.3;overflow-wrap:anywhere}.spacer{height:3mm}"
new=".source{font-size:8.5pt;line-height:1.3;overflow-wrap:anywhere}.spacer{height:3mm}.statrow{display:grid;grid-template-columns:34mm 1fr 1fr;gap:0;border-bottom:.3mm solid var(--line)}.statrow>div{padding:2.3mm}.statrow .head{font-weight:700;color:var(--navy)}.status{display:inline-block;border:.35mm solid var(--amber);background:#fff8df;border-radius:2mm;padding:1mm 2.2mm;font-weight:700;font-size:8.8pt}.num{font-variant-numeric:tabular-nums}"
assert old in s
s=s.replace(old,new)
# Cover and contents update.
s=s.replace('<div>2. What Always Free actually includes</div><div class="n">3</div>\n    <div>3. A safe first-VM recipe</div><div class="n">4</div>\n    <div>4. SSH and first-hour setup</div><div class="n">5</div>\n    <div>5. Networking and firewall logic</div><div class="n">6</div>\n    <div>6. Daily operations and troubleshooting</div><div class="n">7</div>\n    <div>7. Cost, backup, and security guardrails</div><div class="n">8</div>\n    <div>8. Glossary and official sources</div><div class="n">9</div>', '<div>2. Your full Always Free VM inventory</div><div class="n">3</div>\n    <div>3. Your VM compared with Sock\'s sandbox</div><div class="n">4</div>\n    <div>4. A safe first-VM recipe</div><div class="n">5</div>\n    <div>5. SSH and first-hour setup</div><div class="n">6</div>\n    <div>6. Networking and firewall logic</div><div class="n">7</div>\n    <div>7. Daily operations and troubleshooting</div><div class="n">8</div>\n    <div>8. Cost, backup, and security guardrails</div><div class="n">9</div>\n    <div>9. Glossary and official sources</div><div class="n">10</div>')
s=s.replace('<span>1 / 9</span>','<span>1 / 10</span>',1)
start=s.index('<section class="page">\n  <div class="header"><b>02 / Always Free</b>')
end=s.index('</section>',start)+len('</section>')
old_section=s[start:end]
new_section='''<section class="page">
  <div class="header"><b>02 / Always Free</b><span>How many VMs you actually get</span></div>
  <h2>You can run up to four free VMs</h2>
  <p>As of September 2026, an Always Free tenancy can hold <strong>up to four compute instances</strong>: as many as <strong>two Ampere A1 Flex VMs</strong> sharing one Arm resource pool, plus <strong>two AMD E2.1.Micro VMs</strong>.</p>
  <div class="grid3">
    <div class="card red"><div class="label">A1 Flex allowance</div><div class="big">2 VMs</div><p class="small">They share 2 OCPUs and 12 GB RAM across the tenancy.</p></div>
    <div class="card teal"><div class="label">E2 Micro allowance</div><div class="big">2 VMs</div><p class="small">Each has 1 AMD OCPU, 2 vCPUs, and 1 GB RAM.</p></div>
    <div class="card"><div class="label">Maximum count</div><div class="big">4 VMs</div><p class="small">Only if the shared 200 GB disk pool can hold all boot volumes.</p></div>
  </div>
  <h3 style="margin-top:5mm">The four slots are not identical</h3>
  <table>
    <thead><tr><th>Free allowance</th><th>CPU</th><th>RAM</th><th>Best use</th></tr></thead>
    <tbody>
      <tr><td><strong>Up to 2 × A1 Flex</strong></td><td>Ampere Altra Arm; <strong>2 OCPUs total</strong> shared</td><td><strong>12 GB total</strong> shared</td><td>Main app server, Docker, agents, Node/Python workloads</td></tr>
      <tr><td><strong>2 × E2.1.Micro</strong></td><td>AMD x86; <strong>1 OCPU = 2 vCPUs</strong> each via hyperthreading</td><td><strong>1 GB each</strong></td><td>Light bot, status page, proxy, tiny sidecar</td></tr>
    </tbody>
  </table>
  <div class="callout"><strong>How the A1 pool splits:</strong> one A1 can use the full <strong>2 OCPUs / 12 GB</strong>, as your planned VM does. If you want two A1 VMs, they must divide that same pool, for example <strong>1 OCPU / 6 GB each</strong>. The pool was reduced from 4 OCPUs / 24 GB in June 2026.</div>
  <h3>Storage determines how many fit</h3>
  <p>All boot and block volumes share <strong>200 GB total</strong>. OCI boot volumes have a 47 GB minimum. Four minimum-size boot volumes need about <strong>188 GB</strong>. Your 100 GB boot volume leaves 100 GB, enough for two more 47 GB boot volumes, so the practical maximum with the current disk choice is <strong>three VMs total</strong>, not four.</p>
  <div class="grid2">
    <div class="card good"><h3>Other free infrastructure</h3><ul><li>10 TB outbound bandwidth each month</li><li>Public IPv4 is free while attached to a running instance</li><li>200 GB combined boot/block storage</li></ul></div>
    <div class="card warn"><h3>Two important caveats</h3><ul><li>Arm capacity can be scarce: retry after <code>Out of host capacity</code>, or try another available region.</li><li>Oracle may reclaim Always Free instances it classifies as idle.</li></ul></div>
  </div>
  <div class="footer"><span>Always Free inventory - September 2026</span><span>3 / 10</span></div>
</section>'''
s=s[:start]+new_section+s[end:]
# Insert the machine comparison as its own page after inventory.
insert_at=s.index('</section>',start)+len('</section>')
comparison='''
<section class="page">
  <div class="header"><b>03 / Machine comparison</b><span>Your VM versus Sock's sandbox</span></div>
  <h2>Your Oracle VM is the bigger Linux box</h2>
  <p><span class="status">nelson-vm-01: provisioning on 24 Sep 2026</span></p>
  <p>This compares the Linux sandbox that runs Sock's tools with the Oracle VM you configured. It does <strong>not</strong> compare against the Meta GPU infrastructure that runs the Muse model itself.</p>
  <div class="statrow"><div></div><div class="head">Sock's sandbox</div><div class="head">nelson-vm-01</div></div>
  <div class="statrow"><div class="head">CPU</div><div>2 shared vCPUs</div><div>2 dedicated OCPUs</div></div>
  <div class="statrow"><div class="head">Processor</div><div>AMD EPYC 9D25</div><div>Ampere Altra</div></div>
  <div class="statrow"><div class="head">Architecture</div><div>x86_64</div><div>Arm64 / aarch64</div></div>
  <div class="statrow"><div class="head">Memory</div><div>7.7 GB RAM</div><div>12 GB RAM</div></div>
  <div class="statrow"><div class="head">Disk</div><div>7.5 GB</div><div>100 GB boot volume</div></div>
  <div class="statrow"><div class="head">Operating system</div><div>Ubuntu 24.04</div><div>Canonical Ubuntu 24.04 Minimal</div></div>
  <div class="statrow"><div class="head">CPU scheduling</div><div>Shared slices of a larger host</div><div>Full physical Arm cores; no hyperthreading</div></div>
  <div class="statrow"><div class="head">Role</div><div>Temporary tool-running workspace</div><div>Your persistent API-and-agent server</div></div>
  <h3 style="margin-top:6mm">Your exact deployment plan</h3>
  <div class="grid2">
    <div class="card red tight"><p><strong>Name:</strong> <code>nelson-vm-01</code></p><p><strong>Shape:</strong> <code>VM.Standard.A1.Flex</code></p><p><strong>Region:</strong> <code>ca-montreal-1</code></p><p><strong>Image:</strong> Canonical Ubuntu 24.04 Minimal aarch64</p></div>
    <div class="card teal tight"><p><strong>Compute:</strong> 2 OCPUs / 12 GB RAM</p><p><strong>Storage:</strong> 100 GB boot volume</p><p><strong>Address:</strong> reserved public IPv4</p><p><strong>Ingress:</strong> TCP 22, 80, and 443</p></div>
  </div>
  <div class="callout good"><strong>Where your VM wins:</strong> 55% more RAM, over 13 times the disk, and dedicated physical CPU cores. It is built to stay online and host your own services.</div>
  <div class="callout"><strong>Where the sandbox differs:</strong> x86_64 has broader compatibility with old or x86-only binaries. On the A1 VM, prefer packages and container images that publish <code>linux/arm64</code> builds.</div>
  <div class="callout warn"><strong>The “brain” is separate from the hardware.</strong> The VM runs the installed agent, command-line interfaces, orchestration, storage, and networking. API keys let those tools call remote large language models; the model inference usually runs at the API provider, not on the two Arm cores.</div>
  <div class="footer"><span>Machine profile</span><span>4 / 10</span></div>
</section>'''
s=s[:insert_at]+comparison+s[insert_at:]
# Shift section labels and all remaining page counters.
repls={
'<b>03 / Create the VM</b>':'<b>04 / Create the VM</b>',
'<b>04 / First connection</b>':'<b>05 / First connection</b>',
'<b>05 / Networking</b>':'<b>06 / Networking</b>',
'<b>06 / Operations</b>':'<b>07 / Operations</b>',
'<b>07 / Guardrails</b>':'<b>08 / Guardrails</b>',
'<b>08 / Reference</b>':'<b>09 / Reference</b>',
'<span>4 / 9</span>':'<span>5 / 10</span>',
'<span>5 / 9</span>':'<span>6 / 10</span>',
'<span>6 / 9</span>':'<span>7 / 10</span>',
'<span>7 / 9</span>':'<span>8 / 10</span>',
'<span>8 / 9</span>':'<span>9 / 10</span>',
'<span>9 / 9</span>':'<span>10 / 10</span>',
}
for a,b in repls.items():
    assert a in s,a
    s=s.replace(a,b,1)
# Personalize the creation recipe to the selected VM without changing the security guidance.
s=s.replace('Use a plain name such as <code>alwaysfree-ubuntu</code>. Confirm the compartment and home region.', 'Use <code>nelson-vm-01</code>. Confirm the compartment and the Montreal home region (<code>ca-montreal-1</code>).')
s=s.replace('Select a current <strong>Ubuntu LTS Arm/aarch64</strong> image for A1.', 'Select <strong>Canonical Ubuntu 24.04 Minimal aarch64</strong> for A1.')
s=s.replace('Use the default boot volume unless you need more. Every instance consumes at least 47 GB from the 200 GB Always Free block-storage pool.', 'Use the selected <strong>100 GB</strong> boot volume. It leaves 100 GB in the Always Free storage pool; every additional instance needs at least 47 GB.')
s=s.replace('public IP, key-based SSH, TCP 22 restricted to your IP, and public 80/443 only when needed.', 'reserved public IP, key-based SSH, TCP 22, and public TCP 80/443 for web traffic.')
p.write_text(s)
