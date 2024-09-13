
last_entity_id = 0
last_event_id = 0



# prepare step, expand the data set
enum_dict = {
    'Binding': ['Blocking', 'Coligation', 'Cross-linking', 'Interaction', 'absence', 'activities', 'activity', 'aggregated', 'associate', 'bind',
                'coengagement', 'coimmunoprecipitation', 'combination', 'comigrate', 'competition', 'complex', 'conjugation', 'contain', 'couple', 'cross-react',
                'detect', 'dimerize', 'engage', 'formation', 'genotype', 'heterodimer', 'homodimer', 'interact', 'ligand', 'ligation', 'linkage', 'migrate', 'multimer',
                'mutant', 'occupancy', 'oligomerization', 'pair', 'participation', 'partner', 'potent', 'presence', 'protein', 'react', 'reactivity', 'receptor',
                'recognition', 'recruit', 'site', 'specificity', 'subunit', 'target'],
    'Gene_expression': ['Co-expression', 'Cotransfection', 'Expression', 'Generation', 'Level', 'Overexpression', 'Production', 'Transfection', 'absence', 'activation',
                        'amount', 'analyze', 'antisense', 'appearance', 'biosynthesis', 'coexpress', 'cotransfect', 'deficient', 'detect', 'distribution', 'express', 'identify', 'induce', 'induction', 'lack', 'low', 'negative', 'overexpress', 'pattern', 'positive',
                        'post-transcription', 'presence', 'produce', 'protein', 'resynthesize', 'secreted', 'select', 'subunit', 'synthesis'],
    'Protein_catabolism': ['breakdown', 'cleavage', 'cleaved', 'degrade', 'intact', 'loss', 'pathway', 'process', 'proteolysis', 'stability', 'stabilized'],
    'Localization': ['Secretion', 'Translocation', 'abundance', 'accumulate', 'appearance', 'co-localization', 'detect', 'direct', 'distribution', 'exclusion',
                     'export', 'expression', 'form', 'found', 'immobilization', 'import', 'liberate', 'localization', 'migrate', 'mobilization', 'precipitation',
                     'presence', 'release', 'reservoir', 'retarget', 'secrete', 'shuttling', 'translocate'],
    'Negative_regulation': ['stabilize', 'Decrease', 'Defective', 'Deregulation', 'Downregulation', 'Impairment', 'Inactivation', 'Inhibition', 'Reduction',
                            'absence', 'affect', 'antagonist', 'attenuate', 'autoregulation', 'block', 'capacity', 'compete', 'deficiency', 'deletion', 'deplete',
                            'deprivation', 'desensitization', 'disrupt', 'downregulate', 'eliminate', 'exclusive', 'fail', 'function', 'hinder', 'inactivate', 'inhibit',
                            'interfere', 'lack', 'level', 'limit', 'loss', 'low', 'negative', 'neutralize', 'opposite', 'prevent', 'reduce', 'repress', 'resistant',
                            'restrict', 'reverse', 'sustain', 'switch', 'undetectable'],
    'Phosphorylation': ['Phosphorylation', 'hyperphosphorylation', 'phosphorylate', 'underphosphorylation'],
    'Regulation': ['Alter', 'Change', 'Control', 'Effect', 'Function', 'Involvement', 'Modulation', 'Regulation', 'Role', 'aberrancy', 'abnormal', 'absence',
                   'accompany', 'account', 'act', 'action', 'activity', 'affect', 'alter', 'alteration', 'associate', 'autoregulation', 'concentration', 'confer',
                   'contribute', 'control', 'cooperate', 'core', 'coregulation', 'critical', 'crucial', 'define', 'depend', 'deregulate', 'determine', 'direct', 'due',
                   'dysregulate', 'dysregulation', 'effect', 'effector', 'efficacy', 'element', 'function', 'half-life', 'hyporesponsiveness', 'immunoreactivity',
                   'implicate', 'importance', 'independent', 'ineffective', 'influence', 'involve', 'level', 'loop', 'measure', 'mechanism', 'mediate', 'modification',
                   'modulate', 'nonresponsive', 'operate', 'participate', 'presence', 'receptor', 'regulate', 'require', 'resistant', 'response', 'result', 'role',
                   'sensitive', 'sensitivity', 'show', 'signal', 'specific', 'specificity', 'stability', 'stimulate', 'subject', 'target', 'through', 'unaffected',
                   'unaltered', 'unchanged', 'underlie', 'upregulate', 'utilize', 'value', 'vary', 'via'],
    'Positive_regulation': ['Activation', 'Augmentation', 'Cooperation', 'Cotransfection', 'Enforcement', 'Enhancement', 'Excess', 'Expression', 'Increase',
                            'Induction', 'Involvement', 'Overexpression', 'Stimulation', 'Target', 'Transactivation', 'Transfection', 'Triggering', 'ability',
                            'accelerate', 'accomplish', 'accumulate', 'act', 'activate', 'affect', 'allow', 'amplify', 'appearance', 'augment', 'autoinduction',
                            'capable', 'cascade', 'change', 'confer', 'consequence', 'contribute', 'control', 'costimulation', 'critical', 'demonstrate', 'depend',
                            'detect', 'direct', 'drive', 'due', 'effect', 'elevate', 'elicit', 'enable', 'enhance', 'essential', 'exert', 'expression', 'facilitate',
                            'function', 'generate', 'importance', 'increase', 'induce', 'involve', 'lead', 'level', 'link', 'maintain', 'mechanism', 'mediate',
                            'modulate', 'necessary', 'observe', 'occur', 'participation', 'permit', 'positive', 'potent', 'present', 'produce', 'promote', 'provide',
                            'require', 'respond', 'result', 'role', 'significant', 'stimulate', 'strong', 'subject', 'subsequent', 'sufficient', 'support', 'sustain',
                            'trigger', 'upregulate', 'vigorous'],
    'Transcription': [
        'Level', 'Transcription', 'absence', 'abundant', 'activity', 'appearance', 'concentration','demonstrate', 'derive', 'detect', 'express', 'expression', 'find',
        'hybridize', 'inducible', 'induce', 'initiate', 'lack', 'mRNA', 'observe', 'perform', 'present', 'production', 'rate', 'regulation', 'synthesis',
        'through', 'transcribe', 'transcript', 'undetectable']}

        # Define the mapping of categories to VerbNet classes
vn_class_mapping = {
    'Binding': ['amalgamate-22.2', 'shake-22.3', 'tape-22.4', 'cooking-45.3', 'mix-22.1', 'funnel-9.3'],
    'Gene_expression': ['declare-29.4', 'illustrate-25.3', 'indicate-78'],
    'Localization': ['put-9.1', 'carry-11.4', 'send-11.1'],
    'Negative_regulation': ['forbid-67', 'stop-55.4', 'neglect-75', 'avoid-52', 'banish-10.2'],
    'Phosphorylation': ['change_bodily_state-40.8.4'],
    'Positive_regulation': ['urge-58', 'force-59', 'enforce-63', 'advise-37.9', 'allow-64', 'approve-77'],
    'Protein_catabolism': ['consume-66', 'remove-10.1', 'destroy-44'],
    'Regulation': ['enforce-63', 'care-88', 'order-60'],
    'Transcription': ['transcribe-25.4', 'transcribe-25.4']
}
side_dic = {
    'amino_acids': {
        'serine', 'threonine', 'tyrosine', 'alanine', 'arginine', 'asparagine', 'aspartic acid', 'cysteine',
        'glutamine', 'glutamic acid', 'glycine', 'histidine', 'isoleucine', 'leucine', 'lysine', 'methionine',
        'phenylalanine', 'proline', 'tryptophan', 'valine', 'phosphoserine', 'phosphothreonine', 'phosphotyrosine',
        'selenocysteine', 'pyrrolysine', 'hydroxyproline', 'methyllysine', 'carboxylated', 'citrulline',
        'ornithine', 'homocysteine', 'hypusine', 'gamma-carboxyglutamate'
    },
    'protein_domains': {
        'SH2 domain', 'SH3 domain', 'kinase domain', 'zinc finger', 'leucine zipper', 'homeobox', 'EF-hand',
        'helix-loop-helix', 'beta-sheet', 'transmembrane domain', 'ankyrin repeat', 'WD40 repeat', 'TIR domain',
        'PAS domain', 'PDZ domain', 'bHLH domain', 'Arm repeat', 'BROMO domain', 'CARD domain'
    },
    'chemical_modifications': {
        'phosphate', 'methyl group', 'acetyl group', 'ubiquitin', 'SUMO', 'N-acetyl', 'glycosyl group',
        'phosphorylation', 'methylation', 'acetylation', 'ubiquitination', 'glycosylation', 'sumoylation',
        'hydroxylation', 'nitration', 'sulfation', 'ADP-ribosylation', 'lipidation', 'aminoethylation'
    },
    'cellular_locations': {
        'nucleus', 'cytoplasm', 'membrane', 'golgi', 'endoplasmic reticulum', 'mitochondria', 'lysosome',
        'peroxisome', 'plasma membrane', 'extracellular matrix', 'nucleolus', 'ribosome', 'centrosome',
        'cilium', 'vesicle', 'chloroplast', 'vacuole', 'cytosol', 'cytoplasmic membrane'
    },
    'molecular_interactions': {
        'binding site', 'active site', 'allosteric site', 'ligand-binding site', 'catalytic site',
        'docking site', 'interaction interface', 'receptor site', 'contact site', 'recognition site',
        'substrate-binding site', 'effector-binding site', 'inhibitory site', 'activation site'
    }
}

biomedical_phrases = [
    'caused by',
    'as a result of',
    'owing to',
    'resulting from',
    'arising from',
    'stemming from',
    'triggered by',
    'influenced by',
    'associated with',
    'linked to',
    'related to',
    'derived from',
    'contingent upon',
    'mediated by',
    'facilitated by',
    'through',
    'in response to',
    'via',
    'performed by',
    'activated by',
    'initiated by',
    'conducted by',
    'executed by',
    'influenced by',
    'carried out by',
    'regulated by',
    'extracted from',
    'obtained from',
    'sourced from',
    'sampled from',
    'harvested from',
    'under conditions of',
    'in the presence of',
    'in light of',
    'regarding',
    'considering',
    'in terms of'
]
