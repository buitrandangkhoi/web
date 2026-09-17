"""
Writing Collector for IELTS Learning Web
Expanded comprehensive database for Writing Task 1, Task 2,
Manchester Academic Phrasebank, and Official Band Descriptors.
"""
import json
from pathlib import Path
from pipeline.config import WRITING_DIR

TASK1_DIR = WRITING_DIR / "task1"
TASK2_DIR = WRITING_DIR / "task2"
PHRASEBANK_DIR = WRITING_DIR / "phrasebank"

def generate_task1_dataset():
    TASK1_DIR.mkdir(parents=True, exist_ok=True)
    task1_items = [
        {
            "id": "wri_t1_01",
            "chart_type": "Line Graph",
            "topic": "Renewable Energy Consumption (2000-2020)",
            "prompt": "The graph below shows the proportion of energy generated from renewable sources in four European countries between 2000 and 2020.",
            "time_period": "2000 - 2020",
            "overview_focus": "Overall upward trend across all nations, with Germany maintaining the dominant position throughout the period.",
            "band_score": 9.0,
            "model_answer": {
                "introduction": "The line graph illustrates the percentage of total energy produced from renewable resources in four European nations (Germany, France, Sweden, and Spain) over a twenty-year period from 2000 to 2020.",
                "overview": "Overall, it is evident that all four countries experienced an upward trajectory in their utilization of green energy. Germany consistently generated the highest share of renewable power, whereas France recorded the lowest figures despite notable progress.",
                "body_1": "In 2000, Germany began at approximately 25%, rising steadily to reach roughly 38% by 2010, before surging to a peak of nearly 52% at the close of the timeline. Sweden followed a comparable pattern, climbing from 18% in the initial year to finish at approximately 36% in 2020.",
                "body_2": "Conversely, Spain and France started from significantly lower baselines of 10% and 6% respectively. While Spain witnessed substantial fluctuations before settling around 24%, France demonstrated gradual but consistent growth, ultimately doubling its initial contribution to conclude at 12% in 2020."
            },
            "academic_collocations": [
                {"phrase": "experienced an upward trajectory", "meaning": "went through a continuous rise"},
                {"phrase": "consistently generated the highest share", "meaning": "held the top proportion throughout"},
                {"phrase": "surging to a peak of", "meaning": "rising rapidly to the highest point"},
                {"phrase": "started from significantly lower baselines", "meaning": "began at much lower initial figures"}
            ]
        },
        {
            "id": "wri_t1_02",
            "chart_type": "Bar Chart",
            "topic": "Global Smartphone Market Share by Operating System",
            "prompt": "The bar chart compares mobile operating system market shares across five distinct geographical zones in the year 2024.",
            "time_period": "2024 (Static Comparison)",
            "overview_focus": "Android commanded substantial dominance across developing regions while iOS led in North America.",
            "band_score": 9.0,
            "model_answer": {
                "introduction": "The bar chart compares the regional distribution of mobile operating system market shares across five distinct geographical zones in the year 2024.",
                "overview": "Overall, the market was heavily polarized between Android and iOS, with alternative platforms occupying negligible shares. Android commanded substantial dominance across Asia, Africa, and South America, while iOS achieved superiority in North America.",
                "body_1": "In Asia and South America, Android accounted for the lion's share of the market, registering approximately 78% and 82% respectively. By comparison, iOS captured merely 20% in Asia and 16% in South America. In Africa, the disparity was even more pronounced, with Android surpassing 85%.",
                "body_2": "In stark contrast, North America presented a reversed scenario, where iOS led the market with roughly 58%, outperforming Android's 41%. The Oceania market was evenly split, with both major operating systems hovering around 48-50%."
            },
            "academic_collocations": [
                {"phrase": "heavily polarized between", "meaning": "divided sharply into two main groups"},
                {"phrase": "accounted for the lion's share", "meaning": "represented the majority portion"},
                {"phrase": "in stark contrast", "meaning": "in sharp opposition or difference"}
            ]
        },
        {
            "id": "wri_t1_03",
            "chart_type": "Pie Chart",
            "topic": "Household Expenditure in the UK (1990 vs 2020)",
            "prompt": "The two pie charts compare household spending patterns across five categories in the United Kingdom in 1990 and 2020.",
            "time_period": "1990 vs 2020",
            "overview_focus": "Housing and technology expenditures expanded dramatically, replacing food and apparel as the largest budgetary components.",
            "band_score": 9.0,
            "model_answer": {
                "introduction": "The pie charts illustrate how British households allocated their annual expenditures across five key sectors—housing, food, transportation, leisure/technology, and clothing—in 1990 and 2020.",
                "overview": "Overall, the thirty-year timeframe witnessed a profound budgetary reallocation. While food and clothing expenditure diminished substantially, outlays on housing and leisure/technology expanded to dominate total household spending.",
                "body_1": "In 1990, food constituted the predominant expenditure, representing 32% of family budgets, followed closely by housing at 22%. By 2020, this allocation reversed drastically: housing escalated to 35%, making it the largest financial commitment, whereas expenditure on food dwindled by nearly half to 17%.",
                "body_2": "Similarly, spending on leisure and digital technology saw a threefold surge from 8% to 24%. In contrast, expenditures on apparel and personal transport recorded downward trends, contracting from 18% and 20% down to 9% and 15% respectively by the end of the period."
            },
            "academic_collocations": [
                {"phrase": "witnessed a profound budgetary reallocation", "meaning": "saw a major change in how money was divided"},
                {"phrase": "constituted the predominant expenditure", "meaning": "formed the largest expense"},
                {"phrase": "saw a threefold surge", "meaning": "increased three times over"},
                {"phrase": "contracting down to", "meaning": "shrinking or declining to"}
            ]
        },
        {
            "id": "wri_t1_04",
            "chart_type": "Table",
            "topic": "Undergraduate Student Enrollment Across Academic Faculties",
            "prompt": "The table gives information about student enrollment numbers and female representation in five university faculties in 2023.",
            "time_period": "2023",
            "overview_focus": "Business and Computer Science attracted the highest aggregate enrollments, though gender distribution varied markedly across disciplines.",
            "band_score": 9.0,
            "model_answer": {
                "introduction": "The table details the total enrollment of undergraduate students alongside the proportion of female participants across five university academic faculties in the year 2023.",
                "overview": "Overall, the Faculty of Business and Management enrolled the highest absolute volume of scholars, whereas Humanities maintained the smallest cohort. In terms of gender balance, women were heavily concentrated in Healthcare and Humanities, yet significantly underrepresented in Engineering and Computer Science.",
                "body_1": "Business and Management topped the enrollment rankings with 4,200 students, exhibiting an equitable gender distribution of 51% female attendees. In comparison, Computer Science registered 3,100 students, yet female involvement was limited to merely 22%. Engineering recorded the most severe gender disparity, where women constituted just 16% of the 2,800 matriculated candidates.",
                "body_2": "Conversely, the Faculty of Healthcare and Medicine accounted for 2,500 students, with females comprising a staggering 68% majority. Similarly, in Humanities and Arts (1,900 students), women represented nearly two-thirds of the cohort (64%)."
            },
            "academic_collocations": [
                {"phrase": "equitable gender distribution", "meaning": "balanced proportion between males and females"},
                {"phrase": "exhibiting an equitable distribution", "meaning": "showing fair and balanced figures"},
                {"phrase": "matriculated candidates", "meaning": "enrolled university students"},
                {"phrase": "staggering majority", "meaning": "overwhelmingly high percentage"}
            ]
        },
        {
            "id": "wri_t1_05",
            "chart_type": "Process Diagram",
            "topic": "Industrial Desalination and Potable Water Production",
            "prompt": "The diagram illustrates the sequential stages of sea water desalination to produce drinking water.",
            "time_period": "Cyclical Industrial Process",
            "overview_focus": "A five-stage industrial transformation separating saline effluent and producing potable water through pressurized reverse osmosis.",
            "band_score": 9.0,
            "model_answer": {
                "introduction": "The flow diagram delineates the multi-stage industrial process through which seawater is desalinated and purified to produce potable drinking water for municipal consumption.",
                "overview": "Overall, the desalination procedure comprises five principal consecutive stages, commencing with seawater intake and filtration, proceeding through high-pressure reverse osmosis, and culminating in post-treatment remineralization and municipal distribution.",
                "body_1": "Initially, raw seawater is drawn from the ocean via deep intake pipelines equipped with coarse mesh screens to exclude marine life and large debris. Next, the water enters a pre-filtration settling chamber where suspended solids are removed, before undergoing chemical pre-treatment to neutralize organic contaminants.",
                "body_2": "In the critical phase, the pre-treated brine is pumped under immense hydraulic pressure through semi-permeable membranes. This process separates concentrated salt effluent, which is funneled back to sea, from purified fresh permeate. Finally, the desalinated water is chlorinated, enriched with minerals for taste, and transferred into the public supply reservoir."
            },
            "academic_collocations": [
                {"phrase": "delineates the multi-stage process", "meaning": "clearly illustrates the various steps"},
                {"phrase": "semi-permeable membranes", "meaning": "special selective filters"},
                {"phrase": "commencing with ... culminating in", "meaning": "starting from ... finishing at"}
            ]
        },
        {
            "id": "wri_t1_06",
            "chart_type": "Map Comparison",
            "topic": "Redevelopment of Norbury Industrial Port (2005 vs Present)",
            "prompt": "The maps show the layout of the port town of Norbury in 2005 and after comprehensive urban redevelopment in the present day.",
            "time_period": "2005 vs Present Day",
            "overview_focus": "The transition of a heavy industrial cargo harbor into an eco-friendly pedestrian, residential, and commercial waterfront.",
            "band_score": 9.0,
            "model_answer": {
                "introduction": "The two maps depict the architectural and infrastructural transformation of the coastal town of Norbury between 2005 and the present day.",
                "overview": "Overall, Norbury has evolved from a heavy manufacturing and shipping depot into a modern commercial and residential district, characterized by the eradication of industrial facilities and the expansion of recreational and public transport amenities.",
                "body_1": "In 2005, the eastern shoreline was occupied by large derelict warehouses and a container terminal. In the modern layout, these logistics hubs have been dismantled to make way for a pedestrianized marina, luxury waterfront apartments, and an array of retail outlets. The previous rail cargo spur running along the coast has been converted into an electric light rail tramway.",
                "body_2": "To the west, the former open-cast gravel pit has been remediated and converted into a public botanical park with artificial wetlands. Additionally, the southern vehicular ring road was replaced with dedicated cycle paths and pedestrian boulevards, emphasizing sustainable transit throughout the revitalized hub."
            },
            "academic_collocations": [
                {"phrase": "infrastructural transformation", "meaning": "systemic redevelopment of buildings and transport"},
                {"phrase": "pedestrianized marina", "meaning": "harbor area reserved for walking visitors"},
                {"phrase": "has been remediated and converted", "meaning": "cleaned up environmentally and transformed"},
                {"phrase": "derelict warehouses", "meaning": "abandoned or rundown storage buildings"}
            ]
        }
    ]

    with open(TASK1_DIR / "task1_bank.json", "w", encoding="utf-8") as f:
        json.dump({"total_prompts": len(task1_items), "prompts": task1_items}, f, ensure_ascii=False, indent=2)
    print(f"[Writing] Task 1 expanded: {len(task1_items)} items saved.")
    return task1_items

def generate_task2_dataset():
    TASK2_DIR.mkdir(parents=True, exist_ok=True)
    task2_items = [
        {
            "id": "wri_t2_01",
            "essay_type": "Opinion (To what extent do you agree or disagree?)",
            "category": "Technology & Artificial Intelligence",
            "prompt": "Some people believe that artificial intelligence will create more opportunities than it eliminates, while others argue it poses an existential threat to employment. To what extent do you agree or disagree?",
            "band_score": 9.0,
            "outline": {
                "thesis": "AI serves as a catalyst for net job creation and productivity, provided governments implement active vocational retraining.",
                "point_1": "Automation replaces routine clerical/mechanical work but historic industrial shifts consistently spark larger, higher-value sectors.",
                "point_2": "AI augmentative capabilities free human intellect to focus on strategic, empathetic, and creative problem solving."
            },
            "sample_essay": "The rapid proliferation of artificial intelligence (AI) has sparked intense discourse regarding its net impact on human labor. While critics contend that automation will precipitate unprecedented joblessness, I firmly agree that AI will fundamentally act as a catalyst for economic diversification and novel vocational opportunities, provided society undertakes proactive workforce restructuring.\n\nOpponents often highlight that algorithmic systems and machine learning models are systematically displacing repetitive cognitive and physical occupations. Routine administrative positions, assembly line roles, and basic data analysis are increasingly performed with superior efficiency by automated software. Nonetheless, historical precedents demonstrate that technological revolutions—from the Industrial Revolution to the advent of personal computing—inevitably render certain archaic jobs obsolete while catalyzing far more sophisticated industries.\n\nMore significantly, the integration of AI augments human productivity rather than entirely supplanting it. First, the emergence of AI architecture necessitates burgeoning sectors in machine learning engineering, prompt design, ethical compliance, and cybersecurity. Second, by automating mundane burdens, AI liberates professionals in medical diagnostics, scientific research, and pedagogical design to concentrate on empathetic, creative, and high-order strategic problem-solving. This symbiotic interaction inevitably stimulates higher value-added economic sectors.\n\nIn conclusion, although the transitionary disruption caused by algorithmic automation poses legitimate short-term friction, I maintain that AI represents an indispensable driver of future job creation and human advancement. Strategic investment in vocational retraining will ensure that the technology enriches human employment rather than diminishing it.",
            "lexical_highlights": ["proliferation", "catalyst for economic diversification", "precedented joblessness", "symbiotic interaction", "vocational retraining"]
        },
        {
            "id": "wri_t2_02",
            "essay_type": "Discussion (Discuss both views and give your opinion)",
            "category": "Education & Economy",
            "prompt": "Some educators argue that higher education should focus entirely on preparing students for specific commercial careers. Others believe that university should aim to provide a broad intellectual foundation. Discuss both views and give your own opinion.",
            "band_score": 8.5,
            "outline": {
                "thesis": "Universities must balance technical employability skills with holistic critical reasoning to prepare resilient graduates.",
                "view_1": "Vocational training minimizes graduate underemployment and drives immediate economic productivity.",
                "view_2": "Broad liberal arts and philosophical education cultivate long-term adaptability in dynamic markets."
            },
            "sample_essay": "Whether tertiary academic institutions should function primarily as vocational training academies or as centers of holistic intellectual cultivation remains a contentious pedagogical dispute. While commercial career preparation undoubtedly optimizes immediate graduate employability, I advocate for an educational ethos that combines rigorous vocational aptitude with comprehensive critical thinking.\n\nOn the one hand, advocates of vocation-oriented curriculums argue that tertiary education represents a substantial financial investment. In an increasingly competitive globalized economy, graduates possessing targeted practical competencies—such as software engineering, accounting, or clinical healthcare—seamlessly transition into the workforce, mitigating graduate underemployment. This targeted output directly fuels national economic productivity.\n\nOn the other hand, proponents of a broad intellectual curriculum emphasize that technical proficiencies quickly turn obsolete in modern dynamic markets. A foundational education in humanities, logic, philosophy, and interdisciplinary sciences fosters cognitive agility, ethical deliberation, and adaptable problem-solving faculties. Graduates endowed with versatile analytical acumen can effortlessly pivot across evolving industries throughout multi-decade careers.\n\nTo synthesize both perspectives, I believe the dichotomous view of higher education is fundamentally flawed. Modern universities should construct integrated curricula where rigorous discipline-specific skills are underpinned by robust liberal arts reasoning, thereby producing both employable and visionary professionals.",
            "lexical_highlights": ["holistic intellectual cultivation", "pedagogical dispute", "cognitive agility", "dichotomous view", "mitigating graduate underemployment"]
        },
        {
            "id": "wri_t2_03",
            "essay_type": "Problem and Solution (Causes & Solutions)",
            "category": "Environment & Urban Living",
            "prompt": "In many modern metropolitan areas, severe traffic congestion and air pollution are worsening daily. What are the primary causes of this issue, and what viable measures can municipal governments take to alleviate it?",
            "band_score": 9.0,
            "outline": {
                "thesis": "Urban gridlock and pollution stem from inadequate public transit infrastructure and suburban sprawl; solutions require congestion pricing and green transit subsidies.",
                "causes": "Affordable private vehicles coupled with sprawling urban planning and underfunded public transit networks.",
                "solutions": "Implementation of metropolitan congestion zones and municipal subsidization of rapid rail/electric transit."
            },
            "sample_essay": "Escalating vehicular gridlock and the concomitant deterioration of atmospheric quality represent two of the most intractable urban dilemmas confronting contemporary metropolises. This essay will examine how suburban sprawl and underfunded transit infrastructure engender this crisis, before proposing that congestion pricing schemes and subsidized public transport networks offer viable remedies.\n\nThe genesis of metropolitan traffic saturation lies primarily in rapid urbanization coupled with deficient spatial planning. Over recent decades, city borders have expanded into distant commuter suburbs lacking integrated transit links. Consequently, residents are coerced into private automobile dependency for daily commuting. Furthermore, the historic underfunding of municipal metro and bus systems has rendered public transit uncompetitive in terms of reliability, safety, and transit velocity, exacerbating the reliance on fossil-fuel powered private cars.\n\nTo remediate this unsustainable situation, urban authorities must enact a bifurcated policy combining financial disincentives with infrastructure expansion. Primarily, governments should institute electronic congestion pricing schemes in central business districts, similar to those deployed in London and Singapore. By imposing substantial levies on private vehicles entering peak zones, commuting patterns can be altered dramatically. Simultaneously, revenues accrued from these tariffs must be channeled directly into expanding zero-emission electric bus rapid transit (BRT) and regional subway links, ensuring that commuters possess an affordable, punctual alternative.\n\nIn conclusion, while urban congestion and atmospheric degradation stem from unchecked suburban sprawl and car-centric development, they are not irremediable. Through decisive congestion taxes and aggressive public transport modernization, municipal leaders can foster cleaner, livable cities.",
            "lexical_highlights": ["vehicular gridlock", "concomitant deterioration", "spatial planning", "bifurcated policy", "congestion pricing schemes"]
        },
        {
            "id": "wri_t2_04",
            "essay_type": "Advantages vs Disadvantages (Do advantages outweigh disadvantages?)",
            "category": "Globalization & International Tourism",
            "prompt": "International tourism has brought economic prosperity to many historic and remote regions, but also caused cultural erosion and environmental damage. Do the advantages of international tourism outweigh the disadvantages?",
            "band_score": 8.5,
            "outline": {
                "thesis": "The financial capital generated by international tourism outweighs its potential hazards, provided revenue is invested in cultural preservation.",
                "disadvantages": "Over-commercialization, environmental pollution, and localized inflation.",
                "advantages": "Invaluable foreign exchange earnings, infrastructure development, and conservation funding."
            },
            "sample_essay": "The exponential growth of the global travel sector has transformed remote communities and historic heritage sites into thriving tourist destinations. While this influx can precipitate environmental degradation and cultural commodification, I contend that the economic dividends and intercultural preservation financed by international tourism substantially outweigh its drawbacks, provided regulatory oversight is strictly enforced.\n\nAdmittedly, mass tourism poses discernible hazards to fragile host communities. Unregulated footfall often inflicts severe ecological damage on delicate ecosystems, from coral bleaching in tropical reserves to soil compaction at ancient archaeological ruins. Furthermore, local traditions risk being trivialized into superficial commercial spectacles manufactured for transient visitors, diluting authentic cultural rituals. Rapid gentrification driven by international visitors can also inflate local living expenses, displacing indigenous inhabitants from urban centres.\n\nNevertheless, the overarching merits of global tourism remain overwhelmingly positive. Chief among these is the generation of vital foreign exchange reserves and decentralized employment. In agrarian or geographically secluded regions lacking diversified industrial bases, eco-tourism and hospitality provide sustainable livelihoods for local guides, artisans, and transport operators. Moreover, tourism revenue furnishes municipalities with the capital required to maintain cultural monuments that would otherwise fall into decay through state neglect. When communities recognize that international travelers cherish their cultural authenticity, they are paradoxically incentivized to protect their heritage more vigorously.\n\nTo conclude, despite legitimate anxieties regarding environmental wear and commercialization, the socioeconomic liberation and conservation funding generated by global tourism render it an indispensable asset when managed responsibly.",
            "lexical_highlights": ["exponential growth", "cultural commodification", "indigenous inhabitants", "foreign exchange reserves", "socioeconomic liberation"]
        },
        {
            "id": "wri_t2_05",
            "essay_type": "Direct Questions / Double Question",
            "category": "Health & Nutrition",
            "prompt": "Many individuals consume large amounts of fast food and processed meals despite widespread awareness of the associated health risks. Why is this the case, and what actions can be taken to encourage healthier dietary habits?",
            "band_score": 9.0,
            "outline": {
                "thesis": "Fast food prevalence is driven by hyper-palatable ingredient engineering and fast-paced modern work schedules; reform requires taxes on processed sugars and mandatory nutrition education.",
                "question_1": "Hyper-engineered sodium/sugar compositions trigger addictive neural feedback, combined with time-poverty in urban lifestyles.",
                "question_2": "State fiscal policy via junk-food excise duties alongside statutory subsidization of whole organic produce."
            },
            "sample_essay": "Despite universal medical consensus documenting the correlation between processed meals and chronic cardiovascular conditions, global consumption of convenience food continues to escalate. This pervasive paradox is primarily driven by industrial flavor engineering and lifestyle time-poverty, but it can be effectively curtailed through fiscal taxation and public nutritional education.\n\nTwo interrelated factors explain why consumers persist in eating unhealthy foods. Foremost is the scientific formulation of ultra-processed items. Food manufacturers deliberately engineer products with optimal ratios of saturated fats, refined sodium, and high-fructose corn syrup—a phenomenon known as the 'bliss point'—which triggers hyper-palatable dopamine responses akin to chemical dependency. Compounding this neurochemical hook is the relentless pace of contemporary labor. Exhausted commuters, burdened by extended work hours, frequently prioritize the immediate availability of inexpensive drive-through eateries over the laborious process of preparing wholesome domestic meals.\n\nTo counteract this public health crisis, governments must intervene through strategic regulatory and fiscal mechanisms. First, legislators should implement targeted excise duties on foods exceeding specified thresholds of added sugar and trans-fats, mirroring successful international levies on tobacco. By raising the retail price of sugary sodas and fast foods, consumers are steered toward affordable alternatives. Concurrently, tax revenues garnered from these levies must subsidize local agricultural markets, rendering fresh vegetables, legumes, and whole grains financially accessible. Finally, comprehensive culinary and nutrition literacy courses should be integrated into primary school curricula to instill lifelong dietary mindfulness.\n\nIn conclusion, the widespread consumption of junk food is fostered by addictive commercial food engineering and socioeconomic pressures. Decisive state action through fiscal disincentives and educational empowerment is paramount to restoring public wellness.",
            "lexical_highlights": ["universal medical consensus", "hyper-palatable dopamine responses", "laborious process", "targeted excise duties", "nutritional literacy"]
        }
    ]

    with open(TASK2_DIR / "task2_bank.json", "w", encoding="utf-8") as f:
        json.dump({"total_prompts": len(task2_items), "prompts": task2_items}, f, ensure_ascii=False, indent=2)
    print(f"[Writing] Task 2 expanded: {len(task2_items)} items saved.")
    return task2_items

def generate_academic_phrasebank():
    PHRASEBANK_DIR.mkdir(parents=True, exist_ok=True)
    phrasebank = {
        "introducing_work": [
            "A key issue arising from this discussion is whether...",
            "Recent empirical evidence suggests that...",
            "The central premise underlying this debate is that...",
            "The question of whether X should be implemented has gained considerable prominence.",
            "Over the past several decades, considerable research has examined..."
        ],
        "comparing_and_contrasting": [
            "In sharp contrast to conventional assumptions,...",
            "While X demonstrates substantial growth, Y exhibits a diametrically opposed trend.",
            "A profound disparity exists between the outcomes of A and B.",
            "Whereas proponents champion X, skeptics argue that Y poses greater hazards.",
            "Conversely, the latter perspective reveals marked advantages."
        ],
        "explaining_causes": [
            "This phenomenon can be largely attributed to...",
            "A primary catalyst driving this development is...",
            "The resultant consequence of this policy is twofold:...",
            "This tendency is predominantly engendered by socioeconomic factors.",
            "At the root of this persistent dilemma lies..."
        ],
        "expressing_degrees_of_caution": [
            "It is plausible to hypothesize that...",
            "Preliminary evidence indicates a probable correlation between...",
            "These findings should be interpreted with caution given...",
            "It would be premature to infer that this solution is universally applicable.",
            "There is a discernible likelihood that..."
        ],
        "concluding_and_summarizing": [
            "Weighing both perspectives, it can be cogently argued that...",
            "In the final analysis, the overarching consensus indicates that...",
            "Ultimately, addressing this multifaceted dilemma necessitates concerted action.",
            "To synthesize both viewpoints, the optimal path involves balanced reform.",
            "The balance of evidence strongly tips toward..."
        ]
    }

    with open(PHRASEBANK_DIR / "academic_phrasebank.json", "w", encoding="utf-8") as f:
        json.dump(phrasebank, f, ensure_ascii=False, indent=2)
    print("[Writing] Academic phrasebank saved.")
    return phrasebank

def generate_band_descriptors():
    rubrics = {
        "task_2_bands": {
            "band_9": {
                "Task Response": "Fully addresses all parts of the task with a well-developed response, relevant, fully extended and well-supported ideas.",
                "Coherence & Cohesion": "Uses cohesion in such a way that it attracts no attention. Skilfully manages paragraphing.",
                "Lexical Resource": "Uses a wide range of vocabulary with very natural and sophisticated control of lexical features; rare minor slips only as slips.",
                "Grammatical Range": "Uses a wide range of structures with full flexibility and accuracy; rare minor slips only."
            },
            "band_8": {
                "Task Response": "Sufficiently addresses all parts of the task with a well-developed response, though there may be occasional lapses in content.",
                "Coherence & Cohesion": "Sequences information and ideas logically. Manages all aspects of cohesion well.",
                "Lexical Resource": "Uses a wide range of vocabulary fluently and flexibly to convey precise meanings. Skillfully uses uncommon lexical items.",
                "Grammatical Range": "Uses a wide variety of structures. The majority of sentences are error-free with only very occasional inaccuracies."
            },
            "band_7": {
                "Task Response": "Addresses all parts of the task with a clear position throughout, though some parts may be more fully covered than others.",
                "Coherence & Cohesion": "Logically organizes information and ideas; clear progression throughout. Uses a range of cohesive devices appropriately.",
                "Lexical Resource": "Uses a sufficient range of vocabulary with some flexibility and precision. Uses less common lexical items with some awareness of style and collocation.",
                "Grammatical Range": "Uses a variety of complex structures. Produces frequent error-free sentences with good control of grammar and punctuation."
            }
        }
    }
    with open(WRITING_DIR / "band_descriptors.json", "w", encoding="utf-8") as f:
        json.dump(rubrics, f, ensure_ascii=False, indent=2)
    print("[Writing] Band descriptors saved.")

def fetch_writing_data():
    generate_task1_dataset()
    generate_task2_dataset()
    generate_academic_phrasebank()
    generate_band_descriptors()
    print("[Writing] All writing datasets completed successfully.")

if __name__ == "__main__":
    fetch_writing_data()
