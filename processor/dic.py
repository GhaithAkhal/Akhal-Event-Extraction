
last_entity_id = 0
last_event_id = 0


# prepare step, expand the data set
enum_dict = {
    'Binding': ['bind', 'attach', 'interact', 'associate',  'adhere', 'complex', 'dimerization'],
    'Gene_expression': ['express', 'transcribe', 'synthesize', 'produce', 'encode', 'regulate', 'appear', 'synthesis',
                        'modify', 'Gene_expression'],
    'Localization': ['localize', 'transport', 'relocate', 'target', 'direct', 'position', 'move', 'translocate',
                     'export', 'Localization'],
    'Negative_regulation': ['inhibit', 'suppress', 'decrease', 'downregulate', 'block', 'repress', 'silence', 'diminish', 'inhibit',
                            'RETURN', 'reduction', 'Negative_regulation'],
    'Phosphorylation': ['phosphorylate', 'activate', 'catalyze', 'modify', 'transfer', 'dephosphorylate',
                        'signal', 'Phosphorylation'],
    'Positive_regulation': ['results','activate', 'enhance', 'increase', 'upregulate', 'stimulate', 'promote', 'amplify', 'augment', 'induct', 'perpetuate'],
    'Protein_catabolism': ['catabolite', 'degrade', 'BREAK', 'digest', 'hydrolyze', 'cleave', 'autophagize', 'Positive_regulation',
                           'ubiquitinate', 'Protein_catabolism'],
    'Regulation': ['regulate', 'control', 'modulate', 'adjust', 'maintain', 'balance', 'feedback', 'induce', 'underlie', 'Regulation', 'mediate'],
    'Transcription': ['transcribe', 'copy', 'replicate', 'translate', 'reverse', 'read', 'synthesize', 'Transcription',
                      'initiate', 'terminate']
    }
enum_dict_sec = {
    'Localization': [],
    'Phosphorylation': []
}
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
        'selenocysteine', 'pyrrolysine', 'hydroxyproline', 'methyllysine', 'carboxylated', 'citrulline'
    },
    'protein_domains': {
        'SH2 domain', 'SH3 domain', 'kinase domain', 'zinc finger', 'leucine zipper', 'homeobox', 'EF-hand',
        'helix-loop-helix', 'beta-sheet', 'transmembrane domain'
    },
    'chemical_modifications': {
        'phosphate', 'methyl group', 'acetyl group', 'ubiquitin', 'SUMO', 'N-acetyl', 'glycosyl group'
    },
    'cellular_locations': {
        'nucleus', 'cytoplasm', 'membrane', 'golgi', 'endoplasmic reticulum', 'mitochondria', 'lysosome',
        'peroxisome', 'plasma membrane', 'extracellular matrix'
    },
    'molecular_interactions': {
        'binding site', 'active site', 'allosteric site', 'ligand-binding site', 'catalytic site'
    }
}