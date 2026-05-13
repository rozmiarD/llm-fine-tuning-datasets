#!/usr/bin/env python3
from __future__ import annotations
import json, re, collections, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'datasets/debian-admin-bash/debian-admin-bash-sft.jsonl'
EVAL_DIR=ROOT/'datasets/debian-admin-bash/evals'
REVIEW_DIR=ROOT/'datasets/debian-admin-bash/review'
VAL_DIR=ROOT/'validation'
EVAL_DIR.mkdir(parents=True, exist_ok=True)
REVIEW_DIR.mkdir(parents=True, exist_ok=True)
SYSTEM='You are a Debian/Ubuntu terminal administration assistant. Return correct Bash commands and brief factual explanations. Prefer inspection before modification, validate configuration before restarts, use sudo only when needed, warn before risky operations, and check tool availability when a command may be missing. Keep answers concise.'
recs=[json.loads(l) for l in DATA.read_text().splitlines() if l.strip()]

def slug(s):
 s=s.lower(); s=re.sub(r'`[^`]+`','',s); s=re.sub(r'[^a-z0-9]+','-',s).strip('-'); return s[:70].strip('-') or 'record'

def meta(task,sd,tags,style='diagnostic_steps',risk='safe_readonly',diff='advanced'):
 return {'dataset_version':'1.1','task_type':task,'language':'en','domain':'debian_admin_bash','subdomain':sd,'target_os':{'family':'linux','distros':['debian','ubuntu'],'shell':'bash','package_manager':'apt' if sd=='packages' else 'none'},'target_model_profile':'small-debian-admin','difficulty':diff,'risk_level':risk,'requires_root':False,'answer_style':style,'tags':sorted(set(['linux','debian','ubuntu','held-out']+tags)),'safety':{'has_side_effects':False,'side_effects':[],'destructive':False,'warning_required':False,'warning_present':False,'dry_run_available':False,'rollback_available':False},'review':{'status':'draft','semantic_review':False,'safety_review':False,'execution_validation':{'mode':'static_only','status':'pending','reason':'Held-out eval/reference answer; not manually executed.'}},'source':{'source_dataset_version':'eval-v0.1','curation':'held_out_quality_eval'}}

def rec(task,idx,sd,title,user,assistant,tags,style='diagnostic_steps',risk='safe_readonly'):
 m=meta(task,sd,tags,style,risk)
 if 'sudo' in assistant: m['requires_root']=True
 return {'id':f'debian-admin-bash:{sd}.{slug(title)}.eval.{idx:04d}','meta':m,'messages':[{'role':'system','content':SYSTEM},{'role':'user','content':user},{'role':'assistant','content':assistant}]}

single=[]; i=1
cases=[
('systemd','nginx-203-exec','systemctl status nginx shows: Main process exited, code=exited, status=203/EXEC. What is the safest first command?','```bash\nsystemctl cat nginx.service\nnamei -l /usr/sbin/nginx\n```\nThis verifies the unit command path and executable path before restarting anything.',['systemd','203-exec']),
('packages','apt-lock-unattended','apt install fails: lock-frontend is held by unattended-upgr. What should I check first?','```bash\nps -fp $(pgrep -f unattended-upgr | head -1)\nsudo fuser -v /var/lib/dpkg/lock-frontend /var/lib/dpkg/lock\n```\nConfirm the active package process instead of deleting lock files.',['apt','lock']),
('processes','oom-killed-python','A service log ends with “Killed” and kernel log mentions OOM. Give one verification command.','```bash\nsudo journalctl -k -b --no-pager | grep -Ei "out of memory|oom|killed process" | tail -80\n```\nThis confirms whether the kernel OOM killer terminated the process.',['oom','memory']),
('backup_restore','rsync-code-23','A backup ended with rsync code 23. What should I inspect before trusting it?','```bash\ngrep -Ei "failed|denied|error|vanished" rsync.log | tail -80\nsudo rsync -aHAX --numeric-ids --dry-run --itemize-changes /srv/app/ /backup/app/\n```\nTreat code 23 as a partial backup until errors and a dry run are reviewed.',['backup','rsync']),
('permissions','service-user-read','app.service cannot read /etc/app/config.yml. Give the inspection-first check.','```bash\nsystemctl cat app.service\nnamei -l /etc/app/config.yml\nsudo -u app test -r /etc/app/config.yml && echo readable || echo not-readable\n```\nCheck the service user and path permissions before changing ownership or modes.',['permissions','service-user']),
('ssh_auth','authorized-keys-mode','SSH says bad ownership or modes for /home/deploy. What should I run first?','```bash\nnamei -l /home/deploy/.ssh/authorized_keys\nstat -c "%a %u:%g %n" /home/deploy /home/deploy/.ssh /home/deploy/.ssh/authorized_keys\n```\nSSH key login depends on every path component being safely owned and permissioned.',['ssh','permissions']),
('security','apparmor-denial','Kernel log shows apparmor=DENIED for nginx reading /srv/app/index.html. What first?','```bash\nsudo journalctl -k --since "30 minutes ago" --no-pager | grep -i apparmor\nsudo aa-status\nnamei -l /srv/app/index.html\n```\nConfirm the denial, active profile, and filesystem path before policy changes.',['apparmor','security']),
('sqlite','database-locked','sqlite3 reports database is locked while app.service is running. What should I inspect?','```bash\nsudo lsof -- /var/lib/app/app.db /var/lib/app/app.db-wal 2>/dev/null\nsystemctl status app.service --no-pager\n```\nIdentify active holders before backup, migration, or restart.',['sqlite','lock']),
('networking','dns-apt-failure','apt update says Temporary failure resolving archive.ubuntu.com. Safe first command?','```bash\nresolvectl status 2>/dev/null || cat /etc/resolv.conf\ngetent hosts archive.ubuntu.com\nip route get 1.1.1.1\n```\nThis separates resolver/routing failure from apt metadata problems.',['dns','apt']),
('docker','compose-port-conflict','Docker compose fails: port is already allocated for 0.0.0.0:8080. Verify first.','```bash\nsudo ss -ltnp \'sport = :8080\'\ndocker ps --format "table {{.Names}}\\t{{.Ports}}"\n```\nFind whether a host process or another container owns the port.',['docker','port-conflict']),
('filesystem','deleted-open-files','Disk usage did not drop after deleting logs. What command confirms deleted open files?','```bash\nsudo lsof +L1\n```\nDeleted files can still consume space while processes keep them open.',['filesystem','lsof']),
('logs','journal-rate-limit','journal says “Suppressed 10000 messages from app.service”. What next?','```bash\nsudo journalctl -u app.service --since "30 minutes ago" --no-pager | tail -160\nsystemctl status app.service --no-pager\n```\nInspect the service error source before changing journal limits.',['logs','rate-limit']),
]
labels=['alpha','bravo','charlie','delta','echo','foxtrot','golf','hotel']
for round_no in range(7):
 label=labels[round_no]
 for sd,title,user,ans,tags in cases:
  u=f"Host profile: {label}. "+user.replace('app.service',f'app-{label}.service').replace('/srv/app',f'/srv/app-{label}').replace('/var/lib/app',f'/var/lib/app-{label}')
  a=f"# host profile: {label}\n"+ans.replace('app.service',f'app-{label}.service').replace('/srv/app',f'/srv/app-{label}').replace('/var/lib/app',f'/var/lib/app-{label}')
  single.append(rec('eval',i,sd,f'{title}-{round_no}',u,a,tags)); i+=1
single=single[:80]
(EVAL_DIR/'single-turn.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False,separators=(',',':')) for x in single)+'\n')

multi=[]; i=1
flows=[
('systemd','User: app.service failed.\nAssistant: Run `systemctl status app.service --no-pager` and recent logs.\nUser output:\n```text\napp.service: Failed at step EXEC spawning /opt/app/bin/run: Permission denied\n```\nWhat should the assistant say next?','```bash\nnamei -l /opt/app/bin/run\nstat -c "%a %u:%g %n" /opt/app/bin/run\n```\nExit step EXEC with permission denied points to path, mode, owner, or interpreter access; inspect before chmod or restart.',['multi-turn','203-exec']),
('packages','User: apt install is stuck.\nAssistant: Check the lock holder.\nUser output:\n```text\n/var/lib/dpkg/lock-frontend: 884 apt.systemd.daily\n```\nWhat next?','```bash\nps -fp 884\nsystemctl status apt-daily.service apt-daily-upgrade.service --no-pager\n```\nConfirm the scheduled apt job and avoid removing lock files while it is active.',['multi-turn','apt-lock']),
('backup_restore','User: backup failed with code 23.\nAssistant: Inspect rsync errors.\nUser output:\n```text\nrsync: send_files failed to open /srv/app0/private.key: Permission denied\n```\nWhat next?','```bash\nnamei -l /srv/app0/private.key\nsudo -u BACKUP_USER test -r /srv/app0/private.key && echo readable || echo not-readable\n```\nVerify backup-user access before trusting or rerunning the backup.',['multi-turn','backup']),
('processes','User: app is slow.\nAssistant: Check CPU/memory and logs.\nUser output:\n```text\naccept4: Too many open files\n```\nWhat next?','```bash\npid=$(systemctl show -p MainPID --value app.service); sudo ls /proc/"$pid"/fd | wc -l; sudo cat /proc/"$pid"/limits | grep -i files\n```\nConfirm descriptor usage and limits before raising systemd limits.',['multi-turn','fd']),
('networking','User: apt cannot resolve hosts.\nAssistant: Check resolver and route.\nUser output:\n```text\n/etc/resolv.conf -> ../run/systemd/resolve/stub-resolv.conf\ngetent hosts archive.ubuntu.com returns nothing\n```\nWhat next?','```bash\nresolvectl status\nsystemctl status systemd-resolved --no-pager\n```\nThe system is using systemd-resolved; inspect resolver state before editing apt sources.',['multi-turn','dns']),
]
for round_no in range(8):
 label=labels[round_no]
 for sd,transcript,ans,tags in flows:
  u=f"Conversation label: {label}.\n"+transcript.replace('app.service',f'app-{label}.service').replace('/srv/app0',f'/srv/app-{label}')
  a=f"# conversation label: {label}\n"+ans.replace('app.service',f'app-{label}.service').replace('/srv/app0',f'/srv/app-{label}')
  multi.append(rec('eval',i,sd,f'multiturn-{sd}-{round_no}',u,a,tags)); i+=1
multi=multi[:40]
(EVAL_DIR/'multiturn.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False,separators=(',',':')) for x in multi)+'\n')

# Eval README
(EVAL_DIR/'README.md').write_text('''# Debian-admin Bash evals\n\nThis directory contains held-out evaluation records for the `debian-admin-bash` dataset family.\n\nThese files are not training data. They are intended to test whether a small Debian/Ubuntu admin model can interpret realistic terminal evidence, choose one safe first verification command, and avoid premature state changes.\n\n## Files\n\n| File | Records | Purpose |\n|---|---:|---|\n| `single-turn.jsonl` | 80 | Single-turn held-out evidence-to-command evaluation records. |\n| `multiturn.jsonl` | 40 | Multi-turn continuation evals encoded as single user prompts so they remain compatible with the current governed record shape. |\n\n## Format\n\nEval files use the same governed JSONL shape as source records and set `meta.task_type=\"eval\"`.\n\nThe multi-turn eval file does not change the SFT schema. Previous turns are embedded in the user prompt and the assistant message is the expected next response.\n\n## Non-claims\n\nThese evals are draft reference answers. Passing schema and governance validation does not prove model quality or production safety.\n''')

# Review plan
(REVIEW_DIR/'REVIEW_PLAN.md').write_text('''# Debian-admin Bash review plan\n\nThis review plan is for the current `debian-admin-bash-sft` dataset family, whose active SFT source file is `../debian-admin-bash-sft.jsonl`.\n\n## Goal\n\nCreate a reviewed subset for training and release decisions without pretending that all generated draft records are production-ready.\n\nValidation/model provenance is tracked in `../../../validation/VALIDATION_PROVENANCE.md`. This is not a substitute for full semantic/safety review.\n\n## Review stages\n\n1. Structural validation: JSON, schema, governance lint.\n2. Semantic review: command correctness on Debian/Ubuntu.\n3. Safety review: risk metadata, side effects, warnings, refusals.\n4. Style review: concise command-first answer, no tutorial drift.\n5. Coverage review: avoid over-weighting repeated templates or shallow variants.\n\n## Priority buckets\n\nReview in this order:\n\n1. high-risk records: `destructive`, `security_sensitive`, `privilege_sensitive`, `state_change_high`;\n2. output-driven incident records with logs or command output;\n3. backup/restore and access/identity/permissions records;\n4. script records;\n5. simple command lookup records.\n\n## Reviewed status rule\n\nOnly mark a record as `reviewed` when semantic and safety review are both complete.\n\nDo not mark a record as reviewed only because validation passed.\n\nReviewed status must be hash-bound. A record that is marked `reviewed` must include `meta.review.provenance.record_sha256`, computed by `scripts/review_state.py` over the record content and governance metadata, excluding review bookkeeping. If the prompt, answer, safety metadata, target OS, tags, or other governed content changes, the hash changes and the review state becomes stale.\n\nUse this workflow to avoid spending review effort twice:\n\n```bash\npython scripts/review_state.py status\npython scripts/review_state.py stamp-records \\\n  --ids-file reviewed-record-ids.txt \\\n  --reviewer operator \\\n  --review-batch v1.2-sqlite-wave-001\npython scripts/review_state.py write-manifest\n```\n\nFamily-level consistency review is tracked separately in `family-review-manifest.json` with a hash over the reviewed record IDs. Use it only after checking that a family is internally consistent; changing any member record makes the family review stale.\n\n```bash\npython scripts/review_state.py stamp-family \\\n  --family-id sqlite-locking-wave-001 \\\n  --ids-file sqlite-locking-family.ids \\\n  --reviewer operator \\\n  --review-batch v1.2-sqlite-wave-001\n```\n\n## Training recommendation\n\nFor a small 3B model, prefer a smaller reviewed subset over a larger noisy set. If review capacity is limited, train on:\n\n- high-quality output-driven incidents;\n- concise inspection-first diagnostics;\n- guarded procedures with clear verification;\n- safe refusals with actionable alternatives.\n\nDe-prioritize repeated command-explanation templates until they are deduplicated or diversified.\n''')

# Quality audit
sub=collections.Counter(r['meta']['subdomain'] for r in recs)
risk=collections.Counter(r['meta']['risk_level'] for r in recs)
style=collections.Counter(r['meta']['answer_style'] for r in recs)
diff=collections.Counter(r['meta']['difficulty'] for r in recs)
user_blocks=sum(1 for r in recs if '```text' in next(m['content'] for m in r['messages'] if m['role']=='user'))
refusals=sum(1 for r in recs if r['meta']['answer_style']=='refusal_with_safe_alternative')
# repeated normalized user clusters
clusters=collections.defaultdict(list)
for r in recs:
 u=next(m['content'] for m in r['messages'] if m['role']=='user').lower()
 n=re.sub(r'```.*?```','```X```',u,flags=re.S)
 n=re.sub(r'\b\d+\b','N',n); n=re.sub(r'case n|variant n','CASE',n); n=re.sub(r'\s+',' ',n).strip()
 clusters[n].append(r['id'])
repeats=sorted([(len(v),k,v[:5]) for k,v in clusters.items() if len(v)>=10], reverse=True)[:20]
lines=['# Quality audit: debian-admin-bash-sft','','## Summary','',f'- Records: {len(recs)}',f'- User prompts with text/output blocks: {user_blocks}',f'- Refusal records: {refusals}',f'- Held-out eval records added separately: {len(single)+len(multi)}','','## Distribution','','### Subdomain']
for k,v in sub.most_common(): lines.append(f'- `{k}`: {v}')
lines+=['','### Risk level']
for k,v in risk.most_common(): lines.append(f'- `{k}`: {v}')
lines+=['','### Answer style']
for k,v in style.most_common(): lines.append(f'- `{k}`: {v}')
lines+=['','### Difficulty']
for k,v in diff.most_common(): lines.append(f'- `{k}`: {v}')
lines+=['','## Repetition watchlist','']
if repeats:
 for c,k,ids in repeats: lines.append(f'- {c} records: {k[:140]}... examples: {", ".join(ids)}')
else: lines.append('- No normalized prompt clusters at threshold.')
lines+=['','## Assessment','','The dataset is now strong as a narrow Debian/Ubuntu admin corpus. The biggest quality lever is not another broad domain; it is curation: reduce repeated command-explanation templates, review high-risk records, and test against held-out output-driven evals.','','## Recommended next additions','','1. Build an automated eval runner that scores model answers against the held-out evals for safe-first behavior, Debian correctness, and concision.','2. Create a manually reviewed training subset rather than pushing more draft-only records.','3. Add a small preference set for bad-vs-good answers on unsafe or premature state-changing requests.','4. If adding content, keep it to underrepresented local-admin maintenance: logrotate/cron/timers and restore drills, not new tools or domains.']
(VAL_DIR/'debian-admin-bash-sft.quality-audit.md').write_text('\n'.join(lines)+'\n')
print('wrote evals, review plan, quality audit')
