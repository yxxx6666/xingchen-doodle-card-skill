#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
SKILL_NAME='xingchen-doodle-card-skill'
VERSION='v0.6.2'
DISPLAY_NAME='涂鸦卡片'
ROOT=Path(__file__).resolve().parents[1]
errors=[]
required=[
 'SKILL.md','README.md','VERSION.md','CHANGELOG.md','RELEASE_REPORT.md','agents/openai.yaml',
 'core/anatomy_guard.md','core/scene_limiter.md','core/pose_safety.md','core/prompt_repair_loop.md','core/prompt_composer.md',
 'core/structure_scorer.md','core/layout_graph_compiler.md','core/content_graph_builder.md','core/repair_policy_matrix.md','core/generation_loop.md',
 'core/execution_controller.md','core/state_machine.md','core/layout_prompt_mapping.md','core/gate_system.md',
 'core/runtime_simulator.md','core/encoding_guard.md','core/execution_trace.md',
 'tests/test_cases.json','tests/regression_cases.md','tests/runtime_tests.md','tests/trace_validation.md','scripts/quick_validate.py'
]
for rel in required:
    if not (ROOT/rel).exists(): errors.append('Missing file: '+rel)
if ROOT.name not in {SKILL_NAME, SKILL_NAME+'-v0.6.2'}:
    errors.append(f'Root directory name should be {SKILL_NAME} or {SKILL_NAME}-v0.6.2, got {ROOT.name}')
for rel in ['SKILL.md','README.md','VERSION.md','CHANGELOG.md','RELEASE_REPORT.md']:
    p=ROOT/rel
    if p.exists() and VERSION not in p.read_text(encoding='utf-8'):
        errors.append(f'{rel} missing version {VERSION}')
for rel in ['SKILL.md','README.md','agents/openai.yaml']:
    p=ROOT/rel
    if p.exists() and DISPLAY_NAME not in p.read_text(encoding='utf-8'):
        errors.append(f'{rel} missing display name {DISPLAY_NAME}')
lock_text='\n'.join((ROOT/rel).read_text(encoding='utf-8') for rel in ['SKILL.md','README.md','references/image-gen-text2im-contract.md','references/aspect-ratio-lock.md'] if (ROOT/rel).exists())
for kw in ['image_gen.text2im','Execution Lock','Single Image Gen Authority','STRICT EXACT 3:4 PORTRAIT IMAGE ONLY.','1080×1440','1536×2048','width / height = 0.75','0.745','0.755','fallback renderer','3:4']:
    if kw not in lock_text: errors.append('missing preserved lock keyword: '+kw)
all_text='\n'.join(p.read_text(encoding='utf-8') for p in ROOT.rglob('*.md'))
for kw in ['production-grade deterministic AI pipeline','runtime simulation layer','encoding safety layer','execution trace system','observable','simulation-driven','execution-traceable','simulation before generation','encoding safety before pipeline','execution trace after generation','scorer controls execution','controller is single source of truth','image_gen only allowed if ALL checks pass','white-box AI pipeline','pre-execution validation stage']:
    if kw not in all_text: errors.append('missing v0.6.2 semantic token: '+kw)
module_tokens={
 'core/runtime_simulator.md':['input','content_graph','layout_graph','prompt_composer','fake_image_gen_simulation','structure_scorer','simulated_score','risk_prediction','predicted_issues','should_execute','IF simulated_score < 85','DO NOT CALL image_gen','FORCE repair loop'],
 'core/encoding_guard.md':['全系统 UTF-8 强制锁定','metadata corruption','文本丢失','prompt encoding error','IF any file encoding != UTF-8','BLOCK installation','REQUIRE repair','SKILL.md 中文必须完整','prompt 中文必须保留','image_gen text 必须可解析'],
 'core/execution_trace.md':['input','content_graph','layout_graph','prompt_version','scorer_before','scorer_after','repair_triggered','downgrade_triggered','image_gen_called','final_state','SAFE | FAIL','white-box AI pipeline'],
 'core/execution_controller.md':['runtime_simulator','structure_scorer','encoding_guard','execution_trace','IF encoding_guard FAIL','STOP SYSTEM','IF runtime_simulator FAIL','BLOCK image_gen','IF structure_score < 85','REPAIR'],
 'core/generation_loop.md':['simulation-first pipeline','STATE 1: input parse','STATE 2: encoding guard check','STATE 3: content graph build','STATE 4: layout graph build','STATE 5: runtime simulation','STATE 6: execution controller decision','STATE 7: prompt compose','STATE 8: image_gen call (if allowed)','STATE 9: structure scoring','STATE 11: execution trace write','STATE 12: loop max 3'],
 'core/structure_scorer.md':['simulation-aware scoring','pre_gen_score','post_gen_score','delta'],
 'core/gate_system.md':['IF encoding_guard FAIL','BLOCK ALL','IF runtime_simulator FAIL','BLOCK image_gen','IF structure_score < 85','BLOCK image_gen'],
 'core/repair_policy_matrix.md':['repair now depends on','simulation result','execution trace','scorer delta'],
}
for rel,toks in module_tokens.items():
    p=ROOT/rel
    if p.exists():
        txt=p.read_text(encoding='utf-8')
        for kw in toks:
            if kw not in txt: errors.append(f'{rel} missing {kw}')
try:
    data=json.loads((ROOT/'tests/test_cases.json').read_text(encoding='utf-8'))
    if not isinstance(data,list) or len(data)<10: errors.append('tests/test_cases.json must contain at least 10 cases')
    for i,c in enumerate(data):
        if isinstance(c,dict):
            for f in ['structure_score_expected','failure_modes_expected','repair_strategy_expected','runtime_simulation_expected','encoding_guard_expected','execution_trace_expected']:
                if f not in c: errors.append(f'tests/test_cases.json case {i} missing {f}')
except Exception as e: errors.append('tests/test_cases.json invalid: '+str(e))
for rel,toks in {
 'tests/runtime_tests.md':['encoding failure case','simulation failure case','layout overload case','multi-hand risk case','scoring instability case'],
 'tests/trace_validation.md':['trace 是否完整记录','是否包含所有 pipeline steps','是否能复现生成过程','input','content_graph','layout_graph','prompt_version','scorer_before','scorer_after','image_gen_called','final_state']
}.items():
    p=ROOT/rel
    if p.exists():
        txt=p.read_text(encoding='utf-8')
        for kw in toks:
            if kw not in txt: errors.append(f'{rel} missing {kw}')
# UTF-8 validation and forbidden local rendering imports
for p in ROOT.rglob('*'):
    if not p.is_file(): continue
    if any(part in {'.git','__MACOSX','__pycache__'} for part in p.parts): errors.append('Cache/temp path included: '+str(p.relative_to(ROOT)))
    try: txt=p.read_text(encoding='utf-8')
    except UnicodeDecodeError: errors.append('File is not UTF-8: '+str(p.relative_to(ROOT))); continue
    if p.suffix in {'.py','.js','.ts','.mjs'} and p.name!='quick_validate.py':
        for pat in [r'from\s+PIL\s+import',r'import\s+PIL',r'import\s+canvas',r'import\s+cairo']:
            if re.search(pat,txt): errors.append('Forbidden local rendering import in '+str(p.relative_to(ROOT)))
if errors:
    print('Validation failed:')
    for e in errors: print('-',e)
    sys.exit(1)
print(f'Validation passed for {SKILL_NAME} {VERSION}')
