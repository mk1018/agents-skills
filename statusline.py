#!/usr/bin/env python3
"""Fine-grained progress bar with model/effort on first line"""
import json, sys, subprocess, os, glob, time
from datetime import datetime

data = json.load(sys.stdin)

BLOCKS = ' ▏▎▍▌▋▊▉█'
R = '\033[0m'
DIM = '\033[2m'
BOLD = '\033[1m'

def gradient(pct):
    if pct < 50:
        r = int(pct * 5.1)
        return f'\033[38;2;{r};200;80m'
    else:
        g = int(200 - (pct - 50) * 4)
        return f'\033[38;2;255;{max(g,0)};60m'

def bar(pct, width=5):
    pct = min(max(pct, 0), 100)
    filled = pct * width / 100
    full = int(filled)
    frac = int((filled - full) * 8)
    b = '█' * full
    if full < width:
        b += BLOCKS[frac]
        b += '░' * (width - full - 1)
    return b

def fmt(label, pct):
    p = round(pct)
    return f'{label} {gradient(pct)}{bar(pct)} {p}%{R}'

# Per-MTok USD rates (input, output); cache derived from input rate.
RATES = {'opus': (5.0, 25.0), 'sonnet': (3.0, 15.0), 'haiku': (1.0, 5.0), 'fable': (6.0, 30.0)}
DEFAULT_RATE = RATES['opus']

def rate_for(model_id):
    m = (model_id or '').lower()
    for key, r in RATES.items():
        if key in m:
            return r
    return DEFAULT_RATE

def line_cost_usd(usage, model_id):
    rin, rout = rate_for(model_id)
    cc = usage.get('cache_creation') or {}
    w5 = cc.get('ephemeral_5m_input_tokens', 0)
    w1 = cc.get('ephemeral_1h_input_tokens', 0)
    if not (w5 or w1):
        w5 = usage.get('cache_creation_input_tokens', 0) or 0
    return (
        usage.get('input_tokens', 0) * rin
        + usage.get('output_tokens', 0) * rout
        + usage.get('cache_read_input_tokens', 0) * rin * 0.1
        + w5 * rin * 1.25
        + w1 * rin * 2.0
    ) / 1_000_000

def daily_cost_usd():
    """Sum today's cost across all session transcripts, cached for 60s."""
    today = datetime.now().date().isoformat()
    cache_dir = os.path.expanduser('~/.claude/cache')
    cache_path = os.path.join(cache_dir, 'daily-cost.json')
    try:
        c = json.load(open(cache_path))
        if c.get('date') == today and (time.time() - c.get('at', 0)) < 60:
            return c['usd']
    except Exception:
        pass

    total = 0.0
    today_epoch = time.mktime(time.strptime(today, '%Y-%m-%d'))
    for f in glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')):
        try:
            if os.path.getmtime(f) < today_epoch:
                continue  # file untouched today
            for line in open(f):
                if '"usage"' not in line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                ts = d.get('timestamp')
                if not ts:
                    continue
                try:
                    local_date = datetime.fromisoformat(
                        ts.replace('Z', '+00:00')).astimezone().date().isoformat()
                except Exception:
                    continue
                if local_date != today:
                    continue
                msg = d.get('message') or {}
                usage = msg.get('usage')
                if usage:
                    total += line_cost_usd(usage, msg.get('model'))
        except Exception:
            continue

    try:
        os.makedirs(cache_dir, exist_ok=True)
        json.dump({'date': today, 'at': time.time(), 'usd': total}, open(cache_path, 'w'))
    except Exception:
        pass
    return total

raw_model = data.get('model', {}).get('display_name', 'Claude')
model = raw_model.replace(' context', '').replace('(', '').replace(')', '').strip()
# e.g. "Claude Opus 4.6 (1M context)" -> "Claude Opus 4.6 1M"
effort = data.get('effort_level', '')

# Get current directory
cwd = data.get('cwd') or data.get('workspace', {}).get('current_dir') or os.getcwd()

# Get git branch (skip optional lock with GIT_OPTIONAL_LOCKS=0)
try:
    branch = subprocess.check_output(
        ['git', '-C', cwd, 'symbolic-ref', '--short', 'HEAD'],
        stderr=subprocess.DEVNULL,
        env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}
    ).decode().strip()
except Exception:
    branch = ''

# Git status for branch color
GREEN = '\033[32m'
YELLOW = '\033[33m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
branch_color = CYAN
if branch:
    try:
        status = subprocess.check_output(
            ['git', '-C', cwd, 'status', '--porcelain'],
            stderr=subprocess.DEVNULL,
            env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}
        ).decode()
        has_staged = any(l[0] in 'MADRC' for l in status.splitlines() if l)
        has_unstaged = any(l[1] in 'MADRC?' for l in status.splitlines() if l)
        if has_staged:
            branch_color = MAGENTA
        elif has_unstaged:
            branch_color = YELLOW
    except Exception:
        pass

# Line 0: cwd + branch + model
display_cwd = os.path.basename(cwd)
line0 = f'{GREEN}{display_cwd}{R}'
if branch:
    line0 += f'{branch_color}[{branch}]{R}'
# Line 1: model + usage bars
parts = [f'{BOLD}{model}{R}']
ctx = data.get('context_window', {}).get('used_percentage') or 0
parts.append(fmt('ctx', ctx))

rate_limits = data.get('rate_limits', {})
five = (rate_limits.get('five_hour') or {}).get('used_percentage') or 0
parts.append(fmt('5h', five))

week = (rate_limits.get('seven_day') or {}).get('used_percentage') or 0
parts.append(fmt('7d', week))

line1 = f' {DIM}│{R} '.join(parts)

# Line 2: approximate cost (USD) — today's total (daily) and this session
session_usd = (data.get('cost', {}).get('total_cost_usd')) or 0
day_usd = daily_cost_usd()
line2 = f'今日 ${day_usd:,.2f} {DIM}│{R} 今回 ${session_usd:,.2f}'

print(f'{line0}\n{line1}\n{line2}', end='')
