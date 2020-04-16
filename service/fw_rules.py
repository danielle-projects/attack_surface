class FirewallRule:
    def __init__(self, fw_id, source_tag, dest_tag):
        self.fw_id = fw_id
        self.source_tag = source_tag
        self.dest_tag = dest_tag
