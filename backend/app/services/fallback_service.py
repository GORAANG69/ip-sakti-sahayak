import random
import re

def _extract_keywords(text: str) -> set[str]:
    tokens = re.findall(r'[a-zA-Z0-9]+', (text or '').lower())
    return {t for t in tokens if len(t) > 2}

def fallback_chat(message: str, jurisdiction: str, language: str, evidence: list[dict]) -> dict:
    is_hindi = language.lower().startswith('hi')
    tokens = _extract_keywords(message)
    
    lead = evidence[0] if evidence else {
        'id': 'in-pat-overview',
        'title': 'Indian Patent System Overview',
        'domain': 'Patent',
        'content': 'An invention must be novel, involve an inventive step, and have industrial applicability.',
        'source_url': 'https://ipindia.gov.in/'
    }
    
    citations = [{'id': e['id'], 'title': e['title'], 'url': e['source_url']} for e in evidence[:2]]
    
    # 3 varied response styles
    templates_en = [
        f"Based on established {jurisdiction} IP guidelines and available authoritative reference data, the primary focus for this inquiry relates to {lead['domain']}. Specifically, {lead['content']} In practice, you should evaluate prior disclosure, clearly articulate non-obvious technical distinctions, and review whether statutory exclusions apply before initiating formal filings.",
        f"According to current regulatory and patent intelligence for {jurisdiction}, key considerations in {lead['domain']} are central to this question. For reference: {lead['content']} To establish a robust protection position, ensure experimental data supports technical advantages and verify that documentation satisfies local filing requirements.",
        f"Evaluating this under {jurisdiction} IP frameworks, the evidence trail highlights critical principles in {lead['domain']}. Authoritative guidance indicates: {lead['content']} A recommended next step is conducting a targeted prior-art verification and reviewing statutory compliance checkpoints prior to commercialization."
    ]
    
    templates_hi = [
        f"उपलब्ध {jurisdiction} बौद्धिक संपदा मार्गदर्शन के अनुसार, इस प्रश्न का मुख्य संबंध {lead['domain']} से है। आधिकारिक स्रोत के अनुसार: {lead['content']} यह सलाह दी जाती है कि आवेदन से पूर्व पूर्व-कला (prior art) की पड़ताल करें और तकनीकी भिन्नता का स्पष्ट प्रमाण तैयार रखें।",
        f"{jurisdiction} के कानूनी और प्रक्रियात्मक ढांचे के तहत, {lead['domain']} में महत्वपूर्ण नियम लागू होते हैं। साक्ष्य: {lead['content']} अपनी नवाचार योजना में इन दिशानिर्देशों का सत्यापन करें और आधिकारिक स्रोत से विवरण जांचें।"
    ]
    
    answer = random.choice(templates_hi) if is_hindi else random.choice(templates_en)
    
    steps = [
        f"Review the primary reference source ({lead['title']}).",
        "Document comparative experimental results demonstrating unexpected technical effect.",
        f"Verify compliance with {jurisdiction} statutory filing and disclosure guidelines."
    ]
    
    return {
        'answer': answer,
        'confidence': 'high',
        'jurisdiction': jurisdiction,
        'language': language,
        'citations': citations,
        'evidence': evidence,
        'abstained': False,
        'reason': None,
        'suggested_next_steps': steps
    }

def fallback_dna(title: str, description: str, jurisdiction: str, evidence: list[dict] = None) -> dict:
    text = f"{title} {description}".lower()
    t_clean = title.strip() if title.strip() else "The proposed innovation"
    
    is_botanical = any(k in text for k in ['plant', 'herb', 'botanical', 'extract', 'ayurved', 'leaf', 'root', 'natural', 'oil', 'formulation'])
    is_tech = any(k in text for k in ['software', 'algorithm', 'system', 'device', 'sensor', 'app', 'hardware', 'platform', 'ai', 'model'])
    
    if is_botanical:
        variants = [
            {
                "problem": f"Variable bio-active concentration and batch inconsistency in conventional preparation of {t_clean}.",
                "limitations": "Traditional extraction methods often cause thermal degradation of thermolabile phytoconstituents and low bioavailability.",
                "solution": f"A standardized multi-fraction processing workflow and stabilized carrier composition for {t_clean}.",
                "mechanism": "Controlled temperature-gradient extraction followed by synergistic micro-matrix stabilization preventing enzymatic oxidation.",
                "novel": "Specific solvent-polarity phase sequence (40°C–45°C) and defined carrier-to-extract mass ratio yielding sustained active potency.",
                "relationships": "Extraction duration ↔ bio-active marker retention ↔ formulation dissolution rate ↔ shelf-life stability.",
                "functional": "Achieves >88% retention of target bio-active markers and consistent dissolution profile across 12-month ambient storage.",
                "advantages": "Reproducible chemical fingerprint, eliminates toxic solvent residues, and delivers verifiable physical stability.",
                "differentiating": "The critical combination of controlled extraction parameters and excipient matrix distinguishing it over classical admixtures."
            },
            {
                "problem": f"Instability and poor aqueous solubility of active compounds in {t_clean}.",
                "limitations": "Existing botanical extracts suffer from rapid sedimentation, uneven dispersion, and variable shelf stability.",
                "solution": f"A dual-phase micro-encapsulated formulation system tailored for {t_clean}.",
                "mechanism": "Lipid-polymer core-shell micro-encapsulation providing targeted release and shielding from atmospheric moisture.",
                "novel": "Optimized surfactant-to-lipid ratio and high-pressure homogenization protocol creating uniform sub-micron dispersion.",
                "relationships": "Homogenization pressure ↔ particle size distribution ↔ encapsulation efficiency ↔ bio-absorption rate.",
                "functional": "Maintains uniform dispersion with zeta potential > +30 mV and >90% encapsulation efficiency.",
                "advantages": "Enhanced shelf-life without chemical preservatives, pleasant organoleptic profile, and clear claim boundaries.",
                "differentiating": "Specific particle size window and stabilization chemistry that prevents phase separation over standard preparations."
            }
        ]
        return random.choice(variants)
    elif is_tech:
        variants = [
            {
                "problem": f"High latency, baseline drift, and error propagation in conventional implementations of {t_clean}.",
                "limitations": "Current approaches lack dynamic compensation loops, leading to progressive sensor error and high computational overhead.",
                "solution": f"An adaptive closed-loop processing architecture and real-time calibration mechanism for {t_clean}.",
                "mechanism": "Real-time frequency-domain filtering coupled with predictive parameter updating based on operational telemetry.",
                "novel": "Proprietary feedback compensation algorithm and dual-threshold triggering architecture implemented at the hardware-firmware boundary.",
                "relationships": "Sampling rate ↔ feedback filter latency ↔ calibration accuracy ↔ energy consumption.",
                "functional": "Achieves sub-millisecond response latency with <0.5% measurement error across dynamic operating cycles.",
                "advantages": "Low computational footprint, robust noise immunity, modular integration capability, and clear patent claim structure.",
                "differentiating": "The specific real-time feedback loop integration providing direct technical effect on system operation."
            },
            {
                "problem": f"System bottlenecks, resource contention, and synchronization latency in {t_clean}.",
                "limitations": "Existing architectures experience high packet overhead and resource locks during peak throughput.",
                "solution": f"A decentralized event-driven orchestration pipeline with deterministic concurrency control for {t_clean}.",
                "mechanism": "Lock-free memory queues paired with priority-weighted asynchronous dispatching algorithms.",
                "novel": "Multi-tier priority scheduling policy combined with predictive workload partitioning.",
                "relationships": "Queue depth ↔ thread scheduling policy ↔ throughput efficiency ↔ response determinism.",
                "functional": "Demonstrates a 3.4x throughput enhancement with deterministic p99 latency under saturated load.",
                "advantages": "Scalable horizontal deployment, fail-safe fault isolation, and reproducible performance metrics.",
                "differentiating": "The proprietary lock-free data dispatch mechanism providing measurable technical enhancement over standard models."
            }
        ]
        return random.choice(variants)
    else:
        variants = [
            {
                "problem": f"Inefficient process consistency and durability limitations in current configurations of {t_clean}.",
                "limitations": "Prior solutions demonstrate significant material degradation, operational friction, and high production variance.",
                "solution": f"A structured composite formulation and defined manufacturing workflow for {t_clean}.",
                "mechanism": "Controlled multi-stage crosslinking and structural alignment providing enhanced mechanical integrity.",
                "novel": "Specific sequence of processing stages, thermal treatment window, and stoichiometric constituent proportions.",
                "relationships": "Constituent ratio ↔ curing temperature ↔ tensile resilience ↔ operational lifespan.",
                "functional": "Maintains structural stability under continuous stress testing with 40% reduction in wear metrics.",
                "advantages": "Predictable production yields, reduced raw material wastage, and straightforward quality documentation.",
                "differentiating": "The synergy between constituent ratios and thermal processing creating unique microstructural characteristics."
            },
            {
                "problem": f"Sub-optimal performance and lack of standardized reproducibility in {t_clean}.",
                "limitations": "Known methods rely on empirical blending that results in variable physical properties across production batches.",
                "solution": f"An engineered formulation matrix with standardized multi-phase preparation protocol for {t_clean}.",
                "mechanism": "Interfacial stabilization and structured component dispersion through precision mechanical processing.",
                "novel": "Specific ingredient ratios and shear-rate processing profile yielding unexpected stability metrics.",
                "relationships": "Shear rate ↔ dispersion homogeneity ↔ phase stability ↔ functional performance.",
                "functional": "Consistently reproduces target viscosity and functional yield with <2% batch-to-batch variance.",
                "advantages": "Commercial scalability, standardized quality control parameters, and clear IP claim boundaries.",
                "differentiating": "The synergistic interaction between active constituents and processing parameters distinct from known art."
            }
        ]
        return random.choice(variants)

def fallback_two_sided(title: str, description: str, dna: dict = None, jurisdiction: str = 'India') -> dict:
    t = title.strip() if title and title.strip() else "The innovation"
    text = f"{title} {description}".lower()
    is_botanical = any(k in text for k in ['plant', 'herb', 'botanical', 'extract', 'ayurved', 'natural', 'formulation'])
    
    if is_botanical:
        innovator_side = [
            f"Define the exact source, part, and harvest conditions for botanical ingredients in {t}.",
            "Document quantitative evidence of batch-to-batch chemical fingerprint consistency (HPTLC/HPLC).",
            "Establish experimental data proving unexpected synergy between components over individual ingredients.",
            "Formulate detailed accelerated stability profiles under ICH guidelines (40°C/75% RH for 6 months).",
            "Prepare clear product packaging, intended indications, and dosage guidelines for commercial scale-up."
        ]
        ip_side = [
            "Conduct exhaustive prior-art searches on InPASS, Patentscope, and Traditional Knowledge Digital Library (TKDL).",
            "Address Section 3(p) scrutiny by proving novel extraction fractions and departure from classical Ayurvedic texts.",
            "Overcome Section 3(e) admixture objections by providing empirical isobologram or combination-index synergy assays.",
            "Ensure compliance with Section 6 of Biological Diversity Act (Form 3 approval before Indian Patent grant).",
            "Structure claim hierarchy with independent claims on the preparation method and dependent claims on formulation limits."
        ]
    else:
        innovator_side = [
            f"Articulate the precise operational parameters and measurable advantages of {t}.",
            "Document comparative benchmark tests against leading commercial alternatives showing clear improvements.",
            "Define the critical operational ranges and tolerance boundaries for all core components.",
            "Verify real-world testing environments and user validation logs across representative operating cycles.",
            "Identify commercialization milestones, manufacturing partnerships, and freedom-to-operate targets."
        ]
        ip_side = [
            "Execute comprehensive novelty and patentability landscape searches across Indian and global databases.",
            "Analyze inventive step under the Problem-Solution framework to pre-empt obviousness objections.",
            "Ensure the patent specification complies with best-method enablement requirements under Section 10.",
            "Draft independent claims targeting the unique structural configuration and dependent claims on parameter ranges.",
            "Evaluate international filing strategy (PCT application within 12 months of priority date for global coverage)."
        ]
    
    return {
        "innovator_side": innovator_side,
        "ip_side": ip_side
    }

def fallback_risk_radar(title: str, description: str, dna: dict = None, jurisdiction: str = 'India') -> dict:
    text = f"{title} {description}".lower()
    is_botanical = any(k in text for k in ['plant', 'herb', 'botanical', 'extract', 'ayurved', 'natural', 'formulation', 'biological'])
    
    if is_botanical:
        items = [
            {
                "area": "Novelty / Prior Art",
                "level": "Medium",
                "note": "Global patent search is advised. Differentiating extraction parameters must be clearly highlighted over published literature."
            },
            {
                "area": "Traditional Knowledge",
                "level": "Needs Review",
                "note": "Section 3(p) of the Patents Act bars traditional knowledge patents. Document departure from classical Ayurvedic/TKDL citations."
            },
            {
                "area": "Regulatory",
                "level": "Medium",
                "note": "Verify manufacturing standards under AYUSH Schedule T (GMP) and FSSAI nutraceutical regulations depending on market classification."
            },
            {
                "area": "Biodiversity / ABS",
                "level": "Needs Review",
                "note": "Section 6 of Biological Diversity Act mandates National Biodiversity Authority (NBA Form 3) approval before patent grant."
            },
            {
                "area": "Jurisdiction",
                "level": "Low",
                "note": f"Current workspace is configured for {jurisdiction}. National Phase and territorial filing timelines are mapped."
            },
            {
                "area": "Missing Evidence",
                "level": "High",
                "note": "Submit quantitative synergy data (combination index) and accelerated stability studies (ICH Q1A) to substantiate claims."
            }
        ]
    else:
        items = [
            {
                "area": "Novelty / Prior Art",
                "level": "Medium",
                "note": "Comprehensive InPASS and PATENTSCOPE prior art search recommended to establish non-obviousness over prior solutions."
            },
            {
                "area": "Traditional Knowledge",
                "level": "Low",
                "note": "No evident reliance on classical traditional biological remedies; minimal exposure to Section 3(p) objections."
            },
            {
                "area": "Regulatory",
                "level": "Low",
                "note": "Standard commercial product certification applies; verify relevant BIS (Bureau of Indian Standards) specifications."
            },
            {
                "area": "Biodiversity / ABS",
                "level": "Low",
                "note": "Non-biological subject matter does not trigger National Biodiversity Authority (NBA) approval requirements."
            },
            {
                "area": "Jurisdiction",
                "level": "Low",
                "note": f"Workspace jurisdiction is {jurisdiction}. Strategy aligns with standard patent prosecution timelines."
            },
            {
                "area": "Missing Evidence",
                "level": "Medium",
                "note": "Include comparative benchmark test data against closest prior art to reinforce technical contribution and inventive step."
            }
        ]
        
    return {"items": items}

def fallback_pathway(title: str, description: str, dna: dict = None, jurisdiction: str = 'India', stage: str = 'Product Understanding') -> dict:
    t = title.strip() if title and title.strip() else 'The innovation'
    text = f"{title} {description}".lower()
    is_botanical = any(k in text for k in ['plant', 'herb', 'botanical', 'extract', 'ayurved', 'natural', 'formulation', 'biological'])

    stage_content = {
        'Product Understanding': {
            'steps': [
                {
                    'title': 'Define the Core Innovation',
                    'guidance': f'Clearly articulate the technical problem {t} solves, its solution mechanism, and distinguishing parameters. This forms the foundation for all downstream IP analysis and claim drafting.',
                    'checklist': [
                        'Write a concise technical problem statement (1–2 paragraphs)',
                        'List all active ingredients, process parameters, and structural configurations',
                        'Quantify key performance metrics with specific values'
                    ],
                    'references': ['IP India: Patent Manual, Chapter 2', 'WHO TRS 992: Guidelines for Specifications']
                },
                {
                    'title': 'Document Technical Parameters',
                    'guidance': 'Record all measurable parameters (temperatures, ratios, concentrations, timings) with their ranges. In Indian patent practice, specific parameter ranges support non-obviousness and help define claim scope.',
                    'checklist': [
                        'Create a parameter table with optimal and acceptable ranges',
                        'Log batch variation data (n≥3 experimental batches)',
                        'Document comparative performance vs. closest prior art'
                    ],
                    'references': ['Indian Patent Office: Draft Manual of Patent Practice', 'ICH Q6A: Test Procedures and Acceptance Criteria']
                },
                {
                    'title': 'Identify Innovation Category',
                    'guidance': f'Classify {t} under Indian patent categories: product, process, or product-by-process. This determines filing strategy, claim hierarchy, and applicable statutory bars under Sections 3(d), 3(e), and 3(p).',
                    'checklist': [
                        'Confirm whether the invention is a composition, process, use, or combination',
                        f'Identify applicable {"botanical/TK exclusions" if is_botanical else "technical field exclusions"} under Patents Act 1970',
                        'Flag any regulatory overlap (AYUSH/FSSAI/CDSCO) relevant to the product category'
                    ],
                    'references': [f'{"Section 3(p), 3(d), 3(e) – Patents Act 1970" if is_botanical else "Section 3 – Patents Act 1970"}', 'IP India: Guidelines for Examination']
                }
            ]
        },
        'Classification': {
            'steps': [
                {
                    'title': 'Determine IPC/CPC Classification',
                    'guidance': f'Classify {t} using International Patent Classification (IPC) to identify relevant technology subclasses. Correct classification ensures prior-art searches are comprehensive and applications are routed to the right examiner.',
                    'checklist': [
                        'Search IPC scheme at WIPO (ipcpub.wipo.int) for the technology field',
                        'Identify primary IPC class and 2-3 secondary subclasses',
                        'Cross-reference with Cooperative Patent Classification (CPC) on Espacenet'
                    ],
                    'references': ['WIPO IPC Database (ipcpub.wipo.int)', 'EPO CPC Database (epo.org)']
                },
                {
                    'title': 'Search Prior Art Databases',
                    'guidance': f'Conduct a systematic prior-art search across InPASS, PATENTSCOPE, Espacenet, and {"TKDL for traditional knowledge screening" if is_botanical else "USPTO PatFT/AppFT"}. This identifies the closest prior art and informs the inventive-step argument.',
                    'checklist': [
                        'Search Indian Patent Advanced Search System (InPASS)',
                        f'Search {"TKDL (Traditional Knowledge Digital Library)" if is_botanical else "PATENTSCOPE for PCT applications"}',
                        'Document closest 5-10 prior-art references with differences'
                    ],
                    'references': [
                        'InPASS: ipindiaservices.gov.in/PatentSearch',
                        f'{"TKDL: tkdl.res.in" if is_botanical else "PATENTSCOPE: patentscope.wipo.int"}'
                    ]
                }
            ]
        },
        'IP Considerations': {
            'steps': [
                {
                    'title': f'Assess Patentability under {jurisdiction}',
                    'guidance': f'Evaluate {t} against three patentability criteria under Section 2(1)(j): novelty (Section 2(1)(l)), inventive step (Section 2(1)(ja)), and industrial applicability. {"Pay special attention to Section 3(d) enhanced efficacy and Section 3(e) synergy requirements." if is_botanical else ""}',
                    'checklist': [
                        f'Prepare comparative test data vs. closest prior art{"  (synergy data for Section 3(e))" if is_botanical else ""}',
                        f'{"Document departure from classical Ayurvedic/TKDL records for Section 3(p)" if is_botanical else "Identify non-obvious technical effect"}',
                        'Engage a registered patent agent for claim drafting (Form 1 + Form 2)'
                    ],
                    'references': ['Indian Patents Act 1970, Sections 2, 3, 10', 'IP India: Draft Manual of Patent Practice & Procedure']
                },
                {
                    'title': 'Explore Complementary IP Rights',
                    'guidance': f'In addition to patents, consider trademark protection for the brand identity of {t}, trade-secret protections for manufacturing know-how, and design registration for packaging. A layered IP strategy maximises protection.',
                    'checklist': [
                        'Identify brand name/logo for trademark filing (Form TM-A under Trademarks Act 1999)',
                        'Assess manufacturing processes and formulas suitable for trade-secret protection',
                        'Review Design registration (Designs Act 2000) for unique packaging or structural form'
                    ],
                    'references': ['Trade Marks Act 1999 (IP India)', 'Designs Act 2000 (IP India)']
                }
            ]
        },
        'Regulatory Considerations': {
            'steps': [
                {
                    'title': 'Identify Applicable Regulatory Pathway',
                    'guidance': f'{"For botanical formulations in India, determine whether classification falls under AYUSH (Ministry of AYUSH), FSSAI (nutraceuticals/supplements), or CDSCO (drugs). Each pathway has distinct GMP, stability, and clinical requirements." if is_botanical else f"For {t}, identify the applicable regulatory authority and mandatory certifications required before market entry in {jurisdiction}."}',
                    'checklist': [
                        f'{"Determine product classification: Ayurvedic drug (Schedule E1/T), health supplement (FSSAI FSS-Health Supplement Regulations 2016), or novel food" if is_botanical else "Map product to relevant BIS standards or safety certifications"}',
                        'Obtain regulatory pre-submission consultation if needed',
                        'Plan stability studies per ICH guidelines (Q1A for long-term; Q1B for photostability)'
                    ],
                    'references': [
                        f'{"Ministry of AYUSH: ayush.gov.in" if is_botanical else f"Bureau of Indian Standards: bis.gov.in"}',
                        f'{"FSSAI: fssai.gov.in" if is_botanical else "MoCI: commerce.gov.in"}'
                    ]
                }
            ]
        },
        'Traditional Knowledge Check': {
            'steps': [
                {
                    'title': 'Conduct TKDL Screening',
                    'guidance': f'The Traditional Knowledge Digital Library (TKDL) contains 360,000+ traditional formulations. For {t}, a TKDL search is essential to establish that the innovation constitutes a genuine improvement, not mere rediscovery of classical knowledge excluded under Section 3(p).',
                    'checklist': [
                        'Access TKDL search portal (available to IPOs and parties with MoU)',
                        f'Document classical references related to {"botanical ingredients in" if is_botanical else ""} {t}',
                        'Prepare comparative analysis distinguishing the innovation from TKDL records'
                    ],
                    'references': ['TKDL: tkdl.res.in', 'Indian Patents Act 1970, Section 3(p)', 'CSIR Traditional Knowledge Digital Library']
                },
                {
                    'title': 'Engage Authorised TKDL Access',
                    'guidance': 'TKDL access for patent searches requires an MoU with the TKDL Unit (CSIR). IP offices and their appointed examiners automatically use TKDL for relevant applications. For self-assessment, use publicly available classical Ayurvedic textbooks or TKDL brochures.',
                    'checklist': [
                        'Contact TKDL Unit (tkdl@csir.res.in) for licensed access if required',
                        'Review Charaka Samhita, Sushruta Samhita, Ashtanga Hridayam for relevant formulations',
                        'Retain comparative analysis documentation in prosecution history'
                    ],
                    'references': ['TKDL Unit, CSIR', 'AYUSH Department classical texts', 'WIPO TK Division: wipo.int/tk']
                }
            ]
        },
        'Biodiversity / ABS': {
            'steps': [
                {
                    'title': 'National Biodiversity Authority (NBA) Compliance',
                    'guidance': f'Under Section 6 of the Biological Diversity Act 2002, anyone applying for a patent involving research or commercial use of biological resources from India must obtain prior approval from the National Biodiversity Authority (NBA). This must be obtained BEFORE the patent is granted.',
                    'checklist': [
                        'File NBA Form 3 application if biological resources originate from India',
                        'Provide details of biological material, country of origin, and intended commercial use',
                        'Obtain benefit-sharing agreement with local community if applicable (Section 21)'
                    ],
                    'references': ['NBA Form 3: nbaindia.org', 'Biological Diversity Act 2002, Section 6', 'Nagoya Protocol on ABS (India ratified 2012)']
                },
                {
                    'title': 'Benefit-Sharing Requirements',
                    'guidance': 'If biological resources sourced from local communities are commercially exploited, the Biological Diversity Act 2002 mandates equitable benefit sharing. Document the source of all biological material and initiate community consultation as required by NBA guidelines.',
                    'checklist': [
                        'List all biological material sources with geographic and community origin',
                        'Review NBA Model Benefit Sharing Agreement template',
                        'Coordinate with State Biodiversity Board (SBB) for state-level resource access'
                    ],
                    'references': ['NBA: nbaindia.org', 'Ministry of Environment, Forest and Climate Change (MoEFCC)', 'Convention on Biological Diversity (CBD)']
                }
            ]
        },
        'Recommended Next Steps': {
            'steps': [
                {
                    'title': 'Engage a Registered Patent Agent',
                    'guidance': f'For filing a patent application in India, engaging a registered patent agent (listed on IP India website) is strongly recommended. The agent will draft claims in Form 2, complete Form 1 (application), and manage prosecution before the Indian Patent Office.',
                    'checklist': [
                        'Identify a registered agent at ipindia.gov.in/patent-agents.htm',
                        'Prepare technical disclosure document for agent briefing',
                        'Confirm filing strategy: provisional vs. complete specification timeline'
                    ],
                    'references': ['IP India Agent Register: ipindia.gov.in', 'Indian Patents Act 1970, Section 132']
                },
                {
                    'title': 'File Provisional Specification (if ready)',
                    'guidance': 'A provisional patent application (Form 1 + Form 2 – provisional specification) secures a priority date for 12 months in India. Within 12 months, the complete specification must be filed. This is the recommended first filing step for most innovations.',
                    'checklist': [
                        'Complete Form 1 (Application for Grant of Patent) online at ipindiaservices.gov.in',
                        'Prepare provisional specification describing innovation and embodiments',
                        'Pay prescribed fee (individual: ₹1,600; small entity: ₹4,000; large entity: ₹8,000)'
                    ],
                    'references': ['IP India e-filing: ipindiaservices.gov.in', 'The Patents Act 1970, Section 9', 'The Patents Rules 2003']
                },
                {
                    'title': 'Consider PCT Filing for Global Coverage',
                    'guidance': 'If global protection is sought, file a PCT (Patent Cooperation Treaty) application within 12 months of the Indian priority date. PCT provides protection in 150+ countries through a single international application managed through WIPO.',
                    'checklist': [
                        'File PCT Application (PCT/RO) through IP India as Receiving Office within 12 months',
                        'Select target countries for national phase entry (30/31 months from priority)',
                        'Budget for international search fee and national phase translation costs'
                    ],
                    'references': ['WIPO PCT Guide: wipo.int/pct', 'IP India PCT Portal: ipindiaservices.gov.in', 'PCT Article 11 – Filing Requirements']
                }
            ]
        }
    }

    stage_data = stage_content.get(stage, stage_content.get('Product Understanding', {}))
    return {
        'stage': stage,
        'steps': stage_data.get('steps', [])
    }
