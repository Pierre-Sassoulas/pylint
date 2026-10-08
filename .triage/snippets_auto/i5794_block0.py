class EF_DIR(LinFixedEF):
    class ApplicationLabel(BER_TLV_IE, tag=0x50):
        _construct = GreedyString('ascii')

    class ApplicationTemplate(BER_TLV_IE, tag=0x61,
                              nested=[iso7816_4.ApplicationId, ApplicationLabel, iso7816_4.FileReference,
                                      iso7816_4.CommandApdu, iso7816_4.DiscretionaryData,
                                      iso7816_4.DiscretionaryTemplate, iso7816_4.URL,
                                      iso7816_4.ApplicationRelatedDOSet]):
        pass

    def __init__(self, fid='2f00', sfid=0x1e, name='EF.DIR', desc='Application Directory'):
        super().__init__(fid, sfid=sfid, name=name, desc=desc, rec_len={5, 54})
        self._tlv = EF_DIR.ApplicationTemplate
