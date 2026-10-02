"""Kesinti ve Retry Fırtınası Simülatörü.

Problem: Kesinti sırasında retry politikasının işçi kapasitesi ve toplam gecikme üzerindeki etkisini karşılaştırmak.
Method: Olay kuyruğu, token bucket, jitter, circuit breaker
Invariant: Sanal zaman kullanılır; dört politika aynı varış verisiyle kıyaslanır.
Boundary: Ağ bağlantısı kurmaz; dağıtık devre kesicinin ve HTTP sunucusunun gerçek davranışını ayrıca ölçmek gerekir."""
import heapq, random, statistics

def simulate(arrivals, policy, workers=4, rate=10, burst=10, outage=(20, 35), deadline=30, seed=42, max_attempts=6):
    if workers < 1 or rate <= 0 or burst < 1 or (deadline <= 0):
        raise ValueError('invalid capacity')
    if policy not in ['none', 'fixed', 'jitter', 'circuit']:
        raise ValueError('unknown policy')
    if len({a['id'] for a in arrivals}) != len(arrivals):
        raise ValueError('duplicate request ID')
    rng = random.Random(seed)
    events = []
    available = [0.0] * workers
    heapq.heapify(available)
    tokens = float(burst)
    last = 0.0
    opened_until = 0.0
    streak = 0
    attempts = []
    outcomes = []
    skips = 0
    for a in arrivals:
        if a['at'] < 0 or a['service'] <= 0:
            raise ValueError('invalid arrival')
        heapq.heappush(events, (a['at'], a['id'], 1, a['at'], a['service']))
    while events:
        due, i, n, original, service = heapq.heappop(events)
        if due - original >= deadline:
            outcomes.append({'id': i, 'success': False, 'reason': 'deadline', 'elapsed': round(due - original, 6), 'attempts': n - 1})
            continue
        if policy == 'circuit' and due < opened_until:
            skips += 1
            heapq.heappush(events, (opened_until, i, n, original, service))
            continue
        free = heapq.heappop(available)
        start = max(due, free, last)
        tokens = min(burst, tokens + (start - last) * rate)
        last = start
        if tokens < 1:
            start += (1 - tokens) / rate
            tokens = 0
            last = start
        else:
            tokens -= 1
        if start + service - original > deadline:
            heapq.heappush(available, free)
            outcomes.append({'id': i, 'success': False, 'reason': 'deadline', 'elapsed': round(start - original, 6), 'attempts': n - 1})
            continue
        end = start + service
        heapq.heappush(available, end)
        failed = outage[0] <= start < outage[1]
        attempts.append({'id': i, 'attempt': n, 'start': round(start, 6), 'failed': failed})
        streak = streak + 1 if failed else 0
        if policy == 'circuit' and streak >= 3:
            opened_until = end + 5
            streak = 0
        if failed and policy != 'none' and (n < max_attempts):
            delay = 1 if policy == 'fixed' else rng.uniform(0, min(16, 2 ** (n - 1)))
            heapq.heappush(events, (end + delay, i, n + 1, original, service))
        else:
            outcomes.append({'id': i, 'success': not failed, 'reason': 'accepted' if not failed else 'attempt_budget', 'elapsed': round(end - original, 6), 'attempts': n})
    successful = sorted((o['elapsed'] for o in outcomes if o['success']))
    p95 = successful[min(len(successful) - 1, int(0.95 * (len(successful) - 1)))] if successful else None
    return {'policy': policy, 'requests': len(arrivals), 'success': sum((o['success'] for o in outcomes)), 'calls': len(attempts), 'amplification': len(attempts) / len(arrivals) if arrivals else 0, 'success_p95_s': p95, 'circuit_deferrals': skips, 'outcomes': sorted(outcomes, key=lambda x: x['id']), 'attempt_log': attempts}

def run(config):
    rng = random.Random(config.get('seed', 42))
    arrivals = [{'id': i, 'at': rng.uniform(0, 60), 'service': rng.uniform(0.05, 0.25)} for i in range(config.get('requests', 400))]
    return {'policies': [simulate(arrivals, p, **config.get('capacity', {})) for p in ['none', 'fixed', 'jitter', 'circuit']], 'paired_arrivals': True}

import argparse, json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Run reproducible synthetic project scenario')
    parser.add_argument('command', choices=['demo'])
    parser.add_argument('--input', default='scenario.json')
    parser.add_argument('--output', default='report.json')
    args = parser.parse_args()
    report = run(json.loads(Path(args.input).read_text(encoding='utf-8')))
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    print(f'Report: {target}')
if __name__ == '__main__':
    main()
