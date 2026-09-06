from pathlib import Path
import json, re

DATA = Path(__file__).resolve().parent.parent / 'data' / 'knowledge.json'

STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'if', 'then', 'else', 'when',
    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
    'too', 'very', 'can', 'will', 'just', 'should', 'now', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'what', 'how', 'why', 'where', 'which', 'who', 'whom', 'this',
    'that', 'these', 'those', 'am', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
    'you', 'your', 'yours', 'it', 'its', 'itself', 'they', 'them', 'their'
}

DOMAIN_KEYWORDS = {
    'Patent': {'patent', 'patents', 'novel', 'novelty', 'inventive', 'claims', 'inpass', 'fer', 'controller', 'spec', 'specification', 'infringement', 'fto'},
    'Traditional Knowledge': {'traditional', 'knowledge', 'tkdl', 'ayurveda', 'ayurvedic', 'unani', 'siddha', 'herbal', 'botanical', 'folk', 'tribal', 'plant', 'extract', 'ancient'},
    'Biodiversity': {'biodiversity', 'abs', 'nba', 'biological', 'resource', 'genetic', 'sbb', 'bmc', 'benefit', 'sharing', 'nagoya', 'pbr'},
    'Trademark': {'trademark', 'trademarks', 'brand', 'logo', 'mark', 'class', 'classes', 'nice', 'madrid', 'distinctive', 'confusion', 'passing'},
    'Regulatory': {'regulatory', 'cdsco', 'ayush', 'fssai', 'gmp', 'schedule', 'clinical', 'safety', 'stability', 'ich', 'trial', 'supplement', 'labeling'},
    'Design': {'design', 'designs', 'aesthetic', 'ornament', 'shape', 'configuration', 'locarno', 'hague', 'visual'},
    'Copyright': {'copyright', 'author', 'literary', 'artistic', 'source', 'code', 'software', 'berne', 'expression', 'fair'},
    'Trade Secret': {'secret', 'confidential', 'nda', 'knowhow', 'secrecy', 'agreement'}
}

def load_knowledge():
    if not DATA.exists():
        return []
    return json.loads(DATA.read_text(encoding='utf-8'))

def retrieve(query: str, jurisdiction: str = 'India', limit: int = 5):
    all_records = load_knowledge()
    jur_lower = (jurisdiction or 'India').lower()

    # Filter by jurisdiction
    filtered = []
    for r in all_records:
        r_jur = r.get('jurisdiction', 'Both').lower()
        if jur_lower in ('india', 'in') and r_jur not in ('india', 'both'):
            continue
        if jur_lower in ('international', 'intl', 'global') and r_jur not in ('international', 'both'):
            continue
        filtered.append(r)

    if not filtered:
        filtered = all_records

    raw_tokens = re.findall(r'[a-zA-Z0-9]+', query.lower())
    terms = [t for t in raw_tokens if len(t) > 2 and t not in STOP_WORDS]

    if not terms:
        # Return representative default records across distinct domains
        seen_domains = set()
        defaults = []
        for r in filtered:
            if r['domain'] not in seen_domains:
                seen_domains.add(r['domain'])
                defaults.append(r)
            if len(defaults) >= limit:
                break
        return defaults

    query_str = ' '.join(raw_tokens)
    out = []

    for r in filtered:
        title_lower = r.get('title', '').lower()
        domain_lower = r.get('domain', '').lower()
        content_lower = r.get('content', '').lower()

        score = 0
        # Title match weighting (3x)
        for t in terms:
            if t in title_lower:
                score += 3
            if t in domain_lower:
                score += 2
            if t in content_lower:
                score += 1

        # Domain synergy bonus
        for domain, kw_set in DOMAIN_KEYWORDS.items():
            if r.get('domain') == domain:
                overlap = len(kw_set.intersection(terms))
                if overlap > 0:
                    score += overlap * 2

        if score > 0:
            out.append((score, r))

    out.sort(key=lambda x: x[0], reverse=True)

    if out:
        return [r for _, r in out[:limit]]

    # If no keyword matched, return top diverse records for jurisdiction
    return filtered[:limit]
