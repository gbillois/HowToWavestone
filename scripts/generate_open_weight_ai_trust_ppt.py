#!/usr/bin/env python3
"""Generate a Wavestone-styled PPTX for the open-weight AI trust deck."""
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
import html

OUT = Path('docs/open-weight-ai-trust.pptx')
W,H=12192000,6858000
C={"indigo":"451DC7","indigo2":"2D1380","dark":"1E0D57","green":"04F06A","green2":"E1FDED","teal":"228D95","ink":"16121F","muted":"6B6580","light":"F5F4F9","border":"E6E4EE","white":"FFFFFF","red":"D8412F","warn":"C8861A"}

def emu(x): return int(x*914400)
def esc(s): return html.escape(str(s), quote=True)
def shape(x,y,w,h,fill,line=None):
    ln = f'<a:ln><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>' if line else '<a:ln><a:noFill/></a:ln>'
    return f'<p:sp><p:nvSpPr><p:cNvPr id="1" name="Rect"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>{ln}</p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>'

def text(s,x,y,w,h,size=18,color=None,bold=False,font='Inter',align='l'):
    b='<a:b/>' if bold else ''
    color=color or C['ink']
    return f'<p:sp><p:nvSpPr><p:cNvPr id="2" name="Text"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square"/><a:lstStyle/><a:p><a:pPr algn="{align}"/><a:r><a:rPr lang="en-US" sz="{int(size*100)}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>{b}<a:latin typeface="{font}"/></a:rPr><a:t>{esc(s)}</a:t></a:r></a:p></p:txBody></p:sp>'

def title(slide, title, msg, n, dark=False):
    bg=C['indigo2'] if dark else C['white']; slide.append(shape(0,0,13.333,7.5,bg))
    if dark:
        slide.append(shape(0,0,13.333,0.18,C['green']))
    slide.append(shape(.55,.35,.09,.09,C['green']))
    slide.append(text('WAVESTONE · AI Security & Trust',.72,.28,4.8,.25,10,C['white'] if dark else C['indigo'],True,'Poppins'))
    slide.append(text(title,.55,.75,8.7,.7,28,C['white'] if dark else C['indigo'],True,'Poppins'))
    slide.append(shape(.55,1.55,.55,.045,C['green']))
    slide.append(text(msg,.55,1.72,10.8,.45,13,C['white'] if dark else C['muted'],False,'Inter'))
    slide.append(text(f'{n:02d} / 09',11.7,7.05,1.1,.18,9,C['white'] if dark else C['muted'],False,'IBM Plex Mono','r'))

def table(slide, x,y,w, rows, headers=None, colw=None, font=9.2):
    ncols=len(rows[0]); colw=colw or [w/ncols]*ncols
    rh=.38 if len(rows)<=5 else .32
    if headers:
        cx=x
        for j,hdr in enumerate(headers):
            slide.append(shape(cx,y,colw[j],rh,C['indigo']))
            slide.append(text(hdr,cx+.06,y+.08,colw[j]-.12,rh-.08,font,C['white'],True,'Poppins'))
            cx+=colw[j]
        y+=rh
    for i,row in enumerate(rows):
        cx=x; fill=C['light'] if i%2==0 else C['white']
        for j,cell in enumerate(row):
            slide.append(shape(cx,y,colw[j],rh,fill,C['border']))
            slide.append(text(cell,cx+.06,y+.07,colw[j]-.12,rh-.05,font,C['ink'] if j==0 else C['muted'],j==0,'Inter'))
            cx+=colw[j]
        y+=rh

def bullets(slide, items, x,y,w, size=11, color=None):
    for i,it in enumerate(items):
        slide.append(shape(x,y+i*.38,.07,.07,C['green']))
        slide.append(text(it,x+.15,y+i*.32,w,.25,size,color or C['muted'],False,'Inter'))

slides=[]
# 1
s=[]; title(s,'Open-Weight Is Not Open Source, and Not Trust by Default','Open-weight improves deployment control. It does not prove quality, safety, provenance or integrity.',1,True)
table(s,.65,2.25,11.9,[['Weights','Available','Usually available'],['Training data','Rarely fully disclosed','Sometimes documented'],['Training code','Not guaranteed','Expected or partially available'],['Reproducibility','Often limited','Higher expectation'],['Governance','Vendor-dependent','Community/licence-dependent'],['Security assurance','Not guaranteed','Not guaranteed either']],['Dimension','Open-weight','Open source'],[2.6,4.1,5.2],10)
s.append(shape(.65,6.25,11.9,.45,C['green2'])); s.append(text('Bottom line: Open-weight gives control over execution, not automatic trust in the AI system.',.85,6.36,11.4,.22,13,C['dark'],True,'Poppins')); slides.append(s)
# 2
s=[]; title(s,'Controlled Hosting Reduces Availability and Confidentiality Risks','Controlled hosting can materially reduce two key risks, but only if the surrounding stack is also controlled.',2)
table(s,.65,2.05,11.9,[['Availability','Provider outage, API restriction, regional ban, pricing change','Depends mainly on internal infrastructure'],['Confidentiality','Prompts and data may transit through provider systems','Data can remain within controlled environments'],['Sovereignty','Strong external dependency','Better control over location, runtime and operations'],['Cost model','API/token-driven','Infrastructure and capacity-driven']],['Risk','External API model','Controlled open-weight hosting'],[2,5.1,4.8],9.3)
bullets(s,['Caveat: logs, telemetry, RAG data stores, prompts, plugins, secrets and monitoring tools must also be controlled.'],.9,5.9,11,12,C['ink']); slides.append(s)
# 3
s=[]; title(s,'The Hard Problem Is Results Integrity','The residual risk is broader than model integrity. It is results integrity across the full AI system.',3,True)
table(s,.65,2.0,11.9,[['Model','Biased training, poisoned data, hidden backdoor, degraded reasoning'],['Packaging','Malicious weights, unsafe serialization, compromised tokenizer, runtime script'],['Prompting','Weak system prompt, prompt injection, policy bypass'],['Context / RAG','Wrong source, stale document, poisoned knowledge base, excessive retrieval'],['Tools / agents','Wrong tool call, excessive privilege, action without approval'],['Output','Hallucination, toxic answer, biased recommendation, unsafe decision'],['Monitoring','Drift not detected, incident not escalated, logs incomplete']],['Integrity layer','What can go wrong'],[2.4,9.5],8.7)
s.append(shape(.65,6.45,11.9,.42,C['green'])); s.append(text('Approve an AI system for a specific use case, data scope and autonomy level — not a model in isolation.',.85,6.55,11.2,.22,12,C['dark'],True,'Poppins')); slides.append(s)
# 4
s=[]; title(s,'Trust Must Be Graded, Not Assumed','Trust should be proportional to use-case criticality, evidence depth and operational exposure.',4)
table(s,.45,1.85,12.4,[['0 — No evidence','Vendor claim only','No production use'],['1 — Documentation','Model card, licence, intended use, limitations','Low-risk experiments'],['2 — Supply chain evidence','Hashes, AI-BOM, source registry, dependency review','Internal productivity'],['3 — Independent testing','Benchmarks, red teaming, bias/toxicity tests, malware scan','Sensitive internal use'],['4 — Contractual assurance','Audit rights, warranties, incident notification','Regulated or business-critical use'],['5 — Continuous assurance','Runtime monitoring, drift detection, revalidation, kill switch','High-impact production']],['Trust level','Evidence required','Suitable usage'],[2.6,5.5,4.3],8.2)
bullets(s,['Approve by use case.','Maintain a catalogue of authorized models.','Combine both for enterprise scale.'],.85,6.2,7.5,11,C['ink']); slides.append(s)
# 5
s=[]; title(s,'A Defense-in-Depth Architecture for Open-Weight AI','Controls must cover model intake, packaging, runtime, data, prompts, tools, outputs and monitoring.',5,True)
table(s,.45,1.75,12.4,[['Model intake','Approved source, licence review, model card, AI-BOM, hash validation'],['Artifact security','Malware scan, unsafe format detection, dependency scan, sandboxed loading'],['Runtime isolation','Hardened container, restricted network, secret isolation, no uncontrolled outbound access'],['Data access','Least privilege, RAG ACLs, DLP, classification, retention controls'],['Prompt and tool control','System prompt governance, tool permissioning, MCP gateway, human approval'],['Output control','Guardrails, policy checks, confidence scoring, human validation'],['Continuous monitoring','Drift, anomaly detection, behavioral regression tests, incident playbooks'],['Internal observability','Activation monitoring / “model MRI” for high-risk cases']],['Layer','Controls'],[2.6,9.8],7.7); slides.append(s)
# 6
s=[]; title(s,'Target Operating Model: Who Owns AI Trust?','AI trust is a shared operating model, not a tool decision.',6)
table(s,.45,1.75,12.4,[['AI / Data Science','Model selection, evaluation, benchmarks, fine-tuning, performance monitoring'],['Cybersecurity','Threat model, supply chain controls, runtime hardening, red teaming'],['Legal / Compliance','Licence, copyright, AI Act, contracts, regulatory exposure'],['Data Office','Data classification, RAG governance, sensitive data controls'],['Architecture / Cloud','Hosting pattern, isolation, scalability, observability'],['Business owner','Use case criticality, acceptable risk, human validation'],['Risk / Internal Control','Approval workflow, evidence retention, periodic reassessment']],['Function','Responsibility'],[2.8,9.6],8.8)
s.append(shape(.65,6.45,11.9,.42,C['dark'])); s.append(text('Principle: A model is approved for a class of usage, data and autonomy — not alone.',.85,6.55,11,.22,12,C['white'],True,'Poppins')); slides.append(s)
#7
s=[]; title(s,'How the Market Is Tackling the Problem','The market is converging toward AI supply chain security, runtime protection and model observability.',7,True)
table(s,.35,1.6,12.65,[['Hugging Face + Protect AI','Model scanning at repository scale','Model hubs become AI supply chain control points'],['Microsoft + HiddenLayer','Scanning third-party and open-source models in Azure AI','Curated model catalogues need security gates'],['Palo Alto + Protect AI','Acquisition of Protect AI','AI security is absorbed into major cyber platforms'],['Cisco + Robust Intelligence','AI Defense, red teaming, AI firewall','AI protection becomes a platform capability'],['Realm Labs','“Model MRI” / observing AI behavior during inference','Runtime deviation and internal behavior matter'],['Starseer','Mechanistic interpretability, activation analysis','Glass-box observability is a serious direction']],['Actor','Posture','What it tells us'],[2.6,4.5,5.55],7.5)
bullets(s,['First wave: scan the model package.','Second wave: protect the AI runtime.','Third wave: observe internal model behavior.'],.75,6.15,8,10.5,C['white']); slides.append(s)
#8
s=[]; title(s,'Enterprise Methodology: From Intake to Production Approval','Build a repeatable homologation process for models and AI systems.',8)
steps=['Use case intake — purpose, users, data sensitivity, decisions, autonomy.','Risk tiering — low, medium, high, critical, based on data, impact and action capability.','Model due diligence — licence, provenance, documentation, limitations, known risks.','Supply chain assessment — hashes, AI-BOM, artifact scan, dependencies, tokenizer, scripts.','Security and safety testing — prompt injection, jailbreaks, bias, toxicity, domain tests.','Architecture approval — hosting, identity, network, RAG, logging, DLP, secrets, tools.','Production gate — evidence pack, risk acceptance, monitoring plan, fallback and kill switch.','Continuous assurance — retesting, drift monitoring, incident handling, catalogue update.']
for i,st in enumerate(steps):
    col=i%2; row=i//2; x=.75+col*6.1; y=1.8+row*1.15
    s.append(shape(x,y,5.65,.78,C['light'],C['border'])); s.append(shape(x,y,.45,.78,C['indigo'] if i<6 else C['green'])); s.append(text(f'{i+1}',x+.13,y+.22,.2,.2,12,C['white'] if i<6 else C['dark'],True,'Poppins'))
    s.append(text(st,x+.62,y+.14,4.85,.45,9.5,C['ink'],False,'Inter'))
slides.append(s)
#9
s=[]; title(s,'Implementation Roadmap for a Large Organization','Start with catalogue, tiering and key controls, then industrialize continuous assurance.',9,True)
table(s,.35,1.75,12.65,[['Governance','Define policy, risk tiers, approval workflow','Create model catalogue','Industrialize review boards and evidence packs'],['Technology','Basic scanning, sandbox loading, approved runtime','AI gateway, DLP, RAG controls, monitoring','Runtime protection, model observability, automated revalidation'],['Organization','Assign AI/cyber/legal/data owners','Create AI security review board','Build AI security operations capability'],['Market integration','Use platform scans and vendor evidence','Add third-party tools where justified','Integrate with SOC, GRC and model registry'],['Priority scope','Critical use cases first','Enterprise productivity and RAG','Agents and autonomous workflows']],['Phase','0-3 months','3-6 months','6-12 months'],[2.3,3.35,3.25,3.75],7.5)
s.append(shape(.65,6.3,11.9,.55,C['green'])); s.append(text('Final takeaway: Do not ask “Is this model safe?” Ask whether residual risk is acceptable for this use case, data, autonomy and evidence.',.85,6.42,11.2,.24,11.5,C['dark'],True,'Poppins')); slides.append(s)

def slide_xml(content):
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'+''.join(content)+'</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'

OUT.parent.mkdir(exist_ok=True)
with ZipFile(OUT,'w',ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>' + ''.join(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' for i in range(1,len(slides)+1)) + '</Types>')
    z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>')
    z.writestr('ppt/presentation.xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldSz cx="12192000" cy="6858000" type="wide"/><p:sldIdLst>'+''.join(f'<p:sldId id="{255+i}" r:id="rId{i}"/>' for i in range(1,len(slides)+1))+'</p:sldIdLst><p:notesSz cx="6858000" cy="9144000"/></p:presentation>')
    z.writestr('ppt/_rels/presentation.xml.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>' for i in range(1,len(slides)+1))+'</Relationships>')
    for i,s in enumerate(slides,1):
        z.writestr(f'ppt/slides/slide{i}.xml',slide_xml(s))
        z.writestr(f'ppt/slides/_rels/slide{i}.xml.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>')
print(f'Generated {OUT} with {len(slides)} slides')
